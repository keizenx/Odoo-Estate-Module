# Odoo Estate Module

Ce module est une extension pour Odoo qui permet de gérer des biens immobiliers. Il a été développé comme un module d'apprentissage pour comprendre le développement sous Odoo.

## Fonctionnalités

- Gestion des propriétés immobilières
- Système d'offres sur les propriétés
- Gestion des types de propriétés
- Tags pour catégoriser les propriétés
- Intégration avec le module de comptabilité
- Vue Kanban pour une meilleure visualisation
- Extension du modèle utilisateur pour lier les vendeurs aux propriétés

## Installation

1. Clonez ce dépôt dans le dossier `addons` de votre installation Odoo
2. Mettez à jour la liste des applications dans Odoo
3. Recherchez "Estate" dans les applications
4. Installez le module

## Structure du Module 

estate/
├── models/
│ ├── estate_property.py
│ ├── estate_property_offer.py
│ ├── estate_property_tag.py
│ ├── estate_property_type.py
│ └── res_users.py
├── security/
│ └── ir.model.access.csv
├── views/
│ ├── estate_menus.xml
│ ├── estate_property_views.xml
│ ├── estate_property_offer_views.xml
│ ├── estate_property_tag_views.xml
│ └── estate_property_type_views.xml
├── init.py
└── manifest.py
