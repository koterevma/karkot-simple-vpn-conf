import sqlite3
import logging

from classes import User
from dataclasses import asdict
from pathlib import Path
from typing import Iterable


logger = logging.getLogger(__name__)


USERDATA_DB = Path("./data/userdata.db")

CREATE_TABLE = (
        "CREATE TABLE IF NOT EXISTS user("
        "id INTEGER UNIQUE PRIMARY KEY NOT NULL, "
        "config_path TEXT, "
        "is_admin INTEGER"
        ");"
)

ADD_USER = (
        "INSERT INTO user (id, config_path, is_admin) "
        "VALUES(:id, :config_path, :is_admin);"
)

GET_USER_DATA = (
        "SELECT config_path, is_admin "
        "FROM user "
        "WHERE id = :id;"
)

UPDATE_USER = (
        "UPDATE user "
        "SET config_path = :config_path "
        "is_admin = :is_admin "
        "WHERE id = :id;"
)

GET_ADMIN_IDS = (
        "SELECT id "
        "FROM user "
        "WHERE is_admin = 1;"
)


with sqlite3.connect(USERDATA_DB) as conn:
    conn.execute(CREATE_TABLE)
    conn.commit()


def add_user(user: User) -> None:
    with sqlite3.connect(USERDATA_DB) as conn:
        cur = conn.cursor()
        try:
            cur.execute(ADD_USER, asdict(user))
            conn.commit()
        except sqlite3.IntegrityError:
            logger.warn(f"User {user.id} not added, already exists in database")
    

def add_admins(admin_ids: Iterable) -> None:
    for admin_id in admin_ids:
        add_user(User(id=admin_id, config_path=None, is_admin=1))


def update_user(user: User):
    with sqlite3.connect(USERDATA_DB) as conn:
        cur = conn.cursor()
        try:
            cur.execute(UPDATE_USER, asdict(user))
            conn.commit()
        except sqlite3.Error as e:
            logger.error("In update_user: " + str(e))


def get_user_data(id_: int) -> User:
    with sqlite3.connect(USERDATA_DB) as conn:
        cur = conn.cursor()
        result = cur.execute(GET_USER_DATA, {"id": id_}).fetchone()
        if result is None:
            return User()
        return User(*result)


def get_admin_ids() -> list[int]:
    with sqlite3.connect(USERDATA_DB) as conn:
        cur = conn.cursor()
        result = cur.execute(GET_ADMIN_IDS).fetchall()
        return [i[0] for i in result]

