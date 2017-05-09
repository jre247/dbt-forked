create table "simple_archive_004"."seed" (
	"id" INTEGER,
	"first_name" VARCHAR(50),
	"last_name" VARCHAR(50),
	"email" VARCHAR(50),
	"gender" VARCHAR(50),
	"ip_address" VARCHAR(20),
	"updated_at" TIMESTAMP WITHOUT TIME ZONE
);

create table "simple_archive_004"."archive_expected" (
	"id" INTEGER,
	"first_name" VARCHAR(50),
	"last_name" VARCHAR(50),
	"email" VARCHAR(50),
	"gender" VARCHAR(50),
	"ip_address" VARCHAR(20),

	-- archival fields
	"updated_at" TIMESTAMP WITHOUT TIME ZONE,
	"valid_from" TIMESTAMP WITHOUT TIME ZONE,
	"valid_to"   TIMESTAMP WITHOUT TIME ZONE,
	"scd_id"     VARCHAR(255),
	"dbt_updated_at" TIMESTAMP WITHOUT TIME ZONE
);


-- seed inserts
insert into "simple_archive_004"."seed" ("id", "first_name", "last_name", "email", "gender", "ip_address", "updated_at") values
(1, 'Judith', 'Kennedy', 'jkennedy0@phpbb.com', 'Female', '54.60.24.128', '2015-12-24 12:19:28'),
(2, 'Arthur', 'Kelly', 'akelly1@eepurl.com', 'Male', '62.56.24.215', '2015-10-28 16:22:15'),
(3, 'Rachel', 'Moreno', 'rmoreno2@msu.edu', 'Female', '31.222.249.23', '2016-04-05 02:05:30'),
(4, 'Ralph', 'Turner', 'rturner3@hp.com', 'Male', '157.83.76.114', '2016-08-08 00:06:51'),
(5, 'Laura', 'Gonzales', 'lgonzales4@howstuffworks.com', 'Female', '30.54.105.168', '2016-09-01 08:25:38'),
(6, 'Katherine', 'Lopez', 'klopez5@yahoo.co.jp', 'Female', '169.138.46.89', '2016-08-30 18:52:11'),
(7, 'Jeremy', 'Hamilton', 'jhamilton6@mozilla.org', 'Male', '231.189.13.133', '2016-07-17 02:09:46'),
(8, 'Heather', 'Rose', 'hrose7@goodreads.com', 'Female', '87.165.201.65', '2015-12-29 22:03:56'),
(9, 'Gregory', 'Kelly', 'gkelly8@trellian.com', 'Male', '154.209.99.7', '2016-03-24 21:18:16'),
(10, 'Rachel', 'Lopez', 'rlopez9@themeforest.net', 'Female', '237.165.82.71', '2016-08-20 15:44:49'),
(11, 'Donna', 'Welch', 'dwelcha@shutterfly.com', 'Female', '103.33.110.138', '2016-02-27 01:41:48'),
(12, 'Russell', 'Lawrence', 'rlawrenceb@qq.com', 'Male', '189.115.73.4', '2016-06-11 03:07:09'),
(13, 'Michelle', 'Montgomery', 'mmontgomeryc@scientificamerican.com', 'Female', '243.220.95.82', '2016-06-18 16:27:19'),
(14, 'Walter', 'Castillo', 'wcastillod@pagesperso-orange.fr', 'Male', '71.159.238.196', '2016-10-06 01:55:44'),
(15, 'Robin', 'Mills', 'rmillse@vkontakte.ru', 'Female', '172.190.5.50', '2016-10-31 11:41:21'),
(16, 'Raymond', 'Holmes', 'rholmesf@usgs.gov', 'Male', '148.153.166.95', '2016-10-03 08:16:38'),
(17, 'Gary', 'Bishop', 'gbishopg@plala.or.jp', 'Male', '161.108.182.13', '2016-08-29 19:35:20'),
(18, 'Anna', 'Riley', 'arileyh@nasa.gov', 'Female', '253.31.108.22', '2015-12-11 04:34:27'),
(19, 'Sarah', 'Knight', 'sknighti@foxnews.com', 'Female', '222.220.3.177', '2016-09-26 00:49:06'),
(20, 'Phyllis', 'Fox', 'pfoxj@creativecommons.org', 'Female', '163.191.232.95', '2016-08-21 10:35:19');


-- populate archive table
insert into "simple_archive_004"."archive_expected" (
    "id",
    "first_name",
    "last_name",
    "email",
    "gender",
    "ip_address",
    "updated_at",
    "valid_from",
    "valid_to",
    "dbt_updated_at",
    "scd_id"
)

select
    "id",
    "first_name",
    "last_name",
    "email",
    "gender",
    "ip_address",
    "updated_at",
    -- fields added by archival
    "updated_at" as valid_from,
    null::timestamp as valid_to,
    "updated_at" as dbt_updated_at,
    md5("id" || '-' || "first_name" || '|' || "updated_at"::text) as scd_id
from "simple_archive_004"."seed";
