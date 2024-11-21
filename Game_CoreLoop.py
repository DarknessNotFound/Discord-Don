#Grant Herin
#Game application initialization and loop.
import Game_PlayerLogic
import math, random

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
            
            AssignedRoles = []
            MafiaRoles = []
            FlexRoles = []
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
            
            md = int(max(2,math.floor(self.MafiaPercent * len(self.Players)))) #Mafia role distribution
            fd = int(math.floor(self.FlexPercent * len(self.Players))) #Flex role distribution
            
            #Tack on mafia roles first, because they're arguably most important.
            for n in range(md):
                mrole = random.choice(MafiaRoles)
                AssignedRoles.append(mrole)
                if mrole.RoleUnique:
                    MafiaRoles.remove(mrole)
            
            #Add our flex roles, if any.
            for n in range(fd):
                frole = random.choice(FlexRoles)
                AssignedRoles.append(frole)
                if frole.RoleUnique:
                    FlexRoles.remove(frole)
            
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


    def StartGame(self):
        self.AssignRoles()
        self.GameStarted = True
        return    


    def CheckTeamCounts(self):
        killers = 0
        nonkillers = 0
        for Player in self.Players:
            if Player.PlayerRole.Killer and Player.PlayerState == "Alive":
                killers += 1
            if Player.PlayerRole.RoleTeam == "Innocent" and Player.PlayerState == "Alive":
                nonkillers += 1
        if killers <= 0:
            self.EndGame("The Innocent")
            return 1
        if nonkillers <= 0 or killers >= nonkillers:
            self.EndGame("The Mafia")
            return 2
        return 0

    def AddPlayer(self, newPlayer):
        self.Players.append(Game_PlayerLogic.RoledPlayer(newPlayer.name))
        if(self.GameStarted):
            self.KillPlayer(self,newPlayer)

    def KillPlayer(self, killedPlayer):
        for player in self.Players:
            if player.PlayerName == killedPlayer.name:
                player.PlayerState = "Dead"
                break
        self.CheckTeamCounts()

    def RemovePlayer(self,RemovedPlayer):
        self.KillPlayer(RemovedPlayer.name)
        for player in self.Players:
            if player.PlayerName == RemovedPlayer.name:
                self.Players.remove(player)
                break

    def EndGame(self, winner):
        self.GameStarted = False
        self.EchoStats(winner)
        return
    
    def EchoStats(self, winner):
        statmsg = winner + " Wins!\n"
        for Player in self.Players:
            statmsg = statmsg + Player.PlayerName + " was a " + Player.PlayerRole.RoleName + " and is "+ Player.PlayerState + "\n"
        print(statmsg) #Development Only
        return statmsg
