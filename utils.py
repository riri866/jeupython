from pymongo import MongoClient

def get_db():
    client = MongoClient("mongodb://localhost:27017")
    return client["tp"]


def montre_classement(limit=10):
    db = get_db()
    from pymongo import DESCENDING
    meilleur_scores = list(db.scores.find().sort("vagues", DESCENDING).limit(limit))
    
    if not meilleur_scores:
        print("\nAucun score enregistré pour le moment. Jouez d'abord une partie !\n")
        return

    print(f"\nCLASSEMENT DES TOP {limit}")

    rang = 1
    for score in meilleur_scores:
        print(f"{rang}. {score['pseudo']} - {score['vagues']} vagues")
        rang += 1
    print("\n")


def save_result(pseudo, vague):
    db = get_db()
    db.scores.update_one(
        {"pseudo": pseudo},
        {"$max": {"vagues": vague}, "$setOnInsert": {"pseudo": pseudo}},
        upsert=True,
    )