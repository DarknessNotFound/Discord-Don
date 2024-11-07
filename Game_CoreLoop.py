#Grant Herin
#Game application initialization and loop.
import Game_PlayerLogic
import math, random

class GameInstance:

    Players  = [Game_PlayerLogic.RoledPlayer]
    Roles = [Game_PlayerLogic.Role]
    MafiaPercent: 0.25
    FlexPercent: 0.2
    GameStarted = False

    def __init__(self, Players, RoleList):
        self.Players = Players
        self.Roles = RoleList


    def AssignRoles(self):
        if (self.Roles.len()):
            random.shuffle(self.Players) #Shuffle the players preemptively
            
            AssignedRoles = [Game_PlayerLogic.Role]
            MafiaRoles = [Game_PlayerLogic.Role]
            FlexRoles = [Game_PlayerLogic.Role]
            InnocentRoles = [Game_PlayerLogic.Role]
            
            #switch case to handle role separation because why not.
            for role in self.Roles:
                match role.RoleTeam:
                    case "Mafia":
                        MafiaRoles.append(role)

                    case "Flex":
                        FlexRoles.append(role)

                    case "Innocent":
                        InnocentRoles.append(role)
            
            md = int(max(2,math.floor(self.MafiaPercent * self.Players.len()))) #Mafia role distribution
            fd = int(math.floor(self.FlexPercent * self.Players.len())) #Flex role distribution
            
            #Tack on mafia roles first, because they're arguably most important.
            for n in range(md):
                AssignedRoles.append(random.choice(MafiaRoles))
            
            #Add our flex roles, if any.
            for n in range(fd):
                AssignedRoles.append(random.choice(FlexRoles))
            
            #Fill out the rest of the players with Innocent roles.
            for n in range(self.Players.len() - fd - md):
                AssignedRoles.append(random.choice(InnocentRoles))
            
            #Assign each player with a role, the two arrays should be of equal size outside of unplayable edge cases.
            for each in self.Players:
                each.PlayerRole = AssignedRoles[self.Players.index(each)]
                each.PlayerState = "Alive"        


    def StartGame(self):
        self.AssignRoles()
        self.GameStarted = True
        return    


    def AreKillersAlive(self):
        for Player in self.Players:
            if Player.PlayerRole.RoleTeam != 'Innocent' and Player.PlayerState != 'Dead': #stop once we've found a non-dead non-innocent.
                return
        self.EndGame()

    def AddPlayer(self,newPlayer):
        self.Players.append(Game_PlayerLogic.RoledPlayer(newPlayer))
        if(self.GameStarted):
            self.KillPlayer(self,newPlayer)

    def KillPlayer(self, killedPlayer):
        for player in self.Players:
            if player.PlayerName == killedPlayer:
                player.PlayerState = 'Dead'
                break
        self.AreKillersAlive()

    def RemovePlayer(self,RemovedPlayer):
        self.KillPlayer(RemovedPlayer)
        for player in self.Players:
            if player.PlayerName == RemovedPlayer:
                self.Players.remove(player)
                break

    def EndGame(self):
        self.GameStarted = False
        return
    
    def EchoStats(self):
        statmsg = "Game Ended!"
        for Player in self.Players:
            statmsg = statmsg + Player.PlayerName + " was a " + Player.PlayerRole.RoleName + "\n"
        return statmsg
