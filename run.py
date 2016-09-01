from lib.config.factory import ConfigFactory
from lib.news        	import News
from lib.news        	import Engine
from multiprocessing 	import Pool

def execute_worker(news=None):
	assert news  is not None, "news is not defined."
	assert "url" in news    , "url is not defined."

	engine = Engine()
	engine.crawl(News(url=news["url"], country=news["country"]))

if __name__ == "__main__":
	active_news = News.get_active()
	active_news = list(active_news)

	run_config = ConfigFactory.get(ConfigFactory.RUN)
	workers    = run_config.get("workers")

	with Pool(workers) as pool:
		pool.map(execute_worker, active_news)

