from lxml import html
import requests
import ssl

ssl._create_default_https_context = ssl._create_unverified_context
selector = html.fromstring(requests.get('https://www.mzitu.com/', verify=False).content)

imgs = selector.xpath('//ul[@id="pins"]').child()

print(imgs)
