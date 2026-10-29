import os
import psycopg2

# ⚠️ REMPLACE CETTE LIGNE PAR TON URL NEON COMPLETE
# (Celle qui commence par postgresql://neondb_owner:...)
DATABASE_URL = "postgresql://neondb_owner:TON_MOT_DE_PASSE@ep-divine-shadow-b935z1tq-pooler.c-7.eu-central-1.aws.neon.tech/neondb?sslmode=require"

try:
    conn = psycopg2.connect(DATABASE_URL)
    conn.autocommit = True
    cursor = conn.cursor()
    
    # Creation de la table Commande
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS commande (
            id SERIAL PRIMARY KEY,
            telephone VARCHAR(20) NOT NULL,
            reference VARCHAR(50) UNIQUE,
            statut VARCHAR(50) DEFAULT 'En preparation',
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    
    # Creation de la table CodePromo
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS code_promo (
            id SERIAL PRIMARY KEY,
            code VARCHAR(20) UNIQUE NOT NULL,
            reduction INTEGER NOT NULL,
            actif BOOLEAN DEFAULT TRUE
        );
    """)
    
    print("SUCCES : Les tables ont ete creees sur Neon !")
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"ERREUR : {e}")
