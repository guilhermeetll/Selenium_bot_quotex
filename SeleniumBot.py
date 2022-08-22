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
    print('\nNavegador carregado')
    return navegador


#Muda para o modo de Demo, tirando da conta real
def muda_para_conta_demo(navegador):
    try: #Espera pagina carregar
        WebDriverWait(navegador, 30).until(EC.presence_of_element_located((By.XPATH, espera_broker_carregar)))
    except: #Caso nao carregue em 30s
        muda_para_conta_demo(navegador)
    finally: #Quando carrega muda a conta
        navegador.find_element(By.XPATH, menu_conta_demo).click()
        navegador.find_element(By.XPATH, botao_conta_demo).click()
        print('Conta demo ativada')


#Navega ate a sala de sinais
def clica_sala_de_sinais(navegador):
    navegador.find_element(By.XPATH, sala_de_sinais).click()
    print('Sala de sinais ativada')


#Clica no ativo que apareceu o sinal
def primeiro_sinal(navegador):
    try:
        ativo = WebDriverWait(navegador, 9999999).until(EC.presence_of_element_located((By.XPATH, seleciona_sinal)))
    finally:
        navegador.find_element(By.XPATH, seleciona_sinal).click()
    sleep(0.2)
    print('Primeira negociacao lida')
    return ativo


#Roda o Robo
def le_sinal_e_executa(navegador, ativo):
    print('Operando')
    ativoProx = ativo
    num_operacoes = 0
    while (num_operacoes <= num_max_operacoes):
        try:
            try:
                WebDriverWait(navegador, 9999999).until(EC.presence_of_element_located((By.XPATH, seleciona_sinal)))
                sleep(0.5)
                ativo = navegador.find_element(By.XPATH, seleciona_sinal).text
            except:
                pass
            if ativoProx != ativo: #Compara se o ativo mudou
                ativoProx = ativo  #Atribui o novo ativo para o proximo
                navegador.find_element(By.XPATH, seleciona_sinal).click() #Seleciona esse novo ativo
                try: #Verifica se o sinal foi de compra
                    navegador.find_element(By.XPATH, le_sinal_compra)
                    navegador.find_element(By.XPATH, botao_compra).click()
                except: #Se o sinal de compra não for encontrado retornará um ERRO fazendo assim o sinal de venda executar
                    navegador.find_element(By.XPATH, botao_venda).click() #Sinal de venda
                num_operacoes += 1
        except:
            pass

def main():
    navegador = login_quotex()
    muda_para_conta_demo(navegador)
    clica_sala_de_sinais(navegador)
    ativo = primeiro_sinal(navegador)
    le_sinal_e_executa(navegador, ativo)
    
main()