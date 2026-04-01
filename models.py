class Entity:
    def __init__(self, nom, atk, defense, pv):
        self.nom = nom
        self.atk = atk
        self.defense = defense
        self.pv = pv
        self.max_pv = pv

    def is_alive(self):
        return self.pv > 0

class Character(Entity):
    def __init__(self, nom, atk, defense, pv, _id=None):
        super().__init__(nom, atk, defense, pv)
        self.id = _id

class Monster(Entity):
    def __init__(self, nom, atk, defense, pv):
        super().__init__(nom, atk, defense, pv)