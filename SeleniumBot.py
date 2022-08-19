from distutils.spawn import find_executable
from xml.dom.minidom import Element
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from config import *
import dotenv
import os


#Abre o navegador e Faz login
def login_quotex():
    dotenv.load_dotenv(dotenv.find_dotenv())                               # email e senha
    email = os.getenv('email')
    senha = os.getenv('senha')
    servico = Service(ChromeDriverManager().install())                     # driver navegador
    navegador = webdriver.Chrome(service=servico)
    navegador.get(site)
    navegador.find_element(By.XPATH, campo_email_login).send_keys(email)   # preenche campo email
    navegador.find_element(By.XPATH, campo_senha_login).send_keys(senha)   # preenche campo senha
    navegador.find_element(By.XPATH, campo_login_botao).click()            # clica no botao de 'login'
    return navegador


#Muda para o modo de Demo, tirando da conta real
def muda_conta_demo(navegador):
    try:
        WebDriverWait(navegador, 30).until(EC.presence_of_element_located((By.XPATH, espera_broker_carregar)))
    except:
        muda_conta_demo(navegador)
    finally:
        navegador.find_element(By.XPATH, menu_conta_demo).click()
        navegador.find_element(By.XPATH, botao_conta_demo).click()


#Navega ate a sala de sinais
def clica_sala_de_sinais(navegador):
    navegador.find_element(By.XPATH, sala_de_sinais).click()


#Clica no ativo que apareceu o sinal
def primeiro_sinal(navegador):
    try:
        ativo = WebDriverWait(navegador, 9999999).until(EC.presence_of_element_located((By.XPATH, seleciona_sinal)))
    finally:
        navegador.find_element(By.XPATH, seleciona_sinal).click()
    sleep(0.2)
    return ativo


#Roda o Robo
def loop_execucao(navegador, ativo):
    ativoProx = ativo
    num_operacoes = 0
    while (num_operacoes < num_max_operacoes):
        try:
            WebDriverWait(navegador, 10).until(EC.presence_of_element_located((By.XPATH, seleciona_sinal)))
            ativo = navegador.find_element(By.XPATH, seleciona_sinal).text
            if ativoProx != ativo:
                ativoProx = ativo
                navegador.find_element(By.XPATH, seleciona_sinal).click()
                try:
                    navegador.find_element(By.XPATH, le_sinal_compra)
                    WebDriverWait(navegador, 10).until(EC.presence_of_element_located((By.XPATH, botao_compra)))
                    navegador.find_element(By.XPATH, botao_compra).click()
                except:
                    WebDriverWait(navegador, 10).until(EC.presence_of_element_located((By.XPATH, botao_venda)))
                    navegador.find_element(By.XPATH, botao_venda).click()
                num_operacoes += 1
        except:
            sleep(0.5)

def main():
    navegador = login_quotex()
    muda_conta_demo(navegador)
    clica_sala_de_sinais(navegador)
    ativo = primeiro_sinal(navegador)
    loop_execucao(navegador, ativo)
    
main()