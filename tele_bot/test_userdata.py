import unittest

from classes import User
from dataclasses import astuple


class UserDataTestCase(unittest.TestCase):
    # Test user data conversion to sqlite data (to tuple)
    def testUserDataToSql(self):
        regular_user = User(
            id=1,
            config_path="./config.json",
            is_admin=0
        )
        sql_data = astuple(regular_user)
        self.assertEqual(sql_data, (1, "./config.json", 0))


if __name__ == '__main__':
    unittest.main()
