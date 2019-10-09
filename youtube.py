from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

driver = webdriver.Chrome('F:\python\duanzi\chromedriver.exe')
driver.get("https://www.youtube.com/results?search_query=3d+printer&pbjreload=10")

videoList = driver.find_element_by_id('contents').find_element_by_tag_name('ytd-video-renderer')

for


print(videoList)

# elem.send_keys("pycon")
# elem.send_keys(Keys.RETURN)
# assert "No results found." not in driver.page_source
# driver.close()