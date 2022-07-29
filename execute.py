#========================================
# Scheduler Jobs
#========================================

from apscheduler.schedulers.background import BackgroundScheduler

import main

config = {
    "day_of_job": "mon-fri",
    "hour": "09",
    "minute": "15"
}

scheduler = BackgroundScheduler()
scheduler.add_job(
    main.main,
    "cron",
    day_of_week=config["day_of_job"],
    hour=config["hour"],
    minute=config["minute"]
)
try:
    scheduler.start()
except (KeyboardInterrupt, SystemExit):
    scheduler.shutdown()
#========================================
