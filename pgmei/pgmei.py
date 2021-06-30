from flask import request, send_from_directory #import main Flask class and request object
import re
import os
import shutil
from selenium import webdriver
import time
import chromedriver_binary
from dotenv import load_dotenv
from datetime import datetime, date
load_dotenv()

def create_browser():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.getenv('GOOGLE_CHROME_BIN') #export GOOGLE_CHROME_BIN='/usr/bin/google-chrome'
    chrome_options.add_argument('--headless')
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox") #bypass OS security model
    chrome_options.add_argument("--disable-dev-shm-usage") #overcome limited resource problems
    #chrome_options.add_argument("--shm-size=1024m")
    
    
    chrome_options.add_experimental_option("prefs", {
      "download.default_directory": os.path.abspath(os.path.curdir)+"/downloads",
      "download.directory_upgrade": True,
      "safebrowsing.enabled": True
    })
    browser = webdriver.Chrome(chrome_options=chrome_options)
    print("Done Creating Browser")
    return browser
    
def check_invoice():
    try:
        shutil.rmtree(os.path.abspath(os.path.curdir)+"/downloads/")
    except:
       ...
    os.mkdir(os.path.abspath(os.path.curdir)+"/downloads/")
    cnpj = os.getenv('CNPJ')
    url='http://www8.receita.fazenda.gov.br/SimplesNacional/Aplicacoes/ATSPO/pgmei.app/Identificacao'
    browser = create_browser()
    browser.set_window_size(1440,900)
    browser.get(url)
    time.sleep(3)
    cnpj_field = browser.find_element_by_id('cnpj')
    cnpj_field.send_keys(cnpj)
    continuar_button = browser.find_element_by_class_name('ladda-label')
    continuar_button.click()
    time.sleep(1)
    emissao_url = 'http://www8.receita.fazenda.gov.br/SimplesNacional/Aplicacoes/ATSPO/pgmei.app/emissao'
    browser.get(emissao_url)
    time.sleep(3)
    dropdown = browser.find_element_by_xpath('//button[@data-id="anoCalendarioSelect"]')
    dropdown.click()
    options = browser.find_elements_by_xpath('//a[@role="option"]')
    now = datetime.now()
    year = now.year
    for option in options:
        if(str(year) == option.text):
            year_option = option
    try:
        year_option.click()
    except:
        raise "Ano atual não encontrado"
    
    buttons = browser.find_elements_by_class_name('ladda-label')
    for button in buttons:
        print(button.text)
        if 'OK' in button.text.upper():
            ok_button = button
    try:
        ok_button.click()
    except:
        raise "Botão OK não encontrado"
    time.sleep(1)
    table = browser.find_element_by_tag_name('tbody')
    rows = table.find_elements_by_xpath('//tr[@class]')
    [check_outdated(row) for row in rows]
    time.sleep(3)
    browser.save_screenshot('print1.png')
    return "A"
def check_outdated(month_element):
    outdate = month_element.find_element_by_class_name('vencimento').text
    if(len(outdate)>5):
        paid = month_element.find_elements_by_class_name('text-center')[1].text
        if("Não" in paid):
            now = datetime.now()
            split_date = str(outdate).split('/')
            formated_date = date(int(split_date[2]), int(split_date[1]), int(split_date[0]))
            diff = formated_date-now.date
            print(diff)
            print(outdate)
            print(paid)