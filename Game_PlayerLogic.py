# Grant Herin
# single flexible player object that can be instantialized into multiple roles.

class Role:

    RoleName = "DefaultRole"
    RoleTeam = "Innocent"
    RoleDescription = "You shouldn't even be able to see this, this is default flavortext."

    def __init__(self, Name, Team, Desc):
        self.RoleName = Name
        self.RoleTeam = Team   
        self.RoleDescription = Desc

class RoledPlayer:

    PlayerName = "Anon"
    PlayerRole = Role
    PlayerState = "Dead"
    
    def __init__(self, Name):
        self.PlayerName = Name


