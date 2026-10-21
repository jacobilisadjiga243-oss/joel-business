from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from config import Config
from functools import wraps
import os
from werkzeug.utils import secure_filename
import time
from PIL import Image

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

WHATSAPP_NUMBER = "243992519112"
ADMIN_PASSWORD = "joel2026"

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
    produits = Produit.query.all()
    return render_template("index.html", produits=produits, image_url=image_url)

@app.route("/produits")
def produits_page():
    categorie = request.args.get("categorie", "tous")
    if categorie == "tous":
        liste = Produit.query.all()
    else:
        liste = Produit.query.filter_by(categorie=categorie).all()
    return render_template("produits.html", produits=liste, categorie=categorie, image_url=image_url)

@app.route("/produit/<int:id>")
def produit_detail(id):
    produit = Produit.query.get_or_404(id)
    return render_template("produit.html", produit=produit, image_url=image_url)

@app.route("/panier")
def panier():
    return render_template("panier.html", whatsapp_number=WHATSAPP_NUMBER)

@app.route("/contact")
def contact():
    info = Parametre.query.first()
    if not info:
        info = Parametre()
    return render_template("contact.html", whatsapp_number=WHATSAPP_NUMBER, info=info)

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
    return render_template("admin_dashboard.html", produits=produits, image_url=image_url, edit=None, info=info)

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
        except Exception as e:
            print(f"Erreur image : {e}")
    elif image_url_input:
        nom_image = image_url_input

    if nom and prix and categorie and nom_image:
        nouveau = Produit(nom=nom, prix=int(prix), devise=devise, categorie=categorie.lower(), image=nom_image, description=description)
        db.session.add(nouveau)
        db.session.commit()
        flash("Produit ajoute avec succes !", "success")
    else:
        flash("Erreur : Veuillez remplir tous les champs ou verifier l'image.", "error")
        
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
            except Exception as e:
                print(f"Erreur image : {e}")
        elif image_url_input:
            produit.image = image_url_input
            
        db.session.commit()
        flash("Produit modifie avec succes !", "success")
        return redirect(url_for("admin_dashboard"))
        
    info = Parametre.query.first()
    return render_template("admin_dashboard.html", produits=Produit.query.all(), image_url=image_url, edit=produit, info=info)

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
    
    db.session.commit()
    flash("Informations de livraison mises a jour !", "success")
    return redirect(url_for("admin_dashboard"))

# --- CREATION DES DOSSIERS ET DE LA BASE ---
if not os.path.exists(app.config["UPLOAD_FOLDER"]):
    os.makedirs(app.config["UPLOAD_FOLDER"])

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
