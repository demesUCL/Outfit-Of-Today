const API = "http://127.0.0.1:8000"

async function ajouterVetement() {
    const vetement = {
        nom: document.getElementById("nom").value,
        categorie: document.getElementById("categorie").value,
        couleur: document.getElementById("couleur").value,
        style: Array.from(document.querySelectorAll("#style-options input:checked"))
           .map(cb => cb.value)
           .join(", "),
    }

    await fetch(`${API}/vetements`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(vetement)
    })

    document.getElementById("nom").value = ""
    document.getElementById("couleur").value = ""
    chargerVetements()
}

async function chargerVetements() {
    const res = await fetch(`${API}/vetements`)
    const vetements = await res.json()

    const liste = document.getElementById("liste-vetements")
    liste.innerHTML = ""

    vetements.forEach(v => {
        liste.innerHTML += `
            <div class="vetement-card">
                <span>👕 <b>${v.nom}</b> — ${v.categorie} / ${v.couleur} / ${v.style}</span>
                <button onclick="supprimerVetement(${v.id})">🗑️</button>
            </div>
        `
    })
}

async function supprimerVetement(id) {
    await fetch(`${API}/vetements/${id}`, { method: "DELETE" })
    chargerVetements()
}

async function chargerMeteo() {
    const ville = document.getElementById("ville").value
    if (!ville) return

    const res = await fetch(`${API}/meteo/${ville}`)
    const data = await res.json()

    document.getElementById("meteo-result").innerHTML = `
        <img src="https://openweathermap.org/img/wn/${data.icone}@2x.png">
        <b>${data.temperature}°C</b> — ${data.description} à ${data.ville}
    `
}

chargerVetements()