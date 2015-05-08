__author__ = 'Tual'
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pdb
import traceback

driver = webdriver.Firefox()
driver.get("http://disqus.com/embed/comments/?base=default&version=866b57a6cbb5f3ab2a4b4f4578d489f6&f=dlisted1&t_i=177027 http://dlisted.com/?p=177027&t_u=http://dlisted.com/2015/05/07/blake-lively-is-the-latest-mumbly-actress-to-join-woody-allens-next-film/")
        #myDynamicElement = driver.xpath("//ul[@id=post-list]/li[@class=post]/p")
try:
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "post-list"))
    )
    pdb.set_trace()
finally:
    driver.quit()