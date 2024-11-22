#Grant Herin
#Game application initialization and loop.
import Game_PlayerLogic
import math, random

FILE_NAME = "Game_CoreLoop"

class GameInstance:

    def __init__(self, Players: list[Game_PlayerLogic.RoledPlayer] = [], RoleList = Game_PlayerLogic.DefaultRoles):
        self.Players = Players
        self.Roles = RoleList
        self.MafiaPercent= 0.25
        self.FlexPercent = 0.2
        self.GameStarted = False


    def AssignRoles(self):
        if (len(self.Roles)):
            random.shuffle(self.Players) #Shuffle the players preemptively
            
            lok_counter = 0

            AssignedRoles = []
            MafiaRoles = []
            FlexRoles: Game_PlayerLogic.Role = []
            InnocentRoles = []
            
            #switch case to handle role separation because why not.
            for role in self.Roles:
                match role.RoleTeam:
                    case "Mafia":
                        MafiaRoles.append(role)

                    case "Flex":
                        FlexRoles.append(role)

                    case "Innocent":
                        InnocentRoles.append(role)
            
            md = int(max(1,math.floor(self.MafiaPercent * len(self.Players)))) #Mafia role distribution
            fd = int(math.floor(self.FlexPercent * len(self.Players))) #Flex role distribution
            
            #Tack on mafia roles first, because they're arguably most important.
            for n in range(md):
                mrole = random.choice(MafiaRoles)
                AssignedRoles.append(mrole)
                if mrole.RoleUnique:
                    MafiaRoles.remove(mrole)
            lok_counter += 1

            #Add our flex roles, if any.
            for n in range(fd):
                frole = random.choice(FlexRoles)
                AssignedRoles.append(frole)
                if frole.RoleUnique:
                    FlexRoles.remove(frole)
                
                if frole.RoleName == "Kannibal" or frole.RoleName == "Zombie":
                    lok_counter += 1
            
            #Fill out the rest of the players with Innocent roles.
            for n in range(len(self.Players) - fd - md):
                irole = random.choice(InnocentRoles)
                AssignedRoles.append(irole)
                if irole.RoleUnique:
                    InnocentRoles.remove(irole)
            
            #Assign each player with a role, the two arrays should be of equal size outside of unplayable edge cases.
            for each in self.Players:
                each.PlayerRole = AssignedRoles[self.Players.index(each)]
                each.PlayerState = "Alive" 
            
            return lok_counter

    def StartGame(self):
        num_lok = self.AssignRoles() # Returns number of lok (last of kind).
        self.GameStarted = True
        return num_lok

    def IsPlayerJoined(self, author) -> bool:
        """Checks if a player has already joined the 

        Args:
            author (ctx.author): The ctx.author from Discord.

        Returns:
            bool: True if the ctx.author exists in the players list.
        """
        result = False
        name = author.name
        for p in self.Players:
            if p.PlayerName == name:
                result = True
        return result

    def CheckTeamCounts(self):
        try:
            TeamCounts = {"Living": 0,
                        "Innocent": 0,
                        "Mafia": 0}
            for Player in self.Players:
                if Player.PlayerState == "Alive":
                    TeamCounts["Living"] += 1
                    if Player.PlayerRole.RoleTeam == "Flex":
                        if Player.PlayerRole.RoleName in TeamCounts:
                            TeamCounts[Player.PlayerRole.RoleName] += 1
                        else:
                            TeamCounts[Player.PlayerRole.RoleName] = 1
                    else:
                        TeamCounts[Player.PlayerRole.RoleTeam] += 1
            if TeamCounts["Living"] <=0: # In the weird event of everyone dying.
                self.EndGame("No One")
                return 1
            for team, value in TeamCounts.items():
                match team:
                    case "Living":
                        break
                    case "Innocent":
                        if value >= TeamCounts["Living"]: # If we only have innocents left...
                            self.EndGame(team)
                            return 1
                        break
                    case _:
                        if value >= (TeamCounts["Living"] / 2): #if this team has the majority of players remaining
                            self.EndGame(team)
                            return 1
                        break        
        except Exception as ex:
            print(f"ERROR -- {FILE_NAME} -- CheckTeamCounts -- {ex}")
        return 0

    def AddAuthor(self, author):
        """Adds the author of a discord command to the player list. They spawn in dead if the game is running.

        Args:
            author (ctx.author): The author who sent the message
        """
        try:
            self.Players.append(Game_PlayerLogic.RoledPlayer(author.name, author.id, author.display_name))
            if(self.GameStarted):
                self.KillPlayer(author)
        except Exception as ex:
            print(f"ERROR -- {FILE_NAME} -- AddAuthor -- {ex}")

    def KillPlayer(self, killedPlayer):
        try:
            for player in self.Players:
                if player.PlayerName == killedPlayer.name:
                    player.PlayerState = "Dead"
                    break
            self.CheckTeamCounts()
        except Exception as ex:
            print(f"ERROR -- {FILE_NAME} -- KillPlayer -- {ex}")

    def RemovePlayer(self,RemovedPlayer):
        self.KillPlayer(RemovedPlayer)
        for player in self.Players:
            if player.PlayerName == RemovedPlayer.name:
                self.Players.remove(player)
                break

    def EndGame(self, winner):
        self.GameStarted = False
        msg = self.EchoStats(winner)
        return msg
    
    def EchoStats(self, winner):
        statmsg = winner + " Wins!\n"
        for Player in self.Players:
            statmsg = statmsg + Player.DisplayName + " was a " + Player.PlayerRole.RoleName + " and is "+ Player.PlayerState + "\n"
        print(statmsg) #Development Only
        return statmsg
