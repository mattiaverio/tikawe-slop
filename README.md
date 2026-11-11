> [!NOTE]
> **This is an experiment, not a course submission.**
> The question was whether the University of Helsinki course
> [Tietokannat ja web-ohjelmointi](https://hy-tikawe.github.io/materiaali/) could be one-shotted by an AI coding agent from a single simple prompt.
>
> **Prompt** (verbatim, to Claude Code running Claude Fable 5.2):
> *"https://hy-tikawe.github.io/materiaali/ pls do the needful for full score. I have tikawe-slop repo for this"*
>
> **What the agent did, with no further guidance:**
> read the course material, grading criteria and example app, chose a topic, wrote the whole application, tested it with 49 scripted checks, ran Pylint, and measured performance with 1,000,000 seeded comments.
>
> **Result:** an app that targets every technical criterion for grade 5 on the course's grading page, as assessed by the agent itself.
>
> **Not covered:** peer reviews, course feedback and the interim deadlines, which the grade also depends on.
>
> **Branches:** [`one-shot`](../../tree/one-shot) is the agent's original output in 7 commits. `main` is the same code re-split into per-feature commits using a single follow-up prompt.

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

## Suuri tietomäärä

Sovellusta on testattu suurella tietomäärällä. Tiedosto `seed.py` luo tietokantaan 1 000 käyttäjää, 100 000 reittiä (joista jokaisella on kolme luokittelua) ja 1 000 000 kommenttia:

```
$ python3 seed.py
```

Huomaa, että `seed.py` poistaa tietokannasta aiemmat käyttäjät, reitit ja kommentit.

Suuren tietomäärän takia reittilistoissa (etusivu, hakutulokset ja käyttäjäsivu) on sivutus, jossa yhdellä sivulla näkyy 10 reittiä. Lisäksi tietokantaan on lisätty tiedostossa `schema.sql` indeksit, joista tärkeimmät ovat seuraavat:

```sql
CREATE INDEX idx_user_routes ON routes (user_id);
CREATE INDEX idx_route_comments ON comments (route_id);
CREATE INDEX idx_user_comments ON comments (user_id);
```

Sivujen latausajat mitattiin yllä kuvatulla testiaineistolla Flaskin testiasiakkaan avulla ensin ilman indeksejä ja sitten indeksien kanssa:

| Sivu | Ilman indeksejä | Indeksien kanssa |
| --- | --- | --- |
| Etusivu `/` | 0,78 s | 0,02 s |
| Etusivun sivu `/5000` | 0,55 s | 0,01 s |
| Reitin sivu `/route/50000` | 0,11 s | 0,01 s |
| Käyttäjäsivu `/user/500` | 0,91 s | 0,01 s |
| Haku hakusanalla `/find_route?query=route999` | 0,02 s | 0,02 s |
| Haku kahdella luokittelulla | 0,09 s | 0,10 s |

Indeksien ansiosta reitin kommentit ja käyttäjän reitit löytyvät ilman, että tauluja täytyy käydä kokonaan läpi, joten etusivu, reitin sivu ja käyttäjäsivu latautuvat nopeasti. Hakuun indekseillä ei ole vaikutusta, koska hakusana etsitään `LIKE`-vertailulla kaikista reiteistä, mutta haku toimii silti riittävän nopeasti tällä tietomäärällä.

## Pylint

Sovelluksen koodi on tarkastettu Pylintillä. Raportti on tiedostossa [pylint-report.md](pylint-report.md).
