import sqlite3
from roles import RoleDB

FILE_PATH = "./data/role_info.db"
FILE_NAME = "database.py"
ISOLATION_LEVEL = "DEFERRED"

T_ROLE_INFO = "roleInfo"
T_ROLE_INFO_SCHEMA = f"""
    CREATE TABLE IF NOT EXISTS {T_ROLE_INFO} (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        server_id VARCHAR(255) NOT NULL DEFAULT '',
        discord_id VARCHAR (255) NOT NULL DEFAULT '',
        is_deleted BOOLEAN NOT NULL DEFAULT 0
    );
"""

def CREATE_DATABASE():
    """Creates the database that will be accessed. Program crashes if the database can't be created.
    """
    try:
        conn = sqlite3.Connection(FILE_PATH)
        conn.execute(T_ROLE_INFO_SCHEMA)
        conn.commit()
        return True
    except Exception as ex:
        # LOG
        print(f"CRITICAL ERROR -- {FILE_NAME} -- CREATE_DATABASE -- {ex}")
        return False

def IsOwner(DiscordId: str, ServerId: str) -> bool:
    return True

def IsAdmin(DiscordId: str, ServerId: str) -> bool:
    """Checks if the user has admin permissions.

    Args:
        DiscordId (str): _description_
        ServerId (str): _description_

    Returns:
        bool: _description_
    """
    return True