--------------------------------------------AutoTaskNotion-V1[FR]-----------------------------------------------------

Ce script facilite l'intégration de tâches et de projets de Notion dans votre calendrier Google. Vous pouvez importer des tâches et des projets de Notion dans votre Google Calendar en fournissant simplement les clés d'API de Notion et de Google Calendar, ainsi que les identifiants des bases de données Notion. Pour simplifier cela, j'ai créé un modèle Notion [lien vers le modèle à venir].

Pour l'instant ceci est qu'une V1, cela est en grande parti fait pour moi , mais lors d'une V2 je vais améliorer en pasant par une application React donc apparaition d'une interface graphique pour l'utilisateur et je ferais en sorte que tous soit controlable par une paramétrisation dans l'interface graphique.


## Table des matières

1. [Installation](#installation)
2. [Configuration](#configuration)
3. [Utilisation](#utilisation)
4. [Fonctionnalités](#fonctionnalités)
5. [Contributions](#contributions)
6. [Licence](#licence)

## Installation

Pour utiliser ce script, vous devez disposer de Python 3 installé sur votre machine. Ensuite, vous pouvez cloner ce dépôt et installer les dépendances requises via pip :

git clone https://github.com/FlorianCliquet/AutoTaskNotion-V1.git
cd AutoTaskNotion-V1
pip install -r requirements.txt

## Configuration

Avant de commencer à utiliser le script, vous devez configurer les clés d'API de Notion et de Google Calendar, ainsi que les identifiants des bases de données Notion. Voici comment procéder :

1. Créez un fichier `.env` à la racine du projet (Si vous le faites, pensez à changer le path des .env) ou je conseille dans un folder externe tels que :

```
random_folder/
│
├── AutoTaskNotion-V1/
│   └── main.py
│
└── ConfigShit/
    └── AutoTaskNotion-V1/
         └── credentials.json -> obtenable avec Oauth2 sur l'API Google Calendar
         └── .env
         └── token.json (créé automatiquement)
```

2. Ajoutez les clés d'API de Notion et de Google Calendar, ainsi que les identifiants des bases de données Notion dans le fichier `.env` comme suit :

NOTION_API=VOTRE_CLE_API_NOTION
PROJET_ID=ID_DE_VOTRE_BASE_DE_DONNÉES_PROJET_NOTION
TASK_ID=ID_DE_VOTRE_BASE_DE_DONNÉES_TÂCHES_NOTION
EXTERNAL_CALENDAR=ID_DE_VOTRE_CALENDRIER_GOOGLE_IMPORTE ( pas obligatoire )

3. Une fois les clés d'API et les identifiants configurés, vous êtes prêt à utiliser le script.

## Utilisation

Pour utiliser le script, exécutez simplement `main.py` :

python3 main.py


Le script récupérera les tâches et les projets de Notion, les intégrera dans votre Google Calendar et affichera un message indiquant que les tâches et les projets ont été planifiés avec succès.

## Fonctionnalités

- Importation des tâches et des projets de Notion dans Google Calendar.
- Planification des tâches en fonction de la disponibilité dans le calendrier.
- Gestion des priorités et des dates de début des projets.

## Contributions

Les contributions sont les bienvenues ! Si vous souhaitez améliorer ce script ou corriger des bugs, n'hésitez pas à ouvrir une issue ou à soumettre une demande de fusion.

## Licence

Ce projet est sous licence MIT. Voir LICENSE pour plus d'informations.

--------------------------------------------AutoTaskNotion-V1[EN]-----------------------------------------------------

This script facilitates the integration of tasks and projects from Notion into your Google Calendar. You can import tasks and projects from Notion into your Google Calendar by simply providing the Notion and Google Calendar API keys, as well as the Notion database IDs. To simplify this, I have created a Notion template [link to template coming soon].

For now, this is just a V1, mostly done for my own use. However, in a V2, I will improve it by transitioning to a React application, thus introducing a graphical interface for the user. I will ensure that everything is controllable through parameterization in the graphical interface.

## Table of Contents

1. [Installation](#installation)
2. [Configuration](#configuration)
3. [Usage](#usage)
4. [Features](#features)
5. [Contributions](#contributions)
6. [License](#license)

## Installation

To use this script, you need to have Python 3 installed on your machine. Then, you can clone this repository and install the required dependencies via pip:

git clone https://github.com/FlorianCliquet/AutoTaskNotion-V1.git
cd AutoTaskNotion-V1
pip install -r requirements.txt

## Configuration

Before you start using the script, you need to configure the Notion and Google Calendar API keys, as well as the Notion database IDs. Here's how:

1. Create a `.env` file at the root of the project (If you do it, remember to change the path of the .env) or I advise you to put it in an external folder such as:

```
random_folder/
│
├── AutoTaskNotion-V1/
│   └── main.py
│
└── ConfigShit/
    └── AutoTaskNotion-V1/
         └── credentials.json -> obtainable with Oauth2 on the Google Calendar API
         └── .env
         └── token.json (created automatically)
```

2. Add the Notion and Google Calendar API keys, as well as the Notion database IDs, to the `.env` file as follows:

NOTION_API=YOUR_NOTION_API_KEY
PROJET_ID=YOUR_PROJECT_NOTION_DATABASE_ID
TASK_ID=YOUR_TASK_NOTION_DATABASE_ID
EXTERNAL_CALENDAR=YOUR_IMPORTED_GOOGLE_CALENDAR_ID

3. Once the API keys and IDs are configured, you are ready to use the script.

## Usage

To use the script, simply run `main.py`:

python3 main.py

The script will retrieve tasks and projects from Notion, integrate them into your Google Calendar, and display a message indicating that the tasks and projects have been successfully scheduled.

## Features

- Import tasks and projects from Notion into Google Calendar.
- Schedule tasks based on availability in the calendar.
- Manage priorities and start dates of projects.

## Contributions

Contributions are welcome! If you want to improve this script or fix bugs, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See LICENSE for more information.
