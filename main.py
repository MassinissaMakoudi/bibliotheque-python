import json
import os

FICHIER_JSON = "bibliotheque.json"

# Charger la bibliothèque depuis le fichier JSON
def charger_bibliotheque():
    if os.path.exists(FICHIER_JSON):
        with open(FICHIER_JSON, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

# Sauvegarder la bibliothèque dans le fichier JSON
def sauvegarder_bibliotheque(bibliotheque):
    with open(FICHIER_JSON, "w", encoding="utf-8") as f:
        json.dump(bibliotheque, f, indent=4, ensure_ascii=False)

# Générer un nouvel ID unique
def generer_id(bibliotheque):
    return max((livre["ID"] for livre in bibliotheque), default=0) + 1

# Ajouter un livre
def ajouter_livre(bibliotheque):
    titre = input("Titre du livre: ")
    auteur = input("Auteur: ")
    annee = input("Année de publication: ")
    try:
        annee = int(annee)
    except ValueError:
        print("Année invalide.")
        return
    livre = {
        "ID": generer_id(bibliotheque),
        "Titre": titre,
        "Auteur": auteur,
        "Année": annee,
        "Lu": False,
        "Note": None,
        "Commentaire": ""
    }
    bibliotheque.append(livre)
    print("Livre ajouté avec succès.")

# Afficher tous les livres
def afficher_livres(bibliotheque):
    if not bibliotheque:
        print("Aucun livre dans la bibliothèque.")
    for livre in bibliotheque:
        statut = "✔" if livre["Lu"] else "✘"
        print(f"[{livre['ID']}] {livre['Titre']} - {livre['Auteur']} ({livre['Année']}) | Lu: {statut} | Note: {livre['Note'] or 'N/A'}")

# Supprimer un livre
def supprimer_livre(bibliotheque):
    try:
        id_livre = int(input("ID du livre à supprimer: "))
        for livre in bibliotheque:
            if livre["ID"] == id_livre:
                confirm = input(f"Supprimer '{livre['Titre']}' ? (o/n): ")
                if confirm.lower() == "o":
                    bibliotheque.remove(livre)
                    print("Livre supprimé.")
                return
        print("Livre non trouvé.")
    except ValueError:
        print("ID invalide.")

# Rechercher un livre
def rechercher_livre(bibliotheque):
    mot_cle = input("Mot-clé à rechercher: ").lower()
    resultats = [l for l in bibliotheque if mot_cle in l['Titre'].lower() or mot_cle in l['Auteur'].lower()]
    if not resultats:
        print("Aucun résultat.")
    for livre in resultats:
        print(f"[{livre['ID']}] {livre['Titre']} - {livre['Auteur']} ({livre['Année']})")

# Marquer un livre comme lu
def marquer_lu(bibliotheque):
    try:
        id_livre = int(input("ID du livre lu: "))
        for livre in bibliotheque:
            if livre["ID"] == id_livre:
                livre["Lu"] = True
                note = input("Note sur 10: ")
                try:
                    livre["Note"] = float(note)
                except ValueError:
                    livre["Note"] = None
                livre["Commentaire"] = input("Commentaire: ")
                print("Livre mis à jour.")
                return
        print("Livre non trouvé.")
    except ValueError:
        print("ID invalide.")

# Filtrer les livres lus ou non lus
def filtrer_livres(bibliotheque):
    choix = input("Afficher (l)us ou (n)on lus ? ").lower()
    if choix == "l":
        filtres = [l for l in bibliotheque if l["Lu"]]
    elif choix == "n":
        filtres = [l for l in bibliotheque if not l["Lu"]]
    else:
        print("Choix invalide.")
        return
    afficher_livres(filtres)

# Trier les livres
def trier_livres(bibliotheque):
    print("Trier par: 1) Année 2) Auteur 3) Note")
    choix = input("Votre choix: ")
    if choix == "1":
        livres_tries = sorted(bibliotheque, key=lambda l: l["Année"])
    elif choix == "2":
        livres_tries = sorted(bibliotheque, key=lambda l: l["Auteur"].lower())
    elif choix == "3":
        livres_tries = sorted(bibliotheque, key=lambda l: l["Note"] if l["Note"] is not None else -1, reverse=True)
    else:
        print("Choix invalide.")
        return
    afficher_livres(livres_tries)

# Menu principal
def menu():
    bibliotheque = charger_bibliotheque()
    while True:
        print("\n--- MENU ---")
        print("1. Afficher tous les livres")
        print("2. Ajouter un livre")
        print("3. Supprimer un livre")
        print("4. Rechercher un livre")
        print("5. Marquer un livre comme lu")
        print("6. Afficher les livres lus / non lus")
        print("7. Trier les livres")
        print("8. Quitter")
        choix = input("Votre choix: ")

        if choix == "1":
            afficher_livres(bibliotheque)
        elif choix == "2":
            ajouter_livre(bibliotheque)
        elif choix == "3":
            supprimer_livre(bibliotheque)
        elif choix == "4":
            rechercher_livre(bibliotheque)
        elif choix == "5":
            marquer_lu(bibliotheque)
        elif choix == "6":
            filtrer_livres(bibliotheque)
        elif choix == "7":
            trier_livres(bibliotheque)
        elif choix == "8":
            sauvegarder_bibliotheque(bibliotheque)
            print("Au revoir !")
            break
        else:
            print("Choix invalide. Réessayez.")

if __name__ == "__main__":
    menu()
