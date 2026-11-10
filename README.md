# Retkireitit

Sovelluksessa käyttäjät jakavat retkeily- ja vaellusreittejä sekä kommentoivat ja arvioivat toistensa reittejä.

## Sovelluksen toiminnot

* Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
* Käyttäjä pystyy lisäämään, muokkaamaan ja poistamaan reittejä.
* Käyttäjä pystyy lisäämään reittiin kuvia ja poistamaan niitä.
* Käyttäjä näkee sovellukseen lisätyt reitit, sekä omat että muiden lisäämät.
* Käyttäjä pystyy etsimään reittejä hakusanalla ja luokittelujen perusteella.
* Sovelluksessa on käyttäjäsivut, jotka näyttävät tilastoja (reittien määrä ja yhteispituus, kommenttien määrä, saatujen arvosanojen keskiarvo) ja käyttäjän lisäämät reitit.
* Käyttäjä pystyy valitsemaan reitille yhden tai useamman luokittelun (alue, vaativuus, vuodenaika). Luokittelut ovat tietokannassa.
* Käyttäjä pystyy lisäämään omiin ja muiden reitteihin kommentin ja arvosanan (1–5) sekä poistamaan omia kommenttejaan.

## Sovelluksen asennus

Asenna `flask`-kirjasto:

```
$ pip install flask
```

Luo tietokannan taulut ja lisää alkutiedot:

```
$ sqlite3 database.db < schema.sql
$ sqlite3 database.db < init.sql
```

Voit käynnistää sovelluksen näin:

```
$ flask run
```

Sovellus toimii tämän jälkeen osoitteessa http://127.0.0.1:5000. Testaamista varten luo sovelluksessa tunnus (tai kaksi, jotta voit kokeilla toisen käyttäjän reittien kommentointia) ja kirjaudu sisään.
