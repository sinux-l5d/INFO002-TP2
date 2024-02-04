# INFO002 : TP2 stéganographie & signature

## Décisions

Dans l'image du diplôme j'ai choisi d'inclure le nom du diplôme, la personne diplômée, la moyenne et la date de délivrance.

Je vais signer le nom de l'étudiant (minuscule et sans espace), la moyenne et la date de délivrance ainsi que le nom du diplôme (on ne veux pas que le nom du diplôme soit modifié, et que l'étudiant est soudainement un master en psycologie s'il a fait de l'informatique...).

## Signature

Pour signer, il faut une clé. Elle peut être générée avec la commande suivante :

```bash
python image.py genkey
```

On peut eventuellement ajouter `--name <nom>` pour avoir nos clés `<nom>.priv.pem` et `<nom>.pub.pem`.
A titre d'exemple, les clés dans ce dépôt (`diploma.priv.pem` et `diploma.pub.pem`) sont disponibles avec la _passphrase_ `universite`.
