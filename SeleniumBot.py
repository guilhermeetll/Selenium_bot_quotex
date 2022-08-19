from distutils.spawn import find_executable
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from time import time


#Abre o navegador e Faz login
servico = Service(ChromeDriverManager().install())
navegador = webdriver.Chrome(service=servico)
navegador.get('https://qxbroker.com/pt/sign-in/')
navegador.find_element(By.XPATH, '//*[@id="tab-1"]/form/div[1]/input').send_keys('AprendizSelenium@gmail.com')
navegador.find_element(By.XPATH, '//*[@id="tab-1"]/form/div[2]/input').send_keys('AprendizSelenium963741')
navegador.find_element(By.XPATH, '//*[@id="tab-1"]/form/button').click()
##############################

#Muda para o modo de Demo, tirando da conta real
try:
    WebDriverWait(navegador, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div[1]/header/div[8]/div[2]/div')))
finally:
    navegador.find_element(By.XPATH, '//*[@id="root"]/div/div[1]/header/div[8]/div[2]/div').click()
##############################

#Navega ate a sala de sinais
navegador.find_element(By.XPATH, '//*[@id="root"]/div/div[1]/header/div[8]/div[2]/div[2]/ul[1]/li[3]/a').click()
navegador.find_element(By.XPATH, '//*[@id="root"]/div/aside[1]/nav/button[3]').click()
##############################

#Clica no ativo que apareceu o sinal
try:
    ativo1 = WebDriverWait(navegador, 9999999).until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/aside[2]/div[2]/div[3]/div/div[1]')))
finally:
    sleep(0.8)
    navegador.find_element(By.XPATH, '//*[@id="root"]/div/aside[2]/div[2]/div[3]/div/div[1]/div[1]/div').click()
####################################

sleep(0.2)
ativo = ativo1
ativoProx = ativo
tempoAEsperar= 200000
start = time()
while (time()-start < tempoAEsperar):
    try:
        ativo = navegador.find_element(By.XPATH, '//*[@id="root"]/div/aside[2]/div[2]/div[3]/div/div[1]/div[1]/div').text
        if ativoProx != ativo:
            ativoProx = ativo
            navegador.find_element(By.XPATH, '//*[@id="root"]/div/aside[2]/div[2]/div[3]/div/div[1]/div[1]/div').click()
            try:
                navegador.find_element(By.XPATH, '//*[@id="root"]/div/aside[2]/div[2]/div[3]/div/div[1]/div[1]/*[@class="icon-arrow-up-circle panel-trading-signals__circle--up"]')
                navegador.find_element(By.XPATH, '//*[@id="root"]/div/div[1]/main/div[2]/div[1]/div/div[6]/div[1]/button').click()
            except:
                navegador.find_element(By.XPATH, '//*[@id="root"]/div/div[1]/main/div[2]/div[1]/div/div[6]/div[4]/button').click()
    except:
        sleep(0.1)