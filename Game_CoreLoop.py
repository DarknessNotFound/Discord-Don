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
            KillerRoles = []
            FlexRoles: Game_PlayerLogic.Role = []
            InnocentRoles = []
            GoodInnocentRoles = []
            TownieRoles = []
            
            #switch case to handle role separation because why not.
            for role in self.Roles:
                match role.RoleTeam:
                    case "Mafia":
                        MafiaRoles.append(role)

                    case "Killer":
                        KillerRoles.append(role)

                    case "Flex":
                        FlexRoles.append(role)

                    case "GoodInnocent":
                        GoodInnocentRoles.append(role)

                    case "Innocent":
                        InnocentRoles.append(role)

                    case "Townie":
                        TownieRoles.append(role)
            
            # amounts = [Mafia, Killer, Flex, GoodInnocent, Innocent, Townie]
            num_players = len(self.Players)
            match num_players:
                case 6:
                    amounts = [2, 0, 1, 1, 1, 1]
                case 7:
                    amounts = [2, 0, 1, 2, 1, 1]
                case 8:
                    amounts = [2, 1, 1, 2, 1, 1]
                case 9:
                    amounts = [2, 1, 1, 2, 1, 2]
                case 10:
                    amounts = [2, 2, 1, 2, 1, 2]
                case 11:
                    amounts = [2, 1, 2, 2, 1, 2]
                case 12:
                    amounts = [2, 2, 2, 3, 1, 2]
                case 13:
                    amounts = [2, 2, 2, 3, 2, 2]
                case 14:
                    amounts = [2, 2, 3, 3, 2, 2]
                case _:
                    if num_players < 5:
                        amounts = [2, 0, 0, 1, 0, max(num_players - 3, 0)]
                    
                    if num_players > 14:
                        num_killers = ((num_players - 14) // 4) + 3
                        num_townie = max(((num_players - 14 - num_killers)), 0) + 2
                        amounts = [2, num_killers, 3, 3, 2, num_townie]
                    
            
            #Tack on mafia roles first, because they're arguably most important.
            for n in range(amounts[0]):
                mrole = random.choice(MafiaRoles)
                AssignedRoles.append(mrole)
                if mrole.RoleUnique:
                    MafiaRoles.remove(mrole)
            lok_counter += 1

            #Add our killer roles, if any.
            for n in range(amounts[1]):
                frole = random.choice(KillerRoles)
                AssignedRoles.append(frole)
                if frole.RoleUnique:
                    FlexRoles.remove(frole)
            lok_counter += amounts[1]

            #Add our flex roles, if any.
            for n in range(amounts[2]):
                frole = random.choice(FlexRoles)
                AssignedRoles.append(frole)
                if frole.RoleUnique:
                    FlexRoles.remove(frole)

            #Add our GoodInnocent roles, if any.
            for n in range(amounts[3]):
                frole = random.choice(GoodInnocentRoles)
                AssignedRoles.append(frole)
                if frole.RoleUnique:
                    FlexRoles.remove(frole)
            
            #Add our Innocent roles, if any.
            for n in range(amounts[4]):
                frole = random.choice(InnocentRoles)
                AssignedRoles.append(frole)
                if frole.RoleUnique:
                    FlexRoles.remove(frole)

            #Add our Basic Townie roles, if any.
            for n in range(amounts[5]):
                frole = random.choice(TownieRoles)
                AssignedRoles.append(frole)
                if frole.RoleUnique:
                    FlexRoles.remove(frole)
            
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
        statmsg = "Game Over!\n"
        for Player in self.Players:
            statmsg = statmsg + Player.DisplayName + " was a " + Player.PlayerRole.RoleName + " and is "+ Player.PlayerState + "\n"
        print(statmsg) #Development Only
        return statmsg
