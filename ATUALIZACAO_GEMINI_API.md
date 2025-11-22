# 🔄 Atualização para Nova API do Gemini

## ⚠️ AÇÃO NECESSÁRIA

O código foi atualizado para usar a **nova API oficial do Google Gemini** conforme a [documentação oficial](https://ai.google.dev/gemini-api/docs/quickstart?hl=pt-br).

## 📋 O que mudou?

### Biblioteca Antiga ❌
```python
import google.generativeai as genai

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.5-flash')
response = model.generate_content(prompt)
```

### Nova Biblioteca Oficial ✅
```python
from google import genai

client = genai.Client(api_key=api_key)
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt
)
```

## 🔧 Como Atualizar

### 1. Desinstalar a biblioteca antiga
```bash
pip uninstall google-generativeai
```

### 2. Instalar a nova biblioteca oficial
```bash
pip install google-genai
```

### 3. Ou atualizar todas as dependências
```bash
pip install -r requirements.txt --upgrade
```

## ✅ Verificar Instalação

Teste se a nova biblioteca está instalada corretamente:

```bash
python -c "from google import genai; print('Gemini API instalada corretamente!')"
```

Você deve ver a mensagem: `Gemini API instalada corretamente!`

## 📦 Dependências Atualizadas

O arquivo `requirements.txt` foi atualizado de:
```txt
google-generativeai>=0.3.0  # ❌ Antiga
```

Para:
```txt
google-genai>=1.0.0  # ✅ Nova e oficial
```

## 🚀 Benefícios da Nova API

- ✅ **API Oficial** - Suportada diretamente pelo Google
- ✅ **Mais Estável** - Menos mudanças breaking
- ✅ **Melhor Performance** - Otimizações internas
- ✅ **Documentação Atualizada** - Alinhada com a documentação oficial
- ✅ **Compatível com Gemini 2.5 Flash** - Última versão do modelo

## 🔍 Arquivos Modificados

1. **`src/services/relatorio_service.py`** - Atualizado para nova API
2. **`requirements.txt`** - Biblioteca atualizada
3. **`CONFIGURACAO_GEMINI.md`** - Documentação atualizada

## 🧪 Testando

Após atualizar, teste o endpoint de relatórios:

```bash
POST /api/v1/relatorios/gerar
Authorization: Bearer {token_do_analista}

{
  "subsecional_id": 1,
  "unidade_id": 2,
  "coworking_id": 3
}
```

## 📚 Referências

- [Documentação Oficial da API Gemini](https://ai.google.dev/gemini-api/docs/quickstart?hl=pt-br)
- [Guia de Migração](https://ai.google.dev/gemini-api/docs)
- [Repositório GitHub](https://github.com/google/generative-ai-python)

## ⚡ Nota Importante

A variável de ambiente `GEMINI_API_KEY` continua a mesma. Não é necessário alterar o arquivo `.env`.

---

**Última atualização:** 22/11/2025

