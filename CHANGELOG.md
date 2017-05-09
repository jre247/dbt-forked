## dbt 0.8.0 (April 17, 2017)


### Overview

- Bugfixes
- True concurrency
- More control over "advanced" incremental model configurations [more info](http://dbt.readthedocs.io/en/master/guide/configuring-models/)

### Bugfixes

- Fix ephemeral load order bug ([#292](https://github.com/fishtown-analytics/dbt/pull/292), [#285](https://github.com/fishtown-analytics/dbt/pull/285))
- Support composite unique key in archivals ([#324](https://github.com/fishtown-analytics/dbt/pull/324))
- Fix target paths ([#331](https://github.com/fishtown-analytics/dbt/pull/331), [#329](https://github.com/fishtown-analytics/dbt/issues/329))
- Ignore commented-out schema tests ([#330](https://github.com/fishtown-analytics/dbt/pull/330), [#328](https://github.com/fishtown-analytics/dbt/issues/328))
- Fix run levels ([#343](https://github.com/fishtown-analytics/dbt/pull/343), [#340](https://github.com/fishtown-analytics/dbt/issues/340), [#338](https://github.com/fishtown-analytics/dbt/issues/338))
- Fix concurrency, open a unique transaction per model ([#345](https://github.com/fishtown-analytics/dbt/pull/345), [#336](https://github.com/fishtown-analytics/dbt/issues/336))
- Handle concurrent `DROP ... CASCADE`s in Redshift ([#349](https://github.com/fishtown-analytics/dbt/pull/349))
- Always release connections (use `try .. finally`) ([#354](https://github.com/fishtown-analytics/dbt/pull/354))

### Changes

- Changed: different syntax for "relationships" schema tests ([#339](https://github.com/fishtown-analytics/dbt/pull/339))
- Added: `already_exists` context function ([#372](https://github.com/fishtown-analytics/dbt/pull/372))
- Graph refactor: fix common issues with load order ([#292](https://github.com/fishtown-analytics/dbt/pull/292))
- Graph refactor: multiple references to an ephemeral models should share a CTE ([#316](https://github.com/fishtown-analytics/dbt/pull/316))
- Graph refactor: macros in flat graph ([#332](https://github.com/fishtown-analytics/dbt/pull/332))
- Refactor: factor out jinja interactions ([#309](https://github.com/fishtown-analytics/dbt/pull/309))
- Speedup: detect cycles at the end of compilation ([#307](https://github.com/fishtown-analytics/dbt/pull/307))
- Speedup: write graph file with gpickle instead of yaml ([#306](https://github.com/fishtown-analytics/dbt/pull/306))
- Clone dependencies with `--depth 1` to make them more compact ([#277](https://github.com/fishtown-analytics/dbt/issues/277), [#342](https://github.com/fishtown-analytics/dbt/pull/342))
- Rewrite materializations as macros ([#356](https://github.com/fishtown-analytics/dbt/pull/356))

## dbt 0.7.1 (February 28, 2017)

### Overview

- [Improved graph selection](http://dbt.readthedocs.io/en/master/guide/usage/#run)
- A new home for dbt
- Snowflake improvements

#### New Features

- improved graph selection for `dbt run` and `dbt test` ([more information](http://dbt.readthedocs.io/en/master/guide/usage/#run)) ([#279](https://github.com/fishtown-analytics/dbt/pull/279))
- profiles.yml now supports Snowflake `role` as an option ([#291](https://github.com/fishtown-analytics/dbt/pull/291))

#### A new home for dbt

In v0.7.1, dbt was moved from the analyst-collective org to the fishtown-analytics org ([#300](https://github.com/fishtown-analytics/dbt/pull/300))

#### Bugfixes

- nicer error if `run-target` was not changed to `target` during upgrade to dbt>=0.7.0


## dbt 0.7.0 (February 9, 2017)

### Overview

- Snowflake Support
- Deprecations

### Snowflake Support

dbt now supports [Snowflake](https://www.snowflake.net/) as a target in addition to Postgres and Redshift! All dbt functionality is supported in this new warehouse. There is a sample snowflake profile in [sample.profiles.yml](https://github.com/fishtown-analytics/dbt/blob/development/sample.profiles.yml) -- you can start using it right away.

### Deprecations

There are a few deprecations in 0.7:

 - `run-target` in profiles.yml is no longer supported. Use `target` instead.
 - Project names (`name` in dbt_project.yml) can now only contain letters, numbers, and underscores, and must start with a letter. Previously they could contain any character.
 - `--dry-run` is no longer supported.

### Notes

#### New Features

- dbt now supports [Snowflake](https://www.snowflake.net/) as a warehouse ([#259](https://github.com/fishtown-analytics/dbt/pull/259))

#### Bugfixes

- use adapter for sort/dist ([#274](https://github.com/fishtown-analytics/dbt/pull/274))

#### Deprecations

- run-target and name validations ([#280](https://github.com/fishtown-analytics/dbt/pull/280))
- dry-run removed ([#281](https://github.com/fishtown-analytics/dbt/pull/281))

#### Changes

- fixed a typo in the docs related to post-run hooks ([#271](https://github.com/fishtown-analytics/dbt/pull/271))
- refactored tracking code to refresh invocation id in a multi-run context ([#273](https://github.com/fishtown-analytics/dbt/pull/273))
- added unit tests for the graph ([#270](https://github.com/fishtown-analytics/dbt/pull/270))

## dbt 0.6.2 (January 16, 2017)

#### Changes

- condense error output when `--debug` is not set ([#265](https://github.com/fishtown-analytics/dbt/pull/265))

## dbt 0.6.1 (January 11, 2017)

#### Bugfixes

- respect `config` options in profiles.yml ([#255](https://github.com/fishtown-analytics/dbt/pull/255))
- use correct `on-run-end` option for post-run hooks ([#261](https://github.com/fishtown-analytics/dbt/pull/261))

#### Changes

- add `--debug` flag, replace calls to `print()` with a global logger ([#256](https://github.com/fishtown-analytics/dbt/pull/256))
- add pep8 check to continuous integration tests and bring codebase into compliance ([#257](https://github.com/fishtown-analytics/dbt/pull/257))

## dbt release 0.6.0

### tl;dr
 - Macros
 - More control over how models are materialized
 - Minor improvements
 - Bugfixes
 - Connor McArthur

### Macros

Macros are snippets of SQL that can be called like functions in models. Macros make it possible to re-use SQL between models
in keeping with the engineering principle of DRY (Dont Repeat Yourself). Moreover, packages can expose Macros that you can use in your own dbt project.

For detailed information on how to use Macros, check out the pull request [here](https://github.com/fishtown-analytics/dbt/pull/245)


### Runtime Materialization Configs
DBT Version 0.6.0 introduces two new ways to control the materialization of models:

#### Non-destructive dbt run [more info](https://github.com/fishtown-analytics/dbt/issues/137)

If you provide the `--non-destructive` argument to `dbt run`, dbt will minimize the amount of time during which your models are unavailable. Specfically, dbt
will
 1. Ignore models materialized as `views`
 2. Truncate tables and re-insert data instead of dropping and re-creating

This flag is useful for recurring jobs which only need to update table models and incremental models.

```bash
dbt run --non-destructive
```

#### Incremental Model Full Refresh [more info](https://github.com/fishtown-analytics/dbt/issues/140)

If you provide the `--full-refresh` argument to `dbt run`, dbt will treat incremental models as table models. This is useful when

1. An incremental model schema changes and you need to recreate the table accordingly
2. You want to reprocess the entirety of the incremental model because of new logic in the model code

```bash
dbt run --full-refresh
```

Note that `--full-refresh` and `--non-destructive` can be used together!

For more information, run
```
dbt run --help
```

### Minor improvements [more info](https://github.com/fishtown-analytics/dbt/milestone/15?closed=1)

#### Add a `{{ target }}` variable to the dbt runtime [more info](https://github.com/fishtown-analytics/dbt/issues/149)
Use `{{ target }}` to interpolate profile variables into your model definitions. For example:

```sql
-- only use the last week of data in development
select * from events

{% if target.name == 'dev' %}
where created_at > getdate() - interval '1 week'
{% endif %}
```

#### User-specified `profiles.yml` dir [more info](https://github.com/fishtown-analytics/dbt/issues/213)
DBT looks for a file called `profiles.yml` in the `~/.dbt/` directory. You can now overide this directory with
```bash
$ dbt run --profiles-dir /path/to/my/dir
```
#### Add timestamp to console output [more info](https://github.com/fishtown-analytics/dbt/issues/125)
Informative _and_ pretty

#### Run dbt from subdirectory of project root [more info](https://github.com/fishtown-analytics/dbt/issues/129)
A story in three parts:
```bash
cd models/snowplow/sessions
vim sessions.sql
dbt run # it works!
```

#### Pre and post run hooks [more info](https://github.com/fishtown-analytics/dbt/issues/226)
```yaml
# dbt_project.yml
name: ...
version: ...

...

# supply either a string, or a list of strings
on-run-start: "create table public.cool_table (id int)"
on-run-end:
  - insert into public.cool_table (id) values (1), (2), (3)
  - insert into public.cool_table (id) values (4), (5), (6)
```

### Bug fixes

We fixed 10 bugs in this release! See the full list [here](https://github.com/fishtown-analytics/dbt/milestone/11?closed=1)

---

## dbt release 0.5.4

### tl;dr
- added support for custom SQL data tests
  - SQL returns 0 results --> pass
  - SQL returns > 0 results --> fail
- dbt-core integration tests
  - running in Continuous Integration environments
    - windows ([appveyor](https://ci.appveyor.com/project/DrewBanin/dbt/branch/development))
    - linux ([circle](https://circleci.com/gh/fishtown-analytics/dbt/tree/master))
  - with [code coverage](https://circleci.com/api/v1/project/fishtown-analytics/dbt/latest/artifacts/0/$CIRCLE_ARTIFACTS/htmlcov/index.html?branch=development)


### Custom SQL data tests

Schema tests have proven to be an essential part of a modern analytical workflow. These schema tests validate basic constraints about your data. Namely: not null, unique, accepted value, and foreign key relationship properties can be asserted using schema tests.

With dbt v0.5.4, you can now write your own custom "data tests". These data tests are SQL SELECT statements that return 0 rows on success, or > 0 rows on failure. A typical data test might look like:

```sql
-- tests/assert_less_than_5_pct_event_cookie_ids_are_null.sql

-- If >= 5% of cookie_ids are null, then the test returns 1 row (failure).
-- If < 5% of cookie_ids are null, then the test returns 0 rows (success)

with calc as (

    select
      sum(case when cookie_id is null then 1 else 0 end)::float / count(*)::float as fraction
    from {{ ref('events') }}

)

select * from calc where fraction < 0.05
```

To enable data tests, add the `test-paths` config to your `dbt_project.yml` file:

```yml
name: 'Vandelay Industries`
version: '1.0'

source-paths: ["models"]
target-path: "target"
test-paths: ["tests"]        # look for *.sql files in the "tests" directory
....
```

Any `.sql` file found in the `test-paths` director(y|ies) will be evaluated as data tests. These tests can be run with:

```bash
dbt test # run schema + data tests
dbt test --schema # run only schema tests
dbt test --data # run only data tests
dbt test --data --schema # run schema + data tests

# For more information, try
dbt test -h
```

### DBT-core integration tests

With the dbt 0.5.4 release, dbt now features a robust integration test suite. These integration tests will help mitigate the risk of software regressions, and in so doing, will help us develop dbt more quickly. You can check out the tests [here](https://github.com/fishtown-analytics/dbt/tree/development/test/integration), and the test results [here (linux/osx)](https://circleci.com/gh/fishtown-analytics/dbt/tree/master) and [here (windows)](https://ci.appveyor.com/project/DrewBanin/dbt/branch/development).


### The Future

You can check out the DBT roadmap [here](https://github.com/fishtown-analytics/dbt/milestones). In the next few weeks, we'll be working on [bugfixes](https://github.com/fishtown-analytics/dbt/milestone/11), [minor features](https://github.com/fishtown-analytics/dbt/milestone/15), [improved macro support](https://github.com/fishtown-analytics/dbt/milestone/14), and  [expanded control over runtime materialization configs](https://github.com/fishtown-analytics/dbt/milestone/9).

As always, feel free to reach out to us on [Slack](http://ac-slackin.herokuapp.com/) with any questions or comments!

---

## dbt release 0.5.3

Bugfix release.

Fixes regressions introduced in 0.5.1 and 0.5.2.

### Fixed 0.5.1 regressions
Incremental models were broken by the new column expansion feature. Column expansion is implemented as
```sql
alter table ... add column tmp_col varchar({new_size});
update ... set tmp_col = existing_col
alter table ... drop column existing_col
alter table ... rename tmp_col to existing_col
```

This has the side-effect of moving the `existing_col` to the "end" of the table. When an incremental model tries to
```sql
insert into {table} (
   select * from tmp_table
)
```
suddenly the columns in `{table}` are incongruent with the columns in `tmp_table`. This insert subsequently fails.

The fix for this issue is twofold:

1. If the incremental model table DOES NOT already exist, avoid inserts altogether. Instead, run a `create table as (...)` statement
2. If the incremental model table DOES already exist, query for the columns in the existing table and use those to build the insert statement, eg:

```sql
insert into "dbt_dbanin"."sessions" ("session_end_tstamp", "session_start_tstamp", ...)
(
    select "session_end_tstamp", "session_start_tstamp", ...
    from "sessions__dbt_incremental_tmp"
);
```

In this way, the source and destination columns are guaranteed to be in the same order!

### Fixed 0.5.2 regressions

We attempted to refactor the way profiles work in dbt. Previously, a default `user` profile was loaded, and the profiles specified in `dbt_project.yml` or on the command line (`with --profile`) would be applied on top of the `user` config. This implementation is [some of the earliest code](https://github.com/fishtown-analytics/dbt/commit/430d12ad781a48af6a754442693834efdf98ffb1) that was committed to dbt.

As `dbt` has grown, we found this implementation to be a little unwieldy and hard to maintain. The 0.5.2 release made it so that only one profile could be loaded at a time. This profile needed to be specified in either `dbt_project.yml` or on the command line with `--profile`. A bug was errantly introduced during this change which broke the handling of dependency projects.

### The future

The additions of automated testing and a more comprehensive manual testing process will go a long way to ensuring the future stability of dbt. We're going to get started on these tasks soon, and you can follow our progress here: https://github.com/fishtown-analytics/dbt/milestone/16 .

As always, feel free to [reach out to us on Slack](http://ac-slackin.herokuapp.com/) with any questions or concerns:




---

## dbt release 0.5.2

Patch release fixing a bug that arises when profiles are overridden on the command line with the `--profile` flag.

See https://github.com/fishtown-analytics/dbt/releases/tag/v0.5.1

---

## dbt release 0.5.1

### 0. tl;dr

1. Raiders of the Lost Archive -- version your raw data to make historical queries more accurate
2. Column type resolution for incremental models (no more `Value too long for character type` errors)
3. Postgres support
4. Top-level configs applied to your project + all dependencies
5. --threads CLI option + better multithreaded output

### 1. Source table archival https://github.com/fishtown-analytics/dbt/pull/183

Commonly, analysts need to "look back in time" at some previous state of data in their mutable tables. Imagine a `users` table which is synced to your data warehouse from a production database. This `users` table is a representation of what your users look like _now_. Consider what happens if you need to look at revenue by city for each of your users trended over time. Specifically, what happens if a user moved from, say, Philadelphia to New York? To do this correctly, you need to archive snapshots of the `users` table on a recurring basis. With this release, dbt now provides an easy mechanism to store such snapshots.

To use this new feature, declare the tables you want to archive in your `dbt_project.yml` file:

```yaml
archive:
    - source_schema: synced_production_data  # schema to look for tables in (declared below)
      target_schema: dbt_archive             # where to archive the data to
      tables:                                # list of tables to archive
        - source_table: users                # table to archive
          target_table: users_archived       # table to insert archived data into
          updated_at: updated_at             # used to determine when data has changed
          unique_key: id                     # used to generate archival query

        - source_table: some_other_table
           target_table: some_other_table_archive
           updated_at: "updatedAt"
           unique_key: "expressions || work || LOWER(too)"

    - source_schema: some_other_schema
      ....
```

The archived tables will mirror the schema of the source tables they're generated from. In addition, three fields are added to the archive table:

1. `valid_from`: The timestamp when this archived row was inserted (and first considered valid)
1. `valid_to`: The timestamp when this archived row became invalidated. The first archived record for a given `unique_key` has `valid_to = NULL`. When newer data is archived for that `unique_key`, the `valid_to` field of the old record is set to the `valid_from` field of the new record!
1. `scd_id`: A unique key generated for each archive record. Scd = [Slowly Changing Dimension](https://en.wikipedia.org/wiki/Slowly_changing_dimension#Type_2:_add_new_row).

dbt models can be built on top of these archived tables. The most recent record for a given `unique_key` is the one where `valid_to` is `null`.

To run this archive process, use the command `dbt archive`. After testing and confirming that the archival works, you should schedule this process through cron (or similar).

### 2. Incremental column expansion https://github.com/fishtown-analytics/dbt/issues/175

Incremental tables are a powerful dbt feature, but there was at least one edge case which makes working with them difficult. During the first run of an incremental model, Redshift will infer a type for every column in the table. Subsequent runs can insert new data which does not conform to the expected type. One example is a `varchar(16)` field which is inserted into a `varchar(8)` field.
In practice, this error looks like:

```
Value too long for character type
DETAIL:
  -----------------------------------------------
  error:  Value too long for character type
  code:      8001
  context:   Value too long for type character varying(8)
  query:     3743263
  location:  funcs_string.hpp:392
  process:   query4_35 [pid=18194]
  -----------------------------------------------
```

With this release, dbt will detect when column types are incongruent and will attempt to reconcile these different types if possible. Specifically, dbt will alter the incremental model table schema from `character varying(x)` to `character varying(y)` for some `y > x`. This should drastically reduce the occurrence of this class of error.

### 3. First-class Postgres support https://github.com/fishtown-analytics/dbt/pull/183

With this release, Postgres became a first-class dbt target. You can configure a postgres database target in your `~/.dbt/profiles.yml` file:

```yaml
warehouse:
  outputs:
    dev:
      type: postgres    # configure a target for Postgres
      host: localhost
      user: Drew
      ....
  run-target: dev
```

While Redshift is built on top of Postgres, the two are subtly different. For instance, Redshift supports sort and dist keys, while Postgres does not! dbt will use the database target `type` parameter to generate the appropriate SQL for the target database.

### 4. Root-level configs https://github.com/fishtown-analytics/dbt/issues/161

Configurations in `dbt_project.yml` can now be declared at the `models:` level. These configurations will apply to the primary project, as well as any dependency projects. This feature is particularly useful for setting pre- or post- hooks that run for *every* model. In practice, this looks like:

```yaml
name: 'My DBT Project'

models:
    post-hook:
        - "grant select on {{this}} to looker_user"     # Applied to 'My DBT Project' and 'Snowplow' dependency
    'My DBT Project':
        enabled: true
    'Snowplow':
        enabled: true
```

### 5. --threads CLI option https://github.com/fishtown-analytics/dbt/issues/143

The number of threads that DBT uses can now be overridden with a CLI argument. The number of threads used must be between 1 and 8.

```bash
dbt run --threads 1    # fine
# or
dbt run --threads 4    # great
# or
dbt run --threads 42    # too many!
```

In addition to this new CLI argument, the output from multi-threaded dbt runs should be a little more orderly now. Models won't show as `START`ed until they're actually queued to run. Previously, the output here was a little confusing. Happy threading!

### Upgrading

To upgrade to version 0.5.1 of dbt, run:

``` bash
pip install --upgrade dbt
```

### And another thing

- Join us on [slack](http://ac-slackin.herokuapp.com/) with questions or comments

Made with ♥️ by 🐟🏙  📈

---

### 0. tl;dr

- use a temp table when executing incremental models
- arbitrary configuration (using config variables)
- specify branches for dependencies
- more & better docs

### 1. new incremental model generation https://github.com/fishtown-analytics/dbt/issues/138

In previous versions of dbt, an edge case existed which caused the `sql_where` query to select different rows in the `delete` and `insert` steps. As a result, it was possible to construct incremental models which would insert duplicate records into the specified table. With this release, DBT uses a temp table which will 1) circumvent this issue and 2) improve query performance. For more information, check out the GitHub issue: https://github.com/fishtown-analytics/dbt/issues/138

### 2. Arbitrary configuration https://github.com/fishtown-analytics/dbt/issues/146

Configuration in dbt is incredibly powerful: it is what allows models to change their behavior without changing their code. Previously, all configuration was done using built-in parameters, but that actually limits the user in the power of configuration.

With this release, you can inject variables from `dbt_project.yml` into your top-level and dependency models. In practice, variables work like this:

```yml
# dbt_project.yml

models:
  my_project:
    vars:
      exclude_ip: '192.168.1.1'
```

```sql
-- filtered_events.sql

-- source code
select * from public.events where ip_address != '{{ var("exclude_ip") }}'

-- compiles to
select * from public.events where ip_address != '192.168.1.1'
```

The `vars` parameter in `dbt_project.yml` is compiled, so you can use jinja templating there as well! The primary use case for this is specifying "input" models to a dependency.

Previously, dependencies used `ref(...)` to select from a project's base models. That interface was brittle, and the idea that dependency code had unbridled access to all of your top-level models made us a little uneasy. As of this release, we're deprecating the ability for dependencies to `ref(...)` top-level models. Instead, the recommended way for this to work is with vars! An example:

```sql
-- dbt_modules/snowplow/models/events.sql

select * from {{ var('snowplow_events_table') }}
```

and

```yml
models:
  Snowplow:
    vars:
      snowplow_events_table: "{{ ref('base_events') }}"
```

This effectively mirrors the previous behavior, but it much more explicit about what's happening under the hood!

### 3. specify a dependency branch https://github.com/fishtown-analytics/dbt/pull/165

With this release, you can point DBT to a specific branch of a dependency repo. The syntax looks like this:

```
repositories:
    - https://github.com/fishtown-analytics/dbt-audit.git@development # use the "development" branch
```

### 4. More & Better Docs!

Check em out! And let us know if there's anything you think we can improve upon!


### Upgrading

To upgrade to version 0.5.0 of dbt, run:

``` bash
pip install --upgrade dbt
```

---

### 0. tl;dr

- `--version` command
- pre- and post- run hooks
- windows support
- event tracking


### 1. --version https://github.com/fishtown-analytics/dbt/issues/135

The `--version` command was added to help aid debugging. Further, organizations can use it to ensure that everyone in their org is up-to-date with dbt.

```bash
$ dbt --version
installed version: 0.4.7
   latest version: 0.4.7
Up to date!
```

### 2. pre-and-post-hooks https://github.com/fishtown-analytics/dbt/pull/147

With this release, you can now specify `pre-` and `post-` hooks that are run before and after a model is run, respectively. Hooks are useful for running `grant` statements, inserting a log of runs into an audit table, and more! Here's an example of a grant statement implemented using a post-hook:

```yml
models:
  my_project:
    post-hook: "grant select on table {{this}} to looker_user"
    my_model:
       materialized: view
    some_model:
      materialized: table
      post-hook: "insert into my_audit_table (model_name, run_at) values ({{this.name}}, getdate())"
```

Hooks are recursively appended, so the `my_model` model will only receive the `grant select...` hook, whereas the `some_model` model will receive _both_ the `grant select...` and `insert into...` hooks.

Finally, note that the `grant` statement uses the (hopefully familiar) `{{this}}` syntax whereas the `insert` statement uses the `{{this.name}}` syntax. When DBT creates a model:
 - A temp table is created
 - The original model is dropped
 - The temp table is renamed to the final model name

DBT will intelligently uses the right table/view name when you invoke `{{this}}`, but you have a couple of more specific options available if you need them:

```
{{this}} : "schema"."table__dbt_tmp"
{{this.schema}}: "schema"
{{this.table}}: "table__dbt_tmp"
{{this.name}}: "table"
```

### 3. Event tracking https://github.com/fishtown-analytics/dbt/issues/89

We want to build the best version of DBT possible, and a crucial part of that is understanding how users work with DBT. To this end, we've added some really simple event tracking to DBT (using Snowplow). We do not track credentials, model contents or model names (we consider these private, and frankly none of our business). This release includes basic event tracking that reports 1) when dbt is invoked 2) when models are run, and 3) basic platform information (OS + python version). The schemas for these events can be seen [here](https://github.com/fishtown-analytics/dbt/tree/development/events/schemas/com.fishtownanalytics)

You can opt out of event tracking at any time by adding the following to the top of you `~/.dbt/profiles.yml` file:

```yaml
config:
    send_anonymous_usage_stats: False
```

### 4. Windows support https://github.com/fishtown-analytics/dbt/pull/154

![windows](https://pbs.twimg.com/profile_images/571398080688181248/57UKydQS.png)

---

dbt v0.4.1 provides improvements to incremental models, performance improvements, and ssh support for db connections.

### 0. tl;dr

- slightly modified dbt command structure
- `unique_key` setting for incremental models
- connect to your db over ssh
- no more model-defaults
- multithreaded schema tests

If you encounter an SSL/cryptography error while upgrading to this version of dbt, check that your version of pip is up-to-date

```bash
pip install -U pip
pip install -U dbt
```

### 1. new dbt command structure https://github.com/fishtown-analytics/dbt/issues/109
```bash
# To run models
dbt run # same as before

# to dry-run models
dbt run --dry # previously dbt test

# to run schema tests
dbt test # previously dbt test --validate
```

### 2. Incremental model improvements https://github.com/fishtown-analytics/dbt/issues/101

Previously, dbt calculated "new" incremental records to insert by querying for rows which matched some `sql_where` condition defined in the model configuration. This works really well for atomic datasets like a clickstream event log -- once inserted, these records will never change. Other datasets, like a sessions table comprised of many pageviews for many users, can change over time. Consider the following scenario:

User 1 Session 1 Event 1 @ 12:00
User 1 Session 1 Event 2 @ 12:01
-- dbt run --
User 1 Session 1 Event 3 @ 12:02

In this scenario, there are two possible outcomes depending on the `sql_where` chosen: 1) Event 3 does not get included in the Session 1 record for User 1 (bad), or 2) Session 1 is duplicated in the sessions table (bad). Both of these outcomes are inadequate!

With this release, you can now add a `unique_key` expression to an incremental model config. Records matching the `unique_key` will be `delete`d from the incremental table, then `insert`ed as usual. This makes it possible to maintain data accuracy without recalculating the entire table on every run.

The `unique_key` can be any expression which uniquely defines the row, eg:
```yml
sessions:
  materialized: incremental
  sql_where: "session_end_tstamp > (select max(session_end_tstamp) from {{this}})"
  unique_key: user_id || session_index
```

### 3. Run schema validations concurrently https://github.com/fishtown-analytics/dbt/issues/100

The `threads` run-target config now applies to schema validations too. Try it with `dbt test`

### 4. Connect to database over ssh https://github.com/fishtown-analytics/dbt/issues/93

Add an `ssh-host` parameter to a run-target to connect to a database over ssh. The `ssh-host` parameter should be the name of a `Host` in your `~/.ssh/config` file [more info](http://nerderati.com/2011/03/17/simplify-your-life-with-an-ssh-config-file/)

```yml
warehouse:
  outputs:
    dev:
      type: redshift
      host: my-redshift.amazonaws.com
      port: 5439
      user: my-user
      pass: my-pass
      dbname: my-db
      schema: dbt_dbanin
      threads: 8
      ssh-host: ssh-host-name  # <------ Add this line
  run-target: dev
```

### Remove the model-defaults config https://github.com/fishtown-analytics/dbt/issues/111

The `model-defaults` config doesn't make sense in a dbt world with dependencies. To apply default configs to your package, add the configs immediately under the package definition:

```yml
models:
    My_Package:
        enabled: true
        materialized: table
        snowplow:
            ...
```

---

## dbt v0.4.0

dbt v0.4.0 provides new ways to materialize models in your database.

### 0. tl;dr
 - new types of materializations: `incremental` and `ephemeral`
 - if upgrading, change `materialized: true|false` to `materialized: table|view|incremental|ephemeral`
 - optionally specify model configs within the SQL file

### 1. Feature: `{{this}}` template variable https://github.com/fishtown-analytics/dbt/issues/81
The `{{this}}` template variable expands to the name of the model being compiled. For example:

```sql
-- my_model.sql
select 'the fully qualified name of this model is {{ this }}'
-- compiles to
select 'the fully qualified name of this model is "the_schema"."my_model"'
```

### 2. Feature: `materialized: incremental` https://github.com/fishtown-analytics/dbt/pull/90

After initially creating a table, incremental models will `insert` new records into the table on subsequent runs. This drastically speeds up execution time for large, append-only datasets.

Each execution of dbt run will:
 - create the model table if it doesn't exist
 - insert new records into the table

New records are identified by a `sql_where` model configuration option. In practice, this looks like:

```yml

sessions:
    materialized: incremental
    sql_where: "session_start_time > (select max(session_start_time) from {{this}})"
```

There are a couple of new things here. Previously, `materialized` could either be set to `true` or `false`. Now, the valid options include `view`, `table,` `incremental`, and `ephemeral` (more on this last one below). Also note that incremental models generally require use of the {{this}} template variable to identify new records.

The `sql_where` field is supplied as a `where` condition on a subquery containing the model definition. This resultset is then inserted into the target model. This looks something like:

```sql
insert into schema.model (
    select * from (
        -- compiled model definition
    ) where {{sql_where}}
)
```

### 3. Feature: `materialized: ephemeral` https://github.com/fishtown-analytics/dbt/issues/78

Ephemeral models are injected as CTEs (`with` statements) into any model that `ref`erences them. Ephemeral models are part of the dependency graph and generally function like any other model, except ephemeral models are not compiled to their own files or directly created in the database. This is useful for intermediary models which are shared by other downstream models, but shouldn't be queried directly from outside of dbt.

To make a model ephemeral:

```yml
employees:
    materialized: ephemeral
```

Suppose you wanted to exclude `employees` from your `users` table, but you don't want to clutter your analytics schema with an `employees` table.

```sql
-- employees.sql
select * from public.employees where is_deleted = false

-- users.sql
select *
from {{ref('users')}}
where email not in (select email from {{ref('employees')}})
```

The compiled SQL would look something like:
```sql
with __dbt__CTE__employees as (
  select * from public.employees where is_deleted = false
)
select *
from users
where email not in (select email from __dbt__CTE__employees)
```

Ephemeral models play nice with other ephemeral models, incremental models, and regular table/view models. Feel free to mix and match different materialization options to optimize for performance and simplicity.


### 4. Feature: In-model configs https://github.com/fishtown-analytics/dbt/issues/88

Configurations can now be specified directly inside of models. These in-model configs work exactly the same as configs inside of the dbt_project.yml file.

An in-model-config looks like this:

```sql
-- users.sql

-- python function syntax
{{ config(materialized="incremental", sql_where="id > (select max(id) from {{this}})") }}
-- OR json syntax
{{
    config({"materialized:" "incremental", "sql_where" : "id > (select max(id) from {{this}})"})
}}

select * from public.users
```

The config resolution order is:
  1. dbt_project.yml `model-defaults`
  2. in-model config
  3. dbt_project.yml `models` config

### 5. Fix: dbt seed null values https://github.com/fishtown-analytics/dbt/issues/102

Previously, `dbt seed` would insert empty CSV cells as `"None"`, whereas they should have been `NULL`. Not anymore!


---

## dbt v0.3.0

Version 0.3.0 comes with the following updates:

#### 1. Parallel model creation https://github.com/fishtown-analytics/dbt/pull/83
dbt will analyze the model dependency graph and can create models in parallel if possible. In practice, this can significantly speed up the amount of time it takes to complete `dbt run`. The number of threads dbt uses must be between 1 and 8. To configure the number of threads dbt uses, add the `threads` key to your dbt target in `~/.dbt/profiles.yml`, eg:

```yml
user:
  outputs:
    my-redshift:
      type: redshift
      threads: 4         # execute up to 4 models concurrently
      host: localhost
      ...
  run-target: my-redshift
```

For a complete example, check out [a sample profiles.yml file](https://github.com/fishtown-analytics/dbt/blob/master/sample.profiles.yml)

#### 2. Fail only within a single dependency chain https://github.com/fishtown-analytics/dbt/issues/63
If a model cannot be created, it won't crash the entire `dbt run` process. The errant model will fail and all of its descendants will be "skipped". Other models which do not depend on the failing model (or its descendants) will still be created.

#### 3. Logging https://github.com/fishtown-analytics/dbt/issues/64, https://github.com/fishtown-analytics/dbt/issues/65
dbt will log output from the `dbt run` and `dbt test` commands to a configurable logging directory. By default, this directory is called `logs/`. The log filename is `dbt.log` and it is rotated on a daily basic. Logs are kept for 7 days.

To change the name of the logging directory, add the following line to your `dbt_project.yml` file:
```yml
log-path: "my-logging-directory" # will write logs to my-logging-directory/dbt.log
```

#### 4. Minimize time models are unavailable in the database https://github.com/fishtown-analytics/dbt/issues/68
Previously, dbt would create models by:
1. dropping the existing model
2. creating the new model

This resulted in a significant amount of time in which the model was inaccessible to the outside world. Now, dbt creates models by:
1. creating a temporary model `{model-name}__dbt_tmp`
2. dropping the existing model
3. renaming the tmp model name to the actual model name

#### 5. Arbitrarily deep nesting https://github.com/fishtown-analytics/dbt/issues/50
Previously, all models had to be located in a directory matching `models/{model group}/{model_name}.sql`. Now, these models can be nested arbitrarily deeply within a given dbt project. For instance, `models/snowplow/sessions/transformed/transformed_sessions.sql` is a totally valid model location with this release.

To configure these deeply-nested models, just nest the config options within the `dbt_project.yml` file. The only caveat is that you need to specify the dbt project name as the first key under the `models` object, ie:

```yml
models:
  'Your Project Name':
    snowplow:
      sessions:
        transformed:
          transformed_sessions:
            enabled: true
```

More information is available on the [issue](https://github.com/fishtown-analytics/dbt/issues/50) and in the [sample dbt_project.yml file](https://github.com/fishtown-analytics/dbt/blob/master/sample.dbt_project.yml)

#### 6. don't try to create a schema if it already exists https://github.com/fishtown-analytics/dbt/issues/66
dbt run would execute `create schema if not exists {schema}`. This would fail if the dbt user didn't have sufficient permissions to create the schema, even if the schema already existed! Now, dbt checks for the schema existence and only attempts to create the schema if it doesn't already exist.

#### 7. Semantic Versioning
The previous release of dbt was v0.2.3.0 which isn't a semantic version. This and all future dbt releases will conform to semantic version in the format `{major}.{minor}.{patch}`.
---

## dbt v0.2.3.0
Version 0.2.3.0 of dbt comes with the following updates:

#### 1. Fix: Flip referential integrity arguments (breaking)
Referential integrity validations in a `schema.yml` file were previously defined relative to the *parent* table:
```yaml
account:
  constraints:
    relationships:
      - {from: id, to: people, field: account_id}
```

Now, these validations are specified relative to the *child* table
```yaml
people:
  constraints:
    relationships:
      - {from: account_id, to: accounts, field: id}
```

For more information, run `dbt test -h`

#### 2. Feature: seed tables from a CSV
Previously, auxiliary data needed to be shoehorned into a view comprised of union statements, eg.
```sql
select 22 as "type", 'Chat Transcript' as type_name, 'chatted via olark' as event_name union all
select 21, 'Custom Redirect', 'clicked a custom redirect' union all
select 6, 'Email', 'email sent' union all
...
```

That's not a scalable solution. Now you can load CSV files into your data warehouse:
1. Add a CSV file (with a header) to the `data/` directory
2. Run `dbt seed` to create a table from the CSV file!
3. The table name with be the filename (sans `.csv`) and it will be placed in your `run-target`'s schema

Subsequent calls to `dbt seed` will truncate the seeded tables (if they exist) and re-insert the data. If the table schema changes, you can run `dbt seed --drop-existing` to drop the table and recreate it.

For more information, run `dbt seed -h`

#### 3. Feature: compile analytical queries

Versioning your SQL models with dbt is a great practice, but did you know that you can also version your analyses? Any SQL files in the `analysis/` dir will be compiled (ie. table names will be interpolated) and placed in the `target/build-analysis/` directory. These analytical queries will _not_ be run against your data warehouse with `dbt run` -- you should copy/paste them into the data analysis tool of your choice.

#### 4. Feature: accepted values validation

In your `schema.yml` file, you can now add `accepted-values` validations:
```yaml
accounts:
  constraints:
    accepted-values:
      - {field: type, values: ['paid', 'free']}
```

This test will determine how many records in the `accounts` model have a `type` other than `paid` or `free`.

#### 5. Feature: switch profiles and targets on the command line

Switch between profiles with `--profile [profile-name]` and switch between run-targets with `--target [target-name]`.

Targets should be something like "prod" or "dev" and profiles should be something like "my-org" or "my-side-project"

```yaml
side-project:
  outputs:
    prod:
      type: redshift
      host: localhost
      port: 5439
      user: Drew
      pass:
      dbname: data_generator
      schema: ac_drew
    dev:
      type: redshift
      host: localhost
      port: 5439
      user: Drew
      pass:
      dbname: data_generator
      schema: ac_drew_dev
  run-target: dev
```

To compile models using the `dev` environment of my `side-project` profile:
`$ dbt compile --profile side-project --target dev`
or for `prod`:
`$ dbt compile --profile side-project --target prod`

You can also add a "profile' config to the `dbt_config.yml` file to fix a dbt project to a specific profile:

```yaml
...
test-paths: ["test"]
data-paths: ["data"]

# Fix this project to the "side-project" profile
# You can still use --target to switch between environments!
profile: "side-project"

model-defaults:
....
```
