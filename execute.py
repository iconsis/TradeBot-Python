#========================================
# Scheduler Jobs
#========================================

from apscheduler.schedulers.background import BackgroundScheduler

# jobs
from strategies.ema_5 import ema_5_strategy, ema_5_strategy_v1, ema_5_strategy_v2

config = {
    "day_of_job": "mon-fri",
    "hour": "09",
    "minute": "15"
}

scheduler = BackgroundScheduler()
scheduler.add_job(
    ema_5_strategy_v2.main,
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
