from behave import *
from selenium import webdriver
import time
from datetime import datetime
from selenium.common.exceptions import *
import os


@when("Считать имя канала из текстового файла channel_name.txt")
def step_impl(context):
    with open(os.path.realpath("channel_name.txt"), "r") as channel_name_file:
        context.channel_name = channel_name_file.readline()


@step("Зайти на этот канал на твиче")
def step_impl(context):
    context.driver = webdriver.Chrome(os.path.realpath("chromedriver.exe"))
    context.driver.get("http:\\twitch.tv\\" + context.channel_name)


@step("Сделать полноэкрнный режим")
def step_impl(context):
    context.driver.maximize_window()


@then('Просмотреть стрим "{second}" секунд')
def step_impl(context, second):
    try:
        try:
            but_play = context.driver.find_element_by_xpath('//*[@class="player-button qa-pause-play-button"]').click()
        except WebDriverException:
            but_play = context.driver.find_element_by_xpath('//*[@class="player-content-button js-player-matur'
                                                        'e-accept js-mature-accept-label"]').click()
    except NoSuchElementException:
        skip_scenario(context, context.result)
    time.sleep(int(second))


@then('Перейти на вкладку "{tab_name}"')
def step_impl(context, tab_name):
    need_tab = context.driver.find_element_by_xpath((('//*[@class="tw-font-size-5" and contains(text(), '
                                                      '"{}")]').format(tab_name))).click()


@then('Просмотреть содержимое вкладки в течении "{second}" секунд')
def step_impl(context, second):
    time.sleep(int(second))


@step('Записать в логи результат')
def step_impl(context):
    with open(os.path.realpath("log.txt"), "a") as log:
        log.write("{0} Сценарий выполнен.\n".format(datetime.now()))


def skip_scenario(context, result):
    if result == "Неудачно":
        with open("C:\\Users\\Ivan\\PycharmProjects\\untitled3\\Features\\steps\\log.txt", "a") as log:
            log.write("{0} Сценарий не выполнен.\n".format(datetime.now()))
            context.scenario.skip(require_not_executed=True)
