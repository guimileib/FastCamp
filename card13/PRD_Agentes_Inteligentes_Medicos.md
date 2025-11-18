# PRD - Protótipo de Agentes Inteligentes para Área Médica
## Product Requirements Document

---

## 1. Visão Geral do Projeto

### 1.1 Objetivo
Desenvolver um protótipo de sistema baseado em agentes inteligentes utilizando Google ADK (Agent Development Kit) para extrair insights valiosos, automatizar tarefas e melhorar a tomada de decisão na área médica.

### 1.2 Escopo
- Prototipagem rápida com foco em demonstração de capacidades
- Implementação usando Google ADK
- Integração com base de dados médica
- Sistema de agentes inteligentes colaborativos

---

## 2. Definição do Problema

### 2.1 Contexto
A área médica gera grandes volumes de dados que precisam ser analisados para:
- Apoiar decisões clínicas
- Identificar padrões em dados de pacientes
- Automatizar tarefas administrativas e de triagem
- Extrair insights de registros médicos

### 2.2 Desafios
- Volume massivo de dados não estruturados
- Necessidade de respostas rápidas e precisas
- Integração de múltiplas fontes de informação
- Suporte à decisão médica baseada em evidências

---

## 3. Seleção da Base de Dados

### 3.1 Bases de Dados Selecionadas

#### 3.1.1 **Medical Transcriptions Dataset** (PRIMÁRIA)
**Fonte:** https://www.kaggle.com/datasets/tboyle10/medicaltranscriptions/data

**Características:**
- **Tamanho:** 17.01 MB (mtsamples.csv)
- **Estrutura:** 6 colunas de dados textuais
- **Conteúdo:** Transcrições médicas reais de diversas especialidades
- **Origem:** Dados raspados de mtsamples.com
- **Licença:** CC0: Public Domain
- **Downloads:** 23.5K+ (alta popularidade)
- **Usabilidade Score:** 8.53/10

**Colunas do Dataset:**
- `description`: Descrição do caso
- `medical_specialty`: Especialidade médica (ex: Cardiologia, Neurologia)
- `sample_name`: Nome da amostra/procedimento
- `transcription`: Texto completo da transcrição médica
- `keywords`: Palavras-chave relevantes
- `age`: Idade do paciente (quando disponível)

**Casos de Uso Ideais:**
- Classificação automática de especialidades médicas
- Extração de informações clínicas de texto não estruturado
- Sumarização de transcrições médicas
- Identificação de procedimentos e diagnósticos
- Análise de padrões de linguagem médica

**Vantagens para o Projeto:**
✅ Dados reais e representativos da prática clínica
✅ Múltiplas especialidades médicas cobertas
✅ Textos completos permitem análise contextual profunda
✅ Ideal para NLP e processamento de linguagem natural
✅ Tamanho adequado para prototipagem rápida

#### 3.1.2 **200k Medical Research Paper Abstracts** (SECUNDÁRIA)
**Fonte:** https://www.kaggle.com/datasets/anshulmehtakaggl/200000-abstracts-for-seq-sentence-classification

**Características:**
- **Tamanho:** 805.78 MB (train: 357.62 MB, test: 4.74 MB, dev: 4.71 MB)
- **Estrutura:** Sentenças sequencialmente classificadas
- **Conteúdo:** 200.000 abstracts de papers médicos do PubMed
- **Licença:** CC0: Public Domain
- **Downloads:** 1.3K+
- **Usabilidade Score:** 9.38/10

**Classificação de Sentenças:**
- **OBJECTIVE**: Objetivos da pesquisa
- **METHODS**: Metodologia utilizada
- **RESULTS**: Resultados encontrados
- **CONCLUSIONS**: Conclusões do estudo
- **BACKGROUND**: Contextualização/introdução

**Casos de Uso Ideais:**
- Classificação sequencial de sentenças
- Estruturação automática de textos médicos
- Sumarização de literatura científica
- Extração de evidências médicas
- Análise de qualidade de pesquisas

**Vantagens para o Projeto:**
✅ Dataset massivo para treinamento robusto
✅ Estruturação pré-definida facilita análise
✅ Base científica para recomendações baseadas em evidências
✅ Ideal para busca de conhecimento médico
✅ Permite validação de diagnósticos com literatura

### 3.2 Estratégia de Uso Combinado
**RECOMENDAÇÃO: Utilizar ambos os datasets de forma complementar**

**Medical Transcriptions (Foco Clínico):**
- Agente de Triagem e Diagnóstico
- Análise de casos clínicos reais
- Classificação de especialidades
- Extração de sintomas e procedimentos

**Research Abstracts (Foco em Evidências):**
- Agente de Insights e Pesquisa
- Busca de evidências científicas
- Recomendações baseadas em literatura
- Contextualização de diagnósticos

**Integração:**
1. Transcrições fornecem dados clínicos do paciente
2. Abstracts fornecem evidências científicas de suporte
3. Agentes combinam ambas as fontes para decisões informadas

---

## 4. Arquitetura de Agentes Inteligentes

### 4.1 Agentes Propostos

#### 4.1.1 Agente de Triagem e Classificação (Triage Agent)
**Responsabilidades:**
- Analisar transcrições médicas e extrair informações-chave
- Classificar especialidade médica apropriada (baseado em Medical Transcriptions)
- Identificar urgência e prioridade do caso
- Extrair sintomas, procedimentos e diagnósticos mencionados

**Inputs:**
- Transcrição médica (texto livre)
- Descrição de sintomas
- Dados demográficos (idade, quando disponível)

**Outputs:**
- Especialidade médica recomendada (40+ especialidades disponíveis)
- Nível de prioridade (alto/médio/baixo)
- Keywords e termos médicos identificados
- Sumário estruturado da transcrição

**Dataset Utilizado:** Medical Transcriptions
**Modelo de Classificação:** ~40 especialidades médicas diferentes

#### 4.1.2 Agente de Análise Diagnóstica (Diagnostic Agent)
**Responsabilidades:**
- Processar transcrições médicas completas usando NLP
- Identificar entidades médicas (sintomas, doenças, medicamentos)
- Comparar com casos similares na base de 4.999 transcrições
- Extrair relações entre sintomas e diagnósticos
- Sugerir diagnósticos diferenciais

**Inputs:**
- Transcrição médica completa
- Especialidade identificada
- Histórico clínico (quando disponível)
- Resultados de exames mencionados

**Outputs:**
- Diagnósticos mencionados na transcrição
- Casos similares encontrados no dataset
- Procedimentos realizados/recomendados
- Medicamentos prescritos
- Padrões identificados por especialidade

**Dataset Utilizado:** Medical Transcriptions
**Técnicas:** NER (Named Entity Recognition), Similarity Search

#### 4.1.3 Agente de Insights e Pesquisa Científica (Research Insights Agent)
**Responsabilidades:**
- Extrair padrões e tendências de 200k abstracts científicos
- Buscar evidências científicas para diagnósticos
- Classificar sentenças em OBJECTIVE/METHODS/RESULTS/CONCLUSIONS
- Gerar estatísticas sobre especialidades e procedimentos
- Produzir relatórios automatizados baseados em evidências

**Inputs:**
- Consultas em linguagem natural sobre condições médicas
- Diagnóstico ou procedimento para validação
- Parâmetros de busca (especialidade, keywords)

**Outputs:**
- Abstracts relevantes com classificação de sentenças
- Evidências científicas (RESULTS e CONCLUSIONS)
- Estatísticas por especialidade médica
- Visualizações de distribuição de casos
- Tendências em procedimentos médicos
- Correlações entre sintomas e diagnósticos
- Relatórios estruturados em linguagem natural

**Datasets Utilizados:** 
- Medical Transcriptions (estatísticas clínicas)
- 200k Research Abstracts (evidências científicas)

**Capacidades Especiais:**
- Busca semântica em 200.000 papers médicos
- Classificação automática de estrutura de abstracts
- Sumarização de literatura científica

#### 4.1.4 Agente de Estruturação de Texto Médico (Text Structuring Agent)
**NOVO - Baseado em 200k Abstracts Dataset**

**Responsabilidades:**
- Estruturar textos médicos não organizados
- Classificar sentenças em categorias (OBJECTIVE/METHODS/RESULTS/CONCLUSIONS)
- Melhorar legibilidade de transcrições complexas
- Extrair seções-chave de documentos médicos

**Inputs:**
- Texto médico não estruturado (transcrições, notas clínicas)
- Abstracts ou relatórios para organizar

**Outputs:**
- Texto estruturado por seções
- Classificação de cada sentença
- Sumário executivo
- Versão simplificada para pacientes

**Dataset Utilizado:** 200k Research Abstracts
**Modelo:** Sequential Sentence Classification

#### 4.1.5 Agente Coordenador (Orchestrator Agent)
**Responsabilidades:**
- Gerenciar fluxo entre os 4 agentes especializados
- Consolidar informações de múltiplas fontes
- Interagir com o usuário em linguagem natural
- Decidir qual agente acionar baseado na requisição

**Inputs:**
- Requisições do usuário (texto livre ou voz transcrita)
- Respostas de todos os agentes especializados
- Contexto da conversa

**Outputs:**
- Resposta consolidada e coerente
- Recomendações finais baseadas em múltiplos agentes
- Explicações das decisões tomadas
- Próximos passos sugeridos
- Disclaimer médico quando apropriado

**Datasets Utilizados:** Ambos (orquestração)

---

## 5. Requisitos Funcionais

### 5.1 RF-001: Ingestão de Dados
- O sistema DEVE carregar e processar a base de dados médica selecionada
- O sistema DEVE validar a integridade dos dados
- O sistema DEVE normalizar dados quando necessário

### 5.2 RF-002: Análise de Pacientes
- O sistema DEVE aceitar dados de novos pacientes
- O sistema DEVE realizar análise comparativa com a base histórica
- O sistema DEVE gerar scores de risco/probabilidade

### 5.3 RF-003: Extração de Insights
- O sistema DEVE permitir consultas em linguagem natural
- O sistema DEVE gerar visualizações de dados
- O sistema DEVE identificar correlações estatísticas

### 5.4 RF-004: Geração de Relatórios
- O sistema DEVE gerar relatórios automatizados
- O sistema DEVE explicar as recomendações em linguagem clara
- O sistema DEVE citar fontes de dados utilizadas

### 5.5 RF-005: Interface de Usuário
- O sistema DEVE fornecer interface conversacional
- O sistema DEVE aceitar múltiplos formatos de entrada
- O sistema DEVE apresentar resultados de forma estruturada

---

## 6. Requisitos Não Funcionais

### 6.1 RNF-001: Tecnologia
- Implementação obrigatória com **Google ADK**
- Linguagem: Python 3.9+
- Framework de agentes: Google ADK

### 6.2 RNF-002: Performance
- Tempo de resposta < 10 segundos para consultas simples
- Tempo de resposta < 30 segundos para análises complexas
- Suporte a pelo menos 100 registros simultâneos

### 6.3 RNF-003: Usabilidade
- Interface intuitiva e auto-explicativa
- Mensagens de erro claras e acionáveis
- Documentação de uso incluída

### 6.4 RNF-004: Confiabilidade
- Tratamento de erros robusto
- Logs de todas as operações
- Validação de dados de entrada

### 6.5 RNF-005: Ética e Privacidade
- Não armazenar dados sensíveis de pacientes reais
- Usar apenas dados públicos e anonimizados
- Incluir disclaimers sobre uso assistivo (não substitui médico)

---

## 7. Casos de Uso

### 7.1 UC-001: Análise e Classificação de Transcrição Médica
**Ator:** Profissional de Saúde

**Fluxo:**
1. Usuário fornece transcrição médica (texto livre ou áudio transcrito)
2. Agente de Estruturação organiza o texto em seções
3. Agente de Triagem identifica especialidade médica (ex: Cardiologia)
4. Agente Diagnóstico extrai entidades (sintomas, procedimentos, medicamentos)
5. Agente de Insights busca casos similares nas 4.999 transcrições
6. Sistema retorna análise completa estruturada

**Exemplo de Input:**
```
"Paciente masculino de 62 anos com histórico de hipertensão 
e diabetes. Apresenta dor torácica há 3 horas, irradiando 
para braço esquerdo. PA: 160/95. Realizado ECG mostrando 
elevação do segmento ST em derivações anteriores."
```

**Resultado Esperado:**
- Especialidade: **Cardiologia** (confiança: 95%)
- Estrutura:
  - OBJETIVO: Avaliação de dor torácica aguda
  - ACHADOS: Elevação ST, PA elevada
  - CONCLUSÃO: Suspeita de IAM anterior
- Entidades identificadas:
  - Sintomas: dor torácica, irradiação para braço
  - Condições: hipertensão, diabetes
  - Procedimento: ECG
  - Achado: elevação segmento ST
- 12 casos similares encontrados
- Urgência: **ALTA**
- Recomendação: Acionamento de protocolo de IAM

### 7.2 UC-002: Busca de Evidências Científicas
**Ator:** Médico/Pesquisador

**Fluxo:**
1. Usuário consulta: "Quais são as evidências para uso de estatinas em prevenção primária?"
2. Agente Coordenador identifica intenção de pesquisa
3. Agente de Insights busca nos 200k abstracts
4. Sistema filtra papers relevantes
5. Agente de Estruturação extrai RESULTS e CONCLUSIONS
6. Sistema retorna síntese de evidências

**Exemplo de Input:**
```
"Mostre evidências sobre eficácia de metformina em 
pré-diabetes"
```

**Resultado Esperado:**
```
EVIDÊNCIAS CIENTÍFICAS ENCONTRADAS
==================================

15 estudos relevantes encontrados (de 200.000 abstracts)

RESULTADOS PRINCIPAIS:
- Redução de 31% no risco de progressão para diabetes (n=8 estudos)
- Melhora na sensibilidade à insulina (n=12 estudos)
- Redução de HbA1c em média 0.6% (n=10 estudos)

CONCLUSÕES:
Metformina demonstra eficácia em retardar progressão de 
pré-diabetes para diabetes tipo 2, com perfil de segurança 
aceitável.

NÍVEL DE EVIDÊNCIA: Alto (múltiplos RCTs)
GRAU DE RECOMENDAÇÃO: Classe I

Fontes: [15 abstracts PubMed]
```

### 7.2.1 UC-002B: Análise Estatística por Especialidade
**Ator:** Gestor de Saúde/Pesquisador

**Fluxo:**
1. Usuário: "Quais são os procedimentos mais comuns em Cardiologia?"
2. Agente de Insights analisa Medical Transcriptions
3. Sistema agrega dados por especialidade
4. Gera visualizações e estatísticas

**Resultado Esperado:**
- Top 10 procedimentos em Cardiologia
- Distribuição por faixa etária
- Keywords mais frequentes
- Gráficos de tendências

### 7.3 UC-003: Sugestão de Diagnóstico Diferencial
**Ator:** Médico

**Fluxo:**
1. Usuário apresenta caso clínico
2. Agente Diagnóstico busca casos similares
3. Sistema analisa padrões e correlações
4. Retorna diagnósticos diferenciais ranqueados

**Resultado Esperado:**
- Lista de diagnósticos com probabilidades
- Evidências de suporte
- Exames sugeridos

### 7.4 UC-004: Geração de Relatório Epidemiológico
**Ator:** Gestor de Saúde

**Fluxo:**
1. Usuário solicita relatório sobre condição específica
2. Agente de Insights agrega dados
3. Sistema gera visualizações
4. Relatório em PDF/texto é produzido

**Resultado Esperado:**
- Relatório estruturado
- Gráficos e tabelas
- Conclusões e recomendações

---

## 8. Arquitetura Técnica

### 8.1 Componentes do Sistema

```
┌─────────────────────────────────────────────┐
│         Interface do Usuário (CLI/Web)      │
└────────────────┬────────────────────────────┘
                 │
┌────────────────▼────────────────────────────┐
│        Agente Coordenador (ADK)             │
│  - Roteamento de requisições                │
│  - Consolidação de respostas                │
└────┬───────────┬───────────┬────────────────┘
     │           │           │
┌────▼────┐ ┌───▼─────┐ ┌──▼──────────┐
│ Agente  │ │ Agente  │ │   Agente    │
│ Triagem │ │Diagnóst.│ │  Insights   │
└────┬────┘ └───┬─────┘ └──┬──────────┘
     │          │           │
     └──────────┴───────────┘
                 │
┌────────────────▼────────────────────────────┐
│      Camada de Dados                        │
│  - Pandas DataFrames                        │
│  - SQL/SQLite                               │
│  - Cache em memória                         │
└────────────────┬────────────────────────────┘
                 │
┌────────────────▼────────────────────────────┐
│      Base de Dados Médica                   │
│  (CSV/JSON/Database)                        │
└─────────────────────────────────────────────┘
```

### 8.2 Preparação dos Datasets

#### 8.2.1 Medical Transcriptions Dataset

**Download e Carregamento:**
```python
import pandas as pd

# Carregar dataset principal
df_transcriptions = pd.read_csv('mtsamples.csv')

# Estrutura esperada:
# - description: str
# - medical_specialty: str (40 especialidades)
# - sample_name: str
# - transcription: str (texto completo)
# - keywords: str (separadas por vírgula)
```

**Pré-processamento:**
1. Limpeza de textos (remoção de caracteres especiais)
2. Normalização de especialidades médicas
3. Tratamento de valores nulos
4. Extração de entidades médicas com NER
5. Criação de embeddings para busca semântica

**Indexação:**
- Criar índice vetorial para busca rápida de casos similares
- Indexar por especialidade, keywords, e idade
- Cache de embeddings para performance

#### 8.2.2 200k Research Abstracts Dataset

**Download e Carregamento:**
```python
# Dataset vem em formato TXT com estrutura específica
# train.txt (357 MB) - para treinamento
# test.txt (4.7 MB) - para testes
# dev.txt (4.7 MB) - para validação

# Formato de cada linha:
# {"sentence": "texto", "label": "OBJECTIVE/METHODS/RESULTS/CONCLUSIONS"}
```

**Pré-processamento:**
1. Parse de arquivos TXT para estrutura JSON
2. Agrupamento de sentenças por abstract
3. Criação de índice de busca semântica
4. Embedding de abstracts completos
5. Indexação por termos médicos-chave

**Otimizações:**
- Usar apenas subset para prototipagem inicial (ex: 20k abstracts)
- Criar cache de buscas frequentes
- Pré-computar embeddings dos abstracts

### 8.3 Stack Tecnológico

**Core:**
- Python 3.9+
- Google ADK (Agent Development Kit)
- Google AI (Gemini API)

**Processamento de Dados:**
- Pandas (manipulação de CSV)
- NumPy (operações numéricas)
- Scikit-learn (classificação de especialidades, clustering de casos similares)

**NLP e Processamento de Texto:**
- Transformers / Hugging Face (models pré-treinados médicos)
- spaCy (com modelo sci-spacy para NER médico)
- NLTK (tokenização e processamento básico)
- Sentence-Transformers (embeddings semânticos para busca)
- SciBERT ou BioBERT (modelos especializados em textos médicos)

**Visualização:**
- Matplotlib
- Seaborn
- Plotly (opcional)

**Interface:**
- Streamlit (para web) OU
- Rich (para CLI)
- Gradio (alternativa)

**Utilities:**
- Python-dotenv (variáveis de ambiente)
- Loguru (logging)
- Pydantic (validação de dados)

---

## 9. Fluxo de Dados

### 9.1 Pipeline de Processamento

```
Input do Usuário
    ↓
[Validação e Parsing]
    ↓
[Agente Coordenador]
    ↓
[Identificação de Intenção]
    ↓
┌───────────────┬───────────────┬──────────────┐
│               │               │              │
[Triagem]   [Diagnóstico]  [Insights]
│               │               │              │
└───────────────┴───────────────┴──────────────┘
    ↓
[Consolidação de Resultados]
    ↓
[Formatação de Resposta]
    ↓
Output para Usuário
```

### 9.2 Exemplo de Interação

**Input:**
```
"Analise um paciente de 55 anos, sexo masculino, com 
pressão arterial 160/100, colesterol 240 mg/dL, e 
histórico familiar de doença cardíaca."
```

**Processamento:**
1. Coordenador identifica: análise de risco cardíaco
2. Agente Triagem: calcula score inicial
3. Agente Diagnóstico: busca padrões similares
4. Agente Insights: compara com estatísticas da base

**Output:**
```
ANÁLISE DE RISCO CARDIOVASCULAR
================================

Score de Risco: 72/100 (ALTO)

Fatores de Risco Identificados:
- Hipertensão arterial (PA: 160/100)
- Hipercolesterolemia (240 mg/dL)
- Histórico familiar positivo
- Idade > 50 anos

Diagnósticos Prováveis:
1. Risco elevado de doença coronariana (85%)
2. Hipertensão essencial (90%)
3. Dislipidemia (95%)

Recomendações:
- Consulta cardiológica urgente
- Exames: ECG, teste ergométrico, perfil lipídico completo
- Avaliação para início de terapia anti-hipertensiva
- Modificações no estilo de vida

Base: 156 casos similares analisados
```

---

## 10. Implementação com Google ADK

### 10.1 Estrutura de Agentes ADK

```python
# Pseudocódigo da estrutura

from google.generativeai import adk

# Definição de Agente de Triagem
triage_agent = adk.Agent(
    name="TriageAgent",
    model="gemini-2.0-flash-exp",
    instructions="""
    Você é um agente de triagem médica.
    Analise os dados do paciente e classifique o nível de urgência.
    Retorne um score de 0-100 e justificativa.
    """,
    tools=[analyze_vital_signs, calculate_risk_score]
)

# Definição de Agente Diagnóstico
diagnostic_agent = adk.Agent(
    name="DiagnosticAgent",
    model="gemini-2.0-flash-exp",
    instructions="""
    Você é um agente de análise diagnóstica.
    Compare dados do paciente com a base histórica.
    Sugira diagnósticos prováveis com probabilidades.
    """,
    tools=[search_similar_cases, analyze_patterns]
)

# Agente Coordenador
orchestrator = adk.Agent(
    name="OrchestratorAgent",
    model="gemini-2.0-flash-exp",
    instructions="""
    Você coordena os outros agentes.
    Distribua tarefas e consolide respostas.
    """,
    agents=[triage_agent, diagnostic_agent, insights_agent]
)
```

### 10.2 Ferramentas (Tools) Necessárias

**Tool 1: Busca em Transcrições Médicas**
```python
def search_medical_transcriptions(
    query: str, 
    specialty: str = None,
    top_k: int = 5
) -> List[dict]:
    """
    Busca casos similares nas 4.999 transcrições médicas.
    Usa similarity search com embeddings.
    
    Returns:
    - transcription_id
    - similarity_score
    - medical_specialty
    - transcription_text
    - keywords
    """
    pass
```

**Tool 2: Classificação de Especialidade Médica**
```python
def classify_medical_specialty(transcription: str) -> dict:
    """
    Classifica transcrição em uma das 40 especialidades médicas.
    Dataset: Medical Transcriptions
    
    Returns:
    - specialty: str
    - confidence: float
    - top_3_alternatives: List[tuple]
    """
    pass
```

**Tool 3: Extração de Entidades Médicas (NER)**
```python
def extract_medical_entities(text: str) -> dict:
    """
    Extrai entidades médicas do texto usando spaCy sci-spacy.
    
    Returns:
    - symptoms: List[str]
    - diseases: List[str]
    - medications: List[str]
    - procedures: List[str]
    - anatomy: List[str]
    """
    pass
```

**Tool 4: Busca em Literatura Científica**
```python
def search_scientific_literature(
    query: str,
    section_filter: List[str] = None,  # ['RESULTS', 'CONCLUSIONS']
    top_k: int = 10
) -> List[dict]:
    """
    Busca nos 200k abstracts científicos.
    
    Returns:
    - abstract_id
    - relevance_score
    - sentences_by_category: dict
    - summary: str
    """
    pass
```

**Tool 5: Classificação de Sentenças em Abstracts**
```python
def classify_abstract_sentences(text: str) -> List[dict]:
    """
    Classifica cada sentença como OBJECTIVE/METHODS/RESULTS/CONCLUSIONS.
    Dataset: 200k Research Abstracts
    
    Returns:
    - sentence: str
    - label: str
    - confidence: float
    """
    pass
```

**Tool 6: Estatísticas por Especialidade**
```python
def get_specialty_statistics(specialty: str) -> dict:
    """
    Retorna estatísticas agregadas sobre uma especialidade.
    Dataset: Medical Transcriptions
    
    Returns:
    - total_cases: int
    - common_procedures: List[str]
    - age_distribution: dict
    - top_keywords: List[str]
    - related_specialties: List[str]
    """
    pass
```

**Tool 7: Estruturação de Texto Médico**
```python
def structure_medical_text(text: str) -> dict:
    """
    Organiza texto médico não estruturado em seções.
    
    Returns:
    - structured_text: dict (por seção)
    - summary: str
    - key_points: List[str]
    - simplified_version: str (para pacientes)
    """
    pass
```

**Tool 8: Geração de Visualizações**
```python
def generate_medical_visualization(
    data: pd.DataFrame, 
    chart_type: str,
    specialty: str = None
) -> str:
    """
    Gera gráficos específicos para dados médicos.
    
    Tipos suportados:
    - specialty_distribution
    - age_distribution
    - procedure_frequency
    - keyword_cloud
    
    Returns: caminho do arquivo da imagem
    """
    pass
```

---

## 11. Métricas de Sucesso

### 11.1 Métricas Técnicas
- [ ] Sistema processa consultas em < 10 segundos (90% dos casos)
- [ ] Taxa de erro < 5%
- [ ] Cobertura de testes > 70%
- [ ] 4 agentes implementados e funcionais

### 11.2 Métricas de Qualidade

**Classificação de Especialidades (Medical Transcriptions):**
- [ ] Acurácia > 85% na classificação de especialidades médicas
- [ ] F1-Score > 0.80 para especialidades principais
- [ ] Top-3 accuracy > 95%

**NER - Extração de Entidades:**
- [ ] Precisão > 80% na identificação de sintomas
- [ ] Recall > 75% para medicamentos e procedimentos
- [ ] F1-Score > 0.75 para entidades médicas

**Classificação de Sentenças (Research Abstracts):**
- [ ] Acurácia > 90% para OBJECTIVE/METHODS/RESULTS/CONCLUSIONS
- [ ] Macro F1-Score > 0.88 (benchmark do paper SkimLit)

**Busca Semântica:**
- [ ] Top-5 relevance > 80% (casos similares relevantes)
- [ ] Latência < 2 segundos para busca em 200k abstracts

**Qualidade Geral:**
- [ ] Insights gerados são clinicamente relevantes (avaliação qualitativa)
- [ ] Recomendações são compreensíveis para profissionais de saúde
- [ ] Sistema fornece explicações para suas conclusões
- [ ] Citations corretas de fontes (transcrições ou abstracts)

### 11.3 Métricas de Entrega
- [ ] Protótipo funcional em 2-3 semanas
- [ ] Documentação completa
- [ ] Demo executável
- [ ] Código versionado no GitHub

---

## 12. Entregáveis

### 12.1 Código
- [ ] Repositório GitHub organizado
- [ ] Código-fonte comentado
- [ ] Requirements.txt com dependências
- [ ] .env.example com variáveis necessárias

### 12.2 Documentação
- [ ] README.md com instruções de instalação
- [ ] Documentação de arquitetura
- [ ] Guia de uso dos agentes
- [ ] Exemplos de consultas

### 12.3 Demo
- [ ] Interface funcional (CLI ou Web)
- [ ] Dataset de exemplo incluído
- [ ] Scripts de demonstração
- [ ] Vídeo/apresentação mostrando funcionalidades

### 12.4 Testes
- [ ] Testes unitários dos agentes
- [ ] Testes de integração
- [ ] Casos de teste documentados
- [ ] Resultados de testes incluídos

---

## 13. Cronograma Sugerido

### Semana 1: Setup e Fundação
- **Dias 1-2:** 
  - Configuração do ambiente Python 3.9+
  - Instalação do Google ADK e Gemini API
  - Download dos 2 datasets do Kaggle:
    * Medical Transcriptions (17 MB)
    * 200k Research Abstracts (usar subset inicial de 20k)
  - Instalação de bibliotecas NLP (spaCy, transformers, sci-spacy)
  
- **Dias 3-4:**
  - **EDA - Medical Transcriptions:**
    * Análise das 40 especialidades médicas
    * Distribuição de casos por especialidade
    * Análise de keywords e termos frequentes
    * Identificação de padrões em transcrições
  - **EDA - Research Abstracts:**
    * Análise da distribuição OBJECTIVE/METHODS/RESULTS/CONCLUSIONS
    * Comprimento médio de sentenças por categoria
    * Tópicos médicos mais frequentes
  - Definição final dos 5 agentes
  - Setup da estrutura do projeto

- **Dias 5-7:**
  - Implementação do primeiro agente (Insights)
  - Criação das ferramentas básicas
  - Testes iniciais

### Semana 2: Desenvolvimento Core
- **Dias 8-10:**
  - Implementação do Agente de Triagem
  - Implementação do Agente Diagnóstico
  - Integração com base de dados

- **Dias 11-12:**
  - Implementação do Agente Coordenador
  - Sistema de roteamento entre agentes
  - Testes de integração

- **Dias 13-14:**
  - Interface do usuário
  - Polimento e ajustes
  - Testes end-to-end

### Semana 3: Finalização
- **Dias 15-17:**
  - Documentação completa
  - Casos de uso detalhados
  - Preparação da demo

- **Dias 18-19:**
  - Testes finais
  - Correção de bugs
  - Otimizações

- **Dias 20-21:**
  - Apresentação final
  - Vídeo demonstrativo
  - Entrega do projeto

---

## 14. Riscos e Mitigações

### 14.1 Riscos Técnicos

| Risco | Probabilidade | Impacto | Mitigação |
|-------|---------------|---------|-----------|
| Dificuldade com Google ADK | Média | Alto | Estudar documentação antecipadamente, ter plano B com LangChain |
| Base de dados inadequada | Baixa | Alto | Validar base antes de iniciar desenvolvimento |
| Performance insatisfatória | Média | Médio | Implementar caching, otimizar consultas |
| API Gemini instável | Baixa | Alto | Implementar retry logic, fallbacks |

### 14.2 Riscos de Prazo

| Risco | Probabilidade | Impacto | Mitigação |
|-------|---------------|---------|-----------|
| Complexidade subestimada | Alta | Médio | Priorizar MVPs, cortar features não-essenciais |
| Bloqueios técnicos | Média | Alto | Manter comunicação, buscar ajuda early |
| Escopo aumentado | Média | Médio | Definir claramente MVP, resistir a feature creep |

---

## 15. Critérios de Aceitação

### 15.1 Funcional
✅ O sistema DEVE:
- Processar dados de pelo menos uma base médica pública
- Implementar no mínimo 3 agentes inteligentes com Google ADK
- Gerar insights a partir de consultas em linguagem natural
- Apresentar recomendações com justificativas
- Funcionar de forma demonstrável

### 15.2 Técnico
✅ O código DEVE:
- Estar versionado no Git
- Seguir boas práticas de Python (PEP 8)
- Incluir tratamento de erros
- Ter documentação inline
- Ser executável em ambiente limpo (com requirements.txt)

### 15.3 Documentação
✅ A documentação DEVE:
- Explicar a arquitetura do sistema
- Incluir instruções de instalação e uso
- Conter exemplos de interação
- Documentar cada agente e suas responsabilidades

---

## 16. Exclusões do Escopo (Fora do MVP)

❌ **NÃO incluir na versão inicial:**
- Sistema de autenticação/autorização
- Integração com sistemas hospitalares reais
- Armazenamento persistente de histórico
- Interface web responsiva completa
- Suporte multilíngue
- Deploy em produção
- Validação clínica rigorosa
- Aprovação regulatória (FDA, ANVISA)
- Sistema de agendamento
- Integração com dispositivos IoT

---

## 17. Referências e Recursos

### 17.1 Documentação Técnica
- [Google ADK Documentation](https://ai.google.dev/adk)
- [Gemini API Reference](https://ai.google.dev/gemini-api)
- [Python Best Practices](https://peps.python.org/pep-0008/)

### 17.2 Bases de Dados Utilizadas

**Datasets Principais (OBRIGATÓRIOS):**
- [Medical Transcriptions - Kaggle](https://www.kaggle.com/datasets/tboyle10/medicaltranscriptions/data)
  - 4.999 transcrições médicas reais
  - 40 especialidades médicas
  - 17.01 MB, formato CSV
  - CC0: Public Domain
  
- [200k Medical Research Abstracts - Kaggle](https://www.kaggle.com/datasets/anshulmehtakaggl/200000-abstracts-for-seq-sentence-classification)
  - 200.000 abstracts de papers médicos
  - Classificação sequencial de sentenças
  - 805.78 MB (usar subset inicial)
  - CC0: Public Domain

**Recursos Complementares:**
- [PubMed RCT Dataset](https://github.com/Franck-Dernoncourt/pubmed-rct) - Source original dos 200k abstracts
- [MTSamples.com](https://mtsamples.com) - Source original das transcrições
- [SkimLit Paper](https://arxiv.org/abs/1710.06071) - Inspiração para classificação de sentenças

**Notebooks de Referência:**
- [Clinical Text Classification](https://www.kaggle.com/code/ritheshsreenivasan/clinical-text-classification) - 297 upvotes
- [Abstract Segmentation NLP](https://www.kaggle.com/code/anshulmehtakaggl/abstract-segmentation-nlp) - 54 upvotes
- [SkimLit Multimodal](https://www.kaggle.com/code/kushal1506/skimlit-multimodal) - Implementação de referência

### 17.3 Papers e Artigos Relevantes
- "AI in Healthcare: Applications and Challenges"
- "Multi-Agent Systems in Medical Decision Support"
- "Explainable AI for Clinical Decision Making"

---

## 18. Glossário

| Termo | Definição |
|-------|-----------|
| **ADK** | Agent Development Kit - Framework do Google para construção de agentes |
| **Agente** | Entidade autônoma que percebe e age em um ambiente |
| **Triagem** | Processo de classificação de urgência médica |
| **Score de Risco** | Valor numérico indicando probabilidade de condição médica |
| **Diagnóstico Diferencial** | Lista de possíveis diagnósticos para sintomas apresentados |
| **Insight** | Descoberta ou padrão relevante extraído de dados |
| **Orchestrator** | Agente coordenador que gerencia outros agentes |

---

## 19. Aprovações

| Papel | Nome | Data | Assinatura |
|-------|------|------|------------|
| Product Owner | [A definir] | ___/___/___ | ____________ |
| Tech Lead | [A definir] | ___/___/___ | ____________ |
| Stakeholder Médico | [A definir] | ___/___/___ | ____________ |

---

## 20. Histórico de Revisões

| Versão | Data | Autor | Descrição |
|--------|------|-------|-----------|
| 1.0 | 18/11/2025 | GitHub Copilot | Versão inicial do PRD |

---

## Anexos

### Anexo A: Exemplo de Estrutura de Diretórios

```
medical-ai-agents/
│
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
│
├── data/
│   ├── raw/                    # Dados brutos
│   ├── processed/              # Dados processados
│   └── sample/                 # Dados de exemplo
│
├── src/
│   ├── __init__.py
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── triage_agent.py
│   │   ├── diagnostic_agent.py
│   │   ├── insights_agent.py
│   │   └── orchestrator.py
│   │
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── database_tools.py
│   │   ├── analysis_tools.py
│   │   └── visualization_tools.py
│   │
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── data_loader.py
│   │   ├── validators.py
│   │   └── logger.py
│   │
│   └── main.py
│
├── tests/
│   ├── __init__.py
│   ├── test_agents.py
│   ├── test_tools.py
│   └── test_integration.py
│
├── notebooks/
│   ├── exploratory_analysis.ipynb
│   └── agent_testing.ipynb
│
├── docs/
│   ├── architecture.md
│   ├── user_guide.md
│   └── api_reference.md
│
└── demos/
    ├── demo_script.py
    └── example_queries.txt
```

### Anexo B: Checklist de Implementação

- [ ] Setup do ambiente de desenvolvimento
- [ ] Instalação e configuração do Google ADK
- [ ] Obtenção da API Key do Gemini
- [ ] Download Medical Transcriptions do Kaggle
- [ ] Download 200k Research Abstracts do Kaggle (subset inicial)
- [ ] Implementação do loader para CSV (Medical Transcriptions)
- [ ] Implementação do parser para TXT (Research Abstracts)
- [ ] Pré-processamento e limpeza dos textos
- [ ] Criação de embeddings para busca semântica
- [ ] Setup de modelos NLP (spaCy, BioBERT/SciBERT)
- [ ] Implementação de NER para entidades médicas
- [ ] Criação de índice vetorial para busca rápida
- [ ] Implementação das 8 ferramentas (tools) especializadas
- [ ] Implementação do Agente de Insights
- [ ] Implementação do Agente de Triagem
- [ ] Implementação do Agente Diagnóstico
- [ ] Implementação do Agente Coordenador
- [ ] Integração entre agentes
- [ ] Desenvolvimento da interface
- [ ] Testes unitários
- [ ] Testes de integração
- [ ] Documentação do código
- [ ] README com instruções
- [ ] Casos de uso documentados
- [ ] Demo preparada
- [ ] Vídeo demonstrativo
- [ ] Revisão final do código

---

**Fim do Documento**
