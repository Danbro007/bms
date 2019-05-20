from apscheduler.schedulers.background import BackgroundScheduler


def job():
    print("111111111111")


sched = BackgroundScheduler()

sched.add_job(job, "interval", seconds=3, start_date="2019-03-08 14:43:00", end_date="2019-03-08 14:44:00")
sched.start()
while True:
    pass
