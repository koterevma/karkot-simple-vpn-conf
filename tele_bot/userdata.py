import logging
import sqlite3

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
        "SET config_path = :config_path, "
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
            logger.exception(f"User {user.id} not added, already exists in database")


def add_admins(admin_ids: Iterable[int]) -> None:
    for admin_id in admin_ids:
        add_user(User(id=admin_id, config_path=None, is_admin=1))


def update_user(id_: int, /, *,
                is_admin: int | None = None,
                config_path: str | None = None):
    if is_admin is None and config_path is None:
        logger.error("Neither is_admin nor config_path were specified")
        return

    existing_user = get_user_data(id_)
    if existing_user is None:
        logger.error("Can't update user since it does not exist")
        return

    if is_admin is None:
        is_admin = existing_user.is_admin

    if config_path is None:
        config_path = existing_user.config_path

    updated_user = User(id_, is_admin, config_path)
    with sqlite3.connect(USERDATA_DB) as conn:
        cur = conn.cursor()
        try:
            cur.execute(UPDATE_USER, asdict(updated_user))
            conn.commit()
        except sqlite3.Error as e:
            logger.error("In update_user: " + str(e))


def get_user_data(id_: int, /) -> User | None:
    with sqlite3.connect(USERDATA_DB) as conn:
        cur = conn.cursor()
        result = cur.execute(GET_USER_DATA, {"id": id_}).fetchone()
        if result is None:
            return None
        return User(*result)


def get_admin_ids() -> list[int]:
    with sqlite3.connect(USERDATA_DB) as conn:
        cur = conn.cursor()
        result = cur.execute(GET_ADMIN_IDS).fetchall()
        return [i[0] for i in result]
