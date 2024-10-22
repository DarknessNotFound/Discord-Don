class RoleDB:
    """This holds all of the information as it is nessessary to be put into the database.
    """
    def __init__(
            self, 
            id: int = None, 
            server_id: str = "",
            team_name: str = "",
            role_name: str = None,
            role_description: str = None,
            is_killing: bool = False,
            is_flex: bool = False,
            is_deleted: bool = False,
        ) -> None:
        self.id = id
        self.server_id = server_id
        self.team_name = team_name
        self.role_name = role_name
        self.role_description = role_description
        self.is_killing = is_killing
        self.is_flex = is_flex
        self.is_deleted = is_deleted

    def __str__(self):
        return f"""RoleDB
            \tid: {self.id}
            \tserver_id: {self.server_id}
            \tteam_name: {self.team_name}
            \trole_name: {self.role_name}
            \trole_description: {self.role_description}
            \tis_killing: {self.is_killing}
            \tis_flex: {self.is_flex}
            \tis_deleted: {self.is_deleted}
        """

    def database_gatekeeping(self):
        """Does a check to make sure all the values being inserted into the database are valid.
        """
        # Null assertions
        assert self.server_id is not None, "server_id is None"
        assert self.team_name is not None, "team_name is None"
        assert self.is_killing is not None, "is_killing is None"
        assert self.is_flex is not None, "is_flex is None"
        assert self.is_deleted is not None, "is_deleted is None"

        # Type assertions
        if self.id is not None:
            assert type(self.id) is int, "id is not None nor int"

        assert type(self.server_id) is str, "server_id is not a string"
        assert type(self.team_name) is str, "team_name is not a string"
        if self.role_name is not None:
            assert type(self.role_name) is str, "role_name is not a string"

        if self.role_description is not None:
            assert type(self.role_description) is str, "role_description is not a string"

        assert type(self.is_killing) is bool, "is_killing is not a boolean"
        assert type(self.is_flex) is bool, "is_flex is not a boolean"
        assert type(self.is_deleted) is bool, "is_deleted is not a boolean"

        # Size assertions
        assert len(self.server_id) <= 255, "server_id is greater than 255"
        assert len(self.team_name) <= 255, "team_name is greater than 255"
        assert len(self.role_name) <= 1_000_000_000, "role_name is greater than 1_000_000_000" # Default Max string for SQLite3 

    def to_sqlite_tuple(self) -> tuple:
        self.database_gatekeeping()
        return (
            self.id,
            self.server_id,
            self.team_name,
            self.role_name,
            self.role_description,
            self.is_killing,
            self.is_flex,
            self.is_deleted
        )