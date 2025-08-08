# InfinityZap | Monitor
aplicação que extrai dados de uma table html e converte para enviar mensagens automatizadas pelo whatsapp web

## Primeiros Passos

Iniciar o ambiente virtual

```bash
py -m venv venv
python -m venv venv
```


Entrar no ambiente virtual

```bash
.\venv\Scripts\activate
```

```bash
source \venv\bin\activate
```

Baixar os pacotes necessários

```bash
pip install -r requirements.txt
```

Por fim, vai depender de como a sua tabela é acessada. Caso necessite de algum tipo de autenticação, você vai ficar responsável por editar a função acessar_tabela no main.py

## Rodando o Programa

Após realizar os Primeiros Passos você já deve conseguir rodar o arquivo main.py utilizando:

```py main.py```

Rodando ele pela primeira vez, será gerado um arquivo settings.py e um diretório output

Após isso, modifique o arquivo settings com suas entradas
O código padrão funciona com as entradas:

```bash
TABELA_OUTPUT = ""
URL_LINK = ""
ELEMENTO_LOGIN = ""
DATA_DROP = ["curso (reposicao)", "data marcacao", "curso aluno", "acoes"]
NAME = ""
LOGIN = ""
TELEFONE = ""

# RODA NO MODO DE TESTE (SÓ VOCÊ VAI RECEBER AS MENSAGENS)
# FALSE - PARA MANDAR MENSAGENS PARA PESSOAS
TESTE = True

```

## Proximos passos:

- Interface Gráfica para visualizar reposições
    - Clicar nos alunos e marcar como Compareceu ou Não Compareceu (Explicação)

- Salvar os alunos que já foram notificados
    - Não mandar mensagens para quem já foi notificado

    - A cada nova consulta, adicionar as reposições diferentes
