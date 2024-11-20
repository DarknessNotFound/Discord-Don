# Test suite to make sure logic actually works properly.

import Game_CoreLoop
import Game_PlayerLogic
import random

GI = Game_CoreLoop.GameInstance([],Game_PlayerLogic.DefaultRoles)
endstate = False

# Add n players
living_players = []
for i in range(0,12):
    GI.AddPlayer(f"player{i}")
    living_players.append(f"player{i}")
GI.StartGame()
for i in range(0,12):
    player_to_kill = random.choice(living_players)
    print(f"{player_to_kill} Died!")
    GI.KillPlayer(player_to_kill)
    living_players.remove(player_to_kill)
    if GI.CheckTeamCounts():
        break