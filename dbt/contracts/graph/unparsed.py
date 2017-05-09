from voluptuous import Schema, Required, All, Any, Length

from dbt.compat import basestring
from dbt.contracts.common import validate_with

from dbt.utils import NodeType

unparsed_base_contract = Schema({
    # identifiers
    Required('name'): All(basestring, Length(min=1, max=127)),
    Required('package_name'): basestring,

    # filesystem
    Required('root_path'): basestring,
    Required('path'): basestring,
    Required('raw_sql'): basestring,
})

unparsed_node_contract = unparsed_base_contract.extend({
    Required('resource_type'): Any(NodeType.Model,
                                   NodeType.Test,
                                   NodeType.Analysis)
})

unparsed_nodes_contract = Schema([unparsed_node_contract])


def validate_nodes(nodes):
    validate_with(unparsed_nodes_contract, nodes)
