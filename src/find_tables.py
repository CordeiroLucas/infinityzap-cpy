from collections.abc import Hashable

from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

from io import StringIO
import pandas as pd
from settings import *
from components.tratar_textos import *

from datetime import datetime


def acessar_tabela(
    driver: WebDriver, login: str, seletor_busca: By, nome_elemento: str
):
    """Função personalizada a depender de como a tabela é acessada,
    ela vai definir como a área da tabela será acessada"""

    if type(driver).__name__ != "WebDriver":
        raise TypeError("Driver deve ser do tipo webdriver! (Selenium)")
    if type(login) != str:
        raise TypeError("Login deve ser uma STRING!")

    input_field = driver.find_element(seletor_busca, nome_elemento)
    input_field.send_keys(login)
    input_field.send_keys(Keys.ENTER)
    driver.implicitly_wait(10)  # Espera a página carregar

    ## Pegar a tabela completa


def get_table(url: str):
    """Recebe o Link do website para começar o processo para extrair a tabela\n
    Retorna uma StringIO do html da tabela encontrada"""

    if type(url) != str:
        raise TypeError("Get Table deve receber uma STRING")

    if not url.startswith("https://"):
        raise ValueError("URL deve começar com 'https://'")

    driver = webdriver.Chrome()
    driver.get(url)

    acessar_tabela(driver, LOGIN, By.NAME, ELEMENTO_LOGIN)
    try:
        tabela_locator = (By.TAG_NAME, "table")
        wait = WebDriverWait(driver, 10)
        tabela = wait.until(EC.presence_of_element_located(tabela_locator))
        tabela_html = tabela.get_attribute("outerHTML")
        print("Tabela carregada com sucesso!")
    except TimeoutException as erro:
        print(
            "Timeout: A tabela não foi carregada dentro do tempo limite ou não foi encontrada"
        )
        tabela_html = ""
    finally:
        driver.quit()
        return StringIO(normalizar_text(str(tabela_html)))


def trata_tabela(
    tabela: StringIO | pd.DataFrame, drop_colunas: list[Hashable] | Hashable = []
):
    """Recebe um html de uma tabela como StringIO e uma lista de colunas inuteis para serem removidas\n
    Primeiro ele converte o StringIO em um DataFrame por meio do pd.read_html()\n
    Após isso ela faz o tratamento da tabela removendo as colunas inuteis em (drop_colunas) e retorna o dataframe tratado
    """
    if type(tabela) == StringIO:
        df = pd.read_html(tabela)[0]
    elif type(tabela) == pd.DataFrame:
        df = tabela
    else:
        raise TypeError("Entrada deve ser um dataframe ou um StringIO!")

    if "status" in df.columns:
        df = df[df["status"] == "ocupado"]
        df = df.drop(columns=["status"], errors="ignore")

    try:
        df = df.drop(columns=drop_colunas)
        print("Tabela tratada com sucesso!")

    except KeyError as erro:
        erro = tratar_msg_keyerror(erro)
        print("Chaves não encontradas: ", erro)

    if "data/horario" in df.columns:
        datas = []
        horas = []
        for data_hora in df["data/horario"]:
            data, hora = str(data_hora).split(" ")
            datas.append(data)
            horas.append(hora)

        df = df.drop(columns=["data/horario"])

        df["data"] = datas
        df["hora"] = horas

    if "aluno (cpf)" in df.columns:
        df.rename({"aluno (cpf)": "aluno"}, axis=1, inplace=True)

    if "modulo atual" in df.columns:
        df.rename({"modulo atual": "modulo"}, axis=1, inplace=True)

    return df


def separa_por_dias(tabela: pd.DataFrame, data: datetime) -> pd.DataFrame:
    """Recebe uma tabela e uma data, retorna uma tabela filtrada por essa data"""
    if type(tabela) != pd.DataFrame:
        raise TypeError("Tabela deve ser um DataFrame!")

    if type(data) != datetime:
        raise TypeError("Data deve ser do tipo datetime!")

    data_formatada = data.strftime("%d/%m/%Y")
    tabela_filtrada = tabela[tabela["data"] == data_formatada]

    return tabela_filtrada
