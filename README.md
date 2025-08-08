# 📊 Projeto de Visualização de Dados com Django
Este é um projeto web desenvolvido com **Django** para visualização de dados geográficos (estados, cidades, distritos) e dados de empresas, utilizando gráficos e tabelas interativas em um **dashboard**.

---

## ⚙️ Funcionalidades

- Visualização de dados por meio de um dashboard.
- Tabelas de Estados, Cidades e Distritos (IBGE).
- Importação de dados diretamente da API do IBGE.
- Importação de dados de empresas via script ou pela interface web.
- Configuração opcional com **Docker Compose** para uso de PostgreSQL.

---

## 🚀 Como Executar o Projeto

### 1. Clone o repositório e entre no diretório
```bash
git clone https://github.com/seu-usuario/seu-projeto.git
cd seu-projeto
```
### 2. Crie e ative um ambiente virtual (opcional)
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate      # Windows
```
### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Crie um arquivo .env na raiz do projeto com o seguinte conteúdo:
```bash
SECRET_KEY=django-insecure-k=&9+puvswqe@8w)%r37ymocc9uvb^lmerd-8yl1yc1y!sbc5p
DEBUG=True
ALLOWED_HOSTS=*
DEVELOPMENT_ENV=False

DATABASE_URL=postgres://dev_user:dev_password@host.docker.internal:5432/dev_database

POSTGRES_DB=dev_database
POSTGRES_USER=dev_user
POSTGRES_PASSWORD=dev_password
```
💡 O campo DATABASE_URL será usado pelo Django se você estiver utilizando PostgreSQL com Docker Compose.

## 🐳 Usando Docker Compose (Banco de Dados)
O projeto vem com um arquivo docker-compose.yml para facilitar a configuração do banco de dados PostgreSQL.

### 1. Inicie o banco de dados
```bash
docker-compose up -d
```
Isso criará um banco PostgreSQL acessível em host.docker.internal:5432 com as credenciais definidas no .env.

## 🛠️ Migrações e Importação de Dados

## 1. Aplique as migrações do Django
```bash
python manage.py migrate
```

### 2. Importe os dados da API do IBGE
```bash
python manage.py import_locations_data
```
### 3. (Opcional) Importe dados de empresas via comando
```bash
python manage.py import_companies_data <caminho para o arquivo>
```
🧠 Você também pode importar os dados de empresas diretamente pela interface do dashboard, se preferir.

### ▶️ Inicie o servidor de desenvolvimento
```bash
python manage.py runserver
```
### Acesse o projeto em:
```bash
http://localhost:8000/
```
