# 🚀 Guia Completo de Implementação
## Sistema de Agentes Inteligentes para Área Médica com Google ADK

---

## 📚 Índice

1. [Introdução](#introdução)
2. [Pré-requisitos](#pré-requisitos)
3. [Setup Inicial do Ambiente](#setup-inicial-do-ambiente)
4. [Download e Preparação dos Datasets](#download-e-preparação-dos-datasets)
5. [Estrutura do Projeto](#estrutura-do-projeto)
6. [Implementação dos Datasets Loaders](#implementação-dos-datasets-loaders)
7. [Criação das Ferramentas (Tools)](#criação-das-ferramentas-tools)
8. [Implementação dos Agentes com Google ADK](#implementação-dos-agentes-com-google-adk)
9. [Sistema de Orquestração](#sistema-de-orquestração)
10. [Interface do Usuário](#interface-do-usuário)
11. [Testes e Validação](#testes-e-validação)
12. [Deployment e Otimização](#deployment-e-otimização)
13. [Troubleshooting](#troubleshooting)

---

## 🎯 Introdução

Este guia irá te ensinar, passo a passo, como implementar um sistema completo de agentes inteligentes para a área médica usando **Google ADK (Agent Development Kit)**. 

### O que vamos construir?

Um sistema com **5 agentes inteligentes** que trabalham juntos para:
- 📋 Analisar transcrições médicas
- 🔍 Buscar evidências científicas
- 🏥 Classificar especialidades médicas
- 📊 Gerar insights e estatísticas
- 📝 Estruturar textos médicos

### Tecnologias principais:
- **Google ADK** + **Gemini API**
- **Python 3.9+**
- **spaCy** (NLP médico)
- **Transformers** (modelos pré-treinados)
- **Pandas** (manipulação de dados)
- **Streamlit** (interface)

---

## ⚙️ Pré-requisitos

### Conhecimentos necessários:
- ✅ Python intermediário (funções, classes, async/await)
- ✅ Conceitos básicos de NLP (tokenização, embeddings)
- ✅ Linha de comando (terminal/PowerShell)
- ✅ Git básico
- ⭐ Desejável: familiaridade com APIs REST

### Sistema:
- **Python:** 3.9 ou superior
- **RAM:** Mínimo 8GB (recomendado 16GB)
- **Disco:** ~5GB de espaço livre
- **SO:** Windows 10/11, macOS, ou Linux

### Contas necessárias:
1. **Google AI Studio** (para Gemini API key) - [Obter aqui](https://ai.google.dev/)
2. **Kaggle** (para download dos datasets) - [Criar conta](https://www.kaggle.com/)

---

## 🛠️ Setup Inicial do Ambiente

### Passo 1: Criar diretório do projeto

```powershell
# Navegue até onde deseja criar o projeto
cd $HOME\Desktop

# Crie a estrutura de diretórios
mkdir medical-ai-agents
cd medical-ai-agents
```

### Passo 2: Criar ambiente virtual Python

```powershell
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
.\venv\Scripts\activate

# Você verá (venv) no início do prompt
```

### Passo 3: Instalar dependências básicas

Crie um arquivo `requirements.txt`:

```txt
# Core AI & Agents
google-generativeai>=0.3.0
google-aistudio>=0.1.0

# NLP & Medical Text Processing
spacy>=3.7.0
scispacy>=0.5.0
sentence-transformers>=2.2.0
transformers>=4.35.0
torch>=2.1.0

# Data Processing
pandas>=2.1.0
numpy>=1.24.0
scikit-learn>=1.3.0

# Vector Search & Embeddings
faiss-cpu>=1.7.4
chromadb>=0.4.0

# Visualization
matplotlib>=3.8.0
seaborn>=0.13.0
plotly>=5.18.0

# Interface
streamlit>=1.28.0
gradio>=4.0.0

# Utilities
python-dotenv>=1.0.0
loguru>=0.7.0
pydantic>=2.5.0
tqdm>=4.66.0

# Testing
pytest>=7.4.0
pytest-asyncio>=0.21.0
```

Instale tudo:

```powershell
pip install --upgrade pip
pip install -r requirements.txt

# Baixar modelo do spaCy para inglês médico
pip install https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.5.0/en_core_sci_md-0.5.0.tar.gz
```

### Passo 4: Configurar Google Gemini API

1. **Obter API Key:**
   - Acesse [Google AI Studio](https://ai.google.dev/)
   - Clique em "Get API Key"
   - Copie a chave gerada

2. **Criar arquivo `.env`:**

```bash
# .env (na raiz do projeto)
GOOGLE_API_KEY=sua_api_key_aqui
GEMINI_MODEL=gemini-2.0-flash-exp

# Configurações do projeto
PROJECT_NAME=medical-ai-agents
DATA_DIR=./data
CACHE_DIR=./cache
LOGS_DIR=./logs

# Configurações de performance
MAX_EMBEDDINGS_CACHE=1000
SIMILARITY_THRESHOLD=0.75
MAX_RESULTS=10
```

3. **Teste a conexão:**

```python
# test_api.py
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
model = genai.GenerativeModel('gemini-2.0-flash-exp')

response = model.generate_content("Hello, test!")
print(response.text)
print("✅ API configurada com sucesso!")
```

Execute:
```powershell
python test_api.py
```

---

## 📥 Download e Preparação dos Datasets

### Passo 1: Configurar Kaggle API

1. **Obter Kaggle API Token:**
   - Acesse [Kaggle Account](https://www.kaggle.com/settings)
   - Vá em "API" → "Create New Token"
   - Baixe o arquivo `kaggle.json`

2. **Configurar credenciais:**

```powershell
# Windows
mkdir $HOME\.kaggle
cp kaggle.json $HOME\.kaggle\
```

3. **Instalar Kaggle CLI:**

```powershell
pip install kaggle
```

### Passo 2: Download dos Datasets

```powershell
# Criar diretório de dados
mkdir data
mkdir data\raw
mkdir data\processed

# Download Medical Transcriptions (17 MB)
kaggle datasets download -d tboyle10/medicaltranscriptions -p data/raw --unzip

# Download 200k Medical Abstracts (805 MB - vamos usar subset)
kaggle datasets download -d anshulmehtakaggl/200000-abstracts-for-seq-sentence-classification -p data/raw --unzip
```

### Passo 3: Exploração inicial dos dados

Crie `notebooks/01_exploratory_analysis.ipynb`:

```python
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ========================================
# 1. MEDICAL TRANSCRIPTIONS
# ========================================

print("=" * 60)
print("MEDICAL TRANSCRIPTIONS DATASET")
print("=" * 60)

# Carregar dados
df_transcriptions = pd.read_csv('../data/raw/mtsamples.csv')

print(f"\n📊 Shape: {df_transcriptions.shape}")
print(f"📋 Colunas: {list(df_transcriptions.columns)}")

print("\n🔍 Primeiras linhas:")
print(df_transcriptions.head())

print("\n📈 Info do dataset:")
print(df_transcriptions.info())

print("\n🏥 Especialidades médicas únicas:")
print(f"Total: {df_transcriptions['medical_specialty'].nunique()}")
print("\nTop 10 especialidades:")
print(df_transcriptions['medical_specialty'].value_counts().head(10))

# Visualização
plt.figure(figsize=(12, 6))
df_transcriptions['medical_specialty'].value_counts().head(15).plot(kind='barh')
plt.title('Top 15 Especialidades Médicas')
plt.xlabel('Número de Casos')
plt.tight_layout()
plt.savefig('../data/processed/specialties_distribution.png', dpi=300)
plt.show()

# Análise de texto
df_transcriptions['transcription_length'] = df_transcriptions['transcription'].str.len()
print(f"\n📏 Comprimento médio das transcrições: {df_transcriptions['transcription_length'].mean():.0f} caracteres")
print(f"📏 Mediana: {df_transcriptions['transcription_length'].median():.0f} caracteres")

# ========================================
# 2. RESEARCH ABSTRACTS (usar subset)
# ========================================

print("\n" + "=" * 60)
print("RESEARCH ABSTRACTS DATASET (Subset)")
print("=" * 60)

# Ler primeiras 10.000 linhas do train.txt para análise
abstracts_sample = []
with open('../data/raw/train.txt', 'r', encoding='utf-8') as f:
    for i, line in enumerate(f):
        if i >= 10000:  # Limite para exploração inicial
            break
        parts = line.strip().split('\t')
        if len(parts) >= 2:
            abstracts_sample.append({
                'sentence': parts[0],
                'label': parts[1] if len(parts) > 1 else 'UNKNOWN'
            })

df_abstracts = pd.DataFrame(abstracts_sample)

print(f"\n📊 Shape (sample): {df_abstracts.shape}")
print(f"\n🏷️ Labels encontradas:")
print(df_abstracts['label'].value_counts())

# Visualização de distribuição de labels
plt.figure(figsize=(10, 6))
df_abstracts['label'].value_counts().plot(kind='bar')
plt.title('Distribuição de Labels em Research Abstracts (Sample)')
plt.xlabel('Label')
plt.ylabel('Contagem')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('../data/processed/labels_distribution.png', dpi=300)
plt.show()

print("\n✅ Análise exploratória concluída!")
print("📁 Gráficos salvos em data/processed/")
```

Execute o notebook para entender os dados!

---

## 🏗️ Estrutura do Projeto

Vamos criar a estrutura completa:

```powershell
# Criar toda a estrutura de uma vez
$dirs = @(
    "src",
    "src/agents",
    "src/tools",
    "src/utils",
    "src/data",
    "data/raw",
    "data/processed",
    "data/embeddings",
    "cache",
    "logs",
    "tests",
    "notebooks",
    "docs",
    "demos"
)

foreach ($dir in $dirs) {
    New-Item -ItemType Directory -Force -Path $dir
}
```

Estrutura final:

```
medical-ai-agents/
│
├── .env                          # Variáveis de ambiente
├── .gitignore                    # Arquivos ignorados pelo Git
├── requirements.txt              # Dependências Python
├── README.md                     # Documentação principal
│
├── data/
│   ├── raw/                      # Dados originais (não modificar)
│   │   ├── mtsamples.csv
│   │   ├── train.txt
│   │   ├── test.txt
│   │   └── dev.txt
│   ├── processed/                # Dados processados
│   └── embeddings/               # Embeddings pré-computados
│
├── src/
│   ├── __init__.py
│   │
│   ├── agents/                   # Agentes ADK
│   │   ├── __init__.py
│   │   ├── triage_agent.py
│   │   ├── diagnostic_agent.py
│   │   ├── research_agent.py
│   │   ├── structuring_agent.py
│   │   └── orchestrator.py
│   │
│   ├── tools/                    # Ferramentas para os agentes
│   │   ├── __init__.py
│   │   ├── transcription_tools.py
│   │   ├── research_tools.py
│   │   ├── ner_tools.py
│   │   ├── similarity_tools.py
│   │   └── visualization_tools.py
│   │
│   ├── data/                     # Gerenciamento de dados
│   │   ├── __init__.py
│   │   ├── transcriptions_loader.py
│   │   ├── abstracts_loader.py
│   │   └── embeddings_manager.py
│   │
│   ├── utils/                    # Utilitários
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── logger.py
│   │   └── validators.py
│   │
│   └── main.py                   # Ponto de entrada principal
│
├── tests/                        # Testes
│   ├── test_agents.py
│   ├── test_tools.py
│   └── test_integration.py
│
├── notebooks/                    # Jupyter Notebooks
│   ├── 01_exploratory_analysis.ipynb
│   ├── 02_embeddings_creation.ipynb
│   └── 03_agent_testing.ipynb
│
├── demos/                        # Scripts de demonstração
│   ├── demo_cli.py
│   └── demo_streamlit.py
│
├── docs/                         # Documentação adicional
│   └── architecture.md
│
├── cache/                        # Cache de resultados
└── logs/                         # Logs da aplicação
```

Crie o `.gitignore`:

```bash
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
.env

# Data
data/raw/
data/embeddings/
*.csv
*.txt
*.pkl

# Cache
cache/
*.cache

# Logs
logs/
*.log

# IDE
.vscode/
.idea/
*.swp

# OS
.DS_Store
Thumbs.db
```

---

## 💾 Implementação dos Datasets Loaders

### 1. Loader de Transcrições Médicas

Crie `src/data/transcriptions_loader.py`:

```python
"""
Loader para o dataset Medical Transcriptions.
Carrega e processa as 4.999 transcrições médicas.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Optional
from loguru import logger
import re


class TranscriptionsLoader:
    """Gerencia o carregamento e processamento do dataset Medical Transcriptions."""
    
    def __init__(self, data_path: str = "data/raw/mtsamples.csv"):
        """
        Inicializa o loader.
        
        Args:
            data_path: Caminho para o arquivo CSV
        """
        self.data_path = Path(data_path)
        self.df: Optional[pd.DataFrame] = None
        self.specialties: List[str] = []
        
    def load(self) -> pd.DataFrame:
        """
        Carrega o dataset do CSV.
        
        Returns:
            DataFrame com as transcrições
        """
        logger.info(f"Carregando dataset de {self.data_path}")
        
        try:
            self.df = pd.read_csv(self.data_path)
            logger.info(f"✅ Dataset carregado: {len(self.df)} transcrições")
            
            # Informações básicas
            logger.info(f"📋 Colunas: {list(self.df.columns)}")
            logger.info(f"🏥 Especialidades únicas: {self.df['medical_specialty'].nunique()}")
            
            self.specialties = sorted(self.df['medical_specialty'].dropna().unique().tolist())
            
            return self.df
            
        except Exception as e:
            logger.error(f"❌ Erro ao carregar dataset: {e}")
            raise
    
    def preprocess(self) -> pd.DataFrame:
        """
        Realiza pré-processamento dos dados.
        
        Returns:
            DataFrame processado
        """
        if self.df is None:
            self.load()
        
        logger.info("🔧 Iniciando pré-processamento...")
        
        # 1. Tratar valores nulos
        self.df['description'] = self.df['description'].fillna('')
        self.df['medical_specialty'] = self.df['medical_specialty'].fillna('Unknown')
        self.df['transcription'] = self.df['transcription'].fillna('')
        self.df['keywords'] = self.df['keywords'].fillna('')
        
        # 2. Limpar textos
        self.df['transcription_clean'] = self.df['transcription'].apply(self._clean_text)
        self.df['description_clean'] = self.df['description'].apply(self._clean_text)
        
        # 3. Criar features úteis
        self.df['transcription_length'] = self.df['transcription'].str.len()
        self.df['word_count'] = self.df['transcription'].str.split().str.len()
        self.df['keywords_list'] = self.df['keywords'].str.split(',').apply(
            lambda x: [k.strip() for k in x] if isinstance(x, list) else []
        )
        
        # 4. Normalizar especialidades
        self.df['specialty_normalized'] = self.df['medical_specialty'].str.strip().str.title()
        
        # 5. Criar ID único
        self.df['transcription_id'] = [f"TRANS_{i:05d}" for i in range(len(self.df))]
        
        logger.info("✅ Pré-processamento concluído!")
        
        # Salvar versão processada
        output_path = Path("data/processed/transcriptions_processed.csv")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        self.df.to_csv(output_path, index=False)
        logger.info(f"💾 Dataset processado salvo em {output_path}")
        
        return self.df
    
    @staticmethod
    def _clean_text(text: str) -> str:
        """
        Limpa texto médico.
        
        Args:
            text: Texto original
            
        Returns:
            Texto limpo
        """
        if not isinstance(text, str):
            return ""
        
        # Remover caracteres especiais excessivos
        text = re.sub(r'\s+', ' ', text)  # Múltiplos espaços
        text = re.sub(r'\n+', '\n', text)  # Múltiplas quebras de linha
        text = text.strip()
        
        return text
    
    def get_by_specialty(self, specialty: str) -> pd.DataFrame:
        """
        Retorna transcrições de uma especialidade específica.
        
        Args:
            specialty: Nome da especialidade
            
        Returns:
            DataFrame filtrado
        """
        if self.df is None:
            self.load()
        
        return self.df[self.df['medical_specialty'] == specialty].copy()
    
    def get_random_sample(self, n: int = 5, specialty: Optional[str] = None) -> pd.DataFrame:
        """
        Retorna amostra aleatória de transcrições.
        
        Args:
            n: Número de amostras
            specialty: Filtrar por especialidade (opcional)
            
        Returns:
            DataFrame com amostras
        """
        if self.df is None:
            self.load()
        
        df_filtered = self.df if specialty is None else self.get_by_specialty(specialty)
        
        return df_filtered.sample(n=min(n, len(df_filtered)))
    
    def search_by_keyword(self, keyword: str, top_k: int = 10) -> pd.DataFrame:
        """
        Busca transcrições por palavra-chave.
        
        Args:
            keyword: Palavra-chave para buscar
            top_k: Número máximo de resultados
            
        Returns:
            DataFrame com resultados
        """
        if self.df is None:
            self.load()
        
        # Busca case-insensitive em transcrição e descrição
        mask = (
            self.df['transcription'].str.contains(keyword, case=False, na=False) |
            self.df['description'].str.contains(keyword, case=False, na=False) |
            self.df['keywords'].str.contains(keyword, case=False, na=False)
        )
        
        results = self.df[mask].head(top_k)
        logger.info(f"🔍 Encontrados {len(results)} resultados para '{keyword}'")
        
        return results
    
    def get_statistics(self) -> Dict:
        """
        Retorna estatísticas do dataset.
        
        Returns:
            Dicionário com estatísticas
        """
        if self.df is None:
            self.load()
        
        stats = {
            'total_transcriptions': len(self.df),
            'total_specialties': self.df['medical_specialty'].nunique(),
            'specialties': self.df['medical_specialty'].value_counts().to_dict(),
            'avg_transcription_length': self.df['transcription'].str.len().mean(),
            'median_transcription_length': self.df['transcription'].str.len().median(),
            'avg_word_count': self.df['transcription'].str.split().str.len().mean(),
        }
        
        return stats


# ============================================================================
# EXEMPLO DE USO
# ============================================================================

if __name__ == "__main__":
    # Configurar logger
    logger.add("logs/transcriptions_loader.log", rotation="1 MB")
    
    # Criar loader
    loader = TranscriptionsLoader()
    
    # Carregar dados
    df = loader.load()
    
    # Pré-processar
    df_processed = loader.preprocess()
    
    # Estatísticas
    stats = loader.get_statistics()
    print("\n📊 ESTATÍSTICAS:")
    for key, value in stats.items():
        if key != 'specialties':
            print(f"  {key}: {value}")
    
    print("\n🏥 TOP 10 ESPECIALIDADES:")
    top_specialties = sorted(
        stats['specialties'].items(), 
        key=lambda x: x[1], 
        reverse=True
    )[:10]
    for spec, count in top_specialties:
        print(f"  {spec}: {count}")
    
    # Exemplo de busca
    print("\n🔍 BUSCA POR 'diabetes':")
    results = loader.search_by_keyword('diabetes', top_k=3)
    for idx, row in results.iterrows():
        print(f"\n  ID: {row.get('transcription_id', 'N/A')}")
        print(f"  Especialidade: {row['medical_specialty']}")
        print(f"  Descrição: {row['description'][:100]}...")
```

### 2. Loader de Research Abstracts

Crie `src/data/abstracts_loader.py`:

```python
"""
Loader para o dataset 200k Medical Research Abstracts.
Carrega e processa abstracts com classificação de sentenças.
"""

import pandas as pd
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from loguru import logger
from dataclasses import dataclass
from collections import defaultdict
import json


@dataclass
class AbstractSentence:
    """Representa uma sentença de um abstract."""
    text: str
    label: str  # OBJECTIVE, METHODS, RESULTS, CONCLUSIONS, BACKGROUND
    line_number: int


@dataclass
class Abstract:
    """Representa um abstract completo."""
    abstract_id: str
    sentences: List[AbstractSentence]
    
    def get_by_label(self, label: str) -> List[str]:
        """Retorna sentenças de um label específico."""
        return [s.text for s in self.sentences if s.label == label]
    
    def to_dict(self) -> Dict:
        """Converte para dicionário."""
        return {
            'abstract_id': self.abstract_id,
            'objective': ' '.join(self.get_by_label('OBJECTIVE')),
            'methods': ' '.join(self.get_by_label('METHODS')),
            'results': ' '.join(self.get_by_label('RESULTS')),
            'conclusions': ' '.join(self.get_by_label('CONCLUSIONS')),
            'background': ' '.join(self.get_by_label('BACKGROUND')),
            'full_text': ' '.join([s.text for s in self.sentences])
        }


class AbstractsLoader:
    """Gerencia o carregamento do dataset de Research Abstracts."""
    
    VALID_LABELS = {'OBJECTIVE', 'METHODS', 'RESULTS', 'CONCLUSIONS', 'BACKGROUND'}
    
    def __init__(self, data_dir: str = "data/raw"):
        """
        Inicializa o loader.
        
        Args:
            data_dir: Diretório com os arquivos train.txt, test.txt, dev.txt
        """
        self.data_dir = Path(data_dir)
        self.train_file = self.data_dir / "train.txt"
        self.test_file = self.data_dir / "test.txt"
        self.dev_file = self.data_dir / "dev.txt"
        
        self.abstracts: List[Abstract] = []
        self.df: Optional[pd.DataFrame] = None
    
    def load(
        self, 
        split: str = 'train', 
        max_abstracts: Optional[int] = None
    ) -> List[Abstract]:
        """
        Carrega abstracts de um split específico.
        
        Args:
            split: 'train', 'test', ou 'dev'
            max_abstracts: Número máximo de abstracts a carregar (None = todos)
            
        Returns:
            Lista de objetos Abstract
        """
        # Selecionar arquivo
        file_map = {
            'train': self.train_file,
            'test': self.test_file,
            'dev': self.dev_file
        }
        
        if split not in file_map:
            raise ValueError(f"Split inválido: {split}. Use 'train', 'test' ou 'dev'")
        
        filepath = file_map[split]
        
        if not filepath.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {filepath}")
        
        logger.info(f"📖 Carregando abstracts de {filepath.name}")
        
        # Parsear arquivo
        abstracts = self._parse_file(filepath, max_abstracts)
        
        self.abstracts = abstracts
        logger.info(f"✅ {len(abstracts)} abstracts carregados")
        
        return abstracts
    
    def _parse_file(
        self, 
        filepath: Path, 
        max_abstracts: Optional[int] = None
    ) -> List[Abstract]:
        """
        Faz parse do arquivo TXT.
        
        Formato esperado (tab-separated):
        sentença\tlabel\tnúmero_da_linha\tabstract_id
        
        Args:
            filepath: Caminho do arquivo
            max_abstracts: Limite de abstracts
            
        Returns:
            Lista de abstracts parseados
        """
        abstracts_dict = defaultdict(list)
        
        with open(filepath, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                parts = line.strip().split('\t')
                
                if len(parts) < 2:
                    continue
                
                sentence_text = parts[0]
                label = parts[1].upper()
                
                # Validar label
                if label not in self.VALID_LABELS:
                    logger.warning(f"Label inválido na linha {line_num}: {label}")
                    continue
                
                # Abstract ID (usar número da linha se não fornecido)
                abstract_id = parts[3] if len(parts) > 3 else f"abstract_{line_num}"
                
                # Criar sentença
                sentence = AbstractSentence(
                    text=sentence_text,
                    label=label,
                    line_number=line_num
                )
                
                abstracts_dict[abstract_id].append(sentence)
                
                # Verificar limite
                if max_abstracts and len(abstracts_dict) >= max_abstracts:
                    break
        
        # Converter para lista de Abstracts
        abstracts = [
            Abstract(abstract_id=aid, sentences=sentences)
            for aid, sentences in abstracts_dict.items()
        ]
        
        return abstracts
    
    def to_dataframe(self) -> pd.DataFrame:
        """
        Converte abstracts para DataFrame.
        
        Returns:
            DataFrame com abstracts estruturados
        """
        if not self.abstracts:
            logger.warning("Nenhum abstract carregado. Carregue primeiro com load()")
            return pd.DataFrame()
        
        # Converter cada abstract para dict
        data = [abstract.to_dict() for abstract in self.abstracts]
        
        self.df = pd.DataFrame(data)
        
        logger.info(f"📊 DataFrame criado: {self.df.shape}")
        
        return self.df
    
    def search(self, query: str, top_k: int = 10) -> List[Abstract]:
        """
        Busca abstracts por palavra-chave (busca simples).
        
        Args:
            query: Texto para buscar
            top_k: Número de resultados
            
        Returns:
            Lista de abstracts relevantes
        """
        if not self.abstracts:
            logger.warning("Nenhum abstract carregado")
            return []
        
        query_lower = query.lower()
        results = []
        
        for abstract in self.abstracts:
            # Buscar em todo o texto do abstract
            full_text = ' '.join([s.text for s in abstract.sentences]).lower()
            
            if query_lower in full_text:
                results.append(abstract)
                
                if len(results) >= top_k:
                    break
        
        logger.info(f"🔍 {len(results)} abstracts encontrados para '{query}'")
        
        return results
    
    def get_statistics(self) -> Dict:
        """
        Retorna estatísticas do dataset.
        
        Returns:
            Dicionário com estatísticas
        """
        if not self.abstracts:
            return {}
        
        # Contar labels
        label_counts = defaultdict(int)
        total_sentences = 0
        
        for abstract in self.abstracts:
            total_sentences += len(abstract.sentences)
            for sentence in abstract.sentences:
                label_counts[sentence.label] += 1
        
        stats = {
            'total_abstracts': len(self.abstracts),
            'total_sentences': total_sentences,
            'avg_sentences_per_abstract': total_sentences / len(self.abstracts),
            'label_distribution': dict(label_counts)
        }
        
        return stats
    
    def save_processed(self, output_path: str = "data/processed/abstracts_processed.json"):
        """
        Salva abstracts processados em JSON.
        
        Args:
            output_path: Caminho do arquivo de saída
        """
        if not self.abstracts:
            logger.warning("Nenhum abstract para salvar")
            return
        
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Converter para formato serializável
        data = [abstract.to_dict() for abstract in self.abstracts]
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"💾 {len(data)} abstracts salvos em {output_file}")


# ============================================================================
# EXEMPLO DE USO
# ============================================================================

if __name__ == "__main__":
    logger.add("logs/abstracts_loader.log", rotation="1 MB")
    
    # Criar loader
    loader = AbstractsLoader()
    
    # Carregar subset para teste (primeiros 1000 abstracts)
    abstracts = loader.load(split='train', max_abstracts=1000)
    
    # Estatísticas
    stats = loader.get_statistics()
    print("\n📊 ESTATÍSTICAS:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    # Converter para DataFrame
    df = loader.to_dataframe()
    print(f"\n📋 DataFrame shape: {df.shape}")
    print(df.head())
    
    # Exemplo de busca
    print("\n🔍 BUSCA POR 'diabetes':")
    results = loader.search('diabetes', top_k=3)
    for i, abstract in enumerate(results, 1):
        print(f"\n  Abstract {i}:")
        print(f"    OBJECTIVE: {' '.join(abstract.get_by_label('OBJECTIVE'))[:100]}...")
        print(f"    RESULTS: {' '.join(abstract.get_by_label('RESULTS'))[:100]}...")
    
    # Salvar processado
    loader.save_processed()
```

Execute para testar:

```powershell
python src/data/transcriptions_loader.py
python src/data/abstracts_loader.py
```

---

## 🛠️ Criação das Ferramentas (Tools)

As ferramentas são funções que os agentes podem chamar. Vamos criar as 8 ferramentas principais.

### Tool 1: Busca em Transcrições

Crie `src/tools/transcription_tools.py`:

```python
"""
Ferramentas para busca e análise de transcrições médicas.
"""

import pandas as pd
from typing import List, Dict, Optional
from pathlib import Path
from loguru import logger
from sentence_transformers import SentenceTransformer, util
import torch
import pickle


class TranscriptionSearchTool:
    """Ferramenta de busca semântica em transcrições médicas."""
    
    def __init__(
        self, 
        transcriptions_path: str = "data/processed/transcriptions_processed.csv",
        embeddings_path: str = "data/embeddings/transcriptions_embeddings.pkl"
    ):
        """
        Inicializa a ferramenta.
        
        Args:
            transcriptions_path: Caminho do CSV processado
            embeddings_path: Caminho dos embeddings salvos
        """
        self.transcriptions_path = Path(transcriptions_path)
        self.embeddings_path = Path(embeddings_path)
        
        # Carregar dados
        self.df = pd.read_csv(self.transcriptions_path)
        logger.info(f"✅ {len(self.df)} transcrições carregadas")
        
        # Carregar ou criar embeddings
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.embeddings = self._load_or_create_embeddings()
    
    def _load_or_create_embeddings(self) -> torch.Tensor:
        """Carrega embeddings salvos ou cria novos."""
        if self.embeddings_path.exists():
            logger.info(f"📂 Carregando embeddings de {self.embeddings_path}")
            with open(self.embeddings_path, 'rb') as f:
                embeddings = pickle.load(f)
            return embeddings
        else:
            logger.info("🔄 Criando embeddings (pode demorar alguns minutos)...")
            
            # Concatenar descrição + transcrição para embedding
            texts = (
                self.df['description'].fillna('') + ' ' + 
                self.df['transcription'].fillna('')
            ).tolist()
            
            embeddings = self.model.encode(
                texts, 
                convert_to_tensor=True,
                show_progress_bar=True
            )
            
            # Salvar para uso futuro
            self.embeddings_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.embeddings_path, 'wb') as f:
                pickle.dump(embeddings, f)
            
            logger.info(f"💾 Embeddings salvos em {self.embeddings_path}")
            
            return embeddings
    
    def search_similar_cases(
        self, 
        query: str, 
        specialty: Optional[str] = None,
        top_k: int = 5
    ) -> List[Dict]:
        """
        Busca casos similares usando similarity search.
        
        Args:
            query: Texto da consulta
            specialty: Filtrar por especialidade (opcional)
            top_k: Número de resultados
            
        Returns:
            Lista de casos similares com scores
        """
        # Criar embedding da query
        query_embedding = self.model.encode(query, convert_to_tensor=True)
        
        # Calcular similaridade
        similarities = util.pytorch_cos_sim(query_embedding, self.embeddings)[0]
        
        # Filtrar por especialidade se fornecida
        if specialty:
            mask = self.df['medical_specialty'] == specialty
            similarities = similarities * torch.tensor(mask.values, dtype=torch.float32)
        
        # Top-K resultados
        top_indices = torch.topk(similarities, k=min(top_k, len(similarities))).indices
        
        results = []
        for idx in top_indices:
            idx = idx.item()
            row = self.df.iloc[idx]
            
            result = {
                'transcription_id': row.get('transcription_id', f'TRANS_{idx}'),
                'similarity_score': float(similarities[idx]),
                'medical_specialty': row['medical_specialty'],
                'description': row['description'],
                'transcription': row['transcription'][:500],  # Primeiros 500 chars
                'keywords': row.get('keywords', '')
            }
            
            results.append(result)
        
        logger.info(f"🔍 {len(results)} casos similares encontrados")
        
        return results


def search_transcriptions_tool(
    query: str,
    specialty: Optional[str] = None,
    top_k: int = 5
) -> str:
    """
    Tool function para uso com Google ADK.
    Busca transcrições médicas similares.
    
    Args:
        query: Consulta de busca
        specialty: Especialidade médica (opcional)
        top_k: Número de resultados
        
    Returns:
        String formatada com resultados
    """
    search_tool = TranscriptionSearchTool()
    results = search_tool.search_similar_cases(query, specialty, top_k)
    
    # Formatar resultados para o agente
    output = f"Encontrados {len(results)} casos similares:\n\n"
    
    for i, result in enumerate(results, 1):
        output += f"--- Caso {i} ---\n"
        output += f"ID: {result['transcription_id']}\n"
        output += f"Especialidade: {result['medical_specialty']}\n"
        output += f"Similaridade: {result['similarity_score']:.2%}\n"
        output += f"Descrição: {result['description']}\n"
        output += f"Transcrição (início): {result['transcription'][:200]}...\n"
        output += f"Keywords: {result['keywords']}\n\n"
    
    return output
```

### Tool 2: Classificação de Especialidade

Adicione ao mesmo arquivo:

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import joblib


class SpecialtyClassifierTool:
    """Classifica especialidade médica de uma transcrição."""
    
    def __init__(
        self,
        model_path: str = "data/models/specialty_classifier.pkl"
    ):
        """
        Inicializa o classificador.
        
        Args:
            model_path: Caminho do modelo treinado
        """
        self.model_path = Path(model_path)
        self.vectorizer: Optional[TfidfVectorizer] = None
        self.classifier: Optional[LogisticRegression] = None
        
        # Carregar ou treinar modelo
        self._load_or_train_model()
    
    def _load_or_train_model(self):
        """Carrega modelo existente ou treina novo."""
        if self.model_path.exists():
            logger.info(f"📂 Carregando modelo de {self.model_path}")
            with open(self.model_path, 'rb') as f:
                data = joblib.load(f)
                self.vectorizer = data['vectorizer']
                self.classifier = data['classifier']
        else:
            logger.info("🎓 Treinando novo modelo de classificação...")
            self._train_model()
    
    def _train_model(self):
        """Treina modelo de classificação de especialidades."""
        # Carregar dados
        df = pd.read_csv("data/processed/transcriptions_processed.csv")
        
        # Remover especialidades com poucos exemplos
        specialty_counts = df['medical_specialty'].value_counts()
        valid_specialties = specialty_counts[specialty_counts >= 10].index
        df_filtered = df[df['medical_specialty'].isin(valid_specialties)]
        
        logger.info(f"📚 Treinando com {len(df_filtered)} exemplos de {len(valid_specialties)} especialidades")
        
        # Preparar dados
        X = df_filtered['description'] + ' ' + df_filtered['transcription']
        y = df_filtered['medical_specialty']
        
        # TF-IDF
        self.vectorizer = TfidfVectorizer(
            max_features=5000,
            ngram_range=(1, 2),
            stop_words='english'
        )
        X_tfidf = self.vectorizer.fit_transform(X)
        
        # Treinar classificador
        self.classifier = LogisticRegression(
            max_iter=1000,
            class_weight='balanced',
            random_state=42
        )
        self.classifier.fit(X_tfidf, y)
        
        # Salvar modelo
        self.model_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.model_path, 'wb') as f:
            joblib.dump({
                'vectorizer': self.vectorizer,
                'classifier': self.classifier
            }, f)
        
        logger.info(f"✅ Modelo treinado e salvo em {self.model_path}")
    
    def classify(self, text: str, top_k: int = 3) -> List[Dict]:
        """
        Classifica especialidade médica de um texto.
        
        Args:
            text: Texto da transcrição
            top_k: Número de predições top
            
        Returns:
            Lista de especialidades com probabilidades
        """
        # Vetorizar texto
        X = self.vectorizer.transform([text])
        
        # Predição
        probas = self.classifier.predict_proba(X)[0]
        classes = self.classifier.classes_
        
        # Top-K
        top_indices = probas.argsort()[-top_k:][::-1]
        
        results = [
            {
                'specialty': classes[idx],
                'confidence': float(probas[idx])
            }
            for idx in top_indices
        ]
        
        return results


def classify_specialty_tool(text: str, top_k: int = 3) -> str:
    """
    Tool function para classificação de especialidade.
    
    Args:
        text: Texto médico para classificar
        top_k: Número de predições
        
    Returns:
        String formatada com classificações
    """
    classifier = SpecialtyClassifierTool()
    results = classifier.classify(text, top_k)
    
    output = "Classificação de Especialidade:\n\n"
    
    for i, result in enumerate(results, 1):
        output += f"{i}. {result['specialty']}: {result['confidence']:.1%}\n"
    
    return output
```

Vou continuar criando as outras ferramentas essenciais. Quer que eu continue com as ferramentas de NER, Research Tools e Visualization, ou prefere que eu pule direto para a implementação dos Agentes ADK?