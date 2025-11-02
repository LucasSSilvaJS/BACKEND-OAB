# Middleware OAB API

API REST para gerenciamento de salas de coworking da OAB. Sistema desenvolvido com FastAPI para controlar cadastros, sessões de uso, computadores, salas de coworking, unidades e subsecionais.

## 📋 Sobre o Projeto

Este projeto é uma API backend que permite o gerenciamento completo de salas de coworking da OAB, incluindo:

- **Cadastros**: Gerenciamento de cadastros de pessoas (advogados, analistas, administradores)
- **Sessões**: Controle de sessões de uso de computadores
- **Computadores**: Cadastro e gerenciamento de computadores
- **Salas de Coworking**: Gerenciamento de salas de coworking
- **Unidades**: Gerenciamento de unidades (SEDE ou FILIAL)
- **Subsecionais**: Gerenciamento de subsecionais
- **Usuários Advogados**: Gerenciamento de usuários advogados

## 🛠️ Tecnologias Utilizadas

- **Python 3.8+**
- **FastAPI** - Framework web moderno e rápido para construção de APIs
- **SQLAlchemy** - ORM para Python
- **PyMySQL** - Driver MySQL para Python
- **psycopg2-binary** - Driver PostgreSQL para Python
- **Pydantic** - Validação de dados
- **Uvicorn** - Servidor ASGI de alta performance
- **Alembic** - Ferramenta de migração de banco de dados
- **Passlib** - Biblioteca para hash de senhas

## 📦 Requisitos

Antes de começar, certifique-se de ter instalado:

- Python 3.8 ou superior
- MySQL 5.7+ ou MariaDB 10.2+ (suporte nativo)
- PostgreSQL 12+ (suporte completo)
- pip (gerenciador de pacotes Python)

## 🚀 Instalação

### 1. Clone o repositório

```bash
git clone <url-do-repositorio>
cd BACKEND
```

### 2. Crie um ambiente virtual (recomendado)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto. Você pode usar uma das duas opções:

#### Opção 1: DATABASE_URL (recomendado para PostgreSQL ou serviços em nuvem)

```env
DATABASE_URL=postgresql://usuario:senha@host:porta/nome_do_banco?sslmode=require
```

**Exemplo para PostgreSQL (Neon, Supabase, etc.):**
```env
DATABASE_URL=postgresql://neondb_owner:npg_pZPUj5Kg9Dsh@ep-frosty-recipe-ahqi4ldr-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require
```

#### Opção 2: Variáveis individuais (para MySQL local)

```env
DB_USER=seu_usuario
DB_PASS=sua_senha
DB_HOST=127.0.0.1
DB_PORT=3306
DB_NAME=middleware_oab
```

**Importante**: 
- Se `DATABASE_URL` estiver definida, ela será usada com prioridade
- Se não, o sistema usará as variáveis individuais (MySQL por padrão)
- Substitua os valores pelas credenciais do seu banco de dados

#### Opção 3: URL da API (opcional, para Swagger)

Para que o Swagger possa alternar entre localhost e produção:
```env
API_URL=https://api.seusite.com
```

Se não configurado, o Swagger mostrará apenas o servidor localhost.

### 5. Crie o banco de dados

#### Para MySQL:

```sql
CREATE DATABASE middleware_oab CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

#### Para PostgreSQL:

```sql
CREATE DATABASE middleware_oab;
```

**Nota**: Se você estiver usando um serviço em nuvem (Neon, Supabase, etc.), o banco de dados geralmente já está criado. Apenas configure a `DATABASE_URL` no arquivo `.env`.

## ▶️ Como Executar

### Executar o servidor de desenvolvimento

```bash
uvicorn src.main:app --reload
```

A API estará disponível em: `http://localhost:8000`

### Executar em modo de produção

```bash
uvicorn src.main:app --host 0.0.0.0 --port 8000
```

### Executar com hot reload (desenvolvimento)

```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

## 📚 Documentação da API

A API possui documentação interativa automática gerada pelo Swagger/OpenAPI:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **OpenAPI JSON**: `http://localhost:8000/openapi.json`

### Endpoints Disponíveis

A API possui os seguintes grupos de endpoints:

- **`/api/v1/cadastros`** - Gerenciamento de cadastros
- **`/api/v1/sessoes`** - Gerenciamento de sessões
- **`/api/v1/computadores`** - Gerenciamento de computadores
- **`/api/v1/salas-coworking`** - Gerenciamento de salas de coworking
- **`/api/v1/unidades`** - Gerenciamento de unidades
- **`/api/v1/subsecionais`** - Gerenciamento de subsecionais
- **`/api/v1/usuarios-advogados`** - Gerenciamento de usuários advogados

### Exemplo de Uso

#### Criar um cadastro

```bash
curl -X POST "http://localhost:8000/api/v1/cadastros" \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "João Silva",
    "email": "joao@example.com",
    "telefone": "11999999999",
    "cpf": "12345678901",
    "rg": "123456789",
    "endereco": "Rua Exemplo, 123"
  }'
```

#### Listar cadastros

```bash
curl -X GET "http://localhost:8000/api/v1/cadastros"
```

#### Obter um cadastro específico

```bash
curl -X GET "http://localhost:8000/api/v1/cadastros/1"
```

## 📁 Estrutura do Projeto

```
BACKEND/
│
├── src/
│   ├── entities/          # Modelos do banco de dados (SQLAlchemy)
│   │   ├── cadastro.py
│   │   ├── computador.py
│   │   ├── sessao.py
│   │   └── ...
│   │
│   ├── schemas/           # Schemas Pydantic para validação
│   │   ├── cadastro.py
│   │   ├── sessao.py
│   │   └── ...
│   │
│   ├── repositories/      # Camada de acesso a dados
│   │   ├── base_repository.py
│   │   ├── cadastro_repository.py
│   │   └── ...
│   │
│   ├── services/          # Lógica de negócio
│   │   ├── cadastro_service.py
│   │   ├── sessao_service.py
│   │   └── ...
│   │
│   ├── routes/            # Rotas da API (FastAPI routers)
│   │   ├── cadastro_router.py
│   │   ├── sessao_router.py
│   │   ├── dependencies.py
│   │   └── __init__.py
│   │
│   ├── database/          # Configuração do banco de dados
│   │   ├── base.py
│   │   └── connection.py
│   │
│   ├── utils/             # Utilitários
│   │   └── security.py
│   │
│   └── main.py            # Arquivo principal da aplicação
│
├── requirements.txt        # Dependências do projeto
├── .env                   # Variáveis de ambiente (criar)
└── README.md             # Este arquivo
```

## 🔧 Configuração do Banco de Dados

O projeto suporta tanto MySQL/MariaDB quanto PostgreSQL como banco de dados. As tabelas são criadas automaticamente na primeira execução do servidor.

### Variáveis de Ambiente

Certifique-se de configurar corretamente o arquivo `.env`. Use uma das duas opções:

#### Opção 1: DATABASE_URL (Prioridade)
- `DATABASE_URL`: URL completa de conexão do banco de dados
  - Formato PostgreSQL: `postgresql://usuario:senha@host:porta/dbname?options`
  - Formato MySQL: `mysql+pymysql://usuario:senha@host:porta/dbname?options`

#### Opção 2: Variáveis Individuais (Fallback)
- `DB_USER`: Usuário do banco de dados
- `DB_PASS`: Senha do banco de dados
- `DB_HOST`: Host do banco de dados (padrão: 127.0.0.1)
- `DB_PORT`: Porta do banco de dados (padrão: 3306)
- `DB_NAME`: Nome do banco de dados (padrão: middleware_oab)

## 🧪 Testando a API

### Endpoints de Saúde

- **Health Check**: `GET /health`
- **Raiz**: `GET /`

### Usando o Swagger UI

1. Acesse `http://localhost:8000/docs`
2. Explore os endpoints disponíveis
3. Teste os endpoints diretamente na interface
4. Veja os schemas de request/response

## 🔐 Segurança

- Senhas são hasheadas usando bcrypt
- Validação de dados usando Pydantic
- Tratamento de erros HTTP adequado
- Validação de unicidade (emails, CPFs, etc.)

## 📝 Notas Importantes

- As tabelas são criadas automaticamente na primeira execução
- Certifique-se de que o MySQL está rodando antes de iniciar a API
- Use sempre um ambiente virtual para isolar as dependências
- Mantenha o arquivo `.env` seguro e não o commite no repositório

## 🤝 Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT.

## 📞 Suporte

Para suporte, envie um email para: suporte@oab.org.br

---

**Desenvolvido com ❤️ usando FastAPI**

