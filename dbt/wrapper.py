
from dbt.model import SourceConfig
from dbt.utils import get_materialization, compiler_error
from dbt.adapters.factory import get_adapter
from dbt.compat import basestring

import dbt.clients.jinja
import dbt.flags

from collections import defaultdict

from dbt.logger import GLOBAL_LOGGER as logger  # noqa


def get_sort_qualifier(model, project):
    model_config = model.get('config', {})

    if 'sort' not in model['config']:
        return ''

    if get_materialization(model) not in ('table', 'incremental'):
        return ''

    sort_keys = model_config.get('sort')
    sort_type = model_config.get('sort_type', 'compound')

    if not isinstance(sort_type, basestring):
        compiler_error(
            model,
            "The provided sort_type '{}' is not valid!".format(sort_type)
        )

    sort_type = sort_type.strip().lower()

    adapter = get_adapter(project.run_environment())
    return adapter.sort_qualifier(sort_type, sort_keys)


def get_dist_qualifier(model, project):
    model_config = model.get('config', {})

    if 'dist' not in model_config:
        return ''

    if get_materialization(model) not in ('table', 'incremental'):
        return ''

    dist_key = model_config.get('dist')

    if not isinstance(dist_key, basestring):
        compiler_error(
            model,
            "The provided distkey '{}' is not valid!".format(dist_key)
        )

    dist_key = dist_key.strip().lower()

    adapter = get_adapter(project.run_environment())
    return adapter.dist_qualifier(dist_key)


def get_hooks(model, context, hook_key):
    hooks = model.get('config', {}).get(hook_key, [])

    if isinstance(hooks, basestring):
        hooks = [hooks]

    return hooks


def get_model_identifier(model):
    if dbt.flags.NON_DESTRUCTIVE:
        return model['name']
    else:
        return "{}__dbt_tmp".format(model['name'])


def get_dbt_materialization_macro_uid(macro_name):
    return 'macro.dbt.dbt__{}'.format(macro_name)


def get_wrapping_macro(model, macros):
    mapping = {
        'incremental': get_dbt_materialization_macro_uid('create_incremental'),
        'table': get_dbt_materialization_macro_uid('create_table'),
        'view': get_dbt_materialization_macro_uid('create_view')
    }

    materialization = get_materialization(model)
    uid = mapping[materialization]

    if macros.get(uid) is None:
        dbt.exceptions.macro_not_found(model, uid)

    return macros[uid]['parsed_macro']


def get_macro_context(package, macros):
    global_context = defaultdict(dict)
    package_context = {}

    for _, macro in macros.items():
        if macro['package_name'] in ('dbt', package['name']):
            global_context[macro['name']] = macro['parsed_macro']

        global_context[macro['package_name']][macro['name']] = \
            macro['parsed_macro']

    global_context.update(package_context)
    return global_context


def do_wrap(model, opts, flat_graph, context, package):
    macros = flat_graph['macros']

    macro = get_wrapping_macro(model, macros)
    macro_args = macro.arguments

    relevant_opts = {
        opt: val for (opt, val) in opts.items() if opt in macro_args
    }

    rendered = macro(**relevant_opts)

    wrap_uid = get_dbt_materialization_macro_uid('wrap')

    wrapper_macro = macros.get(wrap_uid, {}).get('parsed_macro')

    if wrapper_macro is None:
        dbt.exceptions.macro_not_found(model, wrap_uid)

    wrapped = wrapper_macro(rendered, opts['pre_hooks'], opts['post_hooks'])

    macro_context = get_macro_context(package, flat_graph['macros'])

    context = context.copy()
    context.update(macro_context)

    return dbt.clients.jinja.get_rendered(
        wrapped,
        context,
        model)


class DatabaseWrapper(object):
    """
    Wrapper for runtime database interaction. Should only call adapter
    functions.
    """

    context_functions = [
        "already_exists",
        "get_columns_in_table",
        "get_missing_columns"
    ]

    def __init__(self, model, adapter, profile):
        self.model = model
        self.adapter = adapter
        self.profile = profile

    def get_context_functions(self):
        return {name: getattr(self, name) for name in self.context_functions}

    def already_exists(self, schema, table):
        return self.adapter.already_exists(
            self.profile, schema, table, self.model.get('name'))

    def get_columns_in_table(self, schema_name, table_name):
        return self.adapter.get_columns_in_table(
            self.profile, schema_name, table_name, self.model.get('name'))

    def get_missing_columns(self, from_schema, from_table,
                            to_schema, to_table):
        return self.adapter.get_missing_columns(
            self.profile, from_schema, from_table,
            to_schema, to_table, self.model.get('name'))


def wrap(model, project, context, injected_graph):
    adapter = get_adapter(project.run_environment())

    schema = context['env'].get('schema', 'public')

    # these are empty strings if configs aren't provided
    dist_qualifier = get_dist_qualifier(model, project)
    sort_qualifier = get_sort_qualifier(model, project)

    pre_hooks = get_hooks(model, context, 'pre-hook')
    post_hooks = get_hooks(model, context, 'post-hook')

    rendered_query = model['injected_sql']

    profile = project.run_environment()

    db_wrapper = DatabaseWrapper(model, adapter, profile)

    opts = {
        "materialization": get_materialization(model),
        "model": model,
        "schema": schema,
        "dist": dist_qualifier,
        "sort": sort_qualifier,
        "pre_hooks": pre_hooks,
        "post_hooks": post_hooks,
        "sql": rendered_query,
        "flags": dbt.flags,
        "adapter": db_wrapper
    }

    opts.update(db_wrapper.get_context_functions())

    return do_wrap(model, opts, injected_graph, context, project)
