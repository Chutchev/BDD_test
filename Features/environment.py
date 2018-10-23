import behave
import os
from selenium import webdriver

def before_all(context):
    context.driver = webdriver.Chrome(os.path.abspath("chromedriver.exe"))
    dirs = os.listdir()
    create = True
    for index in range(len(dirs)):
        if dirs[index] == "Screenshots":
            create == False
            return
    if create == True:
        os.makedirs("\\Screenshots\\")
