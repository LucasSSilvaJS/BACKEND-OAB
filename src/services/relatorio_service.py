import os
from typing import Dict
from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from google import genai

from src.repositories.dashboard_repository import DashboardRepository
from src.repositories.subsecional_repository import SubsecionalRepository
from src.repositories.unidade_repository import UnidadeRepository
from src.repositories.sala_coworking_repository import SalaCoworkingRepository
from src.schemas.relatorio import RelatorioRequest, RelatorioResponse
from src.schemas.dashboard import DashboardFiltros


class RelatorioService:
    def __init__(self, db: Session):
        self.db = db
        self.dashboard_repo = DashboardRepository(db)
        self.subsecional_repo = SubsecionalRepository(db)
        self.unidade_repo = UnidadeRepository(db)
        self.sala_repo = SalaCoworkingRepository(db)
        
        # Configurar Gemini API (nova sintaxe oficial)
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="GEMINI_API_KEY não configurada no arquivo .env"
            )
        # Usar o novo cliente da API Gemini
        self.client = genai.Client(api_key=api_key)

    def _validar_e_obter_dados(self, request: RelatorioRequest) -> Dict:
        """Valida e obtém os dados necessários para o relatório"""
        # Validar subseccional
        subsecional = self.subsecional_repo.get_by_id(request.subsecional_id)
        if not subsecional:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Subseccional não encontrada"
            )
        
        # Validar unidade
        unidade = self.unidade_repo.get_by_id(request.unidade_id)
        if not unidade:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Unidade não encontrada"
            )
        
        if unidade.subsecional_id != request.subsecional_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A unidade não pertence à subseccional informada"
            )
        
        # Validar sala coworking
        sala = self.sala_repo.get_by_id(request.coworking_id)
        if not sala:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Sala de coworking não encontrada"
            )
        
        if sala.unidade_id != request.unidade_id or sala.subsecional_id != request.subsecional_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A sala de coworking não pertence à unidade e subseccional informadas"
            )
        
        # Obter dados do dashboard
        sessoes_ativas = self.dashboard_repo.contar_sessoes_ativas(request.coworking_id)
        total_sessoes = self.dashboard_repo.contar_total_sessoes(request.coworking_id)
        pico_acesso = self.dashboard_repo.obter_pico_acesso(request.coworking_id)
        coworking_mais_utilizado = self.dashboard_repo.obter_coworking_mais_utilizado(
            request.subsecional_id,
            request.unidade_id
        )
        frequencia_mensal = self.dashboard_repo.obter_frequencia_mensal(request.coworking_id)
        
        return {
            "subsecional": subsecional,
            "unidade": unidade,
            "sala": sala,
            "sessoes_ativas": sessoes_ativas,
            "total_sessoes": total_sessoes,
            "pico_acesso": pico_acesso,
            "coworking_mais_utilizado": coworking_mais_utilizado,
            "frequencia_mensal": frequencia_mensal
        }

    def _criar_prompt(self, dados: Dict, analista_nome: str, analista_id: int) -> str:
        """Cria o prompt para o LLM com base nos dados coletados"""
        subsecional = dados["subsecional"]
        unidade = dados["unidade"]
        sala = dados["sala"]
        
        # Formatar dados de frequência mensal
        frequencia_texto = ""
        if dados["frequencia_mensal"]:
            meses = {
                1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril",
                5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto",
                9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"
            }
            frequencia_texto = "\n".join([
                f"- {meses.get(f['mes'], f['mes'])}/{f['ano']}: {f['total_sessoes']} sessões"
                for f in dados["frequencia_mensal"]
            ])
        
        # Formatar pico de acesso
        pico_texto = "Não há dados de pico de acesso disponíveis"
        if dados["pico_acesso"]:
            hora_pico, quantidade = dados["pico_acesso"]
            pico_texto = f"{hora_pico.strftime('%d/%m/%Y às %H:%M')} com {quantidade} sessões"
        
        # Formatar coworking mais utilizado
        coworking_texto = "Não há dados de comparação disponíveis"
        if dados["coworking_mais_utilizado"]:
            coworking_texto = f"{dados['coworking_mais_utilizado']['nome_da_sala']} com {dados['coworking_mais_utilizado']['total_sessoes']} sessões"
        
        data_hora_atual = datetime.now().strftime('%d/%m/%Y às %H:%M')
        
        prompt = f"""
Você é um assistente especializado em análise de dados de salas de coworking da OAB (Ordem dos Advogados do Brasil).

**CONTEXTO DO PROJETO:**
A OAB possui um sistema de gerenciamento de salas de coworking espalhadas por diversas subsecionais e unidades no Brasil. 
Cada sala contém computadores que são utilizados por advogados mediante sessões controladas. 
O sistema monitora o uso desses computadores, registrando início e fim de sessões, picos de acesso, e padrões de utilização.

**INFORMAÇÕES DO RELATÓRIO:**
- **Gerado por:** {analista_nome} (Analista de TI - ID: {analista_id})
- **Data e Hora:** {data_hora_atual}
- **Tipo:** Análise Técnica de Uso de Sala Coworking

**DADOS DA SALA DE COWORKING:**

**📍 Localização:**
- **Subseccional:** {subsecional.nome} (ID: {subsecional.subsecional_id})
- **Unidade:** {unidade.nome} (ID: {unidade.unidade_id})
- **Hierarquia da Unidade:** {unidade.hierarquia.value}
- **Sala de Coworking:** {sala.nome_da_sala} (ID: {sala.coworking_id})

**📊 Métricas de Uso:**
- **Sessões Ativas no Momento:** {dados['sessoes_ativas']}
- **Total Histórico de Sessões:** {dados['total_sessoes']}
- **Pico de Acesso Registrado:** {pico_texto}
- **Coworking Mais Utilizado na Unidade:** {coworking_texto}

**📅 Frequência de Uso Mensal:**
{frequencia_texto if frequencia_texto else "Não há dados históricos de frequência mensal disponíveis"}

**INSTRUÇÕES PARA O RELATÓRIO:**

1. **Estrutura do Relatório (OBRIGATÓRIA):**
   - Cabeçalho com título, data/hora e informações do analista
   - Seção de informações da sala (localização completa)
   - Sumário executivo (breve resumo dos principais insights)
   - Análise detalhada de métricas
   - Padrões identificados e tendências
   - Comparativo com outras salas (se houver dados)
   - Recomendações práticas e acionáveis
   - Conclusão e próximos passos

2. **Análise Esperada:**
   - Interprete os dados de forma profissional e técnica
   - Calcule percentuais e taxas quando possível
   - Identifique padrões de uso (horários de pico, meses mais movimentados)
   - Compare o desempenho desta sala com outras na unidade
   - Identifique possíveis problemas ou oportunidades de melhoria
   - Analise a sazonalidade do uso (se houver dados mensais)

3. **Recomendações:**
   - Sejam específicas e acionáveis
   - Considerem aspectos de manutenção, horários de funcionamento e recursos
   - Incluam prazos estimados quando relevante
   - Priorizem as recomendações por impacto

4. **Formato:**
   - Use Markdown com títulos (##), subtítulos (###), listas e tabelas
   - Inclua emojis relevantes para tornar o relatório mais visual
   - Crie tabelas para comparações quando apropriado
   - Use negrito e itálico para destacar informações importantes
   - Seja conciso mas completo

**IMPORTANTE:** 
- Comece o relatório com um cabeçalho contendo as informações do analista e data/hora
- Inclua TODAS as informações fornecidas acima no relatório
- Seja profissional e técnico na linguagem

Gere o relatório completo em Markdown AGORA:
"""
        return prompt

    def gerar_relatorio(self, request: RelatorioRequest, analista_nome: str, analista_id: int) -> RelatorioResponse:
        """Gera o relatório usando Google Gemini"""
        try:
            # Validar e obter dados
            dados = self._validar_e_obter_dados(request)
            
            # Criar prompt
            prompt = self._criar_prompt(dados, analista_nome, analista_id)
            
            # Gerar relatório com Gemini usando a nova API
            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            
            if not response.text:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Falha ao gerar relatório. O modelo não retornou conteúdo."
                )
            
            return RelatorioResponse(
                markdown=response.text,
                subsecional_id=request.subsecional_id,
                subsecional_nome=dados["subsecional"].nome,
                unidade_id=request.unidade_id,
                unidade_nome=dados["unidade"].nome,
                unidade_hierarquia=dados["unidade"].hierarquia.value,
                coworking_id=request.coworking_id,
                coworking_nome=dados["sala"].nome_da_sala,
                gerado_por=analista_nome,
                gerado_por_id=analista_id,
                data_geracao=datetime.now(),
                total_sessoes=dados["total_sessoes"],
                sessoes_ativas=dados["sessoes_ativas"]
            )
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro ao gerar relatório: {str(e)}"
            )

