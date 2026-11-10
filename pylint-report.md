# Pylint-raportti

Pylint antaa seuraavan raportin sovelluksesta:

```
************* Module app
app.py:1:0: C0114: Missing module docstring (missing-module-docstring)
app.py:19:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:23:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:29:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:32:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:49:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:63:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:72:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:79:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:93:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:111:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:135:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:148:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:158:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:164:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:176:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:191:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:205:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:220:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:241:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:257:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:265:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:287:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:300:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:304:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:330:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:348:0: C0116: Missing function or method docstring (missing-function-docstring)
************* Module config
config.py:1:0: C0114: Missing module docstring (missing-module-docstring)
************* Module db
db.py:1:0: C0114: Missing module docstring (missing-module-docstring)
db.py:4:0: C0116: Missing function or method docstring (missing-function-docstring)
db.py:10:0: C0116: Missing function or method docstring (missing-function-docstring)
db.py:19:0: C0116: Missing function or method docstring (missing-function-docstring)
db.py:22:0: C0116: Missing function or method docstring (missing-function-docstring)
************* Module routes
routes.py:1:0: C0114: Missing module docstring (missing-module-docstring)
routes.py:3:0: C0116: Missing function or method docstring (missing-function-docstring)
routes.py:15:0: C0116: Missing function or method docstring (missing-function-docstring)
routes.py:28:0: C0116: Missing function or method docstring (missing-function-docstring)
routes.py:32:0: C0116: Missing function or method docstring (missing-function-docstring)
routes.py:52:0: C0116: Missing function or method docstring (missing-function-docstring)
routes.py:65:0: C0116: Missing function or method docstring (missing-function-docstring)
routes.py:79:0: C0116: Missing function or method docstring (missing-function-docstring)
routes.py:89:0: C0116: Missing function or method docstring (missing-function-docstring)
routes.py:93:0: C0116: Missing function or method docstring (missing-function-docstring)
routes.py:106:0: C0116: Missing function or method docstring (missing-function-docstring)
routes.py:111:0: C0116: Missing function or method docstring (missing-function-docstring)
routes.py:126:0: C0116: Missing function or method docstring (missing-function-docstring)
routes.py:131:0: C0116: Missing function or method docstring (missing-function-docstring)
routes.py:143:0: C0116: Missing function or method docstring (missing-function-docstring)
routes.py:148:0: C0116: Missing function or method docstring (missing-function-docstring)
routes.py:152:0: C0116: Missing function or method docstring (missing-function-docstring)
routes.py:156:0: C0116: Missing function or method docstring (missing-function-docstring)
routes.py:160:0: C0116: Missing function or method docstring (missing-function-docstring)
routes.py:164:0: C0116: Missing function or method docstring (missing-function-docstring)
routes.py:169:0: C0116: Missing function or method docstring (missing-function-docstring)
************* Module seed
seed.py:1:0: C0114: Missing module docstring (missing-module-docstring)
************* Module users
users.py:1:0: C0114: Missing module docstring (missing-module-docstring)
users.py:5:0: C0116: Missing function or method docstring (missing-function-docstring)
users.py:10:0: C0116: Missing function or method docstring (missing-function-docstring)
users.py:23:0: C0116: Missing function or method docstring (missing-function-docstring)
users.py:33:0: C0116: Missing function or method docstring (missing-function-docstring)
users.py:38:0: C0116: Missing function or method docstring (missing-function-docstring)

------------------------------------------------------------------
Your code has been rated at 8.60/10
```

Kaikki muut Pylintin ilmoitukset on korjattu koodista. Käydään seuraavaksi läpi raportin sisältö ja perustellaan, miksi jäljelle jääneitä asioita ei ole korjattu sovelluksessa.

## Docstring-ilmoitukset

Kaikki raportin ilmoitukset ovat seuraavan tyyppisiä ilmoituksia:

```
app.py:1:0: C0114: Missing module docstring (missing-module-docstring)
app.py:19:0: C0116: Missing function or method docstring (missing-function-docstring)
```

Nämä ilmoitukset tarkoittavat, että moduuleissa ja funktioissa ei ole docstring-kommentteja. Sovelluksen kehityksessä on tehty tietoisesti päätös, ettei käytetä docstring-kommentteja, koska funktiot ovat lyhyitä ja niiden nimet kuvaavat, mitä funktiot tekevät. Tämä vastaa myös kurssin materiaalin ja esimerkkisovelluksen tyyliä.
