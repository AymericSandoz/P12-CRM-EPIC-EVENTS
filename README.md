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
   Si vous souhaitez utiliser Sentry pour la gestion des erreurs, configurez votre clé DSN dans le fichier `config.py`. Votre clé DSN est disponible dans votre interface utilisateur sentry.

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

   Il est possible, si vous préférez, de créer la base de donnée avec un script SQL:
   creation_db.sql

7. Un shéma de la base de donnée est disponible dans db_shema.png

## Authentification avec JWT

L'application utilise un système d'authentification basé sur des tokens JWT. Voici quelques points clés :

Les tokens JWT sont stockés dans un fichier jwt.txt après la connexion.
Le secret utilisé pour signer les tokens est stocké dans la variable SECRET_KEY.
L'algorithme utilisé pour le JWT est défini dans JWT_ALGORITHM.
Après authentification, le token JWT est utilisé pour autoriser l'accès à différentes fonctionnalités du système.

If faut donc configurer dans le fichier 'config.py' les variables JWT_ALGORITHM et SECRET_KEY.

```python
# config.py
JWT_ALGORITHM = 'Votre_algorithme_secret'
SECRET_KEY = 'Votre_clé_secrète'
```

## Gestion des permissions

Les permissions dans cette application sont basées sur les rôles des utilisateurs. Lorsqu'un utilisateur tente de créer, modifier ou supprimer des objets (clients, contrats, etc.), son rôle est vérifié pour s'assurer qu'il dispose des droits nécessaires.

Les rôles et permissions sont définis dans le fichier de configuration et appliqués via des décorateurs dans les services. Il est possible de définir différents niveaux de permissions selon les types d'actions et d'entités.

## Utilisation

### Commandes disponibles

Liste des commandes disponibles dans l'application :

```bash
python main.py --help
```

- Toutes les commandes sont disponibles dans le debugger python grâce au fichier launch.json

#### Exemples d'utilisation

Commandes Utilisateurs
Obtenir tous les utilisateurs :

```bash
python main.py user get_users
```

Obtenir un utilisateur spécifique :

```bash
python main.py user get_user --obj_id <id_utilisateur>
```

Créer un nouvel utilisateur :

```bash
python main.py user create_user --employee_number <numéro_employé> --name <nom_utilisateur> --email <email_utilisateur> --password <mot_de_passe> --department_id <id_département>
```

Mettre à jour un utilisateur :

```bash
python main.py user update_user --obj_id <id_utilisateur> --email <nouvel_email>
```

Supprimer un utilisateur :

```bash
python main.py user delete_user --obj_id <id_utilisateur>
```

Commandes Clients
Obtenir tous les clients :

```bash
python main.py client get_clients
```

Obtenir un client spécifique :

```bash
python main.py client get_client --obj_id <id_client>
```

Créer un nouveau client :

```bash
python main.py client create_client --full_name <nom_complet> --email <email_client> --phone <numéro_téléphone> --company_name <nom_entreprise> --last_update <date_dernière_mise_à_jour> --contact_person <personne_contact>
```

Mettre à jour un client :

```bash
python main.py client update_client --obj_id <id_client> --full_name <nouveau_nom>
```

Supprimer un client :

```bash
python main.py client delete_client --obj_id <id_client>
```

Commandes Contrats
Obtenir tous les contrats :

```bash
python main.py contract get_contracts
```

Obtenir un contrat spécifique :
bash```
python main.py contract get_contract --obj_id <id_contrat>

````

Créer un nouveau contrat :
```bash
python main.py contract create_contract --client_id <id_client> --total_amount <montant_total> --amount_due <montant_dû> --commercial_contact_id <id_contact_commercial>
````

Mettre à jour un contrat :

```bash
python main.py contract update_contract --obj_id <id_contrat> --total_amount <nouveau_montant_total>
```

Supprimer un contrat :

```bash
python main.py contract delete_contract --obj_id <id_contrat>
```

Commandes Événements
Obtenir tous les événements :

```bash
python main.py event get_events
```

Obtenir un événement spécifique :

```bash
python main.py event get_event --obj_id <id_événement>
```

Créer un nouvel événement :

```bash
python main.py event create_event --event_name <nom_événement> --contract_id <id_contrat> --client_id <id_client> --event_start_date <date_début> --event_end_date <date_fin> --support_contact <contact_support> --location <emplacement> --attendees <nombre_participants>
```

Mettre à jour un événement :

```bash
python main.py event update_event --obj_id <id_événement> --event_name <nouveau_nom>
```

Supprimer un événement :

```bash
python main.py event delete_event --obj_id <id_événement>
```

Commandes Départements
Obtenir tous les départements :

```bash
python main.py department get_departments
```

Obtenir un département spécifique :

```bash
python main.py department get_department --obj_id <id_département>
```

Créer un nouveau département :

```bash
python main.py department create_department --name <nom_département>
```

Mettre à jour un département :

```bash
python main.py department update_department --obj_id <id_département> --name <nouveau_nom>
```

Supprimer un département :

```bash
python main.py department delete_department --obj_id <id_département>
```

### Journalisation avec Sentry

Les erreurs critiques seront automatiquement envoyées à Sentry. Les événements tels que la création et modification des utilisateurs, clients, contrats sont également journalisés.

Actions CRUD : toute modification (création ou mise à jour) de la base de donnée est enregistrée.
