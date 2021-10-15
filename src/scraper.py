import json
import src.scraper_utils as utils
import os


def main():
    LINK_SOS_FANTA = "https://sosfanta.calciomercato.com/category/chi-schierare/"
    PROBABILI_FORMAZIONI = "https://sosfanta.calciomercato.com/probabili-formazioni/"
    LINK_FANTACALCIO_IT = "https://www.fantacalcio.it/squadre/"

    # lista_giocatori (è un dizionario vuoto)
    data = json.load(open(os.getcwd() + "/app/static/team.json")).get("players")

    # estraggo i dati comuni quali articoli e liste titolari
    contenuto_articoli = utils.estrazione_articoli_da_leggere(LINK_SOS_FANTA)
    liste_status = utils.estrazione_formazioni(PROBABILI_FORMAZIONI)

    # creo l'oggetto Player e inserisco tutte le informazioni
    players = dict((player, utils.Player(player, data.get(player))) for player in data)
    for player in players:
        t = players.get(player)
        t.scraper_notizie(contenuto_articoli)
        t.scraper_status_titolare(liste_status)
        t.scraper_voto()

    # salvo come dizionario
    dictio_finale = {p: players.get(p).__dict__ for p in players}

    # rinomino titoli colonne togliendo underscore e capitalizzando
    for key in dictio_finale:
        dictio_finale[key] = {
            k.replace("_", " ").upper(): v for k, v in dictio_finale[key].items()
        }

    with open(os.getcwd() + "/app/static/data_table.json", "w") as fp:
        json.dump(dictio_finale, fp)
    # print("Scaper Eseguito")


if __name__ == "__main__":
    main()
