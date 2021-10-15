from app.main import app
from src import scraper
from flask_apscheduler import APScheduler

# initialize scheduler
scheduler = APScheduler()
scheduler.api_enabled = True
scheduler.init_app(app)
scheduler.start()

# refresh dello scraper ogni ora
@scheduler.task("interval", id="refresh_dati", seconds=20, misfire_grace_time=900)
def refresh_dati():
    print("Aggiorno i dati...")
    scraper.main()
    print("Scraper aggiornato.")


if __name__ == "__main__":
    app.run(port=8000, debug=True)
