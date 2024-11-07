import json
import random

with open('types.json') as f:
    types = json.load(f)

with open('pokemons.json') as f:
    pokemons_data = json.load(f)

class Pokemon:
    def __init__(self, data):
        self.nom = data["nom"]
        self.type = data["type"]
        self.pv = data["pv"]
        self.attaques = data["attaques"]
        self.pv_max = data["pv"]
    
    def attaquer(self, attaque, cible):
        degats = attaque.get("degats", 0)
        soin = attaque.get("soin", 0)
        
        if soin:
            self.pv = min(self.pv + soin, self.pv_max)
            print(f"{self.nom} utilise {attaque['nom']} et récupère {soin} PV.")
            print(f"Attaque : {attaque['nom']} | Soin : {soin} | PV actuels : {self.pv}/{self.pv_max}")
        else:
            multiplicateur = 1.0
            if cible.type in types[self.type]["faible"]:
                multiplicateur = 0.5
            elif cible.type in types[self.type]["resistant"]:
                multiplicateur = 2.0
            degats_totaux = int(degats * multiplicateur)
            cible.pv = max(cible.pv - degats_totaux, 0)
            print(f"{self.nom} utilise {attaque['nom']} et inflige {degats_totaux} points de dégâts à {cible.nom}!")
            print(f"Attaque : {attaque['nom']} | Dégâts : {degats} | Multiplicateur de type : {multiplicateur} | PV restants de {cible.nom} : {cible.pv}/{cible.pv_max}")

class Combat:
    def __init__(self, pokemon_joueur, pokemon_adversaire):
        self.pokemon_joueur = pokemon_joueur
        self.pokemon_adversaire = pokemon_adversaire
        self.tour = 1

    def choisir_attaque_joueur(self):
        print(f"\n{self.pokemon_joueur.nom} - PV: {self.pokemon_joueur.pv}/{self.pokemon_joueur.pv_max} - PA disponible: {self.tour}")
        
        for i, attaque in enumerate(self.pokemon_joueur.attaques):
            print(f"{i + 1}: {attaque['nom']} (Dégâts: {attaque.get('degats', 0)}, Soin: {attaque.get('soin', 0)}, PA: {attaque['pa']})")

        choix = int(input("Choisissez une attaque : ")) - 1
        attaque = self.pokemon_joueur.attaques[choix]
        
        if attaque["pa"] <= self.tour:
            return attaque
        else:
            print("Pas assez de PA ! Choisissez une autre attaque.")
            return self.choisir_attaque_joueur()

    def choisir_attaque_adversaire(self):
        attaques_disponibles = [attaque for attaque in self.pokemon_adversaire.attaques if attaque["pa"] <= self.tour]
        attaque = random.choice(attaques_disponibles)
        print(f"{self.pokemon_adversaire.nom} utilise {attaque['nom']} (PA: {attaque['pa']})")
        return attaque

    def tour_de_combat(self):
        print(f"\n===== Début du Tour {self.tour} =====")
        
        attaque_joueur = self.choisir_attaque_joueur()
        self.pokemon_joueur.attaquer(attaque_joueur, self.pokemon_adversaire)
        
        if self.pokemon_adversaire.pv > 0:
            attaque_adversaire = self.choisir_attaque_adversaire()
            self.pokemon_adversaire.attaquer(attaque_adversaire, self.pokemon_joueur)

        print(f"Fin du Tour {self.tour} - PV restants: {self.pokemon_joueur.nom}: {self.pokemon_joueur.pv}/{self.pokemon_joueur.pv_max}, {self.pokemon_adversaire.nom}: {self.pokemon_adversaire.pv}/{self.pokemon_adversaire.pv_max}")
        self.tour += 1

    def jouer(self):
        while self.pokemon_joueur.pv > 0 and self.pokemon_adversaire.pv > 0:
            self.tour_de_combat()
        
        if self.pokemon_joueur.pv > 0:
            print(f"{self.pokemon_joueur.nom} a gagné le combat !")
            return "joueur"
        else:
            print(f"{self.pokemon_adversaire.nom} a gagné le combat !")
            return "adversaire"

def choisir_pokemon(pokemon_data, deja_pris=[]):
    print("\nChoisissez votre Pokémon :")
    disponibles = [p for p in pokemon_data if p["nom"] not in deja_pris]
    
    for i, p in enumerate(disponibles):
        print(f"{i + 1}: {p['nom']} (Type: {p['type']})")

    choix = int(input("Entrez le numéro de votre Pokémon : ")) - 1
    return Pokemon(disponibles[choix])

def selectionner_adversaire(pokemon_data, deja_pris=[]):
    disponibles = [p for p in pokemon_data if p["nom"] not in deja_pris]
    choix = random.choice(disponibles)
    print(f"L'adversaire a choisi {choix['nom']} (Type: {choix['type']})")
    return Pokemon(choix)

def lancer_tournoi(pokemon_data):
    deja_pris = []
    score_joueur = 0
    score_adversaire = 0
    
    joueur = choisir_pokemon(pokemon_data, deja_pris)
    deja_pris.append(joueur.nom)
    
    while len(deja_pris) < len(pokemon_data):
        adversaire = selectionner_adversaire(pokemon_data, deja_pris)
        deja_pris.append(adversaire.nom)
        
        combat = Combat(joueur, adversaire)
        gagnant = combat.jouer()
        
        if gagnant == "joueur":
            score_joueur += 50
            print(f"Vous avez gagné ! Score actuel : Vous - {score_joueur}, Adversaire - {score_adversaire}")
        else:
            score_adversaire += 50
            print(f"Vous avez perdu ! Score actuel : Vous - {score_joueur}, Adversaire - {score_adversaire}")
            joueur = choisir_pokemon(pokemon_data, deja_pris)
            deja_pris.append(joueur.nom)
    
    print(f"\nTournoi terminé ! Score final : Vous - {score_joueur}, Adversaire - {score_adversaire}")

lancer_tournoi(pokemons_data)
