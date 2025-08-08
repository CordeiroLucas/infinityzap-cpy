from os import mkdir, system, name as os_name
from pathlib import Path
from pandas.errors import EmptyDataError
from datetime import datetime, timedelta
from components.template_settings import TEMPLATE

SETTINGS_PATH = Path(__file__).parent / "settings.py"
ROOT_PATH = Path(__file__).parent
FOLDER_OUTPUT = ROOT_PATH / "output"
DATA_ATUAL = datetime.today().strftime("%d/%m/%Y")

# Check if the file exists
if not (SETTINGS_PATH).exists():
    with open(SETTINGS_PATH, "w") as settings:
        settings.write(f"{TEMPLATE}\n")
        settings.close()
    raise FileNotFoundError(
        "settings.py não encontrado, foi criado um novo arquivo com o template padrão. Edite-o com suas informações."
    )
else:
    from src.find_tables import *
    from src.send_messages import *
    from settings import *  # type: ignore

###################

tabela: StringIO | pd.DataFrame = pd.DataFrame()

if not (FOLDER_OUTPUT).exists():
    print("Pasta 'output' não encontrada, criando...")
    mkdir(FOLDER_OUTPUT)

if not (FOLDER_OUTPUT / f"{TABELA_OUTPUT}.csv").exists():
    print("Arquivo de agendamentos não encontrado, criando...")
    tabela = trata_tabela(get_table(URL_LINK), DATA_DROP)
    tabela.to_csv(FOLDER_OUTPUT / f"{TABELA_OUTPUT}.csv", index=False)
    print("Tabela criada em: ", FOLDER_OUTPUT / f"{TABELA_OUTPUT}.csv")

    ###################
tabela = pd.read_csv(FOLDER_OUTPUT / f"{TABELA_OUTPUT}.csv")
if tabela.empty:
    OPT = input("Tabela está vazia, deseja extrair dados? (s/n): ").strip().lower()
    if OPT == "s":
        tabela = trata_tabela(get_table(URL_LINK))
        tabela.to_csv(FOLDER_OUTPUT / TABELA_OUTPUT, index=False)
        print("Tabela atualizada com sucesso!")
    else:
        raise EmptyDataError("Tabela está vazia, não é possível continuar sem dados.")
###############

for i in range(3):
    data = (datetime.today() + timedelta(days=i)).strftime("%d/%m/%Y")
    CAMINHO = FOLDER_OUTPUT / f"{TABELA_OUTPUT}_{data.replace('/', '-')}.csv"
    tabela_dia = separa_por_dias(tabela, datetime.today() + timedelta(days=i))
    if tabela_dia.empty:
        print(f"\nNenhum agendamento encontrado para {data}.")
        continue
    tabela_dia.to_csv(CAMINHO, index=False)

system(f"rm {FOLDER_OUTPUT / f'{TABELA_OUTPUT}.csv'}")

while True:

    system("cls" if os_name == "nt" else "clear")
    print(f" {DATA_ATUAL} ".center(50, "-"))
    print(f"Bem-vindo ao InfinityZap Monitor! {NAME}.\n")
    # OPCAO = input("0 - Extrair tabela do site\n1 - Pedir Confirmação para alunos\n2 - Confirmar Reposição para alunos\nEscolha uma opção: ").strip().lower()
    OPCAO = input(MENU).strip().lower()

    if OPCAO not in ["0", "1", "2", "s"]:
        print("Opção inválida! Escolha uma opção válida (0, 1, 2 ou S).")
        continue

    if OPCAO == "s" or OPCAO == "sair":
        print("Saindo do InfinityZap Monitor...")
        break

    match OPCAO:
        case "0":
            try:
                tabela = separa_por_dias(tabela, datetime.today())
                if tabela.empty:
                    print("Nenhuma reposição agendada para hoje!")
                else:
                    print("Reposições agendadas para hoje:\n")
                    print(tabela)
                    input("\nPressione ENTER para continuar...")

                    tabela.to_csv(
                        FOLDER_OUTPUT
                        / f"{TABELA_OUTPUT}_{DATA_ATUAL.replace('/', '-')}.csv",
                        index=False,
                    )

            except TypeError as erro:
                raise TypeError("Erro ao tratar tabela: ") from erro
            except EmptyDataError as erro:
                raise EmptyDataError(
                    "Tabela está vazia, verifique a conexão com a internet ou o site."
                ) from erro

        case "1":
            # 'confirmar_reposicao' ou 'status_reposicao'
            STATUS = "status_reposicao"
            enviar(
                FOLDER_OUTPUT / f"{TABELA_OUTPUT}_{DATA_ATUAL.replace('/', '-')}.csv",
                LOGIN,
                STATUS,
                TESTE,
            )
        case "2":
            STATUS = "confirmar_reposicao"
            enviar(
                FOLDER_OUTPUT / f"{TABELA_OUTPUT}_{DATA_ATUAL.replace('/', '-')}.csv",
                LOGIN,
                STATUS,
                TESTE,
            )
