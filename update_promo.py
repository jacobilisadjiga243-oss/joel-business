import sqlite3
import os

# On cherche la base de donnees
chemins = ['instance/boutique.db', 'boutique.db']
trouve = False

for chemin in chemins:
    if os.path.exists(chemin):
        conn = sqlite3.connect(chemin)
        try:
            # On essaie d'ajouter la colonne promo_texte
            conn.execute("ALTER TABLE parametre ADD COLUMN promo_texte VARCHAR(255) DEFAULT 'PROMO : Livraison offerte des 50$ d''achat !'")
            conn.commit()
            print(f"OK : Colonne promo_texte ajoutee dans {chemin}")
        except Exception as e:
            print(f"Info promo_texte : {e}")
        
        try:
            # On essaie d'ajouter la colonne promo_active
            conn.execute("ALTER TABLE parametre ADD COLUMN promo_active BOOLEAN DEFAULT 0")
            conn.commit()
            print(f"OK : Colonne promo_active ajoutee dans {chemin}")
        except Exception as e:
            print(f"Info promo_active : {e}")
        
        conn.close()
        trouve = True
        break

if not trouve:
    print("Erreur : Impossible de trouver le fichier boutique.db")
