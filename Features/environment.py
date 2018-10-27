import behave
import shutil
import os
from selenium import webdriver

def before_all(context):
    if os.path.exists(os.path.abspath(".\\Screenshots")):
        shutil.rmtree(os.path.abspath(".\\Screenshots"))
    else:
        os.makedirs(".\\Screenshots\\")
    context.driver = webdriver.Chrome(os.path.abspath("chromedriver.exe"))
    context.driver.maximize_window()


def after_all(context):
    shutil.rmtree(os.path.abspath(".\\Screenshots"))
    os.remove(os.path.abspath(".\\Screenshots.zip"))


