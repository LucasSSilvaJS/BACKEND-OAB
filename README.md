# Middleware OAB API

API REST para gerenciamento de salas de coworking da OAB. Sistema desenvolvido com FastAPI para controlar cadastros, sessões de uso, computadores, salas de coworking, unidades e subsecionais.

## 📋 Sobre o Projeto

Este projeto é uma API backend que permite o gerenciamento completo de salas de coworking da OAB, incluindo:

- **Cadastros**: Gerenciamento de cadastros de pessoas (advogados, analistas, administradores)
- **Sessões**: Controle de sessões de uso de computadores com sistema robusto de filtros
- **Computadores**: Cadastro e gerenciamento de computadores
- **Salas de Coworking**: Gerenciamento de salas de coworking
- **Unidades**: Gerenciamento de unidades (SEDE ou FILIAL)
- **Subsecionais**: Gerenciamento de subsecionais
- **Usuários Advogados**: Gerenciamento de usuários advogados
- **Autenticação**: Sistema completo de autenticação com JWT para três tipos de usuários
- **Dashboard**: Dashboard com métricas e estatísticas de uso
- **Relatórios**: Geração de relatórios inteligentes usando IA (Gemini)

## 🛠️ Tecnologias Utilizadas

- **Python 3.8+**
- **FastAPI** - Framework web moderno e rápido para construção de APIs
- **SQLAlchemy 2.0+** - ORM para Python
- **PyMySQL** - Driver MySQL para Python
- **psycopg2-binary** - Driver PostgreSQL para Python
- **Pydantic 2.5+** - Validação de dados
- **Uvicorn** - Servidor ASGI de alta performance
- **Alembic** - Ferramenta de migração de banco de dados
- **Passlib** - Biblioteca para hash de senhas (bcrypt)
- **python-jose** - Geração e validação de tokens JWT
- **google-genai** - Integração com Google Gemini AI para relatórios inteligentes

## 📦 Requisitos

Antes de começar, certifique-se de ter instalado:

- Python 3.8 ou superior
- MySQL 5.7+ ou MariaDB 10.2+ (suporte nativo)
- PostgreSQL 12+ (suporte completo)
- pip (gerenciador de pacotes Python)

## 🚀 Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/LucasSSilvaJS/BACKEND-OAB.git
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

#### Opção 4: Chave da API Gemini (opcional, para relatórios)

Para usar a funcionalidade de relatórios inteligentes:
```env
GEMINI_API_KEY=sua_chave_api_gemini
```

**Nota:** A funcionalidade de relatórios requer uma chave da API Gemini. Consulte a documentação em `CONFIGURACAO_GEMINI.md` para mais detalhes.

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

#### 🔐 Autenticação
- **`/api/v1/auth/login/advogado`** - Login de advogado (registro OAB + código de segurança)
- **`/api/v1/auth/login/administrador`** - Login de administrador (usuário + senha)
- **`/api/v1/auth/login/analista`** - Login de analista de TI (usuário + senha)

#### 👥 Cadastros e Usuários
- **`/api/v1/cadastros`** - Gerenciamento de cadastros
- **`/api/v1/usuarios-advogados`** - Gerenciamento de usuários advogados
- **`/api/v1/analistas-ti`** - Gerenciamento de analistas de TI
- **`/api/v1/administradores-sala`** - Gerenciamento de administradores de sala

#### 💻 Sessões e Computadores
- **`/api/v1/sessoes`** - Gerenciamento de sessões (com sistema robusto de filtros)
- **`/api/v1/computadores`** - Gerenciamento de computadores

#### 🏢 Estrutura Organizacional
- **`/api/v1/salas-coworking`** - Gerenciamento de salas de coworking
- **`/api/v1/unidades`** - Gerenciamento de unidades (SEDE ou FILIAL)
- **`/api/v1/subsecionais`** - Gerenciamento de subsecionais

#### 📊 Dashboard e Relatórios
- **`/api/v1/dashboard`** - Dashboard com métricas e estatísticas
- **`/api/v1/relatorios`** - Geração de relatórios inteligentes (requer autenticação de analista)

#### 🌱 Seed (Desenvolvimento)
- **`/api/v1/seed`** - Endpoints para popular o banco de dados com dados de teste

#### 🔧 Utilitários
- **`/`** - Endpoint raiz com informações da API
- **`/health`** - Health check da API

### 🔐 Sistema de Autenticação

A API possui um sistema completo de autenticação baseado em JWT (JSON Web Tokens) com três tipos de usuários:

1. **Advogados**: Autenticam usando registro OAB e código de segurança
2. **Administradores de Sala**: Autenticam usando usuário e senha (hash bcrypt)
3. **Analistas de TI**: Autenticam usando usuário e senha (hash bcrypt)

**Como usar:**
1. Faça login no endpoint apropriado (`/api/v1/auth/login/{tipo}`)
2. Receba o token JWT na resposta
3. Use o token no header `Authorization: Bearer <token>` para acessar endpoints protegidos

Consulte `src/routes/AUTENTICACAO_EXEMPLO.md` para exemplos detalhados de uso.

### Exemplo de Uso

#### 1. Login de Advogado

```bash
curl -X POST "http://localhost:8000/api/v1/auth/login/advogado" \
  -H "Content-Type: application/json" \
  -d '{
    "registro_oab": "OAB-PE-10001",
    "codigo_de_seguranca": "123"
  }'
```

#### 2. Criar um cadastro

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

#### 3. Listar sessões com filtros

```bash
curl -X GET "http://localhost:8000/api/v1/sessoes?administrador_id=1&apenas_ativas=true&skip=0&limit=50" \
  -H "Authorization: Bearer <seu_token>"
```

#### 4. Obter dashboard

```bash
curl -X GET "http://localhost:8000/api/v1/dashboard?subsecional_id=1&unidade_id=1&coworking_id=1&ano=2025" \
  -H "Authorization: Bearer <seu_token>"
```

## 📁 Estrutura do Projeto

```
BACKEND/
│
├── src/
│   ├── entities/              # Modelos do banco de dados (SQLAlchemy)
│   │   ├── cadastro.py
│   │   ├── computador.py
│   │   ├── sessao.py
│   │   ├── sala_coworking.py
│   │   ├── unidade.py
│   │   ├── subsecional.py
│   │   ├── usuario_advogado.py
│   │   ├── analista_de_ti.py
│   │   ├── administrador_sala_coworking.py
│   │   └── sessoes_analistas.py
│   │
│   ├── schemas/               # Schemas Pydantic para validação
│   │   ├── cadastro.py
│   │   ├── sessao.py
│   │   ├── computador.py
│   │   ├── sala_coworking.py
│   │   ├── unidade.py
│   │   ├── subsecional.py
│   │   ├── usuario_advogado.py
│   │   ├── analista_de_ti.py
│   │   ├── administrador_sala.py
│   │   ├── auth.py
│   │   ├── dashboard.py
│   │   ├── relatorio.py
│   │   ├── filtro_sessao.py
│   │   └── comum.py
│   │
│   ├── repositories/          # Camada de acesso a dados
│   │   ├── base_repository.py
│   │   ├── cadastro_repository.py
│   │   ├── sessao_repository.py
│   │   ├── computador_repository.py
│   │   ├── sala_coworking_repository.py
│   │   ├── unidade_repository.py
│   │   ├── subsecional_repository.py
│   │   ├── usuario_advogado_repository.py
│   │   ├── analista_ti_repository.py
│   │   ├── administrador_sala_repository.py
│   │   └── dashboard_repository.py
│   │
│   ├── services/              # Lógica de negócio
│   │   ├── cadastro_service.py
│   │   ├── sessao_service.py
│   │   ├── computador_service.py
│   │   ├── sala_coworking_service.py
│   │   ├── unidade_service.py
│   │   ├── subsecional_service.py
│   │   ├── usuario_advogado_service.py
│   │   ├── analista_ti_service.py
│   │   ├── administrador_sala_service.py
│   │   ├── dashboard_service.py
│   │   └── relatorio_service.py
│   │
│   ├── routes/                # Rotas da API (FastAPI routers)
│   │   ├── auth_router.py
│   │   ├── auth_dependencies.py
│   │   ├── cadastro_router.py
│   │   ├── sessao_router.py
│   │   ├── computador_router.py
│   │   ├── sala_coworking_router.py
│   │   ├── unidade_router.py
│   │   ├── subsecional_router.py
│   │   ├── usuario_advogado_router.py
│   │   ├── analista_ti_router.py
│   │   ├── administrador_sala_router.py
│   │   ├── dashboard_router.py
│   │   ├── relatorio_router.py
│   │   ├── seed_router.py
│   │   ├── dependencies.py
│   │   └── AUTENTICACAO_EXEMPLO.md
│   │
│   ├── database/              # Configuração do banco de dados
│   │   ├── base.py
│   │   ├── connection.py
│   │   └── seed.py
│   │
│   ├── utils/                  # Utilitários
│   │   └── security.py
│   │
│   └── main.py                # Arquivo principal da aplicação
│
├── requirements.txt           # Dependências do projeto
├── .env                       # Variáveis de ambiente (criar)
├── README.md                  # Este arquivo
├── CONFIGURACAO_GEMINI.md     # Documentação sobre configuração do Gemini
├── ATUALIZACAO_GEMINI_API.md  # Guia de atualização da API Gemini
├── FILTROS_SESSOES.md         # Documentação sobre filtros de sessões
└── EXEMPLO_RELATORIO.md       # Exemplos de relatórios
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
5. Para endpoints protegidos, use o botão "Authorize" e insira seu token JWT

### Sistema de Filtros de Sessões

O endpoint `/api/v1/sessoes` possui um sistema robusto de filtros. Consulte `FILTROS_SESSOES.md` para documentação completa sobre:
- Filtros por data, administrador, IP, status
- Paginação e ordenação
- Exemplos de uso

## 🔐 Segurança

- **Autenticação JWT**: Tokens seguros para autenticação
- **Hash de Senhas**: Senhas hasheadas usando bcrypt
- **Validação de Dados**: Validação robusta usando Pydantic
- **Tratamento de Erros**: Tratamento adequado de erros HTTP
- **Validação de Unicidade**: Validação de unicidade (emails, CPFs, registros OAB, etc.)
- **Controle de Acesso**: Diferentes níveis de acesso por tipo de usuário

## 📝 Notas Importantes

- As tabelas são criadas automaticamente na primeira execução
- Certifique-se de que o banco de dados está rodando antes de iniciar a API
- Use sempre um ambiente virtual para isolar as dependências
- Mantenha o arquivo `.env` seguro e não o commite no repositório
- Para usar relatórios inteligentes, configure a `GEMINI_API_KEY` no arquivo `.env`
- Consulte a documentação específica em `src/routes/AUTENTICACAO_EXEMPLO.md` para exemplos de autenticação

## 📚 Documentação Adicional

- **Autenticação**: `src/routes/AUTENTICACAO_EXEMPLO.md` - Exemplos de uso do sistema de autenticação
- **Filtros de Sessões**: `FILTROS_SESSOES.md` - Documentação completa do sistema de filtros
- **Configuração Gemini**: `CONFIGURACAO_GEMINI.md` - Como configurar a API Gemini para relatórios
- **Atualização Gemini**: `ATUALIZACAO_GEMINI_API.md` - Guia de atualização da API Gemini
- **Exemplos de Relatórios**: `EXEMPLO_RELATORIO.md` - Exemplos de uso dos relatórios

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
