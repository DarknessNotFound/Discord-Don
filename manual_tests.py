import database as db
import roles as r

def DatabaseTesting():
    discord_server_id1 = "1290428323507474656"
    discord_server_id2 = "9999999999999999999"
    print(f"\n\t----- Database Testing -----")
    print("Creating Database")
    if db.CREATE_DATABASE():
        print("Database creation successful.")
    
    villager = r.RoleDB(
        id=None, 
        server_id=discord_server_id1, 
        team_name="Townie", 
        role_name="Villager", 
        role_description="Does Nothing"
        )

    mafia = r.RoleDB(
        id=None,
        server_id=discord_server_id1,
        team_name="Mafia",
        role_name="Mafia",
        role_description="Kill things to win."
    )

    scooby_doo_monster = r.RoleDB(
        id=None,
        server_id=discord_server_id2,
        team_name="Flex",
        role_name="scooby_doo_monster",
        role_description="Scare things to win."
    )
    villagerId = db.UPSERT_ROLE(villager)
    mafiaId = db.UPSERT_ROLE(mafia)
    scoobyId = db.UPSERT_ROLE(scooby_doo_monster)

    villager.id = villagerId
    mafia.id = mafiaId

    villager.role_description = "The class is trying to survive and kill all evil characters."
    villagerId_New = db.UPSERT_ROLE(villager)
    assert villagerId_New == villagerId, "UPSERT didn't update properly"

    villageSelected = db.SELECT_ROLE(villagerId)
    print(f"Selected Village: {villageSelected}")

    scoobySelected = db.SELECT_ROLE(scoobyId)
    print(f"Selected Sooby: {scoobySelected}")

    print(f"Selecting all roles with discord id of {discord_server_id1}")
    for i, role in enumerate(db.SELECT_ROLES(server_id=discord_server_id1)):
        #print(f"{i}: {role}")
        assert role.server_id == discord_server_id1, "Multi select choose a bad discord Id."

    print("\nDeleting Mafia then selecting everything")
    db.DELETE_ROLE(id=mafiaId)
    for i, role in enumerate(db.SELECT_ALL_ROLES()):
        #print(f"{i}: {role}")
        assert role.id != mafiaId, "Mafia wasn't deleted."
    
    print("Trying to select all deleted roles. Should only be mafia.")
    for i, role in enumerate(db.SELECT_ALL_ROLES_DELETED()):
        #print(f"{i}: {role}")
        assert role.is_deleted == True, "Selected something that wasn't deleted."
        assert role.id == mafiaId, "Something other than deleted got selected."

    print("\nUndo Deleting Mafia then selecting everything.")
    db.UNDO_DELETE_ROLE(id=mafiaId)
    found_mafia = False
    for i, role in enumerate(db.SELECT_ALL_ROLES()):
        #print(f"{i}: {role}")
        if role.id == mafiaId:
            found_mafia = True
    assert found_mafia, "Mafia didn't get undo-deleted."


def main():
    DatabaseTesting()
    return None
if __name__ == "__main__":
    main()