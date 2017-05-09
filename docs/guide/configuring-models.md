# Configuring models #

There are a number of configuration options provided to control how dbt interacts with your models. Understanding these configuration options is core to controlling dbt's behavior and optimizing its usage.

## Supplying configuration values

There are multiple ways to supply model configuration values:

- as settings for an entire group of modules, applied at the directory level
- as settings for an individual model, specified within a given model.

All methods accept identical configuration options. dbt provides multiple configuration contexts in order to give model authors maximum control over their model behaviors. In all cases, configuration provided at a more detailed level overrides configuration provided at a more generic level.

Here is how these configuration options look in practice:

```YAML
# dbt_project.yml
# specify project- and directory-level configuration here.

models:
  [project_name]:
    [model-group]: # model groups can be arbitrarily nested and reflect the directory structure of your project.
      enabled: true
      materialized: view
      ...
```

```SQL
--[model_name].sql
--specify model-level configuration here.

-- python function syntax
{{
  config(
    materialized = "incremental",
    sql_where = "id > (select max(id) from {{this}})"
  )
}}

-- OR json syntax
{{
  config({
    "materialized" : "incremental",
    "sql_where" : "id > (select max(id) from {{this}})"
    })
}}
```

## Using enabled

This parameter does exactly what you might think. Setting `enabled` to `false` tells dbt not to compile and run the associated models. Be careful disabling large swaths of your project: if you disable models that are relied upon by enabled models in the dependency chain, compilation will fail.

Note that dbt does not actively delete models in your database that have been disabled. Instead, it simply leaves them out of future rounds of compilation and deployment. If you want to delete models from your schema, you will have to drop them by hand.

## Using materialized

The `materialized` option is provided like so:

```YAML
# dbt_project.yml

materialized: table # other values: view, incremental, ephemeral
```

Each of the four values passed to `materialized` significantly changes how dbt builds the associated models:

- `table` wraps the `SELECT` in a `CREATE TABLE AS...` statement. This is a good option for models that take a long time to execute, but requires the model to be re-built in order to get new data. Each time a `table` model is re-built, it is first dropped and then recreated.
- `view` wraps the `SELECT` in a `CREATE VIEW AS...` statement. This is a good option for models that do not take a long time to execute, as avoids the overhead involved in storing the model's data on disk.
- `incremental` allows dbt to insert or update records into a table since the last time that dbt was run. Incremental models are one of the most powerful features of dbt but require additional configuration; please see the section below for more information on how to configure incremental models.
- `ephemeral` prevents dbt from materializing the model directly into the database. Instead, dbt will interpolate the code from this model into dependent models as a common table expression. This allows the model author to write reusable logic that data consumers don't have access to `SELECT` directly from and thereby allows the analytic schema to act as the "public interface" that gets exposed to users.

### Configuring incremental models

Incremental models are a powerful feature in production dbt deployments. Frequently, certain raw data tables can have billions of rows, which makes performing frequent rebuilds of models dependent on these tables impractical. Incremental tables provide another option. The first time a model is deployed, the table is created and data is inserted. In subsequent runs this model will have new rows inserted and changed rows updated. (Technically, updates happen via deletes and then inserts.)

It's highly recommended to use incremental models rather than table models in production whenever the schema allows for it. This will minimize your model build times and minimize the use of database resources.

There are generally two ways to configure incremental models: Simple and Advanced. While the "simple" incremental models only require a configuration change (and not a code change), they are generally less performant than an "advanced" incremental model setup. First, understand the process of setting up a simple incremental model. Then, read on to understand how to tune your incremental models for optimal performance.

Incremental models accept two configuration options: `sql_where` and `unique_key`.

#### sql_where (required)

`sql_where` identifies the rows that have been updated or added since the most recent run. For instance, in a clickstream table, you might apply the condition:

```SQL
WHERE [source].session_end_timestamp >= (select max(session_end_timestamp) from [model])
```

dbt applies this `WHERE` condition automatically, so it shouldn't be present in the model code: specify it in your model config as so `sql_where = "[condition]"`.

#### unique_key (optional)

`unique_key` is an optional parameter that specifies uniqueness on this table. Records matching this UK that are found in the table will be deleted before new records are inserted. Functionally, this allows for modification of existing rows in an incremental table. `unique_key` can be any valid SQL expression, including a single field, or a function. A common use case is concatenating multiple fields together to create a single unique key, as such: `user_id || session_index`.

#### using {{this}}

`{{this}}` is a special variable that returns the schema and table name of the currently executing model. It is useful when defining a `sql_where` clause. The `sql_where` written above would in practice be written as:

```SQL
WHERE session_end_timestamp >= (select max(session_end_timestamp) from {{this}})
```

See [context variables](context-variables/) for more information on `this`.

### Advanced incremental model usage

Simple incremental models blindly apply the `sql_where` filter to the entire model SELECT query. Depending on the complexity of the SQL in the model, the query planner may be able to optimize the number of records it scans while executing your query. Generally though, the database will build the entire model, then filter the modeled dataset on `sql_where`. This can take as long, or in some cases _even longer_ than a simple `table` materialization! Advanced incremental model usage involves adding a few extra lines of code to your model to ensure that only new or changed data is processed during the dbt run.

With incremental models, there are two scenarios that need to be accounted for.

1. This is the first time the incremental model is running, and the table _does not_ already exist
2. The incremental model has run before, and the table _does_ already exist

It's important to differentiate between these two scenarios. Typically, an advanced incremental model will introspectively look at the `max()` value in one of its own columns to determine the cutoff for new data from some other source table. Consider the case of an clickstream events table:

```sql
-- sessions.sql : Creates sessions from raw clickstream events

-- The event source
with all_events as (

    select * from {{ ref('events') }}

),

-- Filter out only the events that have arrived since events have last been processed
new_events as (

    select *
    from all_events

    -- The line below is problematic! If this model hasn't been run before, then {{ this }}
    -- points to a table which doesn't exist yet. We need to know if {{ this }} already exists
    where received_at > (select max(received_at) from {{ this }})

),

sessions as (
...
```

The above scenario is typical for incremental model use cases. To avoid this "already exists?" problem, dbt provides an adapter function in the dbt environment called... `already_exists`! You can access this function with `adapter.already_exists([schema], [table])`. The above example could be rewritten as:

```sql
-- sessions.sql : Creates sessions from raw clickstream events

with all_events as (

    select * from {{ ref('events') }}

),

-- Filter out only the events that have arrived since events have last been processed
new_events as (

    select *
    from all_events

    -- This conditional is executed just before the model is executed and returns either True or False
    -- The enclosed where filter will be conditionally applied only if this model exists in the current schema
    {% if adapter.already_exists(this.schema, this.table) %}
        where received_at > (select max(received_at) from {{ this }})
    {% endif %}

),

sessions as (
...
```

For backwards compatibility reasons, `sql_where` is required even for "advanced" incremental models. Set `sql_where='TRUE'` to avoid any compilation errors while essentially discarding the associated filtering logic.

Advanced incremental models are, suitably, an advanced dbt feature! They're incredibly powerful, but also not incredibly intuitive. If you have any troubles, please reach out to us in the [dbt slack group](http://ac-slackin.herokuapp.com/).

## Database-specific configuration

In addition to the configuration parameters that apply to all database adapters, there are certain configuration options that apply only to specific databases. See the page on [database-specific optimizations](database-optimizations/).

## Hooks

dbt provides the ability to run arbitrary commands against the database before and after a model is run. These are known as pre- and post-model hooks and configured as such:

```YAML
models:
  project-name:
    pre-hook:       # custom SQL
    post-hook:      # custom SQL

```

Hooks are extremely powerful, allowing model authors to perform tasks such as inserting records into audit tables, executing `GRANT` statements, and running `VACUUM` commands, among others. To learn more about hooks and see examples, see [using hooks](using-hooks/).
