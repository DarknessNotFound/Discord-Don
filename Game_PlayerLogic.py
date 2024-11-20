# Grant Herin
# single flexible player object that can be instantialized into multiple roles.

class Role:

    RoleName = "Townie"
    RoleTeam = "Innocent"
    RoleDescription = "You're nothing special. Try to survive and vote out Mafia."
    RoleUnique = False
    Killer = False

    def __init__(self, Name, Team, Desc, Unique, Killer):
        self.RoleName = Name
        self.RoleTeam = Team   
        self.RoleDescription = Desc
        self.RoleUnique = Unique
        self.Killer = Killer

DefaultRoles = [
    Role("Mafia", "Mafia", "Kill the Innocent to Win.",False, True),
    Role("Janitor","Mafia", "Kill the Innocent to Win, you don't know who the Mafia is. You can dispose of bodies.", True, True),
    Role("TunaBomber", "Flex", "You have no team. Take down as many players as you can by detonating in a room with them.", True, False),
    Role("Cannibal", "Flex", "Kill all other players to win. You can consume one body, so that can't be detected.", False, True),
    Role("Sheriff", "Innocent", "You  have a gun, Mafia are out there. Don't hit an innocent, or you die.", True, False),
    Role("Mute","Innocent","Not much of a talker, are you? You cannot speak for this game.", True, False),
    Role("Townie","Innocent","You're nothing special. Try to survive and vote out Mafia.", False, False),
    Role("Scaredy Cat", "Innocent", "Afraid of the dark? You carry a light!", True, False),
    Role("Judge", "Innocent", "And jury, and executioner. You can overturn one town hall decision.", True, False)
]


class RoledPlayer:

    PlayerName = "Anon"
    PlayerRole = Role
    PlayerState = "Dead"
    
    def __init__(self, Name):
        self.PlayerName = Name


