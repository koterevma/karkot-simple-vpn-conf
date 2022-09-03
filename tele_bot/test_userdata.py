import unittest

from classes import User
from dataclasses import asdict


class UserDataTestCase(unittest.TestCase):
    # Test user data conversion to sqlite data (to tuple)
    def testUserDataToSql(self):
        regular_user = User(
            id=1,
            config_path="./config.json",
            is_admin=0
        )
        sql_data = asdict(regular_user)
        self.assertEqual(sql_data, dict(id=1, config_path="./config.json", is_admin=0))


if __name__ == '__main__':
    unittest.main()
