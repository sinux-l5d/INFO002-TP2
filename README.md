# INFO002 : TP2 stéganographie & signature

## Décisions

Dans l'image du diplôme j'ai choisi d'inclure le nom du diplôme, la personne diplômée, la moyenne, la date de délivrance et la signature des informations précédentes.

Cette signature est faite avec une clé privée, et le message signé donnée à la fonction est formaté de la manière suivante :

```python
nom_du_diplome + nom_etudiant.lower().replace(" ", "") + date + str(moyenne)
```

Inclure le nom du diplôme permet que l'étudiant ne puisse pas être diplômé de plusieurs diplômes différents avec le même diplôme.

Ensuite, on inclue toutes les informations dans l'image avec la signature grace au module `pickle` de python, qui permet de sérialiser et désérialiser des objets python en bytes, qui sont ensuite convertis en base64 et inclus dans l'image.

Je formate en base64 car j'ai écrit ma fonction de stéganographie pour qu'elle accepte une chaîne de caractères, et je n'ai pas eu le temps de la modifier pour qu'elle accepte des bytes.

J'écrit les informations dans les bits de poids faible de l'image, en commençant par les bits de poids faible du pixel en haut à droite, et en allant vers la gauche, puis en descendant d'une ligne.

C'est imparfait : on peut modifier le nom qui figure sur le diplôme sans que ça change les informations cachées. En revanche, le nom qui figure sur le diplôme ne sera plus le même que celui obtenu avec la sous-commande `verify_diploma`. Dans un monde parfait, j'aurais eu le temps d'écrire les informations dans la zone ou les informations du diplôme sont écrites.

## Signature

Pour signer, il faut une clé. Elle peut être générée avec la commande suivante :

```bash
python image.py genkey
```

On peut eventuellement ajouter `--name <nom>` pour avoir nos clés `<nom>.priv.pem` et `<nom>.pub.pem`.
A titre d'exemple, les clés dans ce dépôt (`diploma.priv.pem` et `diploma.pub.pem`) sont disponibles avec la _passphrase_ `universite`.

## Example

```
$ python image.py genkey --name univalchimie
Enter passphrase: alchimie
Enter passphrase again: alchimie

$ python image.py diploma --name "master en alchimie" --output "jean.diplome.png" --student "Jean Dupont" --moyenne 15.5 --privkey univalchimie.priv.pem
Enter passphrase: alchimie
Infos: b'gASVQwIAAAAAAAAojBJtYXN0ZXIgZW4gYWxjaGltaWWUjAtKZWFuIER1cG9udJSMCjA0LzAyLzIwMjSUR0AvAAAAAAAAQgACAABcKeQQePkyEbNRqJioiPKWkR1Ud64f/IZJMLI8kxrcZZumLkoAUG3W6kY8baKN8rg3dY6FZFejWAeo2RpQ1vnrjUugnEIsCuwbZwxF6yzzq5mbjPCFAx1acYKY1BoxKcxU6GwNjxl43hf38y+K/p3Eb+BUi6tMMWtfya6kkn4jab1n8TJ9ah1/zrQ4p+zVmGOMjV5zePC4FFI2Iz/UhrevLiF3oDmhY9Lf3VUMkrPhq1vLXT4YSe0S7/cUgkld8EbfPkZugxGZanXKLvOvIxOg7pbHDpIQLnAnIXRvTqWiVijECMq99r5Z8D5bcYKAKGuIp/2EZwQjvEPaWJj/qrlhcs1uYTMcE5VD6e3+easARsgX875Fy7dcYezA0QmK5MKmEeTkrV7JSmZjELz2mnaebzTV5S4vCSzZs4lSrJa1JXg73+07ig8oItSz5DYY2D7kByZXRKtbHpj0MifW5GWyZxSv+m6S/dHw0Rlzc6chYtKeUT36uc7B5FCZVk9tQVDvUmu8ubPI3mV6RcAtSPAgh3Qwmrg3UES9WaKpZxaT3SXaBfNqM413OSiuTRd4kZERURMEcJEB+m3TqbdwahoDc7kv4bJB+dAl1+0jN7Vl4ZTZAVEVVBqc5Z0avL/7dtQnD/BpYfRxH+9YGVFMPhpGcE8LTUA+zKPBpbCG1ES5O5R0lC4='
Length: 791

$ python image.py verify_diploma --image jean.diplome.png --key univalchimie.pub.pem --length 791 # 791 est la longueur du message caché, elle est ecrite dans le diplome en haut à gauche
Diploma: master en alchimie
Name: Jean Dupont
Date: 04/02/2024
Moyenne: 15.5
Signature: b'\\)\xe4\x10x\xf92\x11\xb3Q\xa8\x98\xa8\x88\xf2\x96\x91\x1dTw\xae\x1f\xfc\x86I0\xb2<\x93\x1a\xdce\x9b\xa6.J\x00Pm\xd6\xeaF<m\xa2\x8d\xf2\xb87u\x8e\x85dW\xa3X\x07\xa8\xd9\x1aP\xd6\xf9\xeb\x8dK\xa0\x9cB,\n\xec\x1bg\x0cE\xeb,\xf3\xab\x99\x9b\x8c\xf0\x85\x03\x1dZq\x82\x98\xd4\x1a1)\xccT\xe8l\r\x8f\x19x\xde\x17\xf7\xf3/\x8a\xfe\x9d\xc4o\xe0T\x8b\xabL1k_\xc9\xae\xa4\x92~#i\xbdg\xf12}j\x1d\x7f\xce\xb48\xa7\xec\xd5\x98c\x8c\x8d^sx\xf0\xb8\x14R6#?\xd4\x86\xb7\xaf.!w\xa09\xa1c\xd2\xdf\xddU\x0c\x92\xb3\xe1\xab[\xcb]>\x18I\xed\x12\xef\xf7\x14\x82I]\xf0F\xdf>Fn\x83\x11\x99ju\xca.\xf3\xaf#\x13\xa0\xee\x96\xc7\x0e\x92\x10.p\'!toN\xa5\xa2V(\xc4\x08\xca\xbd\xf6\xbeY\xf0>[q\x82\x80(k\x88\xa7\xfd\x84g\x04#\xbcC\xdaX\x98\xff\xaa\xb9ar\xcdna3\x1c\x13\x95C\xe9\xed\xfey\xab\x00F\xc8\x17\xf3\xbeE\xcb\xb7\\a\xec\xc0\xd1\t\x8a\xe4\xc2\xa6\x11\xe4\xe4\xad^\xc9Jfc\x10\xbc\xf6\x9av\x9eo4\xd5\xe5./\t,\xd9\xb3\x89R\xac\x96\xb5%x;\xdf\xed;\x8a\x0f("\xd4\xb3\xe46\x18\xd8>\xe4\x07&WD\xab[\x1e\x98\xf42\'\xd6\xe4e\xb2g\x14\xaf\xfan\x92\xfd\xd1\xf0\xd1\x19ss\xa7!b\xd2\x9eQ=\xfa\xb9\xce\xc1\xe4P\x99VOmAP\xefRk\xbc\xb9\xb3\xc8\xdeezE\xc0-H\xf0 \x87t0\x9a\xb87PD\xbdY\xa2\xa9g\x16\x93\xdd%\xda\x05\xf3j3\x8dw9(\xaeM\x17x\x91\x91\x11Q\x13\x04p\x91\x01\xfam\xd3\xa9\xb7pj\x1a\x03s\xb9/\xe1\xb2A\xf9\xd0%\xd7\xed#7\xb5e\xe1\x94\xd9\x01Q\x15T\x1a\x9c\xe5\x9d\x1a\xbc\xbf\xfbv\xd4\'\x0f\xf0ia\xf4q\x1f\xefX\x19QL>\x1aFpO\x0bM@>\xcc\xa3\xc1\xa5\xb0\x86\xd4D\xb9;'
Signature is valid, but check the infos are the same as expected
```

Notez que bien que la signature soit valide, il faut vérifier que les informations qui ont été signées sont bien celles écrites dans le diplôme.

En effet, les informations sont écrites sur les bits de poids faible **à partir d'en haut à droite**, et les informations sont écrites au centre de l'image.

Pour améliorer, il faudrait que les informations soit dans la zone ou les informations du diplôme sont écrites. Je n'ai pas eu le temps de le faire.

D'autres commandes sont disponibles pour tester les sous-fonctions, laissez-vous porter par `python image.py --help` pour les découvrir.
