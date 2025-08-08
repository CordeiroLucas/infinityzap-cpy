import pandas as pd
from components.mensagens import *
from components.tratar_textos import *
import pywhatkit
from settings import *


def seletor_mensagem(linha, tipo_mensagem, nome_remetente) -> str:
    if "aluno (cpf)" in linha:
        nome_pessoa = tratar_nome(str(linha["aluno (cpf)"]))
    elif "aluno" in linha:
        nome_pessoa = tratar_nome(str(linha.aluno))
    if "modulo atual" in linha:
        modulo = str(linha["modulo atual"]).strip()
    elif "modulo" in linha:
        modulo = str(linha.modulo).strip()

    nome_remetente = tratar_nome(nome_remetente).split(" ")[0]
    data = simplificar_data(linha.data)

    match (tipo_mensagem):
        case "confirmar_reposicao":
            mensagem = mensagem_confirmar(
                nome_pessoa.capitalize(),
                nome_remetente,
                linha.modalidade,
                modulo,
                data,
                linha.hora,
            )
        case "status_reposicao":
            confirmou = input(
                f"Reposição {linha.data} as {linha.hora}\n Aluno: {nome_pessoa} confirmou? (s/n)\n"
            )
            descricao = input("Adicione uma descrição ou pressione ENTER:\n")

            if confirmou.lower() == "s":
                mensagem = mensagem_presenca(
                    linha.data, linha.hora, nome_pessoa, descricao=descricao
                )
            elif confirmou.lower() == "n":
                status = input("Qual o status?\n").lower()
                mensagem = mensagem_presenca(
                    linha.data, linha.hora, nome_pessoa, status, descricao, False
                )
            else:
                mensagem = ""
                raise ValueError("Resposta deve ser s ou n!")
        case "presenca_aula":
            pass
        case _:
            raise ValueError(
                "Tipo Mensagem contém uma entrada inválida! (Deve ser: status_reposicao ou confirmar_reposicao)"
            )
    return mensagem


def enviar(
    caminho_tabela_csv: str,
    nome_remetente: str,
    tipo_mensagem: str = "confirmar_reposicao",
    prefix_pais: str = "+55",
    teste: bool = TESTE,
) -> None:
    """Recebe o caminho da tabela csv e envia a mensagem formatada com os dados do remetente para cada pessoa listada na tabela"""

    if not str(caminho_tabela_csv).endswith(".csv"):
        raise ValueError("Diretório deve conter um arquivo .csv!")

    if caminho_tabela_csv.exists() is False:
        raise FileNotFoundError(f"Arquivo {caminho_tabela_csv} não encontrado!")

    tabela_agendamentos = pd.read_csv(caminho_tabela_csv)
    enviados = pd.DataFrame()

    for index, linha in tabela_agendamentos.iterrows():
        try:
            mensagem = seletor_mensagem(linha, tipo_mensagem, nome_remetente)
        except KeyError as erro:
            raise KeyError("Chaves não encontradas: ", erro)

        except Exception as erro:
            raise erro

        if teste:
            print(f"prefixo: {prefix_pais}")
            print(f"telefone: {linha.telefone}")
            pywhatkit.sendwhatmsg_instantly(f"+55{TELEFONE}", mensagem, 9, True, 1)
        else:
            if "telefone" in linha:
                pywhatkit.sendwhatmsg_instantly(
                    f"+55{int(linha.telefone)}", mensagem, 9, True, 1
                )
            else:
                raise KeyError("Chave 'telefone' não encontrada na tabela!")
