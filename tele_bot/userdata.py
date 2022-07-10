import sqlite3
import logging
from pathlib import Path


logger = logging.getLogger(__name__)


USERDATA_DB = Path("./data/userdata.db")

CREATE_TABLE = (
        "CREATE TABLE IF NOT EXISTS user("
        "id INTEGER UNIQUE PRIMARY KEY NOT NULL, "
        "conf_file TEXT, "
        "is_admin INTEGER"
        ");"
)

ADD_USER = (
        "INSERT INTO user (id, conf_file, is_admin)"
        "VALUES(?, ?, ?);"
)

GET_USER_DATA = (
        "SELECT conf_file, is_admin "
        "FROM user "
        "WHERE id == ?;"
)


with sqlite3.connect(USERDATA_DB) as conn:
    conn.execute(CREATE_TABLE)
    conn.commit()


def add_admins(admins: str):
    admins_data = [(admin_id, None, 1) for admin_id in admins.split(",")]
    with sqlite3.connect(USERDATA_DB) as conn:
        cur = conn.cursor()
        for admin_data in admins_data:
            try:
                cur.execute(ADD_USER, admin_data)
                conn.commit()
            except sqlite3.IntegrityError:
                logger.warn(f"Admin {admin_data[0]} not added, already exists")


def get_user_data(id: int) -> tuple[str, int]:
    with sqlite3.connect(USERDATA_DB) as conn:
        cur = conn.cursor()
        result = cur.execute(GET_USER_DATA, (id,)).fetchone()
        if result == None:
            return (None, None)
        return result

