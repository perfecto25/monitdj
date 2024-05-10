
from loguru import logger
from django.utils import timezone
import datetime
from .models import Service, Host
import threading
import time 
#from huey.contrib.djhuey import periodic_task, db_periodic_task

#from huey.contrib import djhuey as huey
#from huey import MemoryHuey, crontab

#huey = MemoryHuey(immediate=True)

#@huey.periodic_task(crontab(minute="*/1"))
def check_service_active():
    def run_check():
        # code for the background job goes here
        logger.info("running background task to remove stale Service records")
        last_min = timezone.now() - datetime.timedelta(seconds=60)
        services = Service.objects.filter(last_checkin__lt=last_min)
        services.delete()
        Host.objects.filter(last_checkin__lt=last_min).update(active=False)
        time.sleep(60)
    thread = threading.Thread(target=run_check, daemon=True)
    thread.start()