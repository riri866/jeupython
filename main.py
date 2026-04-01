import sys
from db_init import init_db
from utils import get_db, montre_classement
from models import Character
from game import debut_combat

def prendre_les_perso_db():
    db = get_db()
    perso = list(db.perso.find())
    if not perso:
        print("Aucun personnage trouvé en base. Ajoutez des personnages dans la collection 'perso'.")
    return perso


def accueil():
    print("Bienvenue sur RPG ARENA\nCréé par Enric")
    print("\n1. Démarrer le jeu")
    print("2. Afficher le classement")
    print("3. Initialiser la base de données")
    print("4. Quitter")


def main():
    actions = {
        "1": commencer,
        "2": montre_classement,
        "3": init_database,
        "4": quitter
    }

    while True:
        accueil()
        choix = input("Votre choix : ")
        
        action = actions.get(choix)
        if action:
            action()
        else:
            print("Option invalide, veuillez choisir 1, 2 ou 3.")

def commencer():
    pseudo = input("\nEntrez votre nom d'utilisateur : ")
    equipe = choix_equipe()
    
    print(f"\nLe combat commence pour {pseudo.upper()}")
    try:
        score = debut_combat(pseudo, equipe)
    except Exception as e:
        print(f"Erreur pendant le combat : {e}")
        return

    print(f"\nPartie terminée. Score final : {score} vagues.")
    montre_classement()

def afficher_personnages(perso):
    print("\nPERSONNAGES DISPONIBLES")
    
    if not perso:
        print("Aucun personnage disponible.")
        return

    for i, stat in enumerate(perso):
        stats = f"ATK:{stat['atk']} | DEF:{stat['defense']} | PV:{stat['pv']}"
        print(f"{i+1}. {stat['nom']} ({stats})")

def choix_equipe():
    list_perso = prendre_les_perso_db()
    equipe = []

    if len(list_perso) < 3:
        print("Il faut au moins 3 personnages dans la base pour démarrer une équipe.")
        sys.exit(1)

    print("\nChoisis 3 guerriers qui t'aideront dans ta quête !")
    
    while len(equipe) < 3:
        afficher_personnages(list_perso)
        choix = choix_du_joueur(len(list_perso))
        
        if choix is not None:
            supp = list_perso.pop(choix)
            nouveau_membre = Character(
                supp['nom'], 
                supp['atk'], 
                supp['defense'], 
                supp['pv']
            )
            equipe.append(nouveau_membre)
            print(f"\n{supp['nom']} a rejoint l'équipe")
        else:
            print("Choix invalide, choisis un nombre entre 1 et", len(list_perso))

    return equipe


def choix_du_joueur(valeur_max):
    saisie = input(f"Sélection (1-{valeur_max}) : ")
    
    if saisie.isdigit():
        choix = int(saisie) - 1
        if 0 <= choix < valeur_max:
            return choix
            
    print("Entrée invalide. Merci de saisir un nombre.")
    return None


def init_database():
    print("\nInitialisation de la base de données MongoDB...")
    try:
        init_db()
        print("Base de données initialisée (perso, monstre, scores).")
    except Exception as e:
        print(f"Erreur d'initialisation : {e}")


def quitter():
    print("\nMerci d'avoir joué à RPG ARENA !")
    sys.exit()

if __name__ == "__main__":
    main()