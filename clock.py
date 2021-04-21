from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()
from mainsite.models import Team



@sched.scheduled_job('interval', minutes=3)
def timed_job():
    t=Team.objects.all()
    t.update(test_t1=3)
    t.update(test_t2=3)
    t.update(test_t3=3)
    t.update(test_t4=3)

@sched.scheduled_job('cron', day_of_week='mon-fri', hour=17)
def scheduled_job():
    print('This job is run every weekday at 5pm.')

sched.start()