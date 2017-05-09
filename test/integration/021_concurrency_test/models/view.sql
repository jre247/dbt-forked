{{
  config(
    materialized = "view"
  )
}}

select * from "concurrency_021"."seed"
