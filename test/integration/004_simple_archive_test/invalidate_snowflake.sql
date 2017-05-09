
-- update records 11 - 21. Change email and updated_at field
update "simple_archive_004"."seed" set
    "updated_at" = DATEADD(hour, 1, "updated_at"),
    "email"      = 'new_' || "email"
where "id" >= 10 and "id" <= 20;


-- invalidate records 11 - 21
update "simple_archive_004"."archive_expected" set
    "valid_to"   = DATEADD(hour, 1, "updated_at")
where "id" >= 10 and "id" <= 20;
