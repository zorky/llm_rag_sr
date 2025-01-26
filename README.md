# Création d'un RAG sur la documentation d'Outscale

A partir d'un post LinkedIn de [Stéphane Robert](https://www.linkedin.com/in/stephanerobert1/), afin de m'autoformer, j'ai repris le source python d'un POC qui permet de créer un RAG sur la documentation d'Outscale.

Post LinkedIn qui cite les articles de Stéphane : https://www.linkedin.com/feed/update/urn:li:activity:7289224764785635328/

Source python initial du POC de Stéphane : https://blog.stephane-robert.info/docs/ia/rag/

## Documents Outscale

Le répertoire a été créé pour stocker les documents Outscale via la commande suivante

```bash
$ wget -mpEk https://docs.outscale.com/
```

L'extraction a été stocké sur le dépôt.

## Prérequis

Un environnement virtuel python est recommandé

```bash
$ virtualenv env
$ source env/Scripts/activate
$ pip install -r requirements.txt
```

## Utilisation

```bash
$ python main.py
```
