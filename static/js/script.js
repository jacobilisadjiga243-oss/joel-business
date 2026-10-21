function getPanier() {
    return JSON.parse(localStorage.getItem("panier") || "[]");
}

function sauvegarderPanier(panier) {
    localStorage.setItem("panier", JSON.stringify(panier));
    mettreAJourCompteur();
}

function ajouterAuPanier(id, nom, prix, image) {
    let panier = getPanier();
    const existant = panier.find(p => p.id === id);
    if (existant) {
        existant.qte += 1;
    } else {
        panier.push({ id, nom, prix, image, qte: 1 });
    }
    sauvegarderPanier(panier);
    alert('"' + nom + '" ajoute au panier !');
}

function retirerDuPanier(id) {
    let panier = getPanier().filter(p => p.id !== id);
    sauvegarderPanier(panier);
    afficherPanier();
}

function changerQte(id, delta) {
    let panier = getPanier();
    const p = panier.find(x => x.id === id);
    if (!p) return;
    p.qte += delta;
    if (p.qte <= 0) panier = panier.filter(x => x.id !== id);
    sauvegarderPanier(panier);
    afficherPanier();
}

function mettreAJourCompteur() {
    const el = document.getElementById("cart-count");
    if (el) {
        const total = getPanier().reduce((s, p) => s + p.qte, 0);
        el.textContent = total;
    }
}

function afficherPanier() {
    const listeDiv = document.getElementById("panier-liste");
    const totalDiv = document.getElementById("panier-total");
    if (!listeDiv) return;

    const panier = getPanier();
    if (panier.length === 0) {
        listeDiv.innerHTML = "<p>Votre panier est vide.</p>";
        totalDiv.innerHTML = "";
        return;
    }

    let html = "";
    let total = 0;
    panier.forEach(p => {
        total += p.prix * p.qte;
        const imgSrc = p.image.startsWith("http") ? p.image : "/static/images/" + p.image;
        html += '<div class="panier-item">' +
            '<img src="' + imgSrc + '" alt="' + p.nom + '">' +
            '<div class="panier-info">' +
                '<h3>' + p.nom + '</h3>' +
                '<p>' + p.prix + ' $ x ' + p.qte + '</p>' +
            '</div>' +
            '<div class="panier-actions">' +
                '<button onclick="changerQte(' + p.id + ', -1)">-</button>' +
                '<span>' + p.qte + '</span>' +
                '<button onclick="changerQte(' + p.id + ', 1)">+</button>' +
                '<button class="btn-suppr" onclick="retirerDuPanier(' + p.id + ')">X</button>' +
            '</div>' +
        '</div>';
    });
    listeDiv.innerHTML = html;
    totalDiv.innerHTML = '<h2>Total : ' + total + ' $</h2>';
}

function commanderWhatsApp() {
    const panier = getPanier();
    if (panier.length === 0) {
        alert("Votre panier est vide !");
        return;
    }
    let msg = "Bonjour Joel Business, je souhaite commander :\n\n";
    let total = 0;
    panier.forEach(p => {
        msg += "- " + p.nom + " x" + p.qte + " = " + (p.prix * p.qte) + " $\n";
        total += p.prix * p.qte;
    });
    msg += "\nTOTAL : " + total + " $\n\nMerci de me confirmer la disponibilite.";

    const url = "https://wa.me/" + WHATSAPP + "?text=" + encodeURIComponent(msg);
    window.open(url, "_blank");
}

function envoyerFormulaireContact(event) {
    event.preventDefault();

    const nom = document.getElementById("nom").value.trim();
    const telephone = document.getElementById("telephone").value.trim();
    const adresse = document.getElementById("adresse").value.trim();
    const heure = document.getElementById("heure").value;
    const message = document.getElementById("message").value.trim();

    if (!nom || !telephone || !adresse) {
        alert("Merci de remplir le nom, le telephone et l'adresse.");
        return;
    }

    let msg = "Bonjour Joel Business,\n\n";
    msg += "Je souhaite passer une commande / avoir des informations.\n\n";
    msg += "Nom : " + nom + "\n";
    msg += "Telephone : " + telephone + "\n";
    msg += "Adresse de livraison : " + adresse + "\n";
    msg += "Heure de livraison souhaitee : " + heure + "\n";
    if (message) {
        msg += "\nProduits / message :\n" + message + "\n";
    }
    msg += "\nMerci de me confirmer.";

    const url = "https://wa.me/" + WHATSAPP_NUMBER + "?text=" + encodeURIComponent(msg);
    window.open(url, "_blank");
}

document.addEventListener("DOMContentLoaded", () => {
    mettreAJourCompteur();
    afficherPanier();
});
