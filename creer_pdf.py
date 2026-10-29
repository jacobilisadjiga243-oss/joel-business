from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        self.set_font('helvetica', 'B', 18)
        self.set_text_color(233, 30, 99) # Rose Joel Business
        self.cell(0, 10, 'Guide de Gestion - Joel Business', align='C')
        self.ln(20)

    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 8)
        self.set_text_color(128)
        self.cell(0, 10, f'Page {self.page_no()}', align='C')

    def chapter_title(self, title):
        self.set_font('helvetica', 'B', 14)
        self.set_text_color(25, 118, 210) # Bleu
        self.cell(0, 10, title)
        self.ln(8)

    def chapter_body(self, text):
        self.set_font('helvetica', '', 11)
        self.set_text_color(50)
        self.multi_cell(0, 6, text)
        self.ln(5)

pdf = PDF()
pdf.add_page()

# Introduction
pdf.set_font('helvetica', 'B', 12)
pdf.set_text_color(0)
pdf.cell(0, 10, '1. Votre Lien Boutique (a partager partout)')
pdf.ln(6)
pdf.set_font('helvetica', '', 11)
pdf.set_text_color(0, 102, 204)
pdf.cell(0, 8, 'https://joel-business.onrender.com')
pdf.ln(15)

# Admin
pdf.chapter_title('2. Votre Espace Admin (pour gerer le site)')
pdf.chapter_body(
    "Lien : https://joel-business.onrender.com/admin\n"
    "Mot de passe : joel2026\n\n"
    "Cet espace vous permet d'ajouter vos produits, de changer les prix, "
    "de gerer les promotions et de moderer les avis des clients."
)

# Ajouter un produit
pdf.chapter_title('3. Comment ajouter un produit ?')
pdf.chapter_body(
    "1. Allez dans votre Espace Admin.\n"
    "2. Remplissez le formulaire : Nom, Prix, Devise (FC ou $), Categorie.\n"
    "3. Choisissez une photo depuis votre telephone/ordinateur.\n"
    "4. Cliquez sur 'Ajouter au catalogue'. Le produit est en ligne !"
)

# Promo
pdf.chapter_title('4. Gerer le Bandeau Promo')
pdf.chapter_body(
    "Dans l'Admin, descendez jusqu'au bloc bleu 'Modifier les infos'.\n"
    "Cochez la case 'Afficher le bandeau promo'.\n"
    "Ecrivez votre texte (ex: 'Livraison gratuite ce week-end !').\n"
    "Cliquez sur 'Enregistrer'."
)

# Avis
pdf.chapter_title('5. Gerer les Avis Clients')
pdf.chapter_body(
    "Quand un client laisse un avis sur le site, il apparait dans l'Admin "
    "dans un bloc orange.\n"
    "Cliquez sur 'Approuver' pour le publier sur le site, ou 'Supprimer' "
    "s'il y a un probleme."
)

# Info livraison
pdf.chapter_title('6. Modifier les infos de Livraison')
pdf.chapter_body(
    "Dans l'Admin, vous pouvez changer la ville, le quartier, les frais de "
    "livraison et les horaires. Ces infos s'afficheront automatiquement sur "
    "la page Contact du site."
)

# Note importante
pdf.ln(10)
pdf.set_font('helvetica', 'B', 11)
pdf.set_text_color(211, 47, 47) # Rouge
pdf.multi_cell(0, 6, "IMPORTANT : Pour ajouter des photos de qualite, hebergez-les sur le site 'imgbb.com' et collez le lien dans le champ 'Lien internet'.")

pdf.output('guide_joel.pdf')
print("Succes : Le fichier guide_joel.pdf a ete cree dans ton dossier !")
