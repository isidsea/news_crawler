from urllib.parse import urlparse

class NetworkTools:
	def __init__(self):
		pass

	@classmethod
	def full_url(self, url=None):
		assert url is not None, "url is not defined"

		if "http://" not in url or "https://" not in url:
			url = "http://%s" % url
		return url

	@classmethod
	def get_domain(self, url=None):
		assert url is not None, "url is not defined."
		parsed_uri = urlparse(url)
		domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
		return domain