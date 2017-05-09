{{
  config(
    materialized = "table",
    sort = 'first_name',
    dist = 'first_name'
  )
}}

select * from "adaper_ddl_018"."seed"
