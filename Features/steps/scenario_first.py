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


@then('Перейти на вкладку "{tab_name}"')
def step_impl(context, tab_name):
    need_tab = context.driver.find_element_by_xpath((('//*[@class="tw-font-size-5" and contains(text(), '
                                                      '"{}")]').format(tab_name))).click()

@step('Записать в логи результат')
def step_impl(context):
    with open(os.path.abspath("log.txt"), "a") as log:
        log.write("{0} Канал существует.\n".format(datetime.now()))


def skip_scenario(context):
    with open(os.path.abspath("log.txt"), "a") as log:
        log.write("{0} Канал не существует. Пропуск сценария.\n".format(datetime.now()))
        context.scenario.skip(require_not_executed=True)

def zip(path, name):
    screenshots_zip = zipfile.ZipFile(name, "w")
    for folder, subfolders, files in os.walk(path):
        for file in files:
            if file.endswith('.jpg'):
                screenshots_zip.write(os.path.join(folder, file),
                                  os.path.relpath(os.path.join(folder, file), path),
                                  compress_type=zipfile.ZIP_DEFLATED)
    screenshots_zip.close()

def send_email(path, mailto):
    msg = MIMEMultipart()
    msg['Subject'] = 'Отчет по тесту'
    msg['From'] = 'testPythonIVT@gmail.com'
    msg['To'] = mailto
    text = MIMEText("Отчет по тесту от {}".format(datetime.now()))
    msg.attach(text)
    part = MIMEApplication(open(path, 'rb').read())
    part.add_header('Content-Disposition', 'attachment', filename=path)
    msg.attach(part)
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login('testPythonIVT@gmail.com', 'testtset12')
    s.sendmail('testPythonIVT@gmail.com', mailto, msg.as_string())
    s.quit()

@when('Зашли на канал твича считанный с  файла "{filename}"')
def step_impl(context, filename):
    with open(os.path.abspath(f"{filename}"), "r") as channel_name_file:
        context.channel_name = channel_name_file.readline()
    context.driver.get("http:\\twitch.tv\\" + context.channel_name)


@step('Подождать "{second}" секунды  и сделать скриншот')
def step_impl(context, second):
    screen = ImageGrab.grab()
    time_now = str(datetime.now()).replace(" ", ' время').replace(":",  " ")
    time_now = time_now[:len(time_now)-7]
    screen.save(os.path.realpath(".\\Screenshots\\"+time_now+".jpg"))
    time.sleep(int(second))


@then('Отправить файлы на почту "{mailto}"')
def step_impl(context, mailto):
    zip(".\\Screenshots", "Screenshots.zip")
    send_email(os.path.realpath(".\\Screenshots.zip"), mailto)

def click_button_play(context):
    try:
        but_play = context.driver.find_element_by_xpath('//*[@class="player-button qa-pause-play-button"]').click()
    except WebDriverException:
        but_play = context.driver.find_element_by_xpath('//*[@class="player-content-button js-player-matur'
                                                        'e-accept js-mature-accept-label"]').click()


@then("Нажать на кнопку Play")
def step_impl(context):
    try:
        click_button_play(context)
    except NoSuchElementException:
        screen = ImageGrab.grab()
        screen.save("Screenshots\\not_find_a_channel.jpg")
        skip_scenario(context)
