from .news         import News
from .news.article import Article
import glob
import os
import importlib
import shutil

class Builder:
	def __init__(self):
		pass

	@classmethod
	def build(self):
		print("[build][debug] Making folders...")
		build_folder    = os.path.join(os.getcwd(),"build")
		crawlers_folder = os.path.join(build_folder, "crawlers")
		lib_folder      = os.path.join(build_folder, "lib")
		if os.path.isdir(build_folder): shutil.rmtree(build_folder)
		os.mkdir(build_folder)
		os.mkdir(crawlers_folder)
		os.mkdir(lib_folder)

		print("[build][debug] Copying files...")
		lib_folder = os.path.join(os.getcwd(), "lib")
		shutil.copy(os.path.join(os.getcwd(),"run.py"), os.path.join(build_folder,"run.py"))
		shutil.copy(os.path.join(lib_folder,"network_tools.py"), os.path.join(build_folder,"lib","network_tools.py"))
		shutil.copy(os.path.join(lib_folder,"database.py"), os.path.join(build_folder,"lib","database.py"))
		shutil.copy(os.path.join(lib_folder,"exceptions.py"), os.path.join(build_folder,"lib","exceptions.py"))
		shutil.copy(os.path.join(lib_folder,"proxy_switcher.py"), os.path.join(build_folder,"lib","proxy_switcher.py"))
		shutil.copy(os.path.join(lib_folder,"logging.py"), os.path.join(build_folder,"lib","logging.py"))
		shutil.copy(os.path.join(lib_folder,"tools.py"), os.path.join(build_folder,"lib","tools.py"))
		shutil.copytree(os.path.join(os.getcwd(),"config"), os.path.join(build_folder,"config"))
		shutil.copytree(os.path.join(lib_folder,"cleanser"), os.path.join(build_folder,"lib","cleanser"))
		shutil.copytree(os.path.join(lib_folder,"config"), os.path.join(build_folder,"lib","config"))
		shutil.copytree(os.path.join(lib_folder,"converter_engine"), os.path.join(build_folder,"lib","converter_engine"))
		shutil.copytree(os.path.join(lib_folder,"news"), os.path.join(build_folder,"lib","news"))
		shutil.copytree(os.path.join(lib_folder,"parser"), os.path.join(build_folder,"lib","parser"))
		shutil.copytree(os.path.join(lib_folder,"validator"), os.path.join(build_folder,"lib","validator"))


		for file_name in glob.iglob(os.path.join(os.getcwd(),"src","*.py")):
			file_name = file_name.replace(os.getcwd(), "")
			file_name = file_name.replace("src","")
			file_name = file_name.replace(".py","")
			file_name = file_name.replace("/","")
			module    = importlib.import_module("src.%s" % file_name)
			module    = module.Crawler()

			for index, category_link in enumerate(module.CATEGORY_LINKS):
				news = News(
					          url = category_link,
					article_xpath = module.ARTICLE_XPATH,
					      country = module.COUNTRY
				)
				article = Article(
					       content_xpath = module.CONTENT_XPATH,
					published_date_xpath = module.PUBLISHED_DATE_XPATH,
					   author_name_xpath = module.AUTHOR_NAME_XPATH,
					         title_xpath = module.TITLE_XPATH
				)
				template_file = open(module.TEMPLATE,"r")
				template      = template_file.read()
				template      = template.format(
					crawler_name = module.CRAWLER_NAME,
					        news = news,
					     article = article
				)
				file_name     = "%s_%s.py" % (module.CRAWLER_NAME, index)
				file_name     = file_name.replace(" ","_")
				template_file = open(os.path.join(build_folder,"crawlers",file_name), "w")
				template_file.write(template)
				template_file.flush()
				template_file.close()