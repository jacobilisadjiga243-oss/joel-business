from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from config import Config
from functools import wraps
import os
from werkzeug.utils import secure_filename
import time
from PIL import Image
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

WHATSAPP_NUMBER = "243992519112"
ADMIN_PASSWORD = "joel2026"
EMAIL_EXPEDITEUR = "ton.email@gmail.com" # ⚠️ À MODIFIER
EMAIL_MOT_DE_PASSE = "ton_mot_de_passe_application" # ⚠️ À MODIFIER

class Produit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    prix = db.Column(db.Integer, nullable=False)
    devise = db.Column(db.String(10), nullable=False, default="$")
    categorie = db.Column(db.String(50), nullable=False)
    image = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)

class Parametre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ville = db.Column(db.String(100), default="Gbadolite / Mobayi-Mbongo")
    quartier = db.Column(db.String(100), default="A preciser")
    frais = db.Column(db.String(100), default="A confirmer selon la zone")
    delai = db.Column(db.String(100), default="24 a 48h")
    heure_debut = db.Column(db.String(10), default="08:00")
    heure_fin = db.Column(db.String(10), default="20:00")
    promo_texte = db.Column(db.String(255), default="PROMO : Livraison offerte des 50$ d'achat !")
    promo_active = db.Column(db.Boolean, default=False)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reference = db.Column(db.String(100), unique=True)
    montant = db.Column(db.String(50))
    devise = db.Column(db.String(10))
    telephone = db.Column(db.String(20))
    statut = db.Column(db.String(20), default="En attente")
    date = db.Column(db.DateTime, default=db.func.now())

class Avis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    note = db.Column(db.Integer, nullable=False, default=5)
    commentaire = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=db.func.now())
    approuve = db.Column(db.Boolean, default=False)

# NOUVEAU : Table pour suivre les commandes
class Commande(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    telephone = db.Column(db.String(20), nullable=False)
    reference = db.Column(db.String(50), unique=True)
    statut = db.Column(db.String(50), default="En preparation")
    date = db.Column(db.DateTime, default=db.func.now())

# NOUVEAU : Table pour les codes promo
class CodePromo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), unique=True, nullable=False)
    reduction = db.Column(db.Integer, nullable=False) # Pourcentage
    actif = db.Column(db.Boolean, default=True)

def image_url(image):
    if not image: return ""
    if image.startswith("http"): return image
    return "/static/images/" + image

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("admin"):
            return redirect(url_for("admin_login"))
        return f(*args, **kwargs)
    return decorated_function

# --- ROUTES PUBLIQUES ---
@app.route("/")
def index():
    tous_produits = Produit.query.order_by(Produit.id.desc()).all()
    top_ventes = tous_produits[:4]
    nouveautes = tous_produits[4:8]
    avis_clients = Avis.query.filter_by(approuve=True).order_by(Avis.date.desc()).limit(3).all()
    info = Parametre.query.first()
    if not info: info = Parametre()
    return render_template("index.html", top_ventes=top_ventes, nouveautes=nouveautes, avis_clients=avis_clients, image_url=image_url, info=info)

@app.route("/apropos")
def apropos():
    return render_template("apropos.html")

@app.route("/ajouter-avis", methods=["POST"])
def ajouter_avis():
    nom = request.form.get("nom")
    note = int(request.form.get("note", 5))
    commentaire = request.form.get("commentaire")
    if nom and commentaire:
        nouvel_avis = Avis(nom=nom, note=note, commentaire=commentaire, approuve=False)
        db.session.add(nouvel_avis)
        db.session.commit()
        flash("Merci ! Votre avis a bien ete envoye et sera publie apres validation.", "success")
    else:
        flash("Erreur : Veuillez remplir tous les champs.", "error")
    return redirect(url_for("index") + "#avis")

@app.route("/produits")
def produits_page():
    categorie = request.args.get("categorie", "tous")
    recherche = request.args.get("q", "")
    if recherche:
        liste = Produit.query.filter(Produit.nom.ilike(f'%{recherche}%')).all()
    elif categorie == "tous":
        liste = Produit.query.all()
    else:
        liste = Produit.query.filter_by(categorie=categorie).all()
    return render_template("produits.html", produits=liste, categorie=categorie, recherche=recherche, image_url=image_url)

@app.route("/produit/<int:id>")
def produit_detail(id):
    produit = Produit.query.get_or_404(id)
    return render_template("produit.html", produit=produit, image_url=image_url)

@app.route("/panier")
def panier():
    return render_template("panier.html", whatsapp_number=WHATSAPP_NUMBER)

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        nom = request.form.get("nom")
        email = request.form.get("email")
        message = request.form.get("message")
        try:
            msg = MIMEText(f"Nom: {nom}\nEmail: {email}\n\nMessage:\n{message}")
            msg['Subject'] = f"Nouveau message de {nom} - Joel Business"
            msg['From'] = EMAIL_EXPEDITEUR
            msg['To'] = EMAIL_EXPEDITEUR
            
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(EMAIL_EXPEDITEUR, EMAIL_MOT_DE_PASSE)
            server.send_message(msg)
            server.quit()
            flash("Message envoye avec succes !", "success")
        except Exception as e:
            flash("Erreur lors de l'envoi de l'email.", "error")
            print(e)
        return redirect(url_for("contact"))
    
    info = Parametre.query.first()
    if not info: info = Parametre()
    return render_template("contact.html", whatsapp_number=WHATSAPP_NUMBER, info=info)

@app.route("/suivi", methods=["GET", "POST"])
def suivi():
    commande = None
    if request.method == "POST":
        telephone = request.form.get("telephone")
        reference = request.form.get("reference")
        commande = Commande.query.filter_by(telephone=telephone, reference=reference).first()
        if not commande:
            flash("Aucune commande trouvee avec ces informations.", "error")
    return render_template("suivi.html", commande=commande)

# --- ROUTES ADMIN ---
@app.route("/admin", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        password = request.form.get("password")
        if password == ADMIN_PASSWORD:
            session["admin"] = True
            return redirect(url_for("admin_dashboard"))
        else:
            flash("Mot de passe incorrect", "error")
    return render_template("admin_login.html")

@app.route("/admin/logout")
def admin_logout():
    session.pop("admin", None)
    return redirect(url_for("index"))

@app.route("/admin/dashboard")
@login_required
def admin_dashboard():
    produits = Produit.query.all()
    info = Parametre.query.first()
    if not info:
        info = Parametre()
        db.session.add(info)
        db.session.commit()
    avis_en_attente = Avis.query.filter_by(approuve=False).order_by(Avis.date.desc()).all()
    avis_approuves = Avis.query.filter_by(approuve=True).order_by(Avis.date.desc()).all()
    commandes = Commande.query.order_by(Commande.date.desc()).all()
    codes_promo = CodePromo.query.all()
    return render_template("admin_dashboard.html", produits=produits, image_url=image_url, edit=None, info=info, avis_en_attente=avis_en_attente, avis_approuves=avis_approuves, commandes=commandes, codes_promo=codes_promo)

@app.route("/admin/ajouter-commande", methods=["POST"])
@login_required
def admin_ajouter_commande():
    telephone = request.form.get("telephone")
    reference = request.form.get("reference")
    if telephone and reference:
        nouvelle_commande = Commande(telephone=telephone, reference=reference)
        db.session.add(nouvelle_commande)
        db.session.commit()
        flash("Commande ajoutee pour suivi !", "success")
    return redirect(url_for("admin_dashboard"))

@app.route("/admin/commande-statut/<int:id>/<statut>")
@login_required
def admin_commande_statut(id, statut):
    commande = Commande.query.get_or_404(id)
    commande.statut = statut
    db.session.commit()
    flash("Statut mis a jour !", "success")
    return redirect(url_for("admin_dashboard"))

@app.route("/admin/ajouter-promo", methods=["POST"])
@login_required
def admin_ajouter_promo():
    code = request.form.get("code").upper()
    reduction = request.form.get("reduction")
    if code and reduction:
        nouveau_code = CodePromo(code=code, reduction=int(reduction))
        db.session.add(nouveau_code)
        db.session.commit()
        flash("Code promo ajoute !", "success")
    return redirect(url_for("admin_dashboard"))

@app.route("/admin/supprimer-promo/<int:id>")
@login_required
def admin_supprimer_promo(id):
    promo = CodePromo.query.get_or_404(id)
    db.session.delete(promo)
    db.session.commit()
    flash("Code promo supprime.", "success")
    return redirect(url_for("admin_dashboard"))

@app.route("/admin/avis/approuver/<int:id>")
@login_required
def admin_avis_approuver(id):
    avis = Avis.query.get_or_404(id)
    avis.approuve = True
    db.session.commit()
    flash("Avis approuve !", "success")
    return redirect(url_for("admin_dashboard"))

@app.route("/admin/avis/supprimer/<int:id>")
@login_required
def admin_avis_supprimer(id):
    avis = Avis.query.get_or_404(id)
    db.session.delete(avis)
    db.session.commit()
    flash("Avis supprime.", "success")
    return redirect(url_for("admin_dashboard"))

@app.route("/admin/transactions")
@login_required
def admin_transactions():
    transactions = Transaction.query.order_by(Transaction.date.desc()).all()
    return render_template("admin_transactions.html", transactions=transactions)

@app.route("/admin/ajouter", methods=["POST"])
@login_required
def admin_ajouter():
    nom = request.form.get("nom")
    prix = request.form.get("prix")
    devise = request.form.get("devise", "$")
    categorie = request.form.get("categorie")
    description = request.form.get("description")
    image_file = request.files.get("image_file")
    image_url_input = request.form.get("image_url")
    nom_image = ""
    if image_file and image_file.filename != "":
        filename = "img_" + str(int(time.time())) + ".jpg"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        try:
            img = Image.open(image_file)
            if img.mode in ("RGBA", "P"): img = img.convert("RGB")
            img.save(filepath, "JPEG", quality=85)
            nom_image = filename
        except Exception as e: print(f"Erreur image : {e}")
    elif image_url_input:
        nom_image = image_url_input
    if nom and prix and categorie and nom_image:
        nouveau = Produit(nom=nom, prix=int(prix), devise=devise, categorie=categorie.lower(), image=nom_image, description=description)
        db.session.add(nouveau)
        db.session.commit()
        flash("Produit ajoute !", "success")
    else:
        flash("Erreur : champs manquants.", "error")
    return redirect(url_for("admin_dashboard"))

@app.route("/admin/modifier/<int:id>", methods=["GET", "POST"])
@login_required
def admin_modifier(id):
    produit = Produit.query.get_or_404(id)
    if request.method == "POST":
        produit.nom = request.form.get("nom")
        produit.prix = int(request.form.get("prix"))
        produit.devise = request.form.get("devise", "$")
        produit.categorie = request.form.get("categorie").lower()
        produit.description = request.form.get("description")
        image_file = request.files.get("image_file")
        image_url_input = request.form.get("image_url")
        if image_file and image_file.filename != "":
            filename = "img_" + str(int(time.time())) + ".jpg"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            try:
                img = Image.open(image_file)
                if img.mode in ("RGBA", "P"): img = img.convert("RGB")
                img.save(filepath, "JPEG", quality=85)
                produit.image = filename
            except Exception as e: print(f"Erreur image : {e}")
        elif image_url_input:
            produit.image = image_url_input
        db.session.commit()
        flash("Produit modifie !", "success")
        return redirect(url_for("admin_dashboard"))
    info = Parametre.query.first()
    avis_en_attente = Avis.query.filter_by(approuve=False).all()
    avis_approuves = Avis.query.filter_by(approuve=True).all()
    commandes = Commande.query.all()
    codes_promo = CodePromo.query.all()
    return render_template("admin_dashboard.html", produits=Produit.query.all(), image_url=image_url, edit=produit, info=info, avis_en_attente=avis_en_attente, avis_approuves=avis_approuves, commandes=commandes, codes_promo=codes_promo)

@app.route("/admin/supprimer/<int:id>")
@login_required
def admin_supprimer(id):
    produit = Produit.query.get_or_404(id)
    db.session.delete(produit)
    db.session.commit()
    flash("Produit supprime.", "success")
    return redirect(url_for("admin_dashboard"))

@app.route("/admin/infos", methods=["POST"])
@login_required
def admin_infos():
    info = Parametre.query.first()
    if not info:
        info = Parametre()
        db.session.add(info)
    info.ville = request.form.get("ville")
    info.quartier = request.form.get("quartier")
    info.frais = request.form.get("frais")
    info.delai = request.form.get("delai")
    info.heure_debut = request.form.get("heure_debut")
    info.heure_fin = request.form.get("heure_fin")
    info.promo_texte = request.form.get("promo_texte")
    info.promo_active = True if request.form.get("promo_active") else False
    db.session.commit()
    flash("Infos mises a jour !", "success")
    return redirect(url_for("admin_dashboard"))

if not os.path.exists(app.config["UPLOAD_FOLDER"]):
    os.makedirs(app.config["UPLOAD_FOLDER"])

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
