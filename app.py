from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from config import Config
from functools import wraps

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

WHATSAPP_NUMBER = "243992519112"
ADMIN_PASSWORD = "joel2026" # ⚠️ Mot de passe pour l'admin

INFO_LIVRAISON = {
    "ville": "Kinshasa", "quartier": "A preciser", "frais": "A confirmer selon la zone",
    "delai": "24 a 48h", "heure_debut": "08:00", "heure_fin": "20:00",
}

# --- MODELES (BASE DE DONNEES) ---
class Produit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    prix = db.Column(db.Integer, nullable=False)
    categorie = db.Column(db.String(50), nullable=False)
    image = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)

# --- FONCTIONS UTILES ---
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

# --- ROUTES DU SITE PUBLIC ---
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
    return render_template("contact.html", whatsapp_number=WHATSAPP_NUMBER, info=INFO_LIVRAISON)

@app.route("/api/whatsapp-number")
def get_whatsapp():
    return jsonify({"number": WHATSAPP_NUMBER})

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
    return render_template("admin_dashboard.html", produits=produits, image_url=image_url)

@app.route("/admin/ajouter", methods=["POST"])
@login_required
def admin_ajouter():
    nom = request.form.get("nom")
    prix = request.form.get("prix")
    categorie = request.form.get("categorie")
    image = request.form.get("image")
    description = request.form.get("description")
    
    nouveau_produit = Produit(nom=nom, prix=int(prix), categorie=categorie, image=image, description=description)
    db.session.add(nouveau_produit)
    db.session.commit()
    flash("Produit ajoute avec succes !", "success")
    return redirect(url_for("admin_dashboard"))

@app.route("/admin/supprimer/<int:id>")
@login_required
def admin_supprimer(id):
    produit = Produit.query.get_or_404(id)
    db.session.delete(produit)
    db.session.commit()
    flash("Produit supprime.", "success")
    return redirect(url_for("admin_dashboard"))

# --- INITIALISATION DE LA BASE ---
with app.app_context():
    db.create_all()
    if Produit.query.count() == 0:
        p1 = Produit(nom="Robe Elegante Noire", prix=35, categorie="femme", image="https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=400&h=500&fit=crop", description="Robe de soiree chic.")
        p2 = Produit(nom="Chemise Homme Bleue", prix=28, categorie="homme", image="https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?w=400&h=500&fit=crop", description="Chemise coton.")
        p3 = Produit(nom="Valise Cabine Rouge", prix=55, categorie="valise", image="https://images.unsplash.com/photo-1565026057447-bc90a3dceb87?w=400&h=500&fit=crop", description="Valise rigide.")
        db.session.add_all([p1, p2, p3])
        db.session.commit()

if __name__ == "__main__":
    app.run(debug=True)
