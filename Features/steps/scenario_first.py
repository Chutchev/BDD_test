from behave import *
from selenium import webdriver
import time
from datetime import datetime
from selenium.common.exceptions import *
import os
from PIL import ImageGrab


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
