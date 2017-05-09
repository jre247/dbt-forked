from nose.plugins.attrib import attr
from test.integration.base import DBTIntegrationTest, DBT_PROFILES
import os, shutil, yaml

class TestCLIInvocation(DBTIntegrationTest):

    def setUp(self):
        DBTIntegrationTest.setUp(self)

        self.run_sql_file("test/integration/015_cli_invocation_tests/seed.sql")

    @property
    def schema(self):
        return "test_cli_invocation_015"

    @property
    def models(self):
        return "test/integration/015_cli_invocation_tests/models"

    @attr(type='postgres')
    def test_toplevel_dbt_run(self):
        self.run_dbt(['run'])
        self.assertTablesEqual("seed", "model")

    @attr(type='postgres')
    def test_subdir_dbt_run(self):
        os.chdir(os.path.join(self.models, "subdir1"))

        self.run_dbt(['run'])
        self.assertTablesEqual("seed", "model")

class TestCLIInvocationWithProfilesDir(DBTIntegrationTest):

    def setUp(self):
        DBTIntegrationTest.setUp(self)

        self.run_sql("DROP SCHEMA IF EXISTS {} CASCADE;".format(self.custom_schema))
        self.run_sql("CREATE SCHEMA {};".format(self.custom_schema))

        if not os.path.exists('./dbt-profile'):
            os.makedirs('./dbt-profile')

        with open("./dbt-profile/profiles.yml", 'w') as f:
            yaml.safe_dump(self.custom_profile_config(), f, default_flow_style=True)

        self.run_sql_file("test/integration/015_cli_invocation_tests/seed_custom.sql")

    def tearDown(self):
        DBTIntegrationTest.tearDown(self)

        shutil.rmtree("./dbt-profile")

    def custom_profile_config(self):
        return {
            'config': {
                'send_anonymous_usage_stats': False
            },
            'test': {
                'outputs': {
                    'default': {
                        'type': 'postgres',
                        'threads': 1,
                        'host': 'database',
                        'port': 5432,
                        'user': 'root',
                        'pass': 'password',
                        'dbname': 'dbt',
                        'schema': self.custom_schema
                    },
                },
                'run-target': 'default'
            }
        }

    @property
    def schema(self):
        return "test_cli_invocation_015"

    @property
    def custom_schema(self):
        return "test_cli_invocation_015_custom"

    @property
    def models(self):
        return "test/integration/015_cli_invocation_tests/models"

    @attr(type='postgres')
    def test_toplevel_dbt_run_with_profile_dir_arg(self):
        self.run_dbt(['run', '--profiles-dir', 'dbt-profile'])

        actual = self.run_sql("select id from {}.model".format(self.custom_schema), fetch='one')

        expected = (1, )
        self.assertEqual(actual, expected)

        res = self.run_dbt(['test', '--profiles-dir', 'dbt-profile'])

        # make sure the test runs against `custom_schema`
        for test_result in res:
            self.assertTrue(self.custom_schema,
                            test_result.node.get('wrapped_sql'))
