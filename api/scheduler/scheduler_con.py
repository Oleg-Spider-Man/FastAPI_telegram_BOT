from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.schedulers.background import BackgroundScheduler

# redis_url = "redis://127.0.0.1:6379/"
#
# jobstores = {
#      'default': RedisJobStore(host='127.0.0.1', port=6379)
#  }
# #
#
# executors = {
#     'default': ThreadPoolExecutor(20),
#     'processpool': ProcessPoolExecutor(5)
# }
# job_defaults = {
#     'coalesce': False,
#     'max_instances': 3,
#     'misfire_grace_time': 600
# }

#scheduler = BackgroundScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults)
scheduler = AsyncIOScheduler()
scheduler.start()


