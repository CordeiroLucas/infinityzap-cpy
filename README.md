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

Após realizar os Primeiros Passos você já deve conseguir rodar os arquivos main.py e send_messages.py utilizando:

```py main.py```

    Que gerará um output com a tabela encontrada e tratada no formato de .csv

Para enviar as mensagens para as pessoas listadas na tabela gerada, utilize:
```py send_messages.py```
    Ele funciona desde que haja uma tabela .csv e que ela possua as colunas 
## setup.py

Arquivo que você cria para definir as entradas do código
O código padrão funciona com as entradas:

```bash
URL_LINK = "https://link.com"
ELEMENTO_LOGIN = "id_input"

# REALIZA UM DROP NAS SEGUINTES TABELAS
DATA_DROP = ['id', 'curso (reposicao)', 'data marcacao', 'curso aluno', 'acoes']

# SEU NOME
NAME = "SEU NOME"

# SEU LOGIN DO SISTEMA E SEU TELEFONE
LOGIN = "SEU LOGIN"
TELEFONE = "SEU NUMERO"

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