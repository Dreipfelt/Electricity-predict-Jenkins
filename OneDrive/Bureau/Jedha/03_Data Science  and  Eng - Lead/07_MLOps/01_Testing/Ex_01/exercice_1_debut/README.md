# 📦 exercice_1 – Pytest Docker Setup

## 📁 Structure du projet

exercice_1/
│
├── app/ # Code source principal
│ ├── basic_operations.py
│ ├── data_validation.py
│ ├── set_operations.py
│ └── string_operations.py
│
├── tests/ # Fichiers de tests Pytest
│ ├── test_basic_operations.py
│ ├── test_data_validation.py
│ ├── test_set_operations.py
│ └── test_string_operations.py
│
├── Dockerfile # Dockerfile principal
├── Dockerfile.python310 # Alternative pour compatibilité Python 3.10+
├── requirements.txt # Dépendances Python
└── .pytest_cache/ # Cache Pytest

---

## 🚀 Lancer les tests avec Docker

### ✅ Option 1 — Dockerfile du cours mis à jour

Fichier `Dockerfile` de base :

```dockerfile
FROM continuumio/miniconda3
WORKDIR /home
COPY . .
RUN apt update -y && apt upgrade -y && apt install -y nano gcc build-essential python3-dev
RUN pip install --upgrade pip setuptools wheel
RUN pip install -v -r requirements.txt
ENV PYTHONPATH=/home
CMD ["python", "-m", "pytest", "tests/"]
```

### ✅ Option 2 — Dockerfile sous 3.10

Fichier `Dockerfile` (3.10) :

```dockerfile
FROM python:3.10
WORKDIR /home
COPY . .

RUN pip install -r requirements.txt
ENV PYTHONPATH=/home
CMD ["-m", "pytest", "tests/"]
```

---

## 🧪 Exécuter les tests

Dans le dossier exercice_1, utilisez ce build :

```bash
docker build . -t pytest-tests
```

---

## ✅ Exemple de fichier requirements.txt

Assurez-vous que les dépendances suivantes sont présentes :

```txt
pandas
scikit-learn
joblib
pytest
great_expectations==0.18.19
```

Ajoutez d’autres librairies si besoin.

### 📝 Notes

- Les modules Python sont importés grâce au PYTHONPATH=/home.
- Le répertoire tests/ contient les fichiers de tests unitaires associés aux modules dans app/.

---

## 🧪 Exécution manuelle des tests un par un

Si vous souhaitez exécuter les fichiers de test **individuellement** depuis le **bash du conteneur**, vous pouvez procéder comme suit :

### 1. Lancer un conteneur interactif

```bash
docker run -it -v "$(pwd):/home" pytest-tests bash
```

### 2. Exécuter les tests un par un

Une fois dans le conteneur, utilisez la commande suivante pour exécuter un test spécifique :

```bash
pytest tests/test_basic_operations.py
```

Répétez avec les autres fichiers de test si nécessaire :

```bash
pytest tests/test_set_operations.py
pytest tests/test_string_operations.py
pytest tests/test_data_validation.py
```

Et sinon pour exécuter l'ensemble des tests:

```bash
pytest tests/
```
