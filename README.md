# ArtriApp - API (Back-end)

Este repositório contém o código do back-end do aplicativo **ArtriApp**, desenvolvido utilizando Django e Django Rest Framework. A API é responsável pelo gerenciamento de usuários, diário de dor/fadiga/sono, checklist de medicamentos e recomendação de exercícios para o aplicativo mobile.

Este projeto é parte da disciplina de Desenvolvimento Mobile. Siga o guia abaixo para executar a API localmente na sua máquina para realizar testes e integrar com o seu front-end em Flutter.

---

## 👥 Integrantes do grupo

- José Maia de Oliveira

---

## 🛠️ Tecnologias Utilizadas
* **Linguagem:** Python 3.12+
* **Framework:** Django 5.x
* **API:** Django Rest Framework (DRF)
* **Banco de Dados:** PostgreSQL
* **Documentação da API:** Swagger/ReDoc (drf-yasg)

---

## ⚙️ Passo 0: Configuração de Variáveis de Ambiente (Obrigatório)

Seja rodando via Docker ou Localmente, o projeto **exige** um arquivo `.env` para conectar ao banco de dados e gerir o cache. Sem ele, a aplicação (e o Docker) irá falhar.

1. Clone o repositório e entre na pasta da API:
```bash
git clone [https://github.com/artri-app/artri-app-api.git](https://github.com/artri-app/artri-app-api.git)
cd artri-app-api/artri_app_api

```

2. Na pasta `docker/django/`, existe um arquivo chamado `artriapp.env.example`.
3. Copie este arquivo para a **raiz** do projeto (onde está o `manage.py`) e renomeie-o para **`.env`** (com o ponto no início).
4. Abra o arquivo `.env`. Ele deve ter este exato formato básico para testes:

```env
# ==========================================
# CONFIGURAÇÕES GERAIS DO DJANGO
# ==========================================
DEBUG=True
SECRET_KEY="chave-secreta-padrao-para-desenvolvimento-local"
ALLOWED_HOSTS=127.0.0.1,localhost,*
INTERNAL_IPS=127.0.0.1,localhost
CORS_ALLOWED_ORIGINS=http://localhost:8000,[http://127.0.0.1:8000](http://127.0.0.1:8000)
CSRF_TRUSTED_ORIGINS=http://localhost:8000,[http://127.0.0.1:8000](http://127.0.0.1:8000)

# ==========================================
# BANCO DE DADOS (PostgreSQL)
# ==========================================
# IMPORTANTE: Se você estiver rodando SEM DOCKER (direto na máquina), 
# troque a palavra 'artriapp-db' por 'localhost' na linha abaixo:
DATABASE_URL=postgres://artriapp:artriapp@artriapp-db:5432/artriapp

# Variáveis lidas pelo Docker para criar o banco na primeira execução
POSTGRES_DB=artriapp
POSTGRES_USER=artriapp
POSTGRES_PASSWORD=artriapp

# ==========================================
# CACHE (Redis)
# ==========================================
# Desativado por padrão para facilitar o desenvolvimento local
CACHE_ENABLED=False  

# Se for ativar o cache e rodar sem Docker, mude 'artriapp-cache' para 'localhost'
CACHE_URL=redis://artriapp-cache:6379/1
CACHE_TIMEOUT=900

# Chaves genéricas para não quebrar a aplicação localmente
SECRET_ENCRYPTION_KEY="dummy_encryption_key_para_testes"
SECRET_ENCRYPTION_SALT="dummy_salt"
PGCRYPTO_KEY="dummy_pgcrypto_key"
RECAPTCHA_SECRET_KEY="dummy_recaptcha"

EMAIL_HOST=localhost
EMAIL_PORT=25
EMAIL_HOST_USER=user
EMAIL_HOST_PASSWORD=password
EMAIL_USE_TLS=True
EMAIL_USE_SSL=False
DEFAULT_FROM_EMAIL=sistema.artriapp@localhost

```

Escolha **APENAS UM** dos caminhos abaixo para rodar o projeto: via Docker (Recomendado) ou Localmente (Nativo).

---

## 🐋 Caminho 1: Execução via Docker (Recomendado)

Esta é a maneira mais rápida e fácil, pois cria o banco de dados PostgreSQL automaticamente sem que você precise instalá-lo no seu computador.

**Pré-requisito:** Ter o [Docker](https://www.docker.com/) e o Docker Compose instalados.

### 1. Subir os contêineres

Na raiz do projeto (onde está o `manage.py`), execute:

```bash
docker-compose -f docker/docker-compose-local.yml up -d --build

```

*(O Docker fará o download do Python, do PostgreSQL, instalará as dependências e iniciará o banco. Aguarde alguns segundos para o banco finalizar a inicialização).*

### 2. Configurar o Banco e Popular Dados (Seed)

Com os contêineres rodando, execute os comandos por dentro do contêiner do Django:

```bash
# Aplica a estrutura das tabelas no banco de dados
docker-compose -f docker/docker-compose-local.yml exec artriapp-django python manage.py migrate

# Roda o script de semeadura (popula o banco com os Treinos e Exercícios)
docker-compose -f docker/docker-compose-local.yml exec artriapp-django python seed_banco.py

# Cria o usuário administrador do sistema
docker-compose -f docker/docker-compose-local.yml exec artriapp-django python manage.py createsuperuser

```

**Tudo pronto!** A API já está rodando em `http://localhost:8000`. Pule para a seção "Endpoints".

---

## 💻 Caminho 2: Execução Local Nativa (Sem Docker)

Siga este caminho apenas se preferir rodar os serviços diretamente na sua máquina.

**Pré-requisitos Críticos:**

1. **Python 3.12+** instalado.
2. **PostgreSQL** instalado na sua máquina (ex: via pgAdmin ou instalador nativo).
3. *(Apenas Linux)*: Você precisa das bibliotecas de desenvolvimento do Postgres para o `pip install` funcionar. Rode: `sudo apt-get install libpq-dev python3-dev gcc`.

### 1. Criar o Banco de Dados no PostgreSQL

Antes de rodar o projeto, abra o seu terminal do Postgres (`psql`) ou o pgAdmin e rode os seguintes comandos SQL para criar a instância que o Django usará:

```sql
CREATE DATABASE artriapp;
CREATE USER artriapp WITH PASSWORD 'artriapp';
ALTER ROLE artriapp SET client_encoding TO 'utf8';
ALTER ROLE artriapp SET default_transaction_isolation TO 'read committed';
ALTER ROLE artriapp SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE artriapp TO artriapp;

```

### 2. Criar e Ativar o Ambiente Virtual (Venv)

**No Linux/macOS:**

```bash
python3 -m venv venv
source venv/bin/activate

```

**No Windows:**

```bash
python -m venv venv
.\venv\Scripts\activate

```

### 3. Instalar as Dependências

Com o ambiente ativado (você verá `(venv)` no terminal):

```bash
pip install -r requirements.pip

```

### 4. Configurar e Popular o Banco (Seed)

**Atenção:** Garanta que a variável `DATABASE_URL` no seu arquivo `.env` foi alterada para `localhost` antes de prosseguir!

```bash
python manage.py migrate
python seed_banco.py
python manage.py createsuperuser

```

### 5. Rodar o Servidor

```bash
python manage.py runserver 0.0.0.0:8000

```

---

## ❓ Resolução de Problemas Frequentes (FAQ)

**1. Erro: `service "api" is not running` ao tentar popular o banco pelo Docker**

> Certifique-se de estar copiando os comandos exatos do tutorial acima. O nome do container do Django não é `api`, mas sim `artriapp-django`.

**2. O meu terminal parou na mensagem `0 static files copied... System check identified no issues`. O servidor travou?**

> **Não! Isso não é um erro.** Essa é a mensagem de SUCESSO do Django. Significa que o servidor iniciou perfeitamente, o banco conectou e ele está esperando as suas requisições. Deixe o terminal aberto e acesse `http://localhost:8000` no seu navegador.

**3. Erro: `could not translate host name "artriapp-db" to address**`

> Esse erro ocorre se você tentou rodar o projeto localmente (sem Docker) usando a configuração padrão do `.env`. Abra o seu arquivo `.env`, encontre a linha `DATABASE_URL` e troque a palavra `artriapp-db` por `localhost`.

**4. Erro no Redis ou Cache na hora de fazer login**

> Abra o seu `.env` e certifique-se de que a variável `CACHE_ENABLED=False`. O cache exige um servidor Redis rodando. Desativando-o, o Django funcionará normalmente para testes de desenvolvimento.

---

## 🔗 Endpoints e Documentação

Com o servidor rodando, você pode acessar os painéis através do seu navegador:

* **Painel Administrativo do Django:** [http://localhost:8000/admin/](https://www.google.com/search?q=http://localhost:8000/admin/)
* **Documentação Interativa da API (Swagger):** [http://localhost:8000/api/schema/swagger-ui/](https://www.google.com/search?q=http://localhost:8000/api/schema/swagger-ui/) *(Aqui você pode testar as rotas de login, envio de métricas de diário e visualizar o formato do JSON).*



