import code_scraping
from django_cron import CronJobBase, Schedule

class MyCronJob(CronJobBase):
	RUN_EVERY_MINS=120

	schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
	code = 'predictions.my_cron_job'
	
	def do(self):
		code_scraping.scrapping_main()