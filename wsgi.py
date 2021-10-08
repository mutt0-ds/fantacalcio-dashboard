from app.main import app
from src import scraper
from flask_apscheduler import APScheduler

# initialize scheduler
scheduler = APScheduler()
scheduler.api_enabled = True
scheduler.init_app(app)
scheduler.start()

# interval example
@scheduler.task('interval', id='check', seconds=30, misfire_grace_time=900)
def job1():
    print('Job 1 executed')
    
if __name__ == '__main__':
    app.run(port= 8000, debug=True)