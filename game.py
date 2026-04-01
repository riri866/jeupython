import random
import time
from models import Character, Monster
from utils import get_db, sauvergarde_resulta, save_result


def calculer_degats(attaquant, defenseur):
    degat = max(0, attaquant.atk - defenseur.defense)
    defenseur.pv -= degat
    return degat

def tour_joueurs(equipe, monstre):
    for char in equipe:
        if char.is_alive() and monstre.is_alive():
            degat = calculer_degats(char, monstre)
            print(f"> {char.nom} inflige {degat} dégâts au {monstre.nom}.")
            time.sleep(0.5)

def tour_monstre(equipe, monstre):
    if monstre.is_alive():
        vivants = [c for c in equipe if c.is_alive()]
        if vivants:
            cible = random.choice(vivants)
            degat = calculer_degats(monstre, cible)
            print(f"< {monstre.nom} attaque {cible.nom} et inflige {degat} dégâts.")
            time.sleep(0.5)

def generer_monstre(db):
    monsters = list(db.monstre.find()) or list(db.monsters.find())
    if not monsters:
        raise RuntimeError("Aucun monstre trouvé en base. Ajoutez des monstres dans la collection 'monstre' ou 'monsters'.")

    m_data = random.choice(monsters)
    nom = m_data.get('nom') or m_data.get('name')
    if nom is None:
        raise RuntimeError("Monstre invalide en base : clé 'nom' ou 'name' manquante.")

    atk = m_data.get('atk')
    defense = m_data.get('defense')
    pv = m_data.get('pv')
    if atk is None or defense is None or pv is None:
        raise RuntimeError("Monstre invalide en base : 'atk', 'defense' et 'pv' doivent être présents.")

    return Monster(nom, atk, defense, pv)

def equipe_vivante(equipe):
    return any(c.is_alive() for c in equipe)


def debut_combat(pseudo, equipe):
    db = get_db()
    vague = 0
    
    while equipe_vivante(equipe):
        vague += 1
        monstre = generer_monstre(db)
        
        print(f"\nVague {vague} : Un {monstre.nom} se dresse devant vous")
        print(f"PV: {monstre.pv} | ATK: {monstre.atk} | DEF: {monstre.defense}")

        while monstre.is_alive() and equipe_vivante(equipe):
            tour_joueurs(equipe, monstre)
            tour_monstre(equipe, monstre)
        
        if not monstre.is_alive():
            print(f"Victoire {vague} ")
        else:
            print(f"Défaite... : {vague - 1}.")

    score_final = vague if equipe_vivante(equipe) else vague - 1
    sauvergarde_resulta(pseudo, score_final)
    return score_final