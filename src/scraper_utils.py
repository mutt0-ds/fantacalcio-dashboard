from bs4 import BeautifulSoup
import requests
import dateparser
from datetime import timedelta, datetime
import re
from dataclasses import dataclass, field
import json

@dataclass
class Player:
    """classe di un calciatore"""
    name: str                                            #nome del giocatore
    team: str                                            #squadra
    ruolo: str =""                                       #ruolo: P,D,C,A
    news: str =""                                        #totale menzioni da sos_fanta
    titolare: str =""                                    #status titolare
    dati: str = ""                                       #gol e assist
    media_voto: float = 0.0                              #media voto
    media_fantavoto: float = 0.0                         #media fantavoto con bonus e malus
    scheda_giocatore: str=""                             #link a fantacalcio.it del giocatore

    #utils
    LINK_SOS_FANTA="https://sosfanta.calciomercato.com/category/chi-schierare/"
    PROBABILI_FORMAZIONI="https://sosfanta.calciomercato.com/probabili-formazioni/"
    LINK_FANTACALCIO_IT = "https://www.fantacalcio.it/squadre/"

    def to_json(self, path):
        """salva in JSON i dati"""
        with open(path, "w") as dump:
            json.dump(self.__dict__, dump)

    def scraper_voto(self):
        """devo collegarmi al link della rosa su fantacalcio.it e trovare il link corrispondente al giocatore
        da li poi estraggo voto e fantavoto di media"""
        
        soup_rosa = BeautifulSoup(requests.get(f"{self.LINK_FANTACALCIO_IT}/{self.team}#rosa").text, 'html.parser')
        print(self.name)
        displayed_name = self.name
        if displayed_name == "Coulibaly": #caso estremo, il sito si confonde
            displayed_name = "Coulibaly M."
            
        link = soup_rosa.find("a", text=displayed_name.upper())["href"]
        
        #trovo il link personale del giocatore e glielo assegno
        self.scheda_giocatore = link

        #leggo voto e media voto
        soup = BeautifulSoup(requests.get(link).text, 'html.parser')

        self.media_voto = float(soup.find_all(class_="nbig2")[0].text.replace(",","."))
        self.media_fantavoto = float(soup.find_all(class_="nbig2")[1].text.replace(",","."))

        #leggo anche il ruolodalla schedina delle info
        infos = soup.find_all(class_="col-lg-6 col-md-6 col-sm-12 col-xs-12")[-2]
        self.ruolo = str(infos.find("span").text)

        #compilo i dati: partite, gol e assist 
        dati_partite = soup.find_all(class_="nbig")
        
        partite = "🥅 "+dati_partite[0].text
        #i portieri hanno statistiche diverse!
        if self.ruolo == "P":
            goal = "❌ "+dati_partite[1].text
            self.dati = "<br>".join([partite, goal])
        else:
            goal = "⚽ "+dati_partite[1].text
            assist = "👟 "+dati_partite[2].text
            self.dati = "<br>".join([partite, goal, assist])

        #aggiungo stellina al nome se hanno una bella media voto
        if self.media_fantavoto > 7:
            self.name +=" ⭐"

    def scraper_notizie(self,contenuto_articoli: list):
        """da una lista di testi di articoli da vedere estrae le menzioni del nome"""
        tot_menzioni = []
        for articolo in contenuto_articoli:
            #estraggo qualsisasi frase che menziona il giocatore
            sel_regex = f"[\w ,;()\'’-]+{self.name}[\w ,;()\'’-]+"
            results = re.findall(sel_regex, articolo)

            for res in results:
                #rimuovo il caso in cui sia solo in un elenco, come ad inizio articoli su ATTACCO
                if not re.search(f", {self.name},",res):
                    tot_menzioni.append(res)
        if len(tot_menzioni) > 0:
            self.news = "• "+"<br>•".join(tot_menzioni)


    def scraper_status_titolare(self,liste_status:list):
        """
        a partire dalle liste delle probabili formazioni,
         lo status (se gioca, è in ballottaggio, rotto, squalificato o fuori)
        """
        titolari, tabella_ballottaggi, tabella_squalificati, tabella_indisponibili,lista_scontri =liste_status

        if self.name in tabella_ballottaggi:
            #prima i ballottagi, essendo piu precisi
            regex_ballottagio = f"([\w -]*{self.name}[\w -]* [\d-]+)%"
            match = re.search(regex_ballottagio, tabella_ballottaggi)
            if match:
                #trovo posizione della strdel mio player e prendo la % corrispondente
                res = match.group(1)
                if res.startswith(self.name):
                    self.titolare = "❔ "+res[-5:-3]+"%"
                else:
                    self.titolare = "❔ "+res[-2:]+"%"

        elif self.name in titolari:
            self.titolare = "✅"

        elif self.name in tabella_squalificati:
            self.titolare = "🛑"

        elif self.name in tabella_indisponibili:
            self.titolare = "🤕"
        
        else: 
            self.titolare = "❌"

        #aggiungo la squadra avversaria del giocatore per la prossima giornata
        opponent = " VS "
        for match in lista_scontri:
            #se trova Juve nella stringa "JuveMilan" lo sostituisce con solo "Milan" e il totale sarà "VS Milan"
            if self.team in match:
                opponent += re.sub(self.team,"",match)
        self.titolare+=opponent
    
def scraper_lista_articoli(LINK_SOS_FANTA: str) -> list:
    """
    nella categoria "da schierare" vi sono 5-6 articoli da leggere
    seleziono quelli degli ultimi 4 giorni o rischio di confondermi con la giornata precedente
    return -> lista di link da aprire e leggere successivamente
    """
    soup = BeautifulSoup(requests.get(LINK_SOS_FANTA).text, 'html.parser')
    body = soup.find(class_="widget-content")
    titoli = body.find_all("li") #lista di tutti gli articoli

    to_scrape=[]
    for post in titoli:
        #parsing della data in italiano, devo pulirla
        data_pubblicazione = post.find(class_="post-meta").text.replace("del","").replace("alle","")
        parsed_data = dateparser.parse(data_pubblicazione, languages=["it"]) 

        #solo ultimi 3 giorni, se ne trovo uno vecchio esco dal loop
        if parsed_data < datetime.now()-timedelta(days=3):
            return to_scrape

        #aggiungo link
        link = post.find('a', href=True)
        to_scrape.append(link["href"])
    
        #caso post "a scheda": sono divisi in categorie, aggiungo link multipli
        post_multipli={"PORTIERI":3, "ATTACCO":8}
        for caso in post_multipli.keys():
            if caso in link["title"]:
                #la struttura della pagina sarà link/1/, link/2/ etc..
                for i in range(post_multipli.get(caso)):
                    to_scrape.append(link["href"]+f"{i}/")
    return to_scrape

def estrazione_articoli_da_leggere(LINK_SOS_FANTA: str):
    """estrae il testo da tutti i link degli ultimi 3 giorni di sosfanta. 
    Ritorna il testo di tutti gli articoli"""
    to_scrape = scraper_lista_articoli(LINK_SOS_FANTA)

    contenuto_articoli = []
    for link in to_scrape:
        soup = BeautifulSoup(requests.get(link).text, 'html.parser')
        content = soup.find_all(class_="entry-content")

        #se è un'errore o vuoto salto
        if len(content) ==0:
            continue
        
        #estraggo il testo rimuovendo gli errori di utf
        testo = content[0].text.replace("\xa0"," ")
        contenuto_articoli.append(testo)
    return contenuto_articoli

def estrazione_formazioni(PROBABILI_FORMAZIONI: str) -> list:
    """
    estrae 5 stringhe di dati riguardanti titolari, ballottaggi, squalifiche e infortuni e gli scontri in programma
    """
    soup = BeautifulSoup(requests.get(PROBABILI_FORMAZIONI).text, 'html.parser')

    #prima i titolari
    titolari = ",".join([x.text for x in soup.find_all(class_="match-players__row")])

    #ballottaggi, squalificati, indisponibili: molto spartano dato che è una lista senza id
    #devo prendere a 4 a 4 perchè è distribuita per squadra come ball, squal, indisp, diffidati
    tabelle =[x.text for x in soup.find_all(class_="match-info__list-item")]
    
    tabella_ballottaggi = ",".join([tabelle[x] for x in range(0, len(tabelle),4)])
    tabella_squalificati = ",".join([tabelle[x] for x in range(1, len(tabelle),4)])
    tabella_indisponibili = ",".join([tabelle[x] for x in range(2, len(tabelle),4)])
    
    #per finire estraggo gli scontri previsti e pulisco il dato (sarebbe tipo Genoa  Modulo 4-3-3 vs Juve Modulo 4-3-3 -> GenoaJuve)
    match = soup.find_all(class_="match-likely__team-names")
    lista_scontri = [re.sub("Modulo|VS|[ \n\d-]","",t.text) for t in match]

    return [titolari, tabella_ballottaggi, tabella_squalificati, tabella_indisponibili,lista_scontri]

  

# soup = BeautifulSoup(requests.get(PROBABILI_FORMAZIONI).text, 'html.parser')
# prima_data = soup.find_all(class_="match-likely__date")[-1]
