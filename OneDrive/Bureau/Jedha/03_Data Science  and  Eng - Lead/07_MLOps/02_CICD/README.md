# 💻 Exercice Jenkins – API DoorDash Fee Service

## 🎯 Objectif

Dans cet exercice, vous allez :

- Créer un Job Freestyle dans Jenkins
- Cloner un projet GitHub contenant une API FastAPI
- Builder et exécuter une image Docker depuis Jenkins
- Tester automatiquement les endpoints de l’API avec curl

---

## 🧱 Étapes détaillées

### 1. 🔧 Créer un projet Jenkins

- Rendez-vous sur votre interface Jenkins
- Cliquez sur "Nouveau Item"
- Choisissez "Projet Freestyle"
- Nommez-le DoorDash-Fee-Service

### 2. 🔁 Cloner le dépôt GitHub

- Forkez ce dépôt GitHub sur votre propre compte :

```git
https://github.com/JedhaBootcamp/doordash-copycat
```

- Dans la configuration du projet Jenkins : - Allez dans "Gestion du code source" - Choisissez Git - Entrez l’URL de votre fork personnel
  (Optionnel) ajoutez vos identifiants si besoin

---

### 3. 🌐 Créer le réseau Docker partagé

Avant de lancer le job, ouvrez un terminal et entrez dans le conteneur jenkins-docker :

```bash
docker exec -it jenkins-docker sh
```

Une fois dans le conteneur, créez le réseau Docker :

```bash
docker network create jenkins-net
```

✅ Ce réseau permettra aux conteneurs lancés par Jenkins de communiquer entre eux (notamment curl → API).

---

### 4. ⚙️ Ajouter les étapes du build dans Jenkins

Dans la section "Étapes du build" → choisissez "Exécuter un script shell"
Ajoutez le script suivant :

```bash
# 1. Build de l’image
docker build -t delivery-fee-service .

# 2. Supprimer tout conteneur existant (évite les conflits de nom)
docker rm -f delivery-fee-container 2>/dev/null || true

# 3. Lancer le conteneur dans le réseau Docker partagé
docker run -d --network jenkins-net -p 8090:8090 --name delivery-fee-container delivery-fee-service

# 4. Attendre que l’API démarre
sleep 10
docker ps

# 5. Tester les endpoints avec curl
echo "GET /"
docker run --rm --network jenkins-net curlimages/curl http://delivery-fee-container:8090/

echo "POST /calculate-fee/"
docker run --rm --network jenkins-net curlimages/curl -X POST http://delivery-fee-container:8090/calculate-fee/ \
  -H "Content-Type: application/json" \
  -d '{"distance_km": 10.5, "weight_kg": 2.0}'

echo "GET /status/"
docker run --rm --network jenkins-net curlimages/curl http://delivery-fee-container:8090/status/

# 6. Nettoyage du conteneur
docker stop delivery-fee-container
docker rm delivery-fee-container
```

---

## 🧠 Rappel – À quoi sert --network jenkins-net ?

Par défaut, chaque conteneur Docker est isolé.
Le flag --network jenkins-net permet aux conteneurs (ex. curl) de "voir" les autres (ex. l'API) via leur nom Docker.
Sans ce réseau, la commande curl http://delivery-fee-container:8090/ échoue avec Could not resolve host.
