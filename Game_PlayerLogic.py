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
    
    def msg(self):
        return f"Role: {self.RoleName}\nTeam: {self.RoleTeam}\n{self.RoleDescription}"

DefaultRoles = [
    Role("Mafia", "Mafia", "Kill the Innocent to Win.",False, True),
    Role("Mafia", "Mafia", "Kill the Innocent to Win.",False, True),
    Role("Janitor","Flex", "Kill the Innocent to Win, you don't know who the Mafia is. You can dispose of a single body, refreshes on at a town meeting.", True, True),
    Role("Zombie", "Flex", "Kill all other players to win. When you kill someone as zombie, you die and they become a zombie.", False, True),
    Role("Kannibal", "Flex", "Kill all other players to win. You can consume one body, so that can't be detected.", False, True),
    Role("Kannibal", "Flex", "Kill all other players to win. You can consume one body, so that can't be detected.", False, True),
    Role("TunaBomber", "Flex", "You have no team. Take down as many players as you can by detonating in a room with them.", False, False),
    Role("Jester", "Flex", "You have no team. You win if and only if you get voted out at a town meeting.", False, False),
    Role("Scooby-Doo Villian", "Flex", "You have no team. Your goal is to scare the other players out of the game.", False, False),
    Role("Sheriff", "Innocent", "You  have a gun, Mafia are out there. Don't hit an innocent, or you die.", True, False),
    Role("Mute","Innocent","Not much of a talker, are you? You cannot speak for this game.", True, False),
    Role("Townie","Innocent","You're nothing special. Try to survive and vote out Mafia.", False, False),
    Role("Scaredy Cat", "Innocent", "Afraid of the dark? You carry a light!", True, False),
    Role("Locksmith", "Innocent", "You are with the town. You can open/close one door per town hall meeting", True, False),
    Role("Judge", "Innocent", "And jury, and executioner. You can overturn one town hall decision.", False, False)
]


class RoledPlayer:

    PlayerName = "Anon"
    DiscordId = 1
    PlayerRole = Role
    PlayerState = "Dead"
    
    def __init__(self, Name: str, DiscordId: str, DisplayName: str = ""):
        self.PlayerName = Name
        self.DiscordId = DiscordId
        self.DisplayName = DisplayName


