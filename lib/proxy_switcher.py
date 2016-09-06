from selenium import webdriver
from pymongo import MongoClient
from subprocess import call
import selenium
import random
import time
import arrow

class ProxySwitcher(object):
	def get_proxy(self):
		db = MongoClient("mongodb://mongo:27017/proxies")
		db = db.proxies

		success = False
		while not success:
			# wait until proxy crawler is running
			proxies = [doc for doc in db.data.find()]
			if len(proxies) > 0: 
				document = proxies[random.randint(0,len(proxies)-1)]
				success  = True
		return {"http":"http://{}:{}".format(document["ip"], document["port"])}		
	#end def
#end class

class ProxyCrawler(object):
	def crawl(self):
		# connect to database
		db = MongoClient("mongodb://mongo:27017/proxies")
		db = db.proxies
		db.data.update_many({},{"$set":{"new":False}})

		success = False
		while not success:
			try:
				driver = webdriver.PhantomJS(executable_path="/usr/local/bin/phantomjs")
				driver.set_window_size(1366, 768)
				driver.set_page_load_timeout(random.randint(5,20))

				driver.get("http://proxylist.hidemyass.com/search-1301708#listable")
				proxies = driver.find_elements_by_xpath("//table/tbody//tr")

				for proxy in proxies[0:10]:
					proxy    = proxy.find_elements_by_xpath(".//td")
					document = dict(
								         ip = proxy[1].text,
								       port = proxy[2].text,
								    country = proxy[3].text,
								insert_date = arrow.utcnow().datetime,
								        new = True
							)
					db.data.insert_one(document)
				#end for
				db.data.remove({"new":False})
				driver.close()
				driver.quit()
				success = True
			except selenium.common.exceptions.TimeoutException as timeout:
				driver.close()
				driver.quit()
				print("[proxy_switcher][error] Ops! Proxy need to be refreshed!")
				time.sleep(random.randint(5,60))
			#end try
		#end while
	#end def
#end class