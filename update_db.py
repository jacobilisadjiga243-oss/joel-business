import sqlite3
import os

# On cherche la base de donnees aux endroits possibles
chemins = ['instance/boutique.db', 'boutique.db']

for chemin in chemins:
    if os.path.exists(chemin):
        try:
            conn = sqlite3.connect(chemin)
            # On ajoute la colonne devise
            conn.execute("ALTER TABLE produit ADD COLUMN devise VARCHAR(10) DEFAULT '$'")
            conn.commit()
            conn.close()
            print(f"SUCCES : La colonne 'devise' a ete ajoutee dans {chemin}")
        except Exception as e:
            print(f"INFO : La colonne existe deja ou erreur dans {chemin} : {e}")
