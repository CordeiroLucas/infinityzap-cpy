import re
import unicodedata


def simplificar_data(data: str):
    "Remove a parte de /YYYY da data"
    data = data.split("/")[0:2]
    return "/".join(data)


def tratar_nome(nome: str):
    "Trata uma string que possui um nome"

    nome = nome.lower().removesuffix(".")
    nome_separado = nome.split(" ")
    return " ".join(
        [
            nome.capitalize() if nome not in ["de", "do", "da"] else nome
            for nome in nome_separado
        ]
    )


def tratar_msg_keyerror(texto: KeyError):
    "Trata a mensagem de erro vinda de KeyError"
    if type(texto) != KeyError:
        raise TypeError("Entrada deve conter um objeto KeyError")

    texto = str(texto).replace("'", "")
    texto = re.findall(r"\[(.*?)\]", texto)
    return list(texto)[0]


def normalizar_text(text: str):
    """Normaliza a string removendo acentuação e tornando minúsculo."""

    if type(text) != str:
        raise TypeError("Normalizar DEVE receber uma STRING!\n")

    normalizado = unicodedata.normalize("NFKD", text)
    sem_acento = "".join([c for c in normalizado if not unicodedata.combining(c)])
    return sem_acento.lower()
