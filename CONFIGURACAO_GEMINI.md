# 🔧 Configuração da API Google Gemini para Geração de Relatórios

## 📋 Pré-requisitos

Para usar o recurso de geração de relatórios com IA, você precisa configurar a API do Google Gemini.

## 🔑 Obtendo a Chave da API

1. Acesse [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Faça login com sua conta Google
3. Clique em "Get API Key" ou "Create API Key"
4. Copie a chave gerada

## ⚙️ Configurando o Projeto

Adicione a seguinte variável de ambiente no seu arquivo `.env`:

```env
# Google Gemini API Configuration
GEMINI_API_KEY=sua_chave_api_do_gemini_aqui
```

### Exemplo completo do arquivo .env:

```env
# Database Configuration
DATABASE_URL=postgresql://usuario:senha@localhost:5432/oab_coworking

# JWT Configuration
SECRET_KEY=sua_chave_secreta_super_segura_aqui_mude_em_producao
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Google Gemini API Configuration
GEMINI_API_KEY=AIzaSyD-exemplo-de-chave-aqui

# API Configuration (optional)
API_URL=http://localhost:8000
```

## 📦 Instalando Dependências

Instale a biblioteca do Google Gemini:

```bash
pip install google-generativeai
```

Ou adicione ao seu `requirements.txt`:

```txt
google-generativeai>=0.3.0
```

## 🧪 Testando a Configuração

Após configurar, você pode testar a geração de relatórios através do endpoint:

```http
POST /api/v1/relatorios/gerar
Authorization: Bearer {token_do_analista}
Content-Type: application/json

{
  "subsecional_id": 1,
  "unidade_id": 2,
  "coworking_id": 3
}
```

**⚠️ Nota:** Este endpoint é **exclusivo para Analistas de TI**.

## 🤖 Modelo de IA Utilizado

O sistema utiliza o **Gemini 1.5 Flash**, o modelo mais recente e rápido do Google:

- ⚡ Respostas rápidas e eficientes
- 🎯 Alta qualidade de análise
- 💰 Custo-efetivo
- 🌐 Suporte multilíngue

## 📊 Recursos do Relatório

O relatório gerado por IA inclui:

- ✅ Sumário executivo
- 📈 Análise detalhada de métricas de uso
- 🔍 Identificação de padrões e tendências
- 💡 Recomendações práticas de otimização
- 📝 Conclusões baseadas em dados reais

## 🔒 Segurança

- **Nunca** compartilhe sua chave de API
- **Não** commite o arquivo `.env` no Git
- Use variáveis de ambiente em produção
- Mantenha o arquivo `.env` no `.gitignore`

## 💰 Custos

O Google Gemini tem um limite gratuito generoso:
- **60 requisições por minuto**
- **1.500 requisições por dia**

Para mais detalhes sobre preços, consulte: [Google AI Pricing](https://ai.google.dev/pricing)

## 🆘 Troubleshooting

### Erro: "GEMINI_API_KEY não configurada no arquivo .env"
- Verifique se o arquivo `.env` está na raiz do projeto
- Confirme se a variável está escrita corretamente (case-sensitive)
- Reinicie o servidor após adicionar a variável

### Erro: "Falha ao gerar relatório"
- Verifique se sua chave de API é válida
- Confirme se não excedeu o limite de requisições
- Verifique sua conexão com a internet

## 📚 Recursos Adicionais

- [Documentação Google Gemini](https://ai.google.dev/docs)
- [Google AI Studio](https://makersuite.google.com/)
- [Exemplos de Uso](https://ai.google.dev/examples)

