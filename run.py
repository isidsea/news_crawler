from multiprocessing    import Pool, Process
from lib.config.factory import ConfigFactory
import os
import glob
import importlib
import time
import random

def execute_worker(crawler=None):
	assert crawler is not None, "crawler is not defined."
	crawler = importlib.import_module("crawlers.%s" % crawler)
	crawler = crawler.Crawler()
	crawler.crawl()
	time.sleep(random.randint(5,10))

def execute_section(crawler_names=None):
	assert crawler_names is not None, "crawlers is not defined."

	crawlers = []
	for name in crawler_names:
		name = name.replace(" ","_")
		for file_name in glob.iglob(os.path.join(os.getcwd(),"crawlers","%s_*.py" % name)):
			file_name = file_name.replace(os.getcwd(), "")
			file_name = file_name.replace("crawlers","")
			file_name = file_name.replace(".py","")
			file_name = file_name.replace("/","")
			crawlers.append(file_name)
	config  = ConfigFactory.get(ConfigFactory.RUN)
	workers = config.get("workers")
	with Pool(workers) as pool:
		pool.map(execute_worker, crawlers)
	time.sleep(random.randint(60,120))

if __name__ == "__main__":
	config = ConfigFactory.get(ConfigFactory.RUN)
	while True:
		workers = list()
		for key,value in config.get("section").items():
			worker = Process(target=execute_section, args=(value,), daemon=False)
			workers.append(worker)
		for worker in workers:
			worker.start()
		for worker in workers:
			worker.join()
		sleep = random.randint(60,360)
		print("=" * 100)
		print("SLEEPING (%ss)" % sleep)
		print("=" * 100)
		time.sleep(sleep)

# from lib.config.factory import ConfigFactory
# from lib.news        	import News
# from lib.news        	import Engine
# from multiprocessing 	import Pool

# def execute_worker(news=None):
# 	assert news  is not None, "news is not defined."
# 	assert "url" in news    , "url is not defined."

# 	engine = Engine()
# 	engine.crawl(News(url=news["url"], country=news["country"]))

# if __name__ == "__main__":
# 	active_news = News.get_active()
# 	active_news = list(active_news)

# 	run_config = ConfigFactory.get(ConfigFactory.RUN)
# 	workers    = run_config.get("workers")

# 	with Pool(workers) as pool:
# 		pool.map(execute_worker, active_news)