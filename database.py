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
        team_name VARCHAR(255) NOT NULL DEFAULT '',
        role_name VARCHAR(255),
        role_description TEXT,
        is_killing BOOLEAN NOT NULL DEFAULT 0,
        is_flex BOOLEAN NOT NULL DEFAULT 0,
        is_deleted BOOLEAN NOT NULL DEFAULT 0
    );
"""

def HELLO():
    print("Hello!")

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

def UPSERT_ROLE(r: RoleDB) -> int | None:
    try:
        conn = sqlite3.Connection(FILE_PATH, isolation_level=ISOLATION_LEVEL)
        sql = f"""
            INSERT INTO {T_ROLE_INFO}
                (id, server_id, team_name, role_name, role_description, is_killing, is_flex, is_deleted)
                VALUES(?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET 
                server_id = excluded.server_id,
                team_name = excluded.team_name,
                role_name = excluded.role_name,
                role_description = excluded.role_description,
                is_killing = excluded.is_killing,
                is_flex = excluded.is_flex,
                is_deleted = excluded.is_deleted
            RETURNING id;
        """
        cur = conn.execute(sql, r.to_sqlite_tuple())
        resultId = cur.fetchone()[0]
        conn.commit()
        return resultId
    except sqlite3.Error as er:
        print(f"ERROR -- {FILE_NAME} -- UPSERT_ROLE -- SQLITE3 Error")
        print(f"Error Code: {er.sqlite_errorcode}")
        print(f"Error Name: {er.sqlite_errorname}")
    except TypeError as ex:
        print(f"TYPE ERROR -- {FILE_NAME} -- UPSERT_ROLE -- {ex}")
    except Exception as ex:
        # LOG
        print(f"ERROR -- {FILE_NAME} -- UPSERT_ROLE -- {ex}")


def SELECT_ROLE(id: int, server_id: str) -> RoleDB | None:
    try:
        conn = sqlite3.Connection(FILE_PATH, isolation_level=ISOLATION_LEVEL)
        sql = f"""
            SELECT id, server_id, team_name, role_name, role_description, is_killing, is_flex, is_deleted
            FROM {T_ROLE_INFO}
            WHERE id=? and server_id=?;
        """
        cur = conn.execute(sql, (id, server_id))
        result = cur.fetchone()
        return RoleDB(*result)
    except sqlite3.Error as er:
        print(f"ERROR -- {FILE_NAME} -- SELECT_ROLE -- SQLITE3 Error")
        print(f"Error Code: {er.sqlite_errorcode}")
        print(f"Error Name: {er.sqlite_errorname}")
    except Exception as ex:
        # LOG
        print(f"ERROR -- {FILE_NAME} -- SELECT_ROLE -- {ex}")

def SELECT_ROLES(server_id: int = None) -> list[RoleDB]:
    try:
        conn = sqlite3.Connection(FILE_PATH, isolation_level=ISOLATION_LEVEL)
        if server_id is not None:
            sql = f"""
                SELECT id, server_id, team_name, role_name, role_description, is_killing, is_flex
                FROM {T_ROLE_INFO}
                WHERE server_id=? and is_deleted=0;
            """
            params = (server_id,)
        else:
            raise NotImplementedError("Select many roles not implemented.")

        cur = conn.execute(sql, params)
        result = cur.fetchall()
        return [RoleDB(*r) for r in result]
    except sqlite3.Error as er:
        print(f"ERROR -- {FILE_NAME} -- SELECT_ROLES -- SQLITE3 Error")
        print(f"Error Code: {er.sqlite_errorcode}")
        print(f"Error Name: {er.sqlite_errorname}")
    except Exception as ex:
        # LOG
        print(f"ERROR -- {FILE_NAME} -- SELECT_ROLES -- {ex}")

def SELECT_ALL_ROLES() -> list[RoleDB]:
    try:
        conn = sqlite3.Connection(FILE_PATH, isolation_level=ISOLATION_LEVEL)
        sql = f"""
            SELECT id, server_id, team_name, role_name, role_description, is_killing, is_flex, is_deleted
            FROM {T_ROLE_INFO}
            WHERE is_deleted=0;
        """

        cur = conn.execute(sql)
        result = cur.fetchall()
        return [RoleDB(*r) for r in result]
    except sqlite3.Error as er:
        print(f"ERROR -- {FILE_NAME} -- SELECT_ROLES -- SQLITE3 Error")
        print(f"Error Code: {er.sqlite_errorcode}")
        print(f"Error Name: {er.sqlite_errorname}")
    except Exception as ex:
        # LOG
        print(f"ERROR -- {FILE_NAME} -- SELECT_ROLES -- {ex}")

def SELECT_ALL_ROLES_DELETED() -> list[RoleDB]:
    try:
        conn = sqlite3.Connection(FILE_PATH, isolation_level=ISOLATION_LEVEL)
        sql = f"""
            SELECT id, server_id, team_name, role_name, role_description, is_killing, is_flex, is_deleted
            FROM {T_ROLE_INFO}
            WHERE is_deleted=1;
        """

        cur = conn.execute(sql)
        result = cur.fetchall()
        return [RoleDB(*r) for r in result]
    except sqlite3.Error as er:
        print(f"ERROR -- {FILE_NAME} -- SELECT_ROLES -- SQLITE3 Error")
        print(f"Error Code: {er.sqlite_errorcode}")
        print(f"Error Name: {er.sqlite_errorname}")
    except Exception as ex:
        # LOG
        print(f"ERROR -- {FILE_NAME} -- SELECT_ROLES -- {ex}")

def DELETE_ROLE(id: int = None, server_id: str = None) -> list[RoleDB]:
    try:
        conn = sqlite3.Connection(FILE_PATH, isolation_level=ISOLATION_LEVEL)
        sql = f"UPDATE {T_ROLE_INFO} SET is_deleted=1 WHERE Id=? AND server_id=?;"
        params = (id,server_id)

        conn.execute(sql, params)
        conn.commit()
        return True
    except sqlite3.Error as er:
        print(f"ERROR -- {FILE_NAME} -- DELETE_ROLE -- SQLITE3 Error")
        print(f"Error Code: {er.sqlite_errorcode}")
        print(f"Error Name: {er.sqlite_errorname}")
    except Exception as ex:
        # LOG
        print(f"ERROR -- {FILE_NAME} -- SELECT_ROLE -- {ex}")
        return False
    
def UNDO_DELETE_ROLE(id: int = None) -> list[RoleDB]:
    try:
        conn = sqlite3.Connection(FILE_PATH, isolation_level=ISOLATION_LEVEL)
        sql = f"UPDATE {T_ROLE_INFO} SET is_deleted=0 WHERE Id=?;"
        params = (id,)

        conn.execute(sql, params)
        conn.commit()
        return True
    except sqlite3.Error as er:
        print(f"ERROR -- {FILE_NAME} -- DELETE_ROLE -- SQLITE3 Error")
        print(f"Error Code: {er.sqlite_errorcode}")
        print(f"Error Name: {er.sqlite_errorname}")
    except Exception as ex:
        # LOG
        print(f"ERROR -- {FILE_NAME} -- SELECT_ROLE -- {ex}")
        return False