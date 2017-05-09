create table test_macros_016.expected_dep_macro (
	foo TEXT,
	bar TEXT
);

create table test_macros_016.expected_local_macro (
	foo2 TEXT,
	bar2 TEXT
);

insert into test_macros_016.expected_dep_macro (foo, bar)
values ('arg1', 'arg2');

insert into test_macros_016.expected_local_macro (foo2, bar2)
values ('arg1', 'arg2'), ('arg3', 'arg4');



