from sqlalchemy.engine.url import make_url

from clickhouse_sqlalchemy.drivers.http.base import ClickHouseDialect_http
from tests.testcase import BaseTestCase


class TestConnectArgs(BaseTestCase):
    def setUp(self):
        self.dialect = ClickHouseDialect_http()

    def credentials(self, url):
        args, _ = self.dialect.create_connect_args(make_url(url))
        return args[2:]

    def test_no_credentials_means_default_user(self):
        self.assertEqual(
            self.credentials('clickhouse+http://localhost/db'), ('default', '')
        )

    def test_user_without_password(self):
        self.assertEqual(
            self.credentials('clickhouse+http://reader@localhost/db'),
            ('reader', '')
        )

    def test_user_and_password(self):
        self.assertEqual(
            self.credentials('clickhouse+http://reader:secret@localhost/db'),
            ('reader', 'secret')
        )
