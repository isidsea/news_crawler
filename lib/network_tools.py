from urllib.parse 	 import urlparse
from .proxy_switcher import ProxySwitcher
from .exceptions     import NetworkError
from lxml 			 import html
import requests
import socket
import lxml

class NetworkTools:
	def __init__(self):
		pass

	@classmethod
	def full_url(self, domain=None, url=None):
		assert url    is not None, "url is not defined"
		assert domain is not None, "domain is not defined."

		if "http://" not in url and "https://" not in url:
			if url[0] == "/":
				url = url[1:]
			domain = NetworkTools.get_domain(domain, with_scheme=True)
			url    = "%s%s" % (domain, url)
		return url

	@classmethod
	def get_domain(self, url=None, with_scheme=True):
		assert url is not None, "url is not defined."
		parsed_uri = urlparse(url)
		if with_scheme:
			domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
		else:
			domain = "{uri.netloc}".format(uri=parsed_uri)
		return domain

	@classmethod
	def parse(self,url=None, parse=True, use_proxy=False):
		""" This function will help to get web source code as HTML document.
			After getting the source code, the function will later decide wheter it will parse to
			HTML Object or leave it as a string. 

			Parse function will automatically failed if face errors for more than 5 errors. 
			Even if the parse failed, the function will return a HTML Object.
			However, the HTML Object will be blank.

			Parameters details:
			- url   : a url to be parse
			- parse : if you speciy parse, means parse to html object using html.fromstring function

			Return details:
			- _html : This variable can be a string or html object. 
		"""
		assert url is not None, "url is not defined."

		proxy_is_ok = False
		_html       = None
		tried  		= 0
		max_try 	= 2
		while not proxy_is_ok and tried < max_try:
			try:
				assert url is not None, "URL is not defined."
				tried = tried + 1
				
				headers = {"user-agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"}
				if use_proxy:
					# print("[networktools][debug] Using Proxy.")
					switcher = ProxySwitcher()
					page     = requests.get(url, proxies=switcher.get_proxy(), timeout=60, headers=headers)
				else:
					# print("[networktools][debug] Direct Connection.")
					page = requests.get(url, timeout=60,  headers=headers)
				if "404 Not Found" in str(page.content):
					raise PageNotFound("404 Not Found (content).")
				if "Location: 404" in str(page.content):
					raise PageNotFound("404 Not Found (content).")
				# Cannot trust status_code because some of the forum return wrong status code
				# if page.status_code == 404:					
				# 	raise PageNotFound("404 Not Found (status).")
				data        = page.content.decode(page.encoding, "ignore")
				_html       = html.fromstring(data) if parse else data
				proxy_is_ok = True
			except requests.exceptions.ProxyError as proxy_error:
				print("[networktools][error] Ops! Proxy is not working. Try again...")
				proxy_is_ok = False
			except requests.exceptions.RequestException as another_requests_error: 
				print("[networktools][error] Ops! Something wrong. Try again...")
				proxy_is_ok = False
			except socket.timeout:
				print("[networktools][error] Ops! Request Time Out")
				proxy_is_ok = False
			except lxml.etree.XMLSyntaxError:
				print("[networktools][error] Ops! Something wrong. Leave it~")
				_html       = html.fromstring("<html><head></head><body></body></html>") if parse else "<html></html>"
				proxy_is_ok = True
			except PageNotFound as page_not_found:
				print("[networktools][error] %s" % page_not_found)
				_html       = html.fromstring("<html><head></head><body></body></html>") if parse else "<html></html>"
				proxy_is_ok = True 
			except:
				raise
		# proxy_is_ok == False only when max_tried exceed.
		if proxy_is_ok == False:
			raise NetworkError("Cannot open the URL given.")
			_html = html.fromstring("<<html><head></head><body></body></html>") if parse else "<html></html>"
		return _html