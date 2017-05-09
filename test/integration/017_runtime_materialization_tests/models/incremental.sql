{{
  config(
    materialized = "incremental",
    sql_where = "id>(select max(id) from {{this}})"
  )
}}

select * from "runtime_materialization_017"."seed"
