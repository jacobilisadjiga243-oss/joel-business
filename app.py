from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Numero WhatsApp business de Joel
WHATSAPP_NUMBER = "243992519112"

# Infos de livraison (PROVISOIRE - a modifier plus tard)
INFO_LIVRAISON = {
    "ville": "Kinshasa",
    "quartier": "A preciser",
    "frais": "A confirmer selon la zone",
    "delai": "24 a 48h",
    "heure_debut": "08:00",
    "heure_fin": "20:00",
}

PRODUITS = [
    {"id": 1, "nom": "Robe Elegante Noire", "prix": 35, "categorie": "femme",
     "image": "https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=400&h=500&fit=crop",
     "description": "Robe de soiree chic, tissu satine."},
    {"id": 2, "nom": "Robe Ete Fleurie", "prix": 25, "categorie": "femme",
     "image": "https://images.unsplash.com/photo-1596783074918-c84cb06531ca?w=400&h=500&fit=crop",
     "description": "Robe legere parfaite pour l'ete."},
    {"id": 3, "nom": "Pantalon Femme Beige", "prix": 22, "categorie": "femme",
     "image": "https://images.unsplash.com/photo-1594633312681-425c7b97ccd1?w=400&h=500&fit=crop",
     "description": "Pantalon fluide, taille haute."},
    {"id": 4, "nom": "Chemise Homme Bleue", "prix": 28, "categorie": "homme",
     "image": "https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?w=400&h=500&fit=crop",
     "description": "Chemise coton, coupe slim."},
    {"id": 5, "nom": "Pantalon Homme Noir", "prix": 30, "categorie": "homme",
     "image": "https://images.unsplash.com/photo-1473966968600-fa801b869a1a?w=400&h=500&fit=crop",
     "description": "Pantalon costume, elegant."},
    {"id": 6, "nom": "Costume Homme Gris", "prix": 75, "categorie": "homme",
     "image": "https://images.unsplash.com/photo-1594938298603-c8148c4dae35?w=400&h=500&fit=crop",
     "description": "Ensemble veste + pantalon."},
    {"id": 7, "nom": "Valise Cabine Rouge", "prix": 55, "categorie": "valise",
     "image": "https://images.unsplash.com/photo-1565026057447-bc90a3dceb87?w=400&h=500&fit=crop",
     "description": "Valise rigide avec roulettes."},
    {"id": 8, "nom": "Grande Valise Bleue", "prix": 80, "categorie": "valise",
     "image": "https://images.unsplash.com/photo-1544816155-12df9643f363?w=400&h=500&fit=crop",
     "description": "Grande capacite, coque solide."},
]


def image_url(image):
    if image.startswith("http"):
        return image
    return "/static/images/" + image


@app.route("/")
def index():
    return render_template("index.html", produits=PRODUITS, image_url=image_url)


@app.route("/produits")
def produits_page():
    categorie = request.args.get("categorie", "tous")
    if categorie == "tous":
        liste = PRODUITS
    else:
        liste = [p for p in PRODUITS if p["categorie"] == categorie]
    return render_template("produits.html", produits=liste, categorie=categorie, image_url=image_url)


@app.route("/produit/<int:id>")
def produit_detail(id):
    produit = next((p for p in PRODUITS if p["id"] == id), None)
    if not produit:
        return "Produit introuvable", 404
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


if __name__ == "__main__":
    app.run(debug=True)
