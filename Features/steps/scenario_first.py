import shutil

from behave import *
import time
from datetime import datetime
from selenium.common.exceptions import *
from PIL import ImageGrab
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
import zipfile


@when("Считать имя канала из текстового файла channel_name.txt")
def step_impl(context):
    with open(os.path.abspath("channel_name.txt"), "r") as channel_name_file:
        context.channel_name = channel_name_file.readline()


@step("Зайти на этот канал на твиче")
def step_impl(context):
    context.driver.get("http:\\twitch.tv\\" + context.channel_name)


@step("Сделать полноэкранный режим")
def step_impl(context):
    context.driver.maximize_window()


@then('Просмотреть стрим "{second}" секунд, в случае ошибки, сделать скриншот браузера')
def step_impl(context, second):
    try:
        try:
            but_play = context.driver.find_element_by_xpath('//*[@class="player-button qa-pause-play-button"]').click()
        except WebDriverException:
            but_play = context.driver.find_element_by_xpath('//*[@class="player-content-button js-player-matur'
                                                            'e-accept js-mature-accept-label"]').click()
    except NoSuchElementException:
        screen = ImageGrab.grab()
        screen.save("Screenshots\\not_find_a_channel.jpg")
        skip_scenario(context)
    time.sleep(int(second))


@then('Перейти на вкладку "{tab_name}"')
def step_impl(context, tab_name):
    need_tab = context.driver.find_element_by_xpath((('//*[@class="tw-font-size-5" and contains(text(), '
                                                      '"{}")]').format(tab_name))).click()


@then('Просмотреть содержимое вкладки "{tab_name}" в течении "{second}" секунд и сделать скриншот')
def step_impl(context, second, tab_name):
    time.sleep(int(second))
    screen = ImageGrab.grab()
    screen.save("Screenshots\\Вкладка {}.jpg".format(tab_name))


@step('Записать в логи результат')
def step_impl(context):
    with open(os.path.abspath("log.txt"), "a") as log:
        log.write("{0} Сценарий выполнен.\n".format(datetime.now()))


def skip_scenario(context):
    with open(os.path.abspath("log.txt"), "a") as log:
        log.write("{0} Сценарий не выполнен.\n".format(datetime.now()))
        context.scenario.skip(require_not_executed=True)


@then("Отправить скриншоты по почте")
def step_impl(context):
    zip(".\\Screenshots", "Screenshots.zip")
    send_email(".\\Screenshots.zip")

def zip(path, name):
    screenshots_zip = zipfile.ZipFile(name, "w")
    for folder, subfolders, files in os.walk(path):
        for file in files:
            if file.endswith('.jpg'):
                screenshots_zip.write(os.path.join(folder, file),
                                  os.path.relpath(os.path.join(folder, file), path),
                                  compress_type=zipfile.ZIP_DEFLATED)
    screenshots_zip.close()

def send_email(path):
    msg = MIMEMultipart()
    msg['Subject'] = 'subject'
    msg['From'] = 'youremail'
    msg['To'] = 'toemail'
    text = MIMEText("text{}".format(datetime.now()))
    msg.attach(text)
    part = MIMEApplication(open(path, 'rb').read())
    part.add_header('Content-Disposition', 'attachment', filename=path)
    msg.attach(part)
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login(youremail, yourpassword)
    s.sendmail('youremail', 'toemail', msg.as_string())
    s.quit()


@then("Удалить скриншоты после отправки")
def step_impl(context):
    shutil.rmtree(".\\Screenshots\\")
    os.remove(".\\Screenshots.zip")
