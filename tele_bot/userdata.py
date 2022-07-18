import sqlite3
import logging
from pathlib import Path


logger = logging.getLogger(__name__)


USERDATA_DB = Path("./data/userdata.db")

CREATE_TABLE = (
        "CREATE TABLE IF NOT EXISTS user("
        "id INTEGER UNIQUE PRIMARY KEY NOT NULL, "
        "data_path TEXT, "
        "is_admin INTEGER"
        ");"
)

ADD_USER = (
        "INSERT INTO user (id, data_path, is_admin)"
        "VALUES(?, ?, ?);"
)

GET_USER_DATA = (
        "SELECT data_path, is_admin "
        "FROM user "
        "WHERE id = ?;"
)

UPDATE_USER = (
        "UPDATE user "
        "SET data_path = ? "
        "is_admin = ? "
        "WHERE id = ?;"
)

GET_ADMIN_IDS = (
        "SELECT id "
        "FROM user "
        "WHERE is_admin = 1;"
)


with sqlite3.connect(USERDATA_DB) as conn:
    conn.execute(CREATE_TABLE)
    conn.commit()


def add_user(user_id: int, data_path: str, is_admin: int) -> None:
    with sqlite3.connect(USERDATA_DB) as conn:
        cur = conn.cursor()
        try:
            cur.execute(ADD_USER, (user_id, data_path, is_admin))
            conn.commit()
        except sqlite3.IntegrityError:
            logger.warn(f"User {user_id} not added, already exists in database")
    

def add_admins(admins: str) -> None:
    admins_data = [(admin_id, None, 1) for admin_id in admins.split(",")]
    for admin_data in admins_data:
        add_user(*admin_data)


def update_user(user_id: int, data_path: str, is_admin: int = None):
    if is_admin is None:
        is_admin = get_user_data(user_id)[1]
    with sqlite3.connect(USERDATA_DB) as conn:
        cur = conn.cursor()
        try:
            cur.execute(UPDATE_USER, (data_path, is_admin, user_id))
            conn.commit()
        except sqlite3.Error as e:
            logger.error("In update_user: " + str(e))


def get_user_data(id_: int) -> tuple[str, int]:
    with sqlite3.connect(USERDATA_DB) as conn:
        cur = conn.cursor()
        result = cur.execute(GET_USER_DATA, (id_,)).fetchone()
        if result == None:
            return (None, None)
        return result


def get_admin_ids() -> list[int]:
    with sqlite3.connect(USERDATA_DB) as conn:
        cur = conn.cursor()
        result = cur.execute(GET_ADMIN_IDS).fetchall()
        return [i[0] for i in result]

