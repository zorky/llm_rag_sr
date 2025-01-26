# Création d'un RAG sur la documentation d'Outscale

A partir d'un post LinkedIn de [Stéphane Robert](https://www.linkedin.com/in/stephanerobert1/), afin d'appréhender ce domaine de l'IA générative, j'ai repris le source python d'un POC pour qu'il soit modulaire, ce source permet de créer un RAG sur la documentation d'Outscale.

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

NB : chez moi, cela se termine par un **Segmentation fault** 

Une astuce serait https://github.com/UKPLab/sentence-transformers/issues/2332 mais j'ai toujours le core dump

ou https://github.com/UKPLab/sentence-transformers/issues/2228#issuecomment-1837129592 descendre PyTorch à la 2.0.* : à tester

```bash
$ pip show torch
Name: torch
Version: 2.5.1
Summary: Tensors and Dynamic neural networks in Python with strong GPU acceleration
Home-page: https://pytorch.org/
```

```bash
$ export OMP_NUM_THREADS=1
$ python main.py
Embedding model loaded: sentence-transformers/all-mpnet-base-v2
Embedding : client=SentenceTransformer(
  (0): Transformer({'max_seq_length': 384, 'do_lower_case': False}) with Transformer model: MPNetModel
  (1): Pooling({'word_embedding_dimension': 768, 'pooling_mode_cls_token': False, 'pooling_mode_mean_tokens': True, 'pooling_mode_max_tokens': False, 'pooling_mode_mean_sqrt_len_tokens': False, 'pooling_mode_weightedmean_tokens': False, 'pooling_mode_lasttoken': False, '
include_prompt': True})
  (2): Normalize()
) model_name='sentence-transformers/all-mpnet-base-v2' cache_folder=None model_kwargs={} encode_kwargs={} multi_process=False show_progress=False
persisting to ./chroma
Segmentation fault
```

Autre piste avec WSL2 : https://discuss.huggingface.co/t/segmentation-fault-core-dumped/58046/14 

```
[wsl2]
memory=16GB 
processors=2
```
