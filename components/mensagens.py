from datetime import time, datetime

MENU = """Ver reposições de hoje -------- 0\n
Confirmar Reposição ------------ 1\n
Status Reposição --------------- 2\n
Sair --------------------------- S\n\n
Escolha uma opção:  """


def mensagem_confirmar(nome_aluno, nome_monitor, modalidade, modulo, data, hora):
    return f"""{' *REPOSIÇÃO | REFORÇO* '.center(50, '=')}\n
Olá *{nome_aluno.split(" ")[0]}*, {cumprimento_horario(datetime.now().time())}!
\nSou o monitor {nome_monitor} e irei ministrar a sua reposição\\reforço {modalidade}
Módulo Atual: *{' '.join(modulo.split(" ")[0:3]).upper()}*
Agendada para *{data} as {hora} horas*.
"""


def mensagem_presenca(
    data: str,
    hora: str,
    nome: str,
    status: str = "compareceu",
    descricao: str = "",
    confirmou: bool = True,
):
    """Contém a data do agendamento, hora, e nome da pessoa\n"""

    mensagem = f"""🔹 DATA DA AULA AGENDADA: {data}
🔹 HORÁRIO: {hora}
🔹 Nome do aluno: {nome}\n"""
    match (status):
        case "compareceu":
            mensagem += f"""🔹 Status: Compareceu ✅"""
        case _:
            mensagem += f"""🔹 Status: {status.capitalize()} ❌"""
    return f"{mensagem} {'('+descricao+')' if descricao else ''}"


def cumprimento_horario(hora: time):
    """Define o cumprimento a depender da hora do dia"""

    if type(hora) != time:
        raise TypeError("hora deve ser do tipo _Time! (datetime.time())")

    hora = int(str(hora).split(":")[0])

    if hora > 5 and hora < 12:
        return "bom dia"
    elif hora >= 12 and hora < 18:
        return "boa tarde"
    else:
        return "boa noite"
