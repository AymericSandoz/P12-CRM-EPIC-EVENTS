# Epic Events CRM CLI

## Description

Epic Events CRM est une application de ligne de commande (CLI) conçue pour gérer les événements, clients, contrats, et collaborateurs d'une entreprise. Elle utilise SQLAlchemy pour la gestion de la base de données et Sentry pour la gestion des erreurs. L'application est composée de plusieurs commandes permettant de créer, lire, mettre à jour, et supprimer des entités telles que des clients, événements, et utilisateurs.

## Fonctionnalités

- **Gestion des utilisateurs** : création, mise à jour, suppression des utilisateurs.
- **Gestion des clients** : ajout, récupération, modification et suppression des clients.
- **Gestion des contrats et événements** : suivi et gestion des contrats signés et des événements organisés.
- **Système d'authentification** : authentification via JWT.
- **Journalisation des actions et erreurs** : Utilisation de Sentry pour enregistrer les erreurs, avec possibilité d'intégration des logs des actions utilisateurs.

## Technologies utilisées

- **Python** : Langage de programmation principal.
- **Click** : Bibliothèque pour la création de CLI.
- **SQLAlchemy** : ORM pour la gestion des bases de données.
- **Sentry** : Gestion des erreurs et journalisation.
- **MySQL** : Base de données relationnelle.

## Prérequis

- Python 3.x
- MySQL
- Un compte Sentry (si vous souhaitez utiliser Sentry pour le suivi des erreurs)

## Installation

1. Cloner le dépôt

   ```bash
   git clone https://github.com/ton-utilisateur/epic-events-crm.git
   cd epic-events-crm
   ```

2. Créer et activer un environnement virtuel

   ```bash
   python -m venv venv
   source venv/bin/activate  # Sur Windows : venv\Scripts\activate
   ```

3. Installer les dépendances

   ```bash
   pip install -r requirements.txt
   ```

4. Configurer la base de données
   Créez une base de données MySQL et mettez à jour le fichier `config.py` avec vos informations de connexion MySQL.

   Exemple de configuration :

   ```python
   # config.py
   SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://username:password@localhost/db_name'
   ```

5. Configurer Sentry (facultatif)
   Si vous souhaitez utiliser Sentry pour la gestion des erreurs, configurez votre clé DSN dans le fichier `config.py`.

   ```python
   # config.py
   SENTRY_DSN = 'https://your_dsn@sentry.io/your_project_id'
   ```

6. Initialiser la base de données
   Si vous n'avez pas encore de base de données initiale, exécutez le script de création de la base de donnée.

   ```bash
   python database.py create
   ```

   Cela va créer la base de données epicevents dans MySQL.

## Authentification avec JWT

L'application utilise un système d'authentification basé sur des tokens JWT. Voici quelques points clés :

Les tokens JWT sont stockés dans un fichier jwt.txt après la connexion.
Le secret utilisé pour signer les tokens est stocké dans la variable SECRET_KEY.
L'algorithme utilisé pour le JWT est défini dans JWT_ALGORITHM.
Après authentification, le token JWT est utilisé pour autoriser l'accès à différentes fonctionnalités du système.

If faut donc configurer dans le fichier 'config.py' les variables JWT_ALGORITHM et SECRET_KEY.

## Gestion des permissions

Les permissions dans cette application sont basées sur les rôles des utilisateurs. Lorsqu'un utilisateur tente de créer, modifier ou supprimer des objets (clients, contrats, etc.), son rôle est vérifié pour s'assurer qu'il dispose des droits nécessaires.

Les rôles et permissions sont définis dans le fichier de configuration et appliqués via des décorateurs dans les services. Il est possible de définir différents niveaux de permissions selon les types d'actions et d'entités.

## Utilisation

### Commandes disponibles

Liste des commandes disponibles dans l'application :

```bash
python main_2.py --help
```

#### Exemples d'utilisation

Authentification
Pour vous connecter avec un utilisateur existant :

```bash
python main_2.py login your_email@example.com your_password
```

#### Gestion des clients

Ajouter un client :

```bash
python main_2.py client create_client --full_name "John Doe" --email "john@example.com" --phone "1234567890" --company_name "Company XYZ" --contact_person "Jane Doe"
```

- Toutes les commandes sont disponibles dans le debugger grâce au fichier launch.json

### Journalisation avec Sentry

Les erreurs critiques seront automatiquement envoyées à Sentry. Les événements tels que la création et modification des utilisateurs, clients, contrats sont également journalisés.

Actions CRUD : toute modification (création ou mise à jour) de la base de donnée est enregistrée.
