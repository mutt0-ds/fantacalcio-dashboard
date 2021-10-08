from app.main import app
from src import scraper
import os

if __name__ == '__main__':
    # scraper.main()
    app.run(port= 8000, debug=True)