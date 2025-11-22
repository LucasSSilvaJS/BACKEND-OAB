# 🔍 Sistema de Filtros Robusto para Sessões

## 📋 Visão Geral

O endpoint `GET /api/v1/sessoes` agora possui um sistema robusto de filtros que permite buscar sessões de forma muito flexível e poderosa.

## 🚀 Endpoint

```
GET /api/v1/sessoes
```

## 📊 Parâmetros Disponíveis

### 📄 Paginação

| Parâmetro | Tipo | Padrão | Descrição |
|-----------|------|--------|-----------|
| `skip` | int | 0 | Número de registros a pular |
| `limit` | int | 100 | Número máximo de registros (máx: 1000) |

### 🔍 Filtros

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| `administrador_id` | int (opcional) | Filtrar por ID do administrador |
| `data_inicio_de` | date (opcional) | Sessões iniciadas a partir desta data (YYYY-MM-DD) |
| `data_inicio_ate` | date (opcional) | Sessões iniciadas até esta data (YYYY-MM-DD) |
| `data_finalizacao_de` | date (opcional) | Sessões finalizadas a partir desta data (YYYY-MM-DD) |
| `data_finalizacao_ate` | date (opcional) | Sessões finalizadas até esta data (YYYY-MM-DD) |
| `data_especifica` | date (opcional) | Filtrar por data específica (prioridade sobre data_inicio) |
| `ip_computador` | string (opcional) | Buscar por IP (busca parcial, case-insensitive) |
| `apenas_ativas` | bool (opcional) | Apenas sessões ativas (True) ou todas (False/None) |

### 📈 Ordenação

| Parâmetro | Tipo | Padrão | Valores | Descrição |
|-----------|------|--------|---------|-----------|
| `ordenar_por_data` | string | `mais_recente` | `mais_recente` ou `mais_antiga` | Ordenar por data de início |
| `ordenar_por_usuario` | bool | `false` | `true` ou `false` | Ordenar alfabeticamente por nome do usuário |

**Nota:** Se `ordenar_por_usuario=true`, a ordenação por data será ignorada.

## 💡 Exemplos de Uso

### 1. Paginação Básica

```http
GET /api/v1/sessoes?skip=0&limit=50
```

### 2. Filtrar por Administrador

```http
GET /api/v1/sessoes?administrador_id=1
```

### 3. Filtrar por Data Específica

```http
GET /api/v1/sessoes?data_especifica=2025-11-22
```

### 4. Filtrar por Intervalo de Datas de Início

```http
GET /api/v1/sessoes?data_inicio_de=2025-11-01&data_inicio_ate=2025-11-30
```

### 5. Filtrar por Intervalo de Datas de Finalização

```http
GET /api/v1/sessoes?data_finalizacao_de=2025-11-01&data_finalizacao_ate=2025-11-30
```

### 6. Apenas Sessões Ativas

```http
GET /api/v1/sessoes?apenas_ativas=true
```

### 7. Buscar por IP do Computador

```http
GET /api/v1/sessoes?ip_computador=192.168.1.100
```

**Busca parcial:** Você pode buscar apenas parte do IP:
```http
GET /api/v1/sessoes?ip_computador=192.168
```

### 8. Ordenar da Mais Antiga para Mais Recente

```http
GET /api/v1/sessoes?ordenar_por_data=mais_antiga
```

### 9. Ordenar por Nome do Usuário (Alfabética)

```http
GET /api/v1/sessoes?ordenar_por_usuario=true
```

### 10. Combinação de Filtros

Exemplo completo com múltiplos filtros:

```http
GET /api/v1/sessoes?apenas_ativas=true&data_inicio_de=2025-11-01&administrador_id=1&ordenar_por_usuario=true&limit=50
```

Este exemplo busca:
- ✅ Apenas sessões ativas
- ✅ Iniciadas a partir de 01/11/2025
- ✅ Do administrador ID 1
- ✅ Ordenadas alfabeticamente por nome do usuário
- ✅ Máximo de 50 resultados

### 11. Sessões Finalizadas em um Período

```http
GET /api/v1/sessoes?data_finalizacao_de=2025-11-01&data_finalizacao_ate=2025-11-30&apenas_ativas=false
```

## 🎯 Casos de Uso Comuns

### Dashboard de Sessões Ativas

```http
GET /api/v1/sessoes?apenas_ativas=true&ordenar_por_data=mais_recente&limit=100
```

### Relatório Mensal

```http
GET /api/v1/sessoes?data_inicio_de=2025-11-01&data_inicio_ate=2025-11-30&ordenar_por_data=mais_antiga
```

### Buscar Sessões de um Computador Específico

```http
GET /api/v1/sessoes?ip_computador=192.168.1.100&ordenar_por_data=mais_recente
```

### Lista de Usuários com Sessões Ativas

```http
GET /api/v1/sessoes?apenas_ativas=true&ordenar_por_usuario=true
```

## ⚠️ Regras e Prioridades

1. **Filtro de Data Específica:** Se `data_especifica` for fornecido, os filtros `data_inicio_de` e `data_inicio_ate` serão ignorados.

2. **Ordenação por Usuário:** Se `ordenar_por_usuario=true`, o parâmetro `ordenar_por_data` será ignorado.

3. **Filtros Combinados:** Todos os filtros podem ser combinados usando o operador `&` (E lógico).

4. **Paginação:** Sempre aplicada no final, após todos os filtros e ordenações.

## 📝 Resposta da API

A resposta segue o schema `SessaoResponse` e inclui todas as informações da sessão, incluindo:
- Dados da sessão (data, início, fim, status)
- Informações do computador
- Informações do usuário
- Informações da sala coworking
- Informações da unidade e subseccional

```json
[
  {
    "sessao_id": 1,
    "data": "2025-11-22",
    "inicio_de_sessao": "2025-11-22T10:00:00",
    "final_de_sessao": null,
    "ativado": true,
    "computador_id": 5,
    "usuario_id": 10,
    "administrador_id": 2,
    "sala_coworking": {
      "coworking_id": 3,
      "nome_da_sala": "Sala A"
    },
    "unidade": {
      "unidade_id": 7,
      "nome": "Unidade Centro"
    },
    "subsecional": {
      "subsecional_id": 4,
      "nome": "Subseccional Norte"
    }
  }
]
```

## 🔒 Autenticação

Todos os endpoints requerem autenticação. Inclua o token no header:

```
Authorization: Bearer {seu_token_jwt}
```

## 🧪 Testando no Swagger

1. Acesse `http://localhost:8000/docs`
2. Encontre o endpoint `GET /api/v1/sessoes`
3. Clique em "Try it out"
4. Preencha os parâmetros desejados
5. Clique em "Execute"

## 💻 Exemplo em Python

```python
import requests

url = "http://localhost:8000/api/v1/sessoes"
headers = {"Authorization": "Bearer seu_token_aqui"}
params = {
    "apenas_ativas": True,
    "data_inicio_de": "2025-11-01",
    "ordenar_por_usuario": True,
    "limit": 50
}

response = requests.get(url, headers=headers, params=params)
sessoes = response.json()

for sessao in sessoes:
    print(f"Sessão {sessao['sessao_id']}: {sessao['sala_coworking']['nome_da_sala']}")
```

## 🌐 Exemplo em JavaScript/TypeScript

```javascript
const url = new URL('http://localhost:8000/api/v1/sessoes');
url.searchParams.append('apenas_ativas', 'true');
url.searchParams.append('data_inicio_de', '2025-11-01');
url.searchParams.append('ordenar_por_usuario', 'true');
url.searchParams.append('limit', '50');

const response = await fetch(url, {
  headers: {
    'Authorization': 'Bearer seu_token_aqui'
  }
});

const sessoes = await response.json();
console.log(sessoes);
```

## 🎨 Frontend - React Example

```jsx
import { useState, useEffect } from 'react';

function SessoesList({ filtros }) {
  const [sessoes, setSessoes] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const params = new URLSearchParams(filtros);
    
    fetch(`/api/v1/sessoes?${params}`, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      }
    })
      .then(res => res.json())
      .then(data => {
        setSessoes(data);
        setLoading(false);
      });
  }, [filtros]);

  if (loading) return <div>Carregando...</div>;

  return (
    <div>
      {sessoes.map(sessao => (
        <div key={sessao.sessao_id}>
          <h3>{sessao.sala_coworking.nome_da_sala}</h3>
          <p>Usuário: {sessao.usuario.nome}</p>
          <p>Data: {sessao.data}</p>
        </div>
      ))}
    </div>
  );
}
```

---

**Última atualização:** 22/11/2025

