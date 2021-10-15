# ⚽ Fantacalcio Dashboard

In order to learn new tools such as Flask and Heroku, I created a **mobile-friendly dashboard for my own Fantacalcio *(Fantasy League?)* team**, which consists of 24 players from Serie A. 
Every week I have to select 11 names from my roster in order to simulate a soccer match against my friends, thus I need to read the suggestions from [SOS Fanta](https://sosfanta.calciomercato.com/), analyze ratings, chances of playing and several other informations before making my final choice. I was looking for a tool to support me in the operation.  

The Web App has an hourly scraper that extracts data of my 24 players *(inserted in app/static/team.json)* using Regex and [requests](https://docs.python-requests.org/en/latest/), then renders an HTML table on [Flask](https://flask.palletsprojects.com/en/2.0.x/) with:
- Any mention of the player's name from one of SOS Fanta articles
- Chance of being in the starting team of the upcoming match
- Number of matches played this year, goals and assists
- Average rating (Voto) and rating with Fantacalcio multipliers (Media Fantavoto)
- Link to additional data on [Fantacalcio.it](https://www.fantacalcio.it)

The Dashboard is publicly available at [https://fanta-dashboard.herokuapp.com/home](https://fanta-dashboard.herokuapp.com/home)

# Dashboard Example
![table](https://github.com/mutt0-ds/fantacalcio-dashboard/blob/master/media/tab.png)
