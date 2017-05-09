{{
  config(
    materialized = "view"
  )
}}

select * from "runtime_materialization_017"."seed"
