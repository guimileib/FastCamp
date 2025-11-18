# 🎯 Passo a Passo - Implementação Completa
## Sistema de Agentes Inteligentes Médicos com Google ADK

---

## 📋 Visão Geral

Este documento é um **guia linear e sequencial** para implementar o sistema completo em **14 dias**. Siga cada passo na ordem apresentada para garantir que todas as dependências sejam satisfeitas.

**Tempo estimado:** 2-3 semanas (60-80 horas)
**Nível:** Intermediário a Avançado

---

## 📅 Cronograma Geral

| Fase | Dias | Atividade Principal |
|------|------|---------------------|
| **Fase 1** | 1-3 | Setup e Preparação de Dados |
| **Fase 2** | 4-7 | Ferramentas e NLP |
| **Fase 3** | 8-11 | Agentes ADK |
| **Fase 4** | 12-14 | Interface e Testes |

---

# FASE 1: Setup e Preparação de Dados (Dias 1-3)

## ✅ DIA 1: Configuração do Ambiente

### Passo 1.1: Criar estrutura do projeto (15 min)

```powershell
# 1. Navegue até o diretório desejado
cd $HOME\Desktop

# 2. Crie o diretório do projeto
mkdir medical-ai-agents
cd medical-ai-agents

# 3. Crie a estrutura completa
$dirs = @(
    "src",
    "src/agents",
    "src/tools",
    "src/utils",
    "src/data",
    "data/raw",
    "data/processed",
    "data/embeddings",
    "data/models",
    "cache",
    "logs",
    "tests",
    "notebooks",
    "demos"
)

foreach ($dir in $dirs) {
    New-Item -ItemType Directory -Force -Path $dir | Out-Null
}

Write-Host "✅ Estrutura criada com sucesso!" -ForegroundColor Green
```

**Checkpoint:** Você deve ter 14 pastas criadas.

### Passo 1.2: Criar ambiente virtual Python (10 min)

```powershell
# 1. Criar ambiente virtual
python -m venv venv

# 2. Ativar ambiente
.\venv\Scripts\activate

# 3. Atualizar pip
python -m pip install --upgrade pip

# 4. Verificar versão do Python
python --version
# Deve mostrar Python 3.9.x ou superior
```

**Checkpoint:** Você deve ver `(venv)` no prompt do terminal.

### Passo 1.3: Instalar dependências (30 min)

**1. Criar arquivo `requirements.txt`:**

```powershell
# Use notepad ou VSCode
notepad requirements.txt
```

Cole o seguinte conteúdo:

```txt
# ============================================
# CORE AI & AGENTS
# ============================================
google-generativeai==0.3.2
google-ai-generativelanguage==0.4.0

# ============================================
# NLP & MEDICAL TEXT PROCESSING
# ============================================
spacy==3.7.2
scispacy==0.5.3
sentence-transformers==2.2.2
transformers==4.36.0
torch==2.1.0
tokenizers==0.15.0

# ============================================
# DATA PROCESSING
# ============================================
pandas==2.1.4
numpy==1.26.2
scikit-learn==1.3.2

# ============================================
# VECTOR SEARCH & EMBEDDINGS
# ============================================
faiss-cpu==1.7.4
chromadb==0.4.22

# ============================================
# VISUALIZATION
# ============================================
matplotlib==3.8.2
seaborn==0.13.0
plotly==5.18.0
wordcloud==1.9.3

# ============================================
# INTERFACE
# ============================================
streamlit==1.29.0
gradio==4.13.0

# ============================================
# UTILITIES
# ============================================
python-dotenv==1.0.0
loguru==0.7.2
pydantic==2.5.3
tqdm==4.66.1
requests==2.31.0
beautifulsoup4==4.12.2

# ============================================
# DATA DOWNLOAD
# ============================================
kaggle==1.5.16

# ============================================
# TESTING
# ============================================
pytest==7.4.3
pytest-asyncio==0.21.1

# ============================================
# JUPYTER (para análise)
# ============================================
jupyter==1.0.0
ipykernel==6.27.1
ipywidgets==8.1.1
```

**2. Instalar todas as dependências:**

```powershell
pip install -r requirements.txt
```

⏰ **Isso vai demorar 10-15 minutos.** Tome um café! ☕

**3. Instalar modelo spaCy médico:**

```powershell
# Modelo base científico
pip install https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.5.3/en_core_sci_md-0.5.3.tar.gz

# Modelo maior (opcional, se tiver espaço)
# pip install https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.5.3/en_core_sci_lg-0.5.3.tar.gz
```

**Checkpoint:** Execute `pip list` e confirme que todos os pacotes foram instalados.

### Passo 1.4: Configurar Google Gemini API (15 min)

**1. Obter API Key:**
- Acesse: https://ai.google.dev/
- Clique em "Get API Key" → "Create API Key"
- Copie a chave (começa com `AIza...`)

**2. Criar arquivo `.env`:**

```powershell
notepad .env
```

Cole:

```bash
# ===========================================
# GOOGLE AI CONFIGURATION
# ===========================================
GOOGLE_API_KEY=AIzaSyCxxxxxxxxxxxxxxxxxxxxxxxxxx
GEMINI_MODEL=gemini-2.0-flash-exp

# ===========================================
# PROJECT CONFIGURATION
# ===========================================
PROJECT_NAME=medical-ai-agents
DATA_DIR=./data
CACHE_DIR=./cache
LOGS_DIR=./logs
MODELS_DIR=./data/models

# ===========================================
# PERFORMANCE SETTINGS
# ===========================================
MAX_EMBEDDINGS_CACHE=1000
SIMILARITY_THRESHOLD=0.75
MAX_RESULTS=10
BATCH_SIZE=32

# ===========================================
# DATASET LIMITS (para desenvolvimento)
# ===========================================
MAX_TRANSCRIPTIONS=5000
MAX_ABSTRACTS=10000

# ===========================================
# LOGGING
# ===========================================
LOG_LEVEL=INFO
LOG_ROTATION=10 MB
```

**⚠️ IMPORTANTE:** Substitua `AIzaSyCxxxxxxxxxxxxxxxxxxxxxxxxxx` pela sua chave real!

**3. Testar conexão com Gemini:**

Crie `test_gemini.py`:

```python
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Carregar variáveis de ambiente
load_dotenv()

# Configurar API
api_key = os.getenv('GOOGLE_API_KEY')
if not api_key:
    raise ValueError("❌ GOOGLE_API_KEY não encontrada no arquivo .env")

genai.configure(api_key=api_key)

# Testar modelo
model = genai.GenerativeModel('gemini-2.0-flash-exp')

try:
    response = model.generate_content("Diga olá em português")
    print("✅ API funcionando!")
    print(f"📝 Resposta: {response.text}")
except Exception as e:
    print(f"❌ Erro: {e}")
```

Execute:

```powershell
python test_gemini.py
```

**Checkpoint:** Você deve ver "✅ API funcionando!" e uma resposta do Gemini.

### Passo 1.5: Configurar Git (10 min)

```powershell
# 1. Inicializar repositório
git init

# 2. Criar .gitignore
notepad .gitignore
```

Cole:

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/

# Environment
.env
.env.local

# Data (não versionar datasets grandes)
data/raw/
data/embeddings/
data/models/
*.csv
*.txt
*.pkl
*.pth
*.bin

# Cache
cache/
*.cache
.cache/

# Logs
logs/
*.log

# Jupyter
.ipynb_checkpoints/
*.ipynb

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
desktop.ini

# Temporary
tmp/
temp/
*.tmp
```

```powershell
# 3. Primeiro commit
git add .
git commit -m "Initial setup: project structure and dependencies"
```

**Checkpoint:** Execute `git status` - deve mostrar "working tree clean".

---

## ✅ DIA 2: Download e Exploração dos Datasets

### Passo 2.1: Configurar Kaggle API (10 min)

**1. Obter token Kaggle:**
- Acesse: https://www.kaggle.com/settings
- Seção "API" → "Create New Token"
- Baixe `kaggle.json`

**2. Configurar credenciais:**

```powershell
# Criar diretório .kaggle
$kaggleDir = "$HOME\.kaggle"
New-Item -ItemType Directory -Force -Path $kaggleDir

# Copiar kaggle.json
Copy-Item kaggle.json $kaggleDir\

# Verificar
Test-Path "$kaggleDir\kaggle.json"
# Deve retornar True
```

### Passo 2.2: Download Medical Transcriptions (5 min)

```powershell
# Download dataset (17 MB)
kaggle datasets download -d tboyle10/medicaltranscriptions -p data/raw --unzip

# Verificar
Test-Path "data/raw/mtsamples.csv"
# Deve retornar True

# Ver tamanho
(Get-Item "data/raw/mtsamples.csv").Length / 1MB
# ~17 MB
```

**Checkpoint:** Arquivo `mtsamples.csv` deve existir em `data/raw/`.

### Passo 2.3: Download Research Abstracts (15 min)

```powershell
# Download dataset (805 MB - pode demorar)
kaggle datasets download -d anshulmehtakaggl/200000-abstracts-for-seq-sentence-classification -p data/raw --unzip

# Verificar arquivos
Get-ChildItem "data/raw" -Filter "*.txt"
# Deve mostrar train.txt, test.txt, dev.txt
```

**Checkpoint:** Você deve ter 3 arquivos TXT em `data/raw/`.

### Passo 2.4: Análise Exploratória (60 min)

**1. Criar notebook de análise:**

```powershell
jupyter notebook
```

No Jupyter, crie `notebooks/01_exploratory_analysis.ipynb`:

**Célula 1 - Setup:**

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import warnings

warnings.filterwarnings('ignore')
sns.set_style('whitegrid')

%matplotlib inline
```

**Célula 2 - Medical Transcriptions:**

```python
# Carregar dataset
df_trans = pd.read_csv('../data/raw/mtsamples.csv')

print("=" * 70)
print("MEDICAL TRANSCRIPTIONS DATASET")
print("=" * 70)

# Informações básicas
print(f"\n📊 Shape: {df_trans.shape}")
print(f"📋 Colunas: {list(df_trans.columns)}")
print(f"\n💾 Memória: {df_trans.memory_usage(deep=True).sum() / 1024**2:.2f} MB")

# Primeiras linhas
print("\n🔍 Primeiras 3 linhas:")
display(df_trans.head(3))

# Informações de tipos
print("\n📈 Info:")
df_trans.info()
```

**Célula 3 - Análise de Especialidades:**

```python
# Especialidades
print("\n🏥 ESPECIALIDADES MÉDICAS")
print(f"Total de especialidades únicas: {df_trans['medical_specialty'].nunique()}")

# Top 15
top_specialties = df_trans['medical_specialty'].value_counts().head(15)
print("\nTop 15 especialidades:")
print(top_specialties)

# Visualização
plt.figure(figsize=(14, 7))
top_specialties.plot(kind='barh', color='steelblue')
plt.title('Top 15 Especialidades Médicas', fontsize=16, fontweight='bold')
plt.xlabel('Número de Casos', fontsize=12)
plt.ylabel('Especialidade', fontsize=12)
plt.grid(axis='x', alpha=0.3)
plt.tight_layout()
plt.savefig('../data/processed/specialties_distribution.png', dpi=300, bbox_inches='tight')
plt.show()
```

**Célula 4 - Análise de Texto:**

```python
# Análise de comprimento
df_trans['trans_length'] = df_trans['transcription'].fillna('').str.len()
df_trans['trans_words'] = df_trans['transcription'].fillna('').str.split().str.len()
df_trans['desc_length'] = df_trans['description'].fillna('').str.len()

print("\n📏 ESTATÍSTICAS DE TEXTO")
print(f"Comprimento médio da transcrição: {df_trans['trans_length'].mean():.0f} caracteres")
print(f"Mediana: {df_trans['trans_length'].median():.0f} caracteres")
print(f"Palavras médias: {df_trans['trans_words'].mean():.0f}")
print(f"\nMenor transcrição: {df_trans['trans_length'].min()} caracteres")
print(f"Maior transcrição: {df_trans['trans_length'].max()} caracteres")

# Distribuição
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

axes[0].hist(df_trans['trans_length'], bins=50, color='skyblue', edgecolor='black')
axes[0].set_title('Distribuição de Comprimento das Transcrições')
axes[0].set_xlabel('Caracteres')
axes[0].set_ylabel('Frequência')
axes[0].axvline(df_trans['trans_length'].mean(), color='red', linestyle='--', label='Média')
axes[0].legend()

axes[1].hist(df_trans['trans_words'], bins=50, color='lightcoral', edgecolor='black')
axes[1].set_title('Distribuição de Palavras')
axes[1].set_xlabel('Palavras')
axes[1].set_ylabel('Frequência')
axes[1].axvline(df_trans['trans_words'].mean(), color='red', linestyle='--', label='Média')
axes[1].legend()

plt.tight_layout()
plt.savefig('../data/processed/text_stats.png', dpi=300)
plt.show()
```

**Célula 5 - Análise de Keywords:**

```python
from collections import Counter

# Extrair todas as keywords
all_keywords = []
for keywords in df_trans['keywords'].dropna():
    kws = [k.strip().lower() for k in keywords.split(',')]
    all_keywords.extend(kws)

# Top keywords
keyword_counts = Counter(all_keywords)
top_keywords = keyword_counts.most_common(30)

print("\n🔑 TOP 30 KEYWORDS MAIS FREQUENTES:")
for kw, count in top_keywords:
    print(f"  {kw}: {count}")

# WordCloud
from wordcloud import WordCloud

wordcloud = WordCloud(
    width=1200, 
    height=600, 
    background_color='white',
    colormap='viridis'
).generate_from_frequencies(dict(top_keywords))

plt.figure(figsize=(15, 7))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title('Keywords Médicas Mais Frequentes', fontsize=18, fontweight='bold')
plt.tight_layout()
plt.savefig('../data/processed/keywords_wordcloud.png', dpi=300, bbox_inches='tight')
plt.show()
```

**Célula 6 - Research Abstracts (Sample):**

```python
print("\n" + "=" * 70)
print("RESEARCH ABSTRACTS DATASET (Sample 10k)")
print("=" * 70)

# Ler primeiras 10k linhas
abstracts_data = []
with open('../data/raw/train.txt', 'r', encoding='utf-8') as f:
    for i, line in enumerate(f):
        if i >= 10000:
            break
        parts = line.strip().split('\t')
        if len(parts) >= 2:
            abstracts_data.append({
                'sentence': parts[0],
                'label': parts[1]
            })

df_abstracts = pd.DataFrame(abstracts_data)

print(f"\n📊 Shape (sample): {df_abstracts.shape}")
print(f"\n🏷️ Labels:")
print(df_abstracts['label'].value_counts())

# Visualização
plt.figure(figsize=(10, 6))
label_counts = df_abstracts['label'].value_counts()
label_counts.plot(kind='bar', color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8'])
plt.title('Distribuição de Labels em Research Abstracts (Sample)', fontsize=14, fontweight='bold')
plt.xlabel('Label', fontsize=12)
plt.ylabel('Contagem', fontsize=12)
plt.xticks(rotation=45)
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('../data/processed/labels_distribution.png', dpi=300)
plt.show()

# Comprimento por label
df_abstracts['sent_length'] = df_abstracts['sentence'].str.len()
print("\n📏 Comprimento médio por label:")
print(df_abstracts.groupby('label')['sent_length'].mean().sort_values(ascending=False))
```

**Célula 7 - Salvar resumo:**

```python
# Criar resumo dos datasets
summary = {
    'medical_transcriptions': {
        'total_records': len(df_trans),
        'specialties': df_trans['medical_specialty'].nunique(),
        'avg_transcription_length': df_trans['trans_length'].mean(),
        'avg_word_count': df_trans['trans_words'].mean(),
        'top_specialties': df_trans['medical_specialty'].value_counts().head(10).to_dict()
    },
    'research_abstracts_sample': {
        'total_sentences': len(df_abstracts),
        'labels': df_abstracts['label'].value_counts().to_dict(),
        'avg_sentence_length': df_abstracts['sent_length'].mean()
    }
}

import json
with open('../data/processed/dataset_summary.json', 'w') as f:
    json.dump(summary, f, indent=2)

print("✅ Resumo salvo em data/processed/dataset_summary.json")
print("\n📊 RESUMO FINAL:")
print(json.dumps(summary, indent=2))
```

**Execute o notebook completo** e verifique se todos os gráficos foram gerados!

**Checkpoint:** 
- ✅ 4 arquivos PNG em `data/processed/`
- ✅ 1 arquivo JSON com o resumo
- ✅ Entendimento claro dos dados

---

## ✅ DIA 3: Implementar Data Loaders

### Passo 3.1: Criar utilitários básicos (30 min)

**1. Logger configurável - `src/utils/logger.py`:**

```python
"""
Sistema de logging configurável para o projeto.
"""

from loguru import logger
import sys
from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()


def setup_logger(
    log_level: str = None,
    log_file: str = "logs/app.log",
    rotation: str = "10 MB",
    retention: str = "1 week"
):
    """
    Configura o logger do projeto.
    
    Args:
        log_level: Nível de log (DEBUG, INFO, WARNING, ERROR)
        log_file: Caminho do arquivo de log
        rotation: Quando rotacionar o arquivo
        retention: Quanto tempo manter logs antigos
    """
    # Remover handler padrão
    logger.remove()
    
    # Obter nível do .env ou usar padrão
    if log_level is None:
        log_level = os.getenv('LOG_LEVEL', 'INFO')
    
    # Console handler (colorido)
    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level=log_level,
        colorize=True
    )
    
    # File handler
    log_path = Path(log_file)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    
    logger.add(
        log_file,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level=log_level,
        rotation=rotation,
        retention=retention,
        compression="zip"
    )
    
    logger.info(f"Logger configurado - Nível: {log_level}")
    
    return logger


# Setup automático ao importar
setup_logger()
```

**2. Configuração centralizada - `src/utils/config.py`:**

```python
"""
Configurações centralizadas do projeto.
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import Optional

# Carregar .env
load_dotenv()


class ProjectConfig(BaseModel):
    """Configurações do projeto."""
    
    # Paths
    project_root: Path = Field(default_factory=lambda: Path(__file__).parent.parent.parent)
    data_dir: Path = Field(default_factory=lambda: Path("data"))
    cache_dir: Path = Field(default_factory=lambda: Path("cache"))
    logs_dir: Path = Field(default_factory=lambda: Path("logs"))
    models_dir: Path = Field(default_factory=lambda: Path("data/models"))
    
    # API
    google_api_key: str = Field(default_factory=lambda: os.getenv('GOOGLE_API_KEY', ''))
    gemini_model: str = Field(default_factory=lambda: os.getenv('GEMINI_MODEL', 'gemini-2.0-flash-exp'))
    
    # Dataset limits
    max_transcriptions: int = Field(default_factory=lambda: int(os.getenv('MAX_TRANSCRIPTIONS', 5000)))
    max_abstracts: int = Field(default_factory=lambda: int(os.getenv('MAX_ABSTRACTS', 10000)))
    
    # Performance
    max_embeddings_cache: int = Field(default_factory=lambda: int(os.getenv('MAX_EMBEDDINGS_CACHE', 1000)))
    similarity_threshold: float = Field(default_factory=lambda: float(os.getenv('SIMILARITY_THRESHOLD', 0.75)))
    max_results: int = Field(default_factory=lambda: int(os.getenv('MAX_RESULTS', 10)))
    batch_size: int = Field(default_factory=lambda: int(os.getenv('BATCH_SIZE', 32)))
    
    # Logging
    log_level: str = Field(default_factory=lambda: os.getenv('LOG_LEVEL', 'INFO'))
    log_rotation: str = Field(default_factory=lambda: os.getenv('LOG_ROTATION', '10 MB'))
    
    class Config:
        arbitrary_types_allowed = True
    
    def create_directories(self):
        """Cria diretórios necessários."""
        for dir_path in [self.data_dir, self.cache_dir, self.logs_dir, self.models_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)


# Instância global
config = ProjectConfig()
config.create_directories()
```

**3. Validadores - `src/utils/validators.py`:**

```python
"""
Funções de validação de dados.
"""

from typing import Optional
import re


def validate_medical_text(text: str, min_length: int = 10) -> bool:
    """
    Valida se um texto médico é válido.
    
    Args:
        text: Texto para validar
        min_length: Comprimento mínimo
        
    Returns:
        True se válido
    """
    if not text or not isinstance(text, str):
        return False
    
    text = text.strip()
    
    if len(text) < min_length:
        return False
    
    # Verificar se tem pelo menos algumas palavras
    words = text.split()
    if len(words) < 3:
        return False
    
    return True


def clean_medical_text(text: str) -> str:
    """
    Limpa texto médico.
    
    Args:
        text: Texto original
        
    Returns:
        Texto limpo
    """
    if not isinstance(text, str):
        return ""
    
    # Remover múltiplos espaços
    text = re.sub(r'\s+', ' ', text)
    
    # Remover múltiplas quebras de linha
    text = re.sub(r'\n+', '\n', text)
    
    # Strip
    text = text.strip()
    
    return text


def extract_age(text: str) -> Optional[int]:
    """
    Tenta extrair idade de um texto.
    
    Args:
        text: Texto contendo possível idade
        
    Returns:
        Idade extraída ou None
    """
    # Padrões comuns: "55 years old", "age 55", "55-year-old"
    patterns = [
        r'(\d{1,3})\s*years?\s*old',
        r'age\s*(\d{1,3})',
        r'(\d{1,3})-year-old'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            age = int(match.group(1))
            if 0 < age < 120:  # Validação básica
                return age
    
    return None
```

**Teste os utilitários:**

```python
# test_utils.py
from src.utils.logger import logger
from src.utils.config import config
from src.utils.validators import validate_medical_text, clean_medical_text, extract_age

# Testar logger
logger.info("✅ Logger funcionando!")
logger.warning("⚠️ Teste de warning")
logger.error("❌ Teste de erro")

# Testar config
print(f"\n📁 Diretório do projeto: {config.project_root}")
print(f"🤖 Modelo Gemini: {config.gemini_model}")
print(f"📊 Max transcrições: {config.max_transcriptions}")

# Testar validators
text1 = "Patient is a 55-year-old male with diabetes"
print(f"\n✅ Texto válido: {validate_medical_text(text1)}")
print(f"🎂 Idade extraída: {extract_age(text1)}")

text2 = "   Multiple    spaces   here   \n\n\n"
print(f"🧹 Texto limpo: '{clean_medical_text(text2)}'")
```

Execute:
```powershell
python test_utils.py
```

**Checkpoint:** Todos os utilitários devem funcionar sem erros.

### Passo 3.2: Implementar TranscriptionsLoader (90 min)

Crie `src/data/transcriptions_loader.py`:

```python
"""
Loader para Medical Transcriptions Dataset.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Optional
from loguru import logger
import re

from src.utils.config import config
from src.utils.validators import clean_medical_text, extract_age


class TranscriptionsLoader:
    """Gerencia o dataset Medical Transcriptions."""
    
    def __init__(self, data_path: str = "data/raw/mtsamples.csv"):
        self.data_path = Path(data_path)
        self.df: Optional[pd.DataFrame] = None
        self.specialties: List[str] = []
        
        logger.info(f"TranscriptionsLoader inicializado: {self.data_path}")
    
    def load(self) -> pd.DataFrame:
        """Carrega dataset do CSV."""
        logger.info(f"📂 Carregando {self.data_path}")
        
        if not self.data_path.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {self.data_path}")
        
        try:
            self.df = pd.read_csv(self.data_path)
            logger.info(f"✅ {len(self.df)} transcrições carregadas")
            logger.info(f"📋 Colunas: {list(self.df.columns)}")
            
            # Especialidades únicas
            self.specialties = sorted(
                self.df['medical_specialty'].dropna().unique().tolist()
            )
            logger.info(f"🏥 {len(self.specialties)} especialidades únicas")
            
            return self.df
            
        except Exception as e:
            logger.error(f"❌ Erro ao carregar: {e}")
            raise
    
    def preprocess(self) -> pd.DataFrame:
        """Pré-processa os dados."""
        if self.df is None:
            self.load()
        
        logger.info("🔧 Iniciando pré-processamento...")
        
        # 1. Tratar nulos
        self.df['description'] = self.df['description'].fillna('')
        self.df['medical_specialty'] = self.df['medical_specialty'].fillna('Unknown')
        self.df['transcription'] = self.df['transcription'].fillna('')
        self.df['keywords'] = self.df['keywords'].fillna('')
        self.df['sample_name'] = self.df['sample_name'].fillna('')
        
        # 2. Limpar textos
        logger.info("  🧹 Limpando textos...")
        self.df['transcription_clean'] = self.df['transcription'].apply(clean_medical_text)
        self.df['description_clean'] = self.df['description'].apply(clean_medical_text)
        
        # 3. Features de texto
        logger.info("  📏 Calculando features...")
        self.df['transcription_length'] = self.df['transcription'].str.len()
        self.df['word_count'] = self.df['transcription'].str.split().str.len()
        self.df['sentence_count'] = self.df['transcription'].str.count(r'[.!?]')
        
        # 4. Parse keywords
        def parse_keywords(kw_str):
            if not kw_str or pd.isna(kw_str):
                return []
            return [k.strip().lower() for k in str(kw_str).split(',')]
        
        self.df['keywords_list'] = self.df['keywords'].apply(parse_keywords)
        self.df['keywords_count'] = self.df['keywords_list'].str.len()
        
        # 5. Normalizar especialidades
        self.df['specialty_normalized'] = (
            self.df['medical_specialty']
            .str.strip()
            .str.title()
            .str.replace(r'\s+', ' ', regex=True)
        )
        
        # 6. Extrair idade quando possível
        logger.info("  🎂 Extraindo idades...")
        self.df['patient_age'] = self.df['transcription'].apply(extract_age)
        
        # 7. Criar IDs únicos
        self.df['transcription_id'] = [f"TRANS_{i:05d}" for i in range(len(self.df))]
        
        # 8. Ordenar colunas
        important_cols = [
            'transcription_id',
            'medical_specialty',
            'specialty_normalized',
            'sample_name',
            'description',
            'transcription',
            'keywords',
            'patient_age'
        ]
        other_cols = [c for c in self.df.columns if c not in important_cols]
        self.df = self.df[important_cols + other_cols]
        
        logger.info("✅ Pré-processamento concluído")
        
        # Salvar
        output_path = Path("data/processed/transcriptions_processed.csv")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        self.df.to_csv(output_path, index=False)
        logger.info(f"💾 Salvo em {output_path}")
        
        return self.df
    
    def get_by_specialty(self, specialty: str) -> pd.DataFrame:
        """Filtra por especialidade."""
        if self.df is None:
            self.load()
        
        mask = (
            (self.df['medical_specialty'] == specialty) |
            (self.df['specialty_normalized'] == specialty)
        )
        
        result = self.df[mask].copy()
        logger.info(f"🔍 {len(result)} casos de {specialty}")
        
        return result
    
    def search_by_keyword(self, keyword: str, top_k: int = 10) -> pd.DataFrame:
        """Busca por palavra-chave."""
        if self.df is None:
            self.load()
        
        keyword_lower = keyword.lower()
        
        mask = (
            self.df['transcription'].str.lower().str.contains(keyword_lower, na=False) |
            self.df['description'].str.lower().str.contains(keyword_lower, na=False) |
            self.df['keywords'].str.lower().str.contains(keyword_lower, na=False)
        )
        
        results = self.df[mask].head(top_k)
        logger.info(f"🔍 {len(results)} resultados para '{keyword}'")
        
        return results
    
    def get_statistics(self) -> Dict:
        """Retorna estatísticas."""
        if self.df is None:
            self.load()
        
        stats = {
            'total_transcriptions': len(self.df),
            'total_specialties': self.df['medical_specialty'].nunique(),
            'specialties_distribution': self.df['medical_specialty'].value_counts().to_dict(),
            'avg_transcription_length': float(self.df['transcription'].str.len().mean()),
            'median_transcription_length': float(self.df['transcription'].str.len().median()),
            'avg_word_count': float(self.df['transcription'].str.split().str.len().mean()),
            'total_with_age': int(self.df['patient_age'].notna().sum()),
            'avg_patient_age': float(self.df['patient_age'].mean()) if 'patient_age' in self.df else None
        }
        
        return stats
    
    def get_random_sample(self, n: int = 5, specialty: Optional[str] = None) -> pd.DataFrame:
        """Amostra aleatória."""
        if self.df is None:
            self.load()
        
        if specialty:
            df_filtered = self.get_by_specialty(specialty)
        else:
            df_filtered = self.df
        
        n_sample = min(n, len(df_filtered))
        return df_filtered.sample(n=n_sample, random_state=42)


# ============================================================================
# TESTE
# ============================================================================

if __name__ == "__main__":
    from src.utils.logger import setup_logger
    setup_logger()
    
    # Criar loader
    loader = TranscriptionsLoader()
    
    # Carregar e processar
    df = loader.load()
    df_processed = loader.preprocess()
    
    # Estatísticas
    stats = loader.get_statistics()
    print("\n📊 ESTATÍSTICAS:")
    for key, value in stats.items():
        if key != 'specialties_distribution':
            print(f"  {key}: {value}")
    
    # Top 10 especialidades
    print("\n🏥 TOP 10 ESPECIALIDADES:")
    top_specs = sorted(
        stats['specialties_distribution'].items(),
        key=lambda x: x[1],
        reverse=True
    )[:10]
    for spec, count in top_specs:
        print(f"  {spec}: {count}")
    
    # Teste de busca
    print("\n🔍 BUSCA: 'diabetes'")
    results = loader.search_by_keyword('diabetes', top_k=3)
    for _, row in results.iterrows():
        print(f"\n  ID: {row['transcription_id']}")
        print(f"  Especialidade: {row['medical_specialty']}")
        print(f"  Descrição: {row['description'][:80]}...")
```

**Execute o teste:**

```powershell
python src/data/transcriptions_loader.py
```

**Checkpoint:** 
- ✅ Arquivo `data/processed/transcriptions_processed.csv` criado
- ✅ Estatísticas exibidas corretamente
- ✅ Busca funcionando

### Passo 3.3: Implementar AbstractsLoader (90 min)

Crie `src/data/abstracts_loader.py`:

```python
"""
Loader para Research Abstracts Dataset.
"""

import pandas as pd
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from loguru import logger
from dataclasses import dataclass, asdict
from collections import defaultdict
import json

from src.utils.config import config


@dataclass
class AbstractSentence:
    """Representa uma sentença de um abstract."""
    text: str
    label: str  # OBJECTIVE, METHODS, RESULTS, CONCLUSIONS, BACKGROUND
    line_number: int
    
    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class Abstract:
    """Representa um abstract completo."""
    abstract_id: str
    sentences: List[AbstractSentence]
    
    def get_by_label(self, label: str) -> List[str]:
        """Retorna sentenças de um label."""
        return [s.text for s in self.sentences if s.label == label]
    
    def get_full_text(self) -> str:
        """Retorna texto completo."""
        return ' '.join([s.text for s in self.sentences])
    
    def to_dict(self) -> Dict:
        """Converte para dicionário."""
        return {
            'abstract_id': self.abstract_id,
            'objective': ' '.join(self.get_by_label('OBJECTIVE')),
            'methods': ' '.join(self.get_by_label('METHODS')),
            'results': ' '.join(self.get_by_label('RESULTS')),
            'conclusions': ' '.join(self.get_by_label('CONCLUSIONS')),
            'background': ' '.join(self.get_by_label('BACKGROUND')),
            'full_text': self.get_full_text(),
            'num_sentences': len(self.sentences)
        }


class AbstractsLoader:
    """Gerencia o dataset de Research Abstracts."""
    
    VALID_LABELS = {'OBJECTIVE', 'METHODS', 'RESULTS', 'CONCLUSIONS', 'BACKGROUND'}
    
    def __init__(self, data_dir: str = "data/raw"):
        self.data_dir = Path(data_dir)
        self.train_file = self.data_dir / "train.txt"
        self.test_file = self.data_dir / "test.txt"
        self.dev_file = self.data_dir / "dev.txt"
        
        self.abstracts: List[Abstract] = []
        self.df: Optional[pd.DataFrame] = None
        
        logger.info(f"AbstractsLoader inicializado: {self.data_dir}")
    
    def load(
        self,
        split: str = 'train',
        max_abstracts: Optional[int] = None
    ) -> List[Abstract]:
        """
        Carrega abstracts de um split.
        
        Args:
            split: 'train', 'test' ou 'dev'
            max_abstracts: Limite de abstracts (None = todos)
            
        Returns:
            Lista de Abstract objects
        """
        file_map = {
            'train': self.train_file,
            'test': self.test_file,
            'dev': self.dev_file
        }
        
        if split not in file_map:
            raise ValueError(f"Split inválido: {split}")
        
        filepath = file_map[split]
        
        if not filepath.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {filepath}")
        
        logger.info(f"📂 Carregando {filepath.name}...")
        
        if max_abstracts is None:
            max_abstracts = config.max_abstracts
        
        # Parse arquivo
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
        Parse do arquivo TXT.
        
        Formato: sentença TAB label TAB line_num TAB abstract_id
        """
        abstracts_dict = defaultdict(list)
        current_abstract_id = None
        sentence_counter = 0
        
        logger.info(f"  📖 Parseando {filepath.name}...")
        
        with open(filepath, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                parts = line.strip().split('\t')
                
                if len(parts) < 2:
                    continue
                
                sentence_text = parts[0].strip()
                label = parts[1].strip().upper()
                
                # Validar label
                if label not in self.VALID_LABELS:
                    logger.warning(f"Label inválido na linha {line_num}: {label}")
                    continue
                
                # Abstract ID (usar número se não fornecido)
                if len(parts) > 3 and parts[3]:
                    abstract_id = parts[3].strip()
                else:
                    # Criar novo ID quando encontrar OBJECTIVE (início de abstract)
                    if label == 'OBJECTIVE' or current_abstract_id is None:
                        sentence_counter += 1
                        current_abstract_id = f"abstract_{sentence_counter:06d}"
                    abstract_id = current_abstract_id
                
                # Criar sentença
                sentence = AbstractSentence(
                    text=sentence_text,
                    label=label,
                    line_number=line_num
                )
                
                abstracts_dict[abstract_id].append(sentence)
                
                # Verificar limite
                if max_abstracts and len(abstracts_dict) >= max_abstracts:
                    logger.info(f"  ⚠️ Limite de {max_abstracts} abstracts atingido")
                    break
        
        # Converter para Abstract objects
        abstracts = [
            Abstract(abstract_id=aid, sentences=sentences)
            for aid, sentences in abstracts_dict.items()
        ]
        
        logger.info(f"  ✅ {len(abstracts)} abstracts parseados")
        
        return abstracts
    
    def to_dataframe(self) -> pd.DataFrame:
        """Converte para DataFrame."""
        if not self.abstracts:
            logger.warning("Nenhum abstract carregado")
            return pd.DataFrame()
        
        logger.info("📊 Convertendo para DataFrame...")
        
        data = [abstract.to_dict() for abstract in self.abstracts]
        self.df = pd.DataFrame(data)
        
        logger.info(f"✅ DataFrame: {self.df.shape}")
        
        return self.df
    
    def search(self, query: str, top_k: int = 10) -> List[Abstract]:
        """Busca simples por keyword."""
        if not self.abstracts:
            logger.warning("Nenhum abstract carregado")
            return []
        
        query_lower = query.lower()
        results = []
        
        for abstract in self.abstracts:
            full_text = abstract.get_full_text().lower()
            
            if query_lower in full_text:
                results.append(abstract)
                
                if len(results) >= top_k:
                    break
        
        logger.info(f"🔍 {len(results)} abstracts encontrados para '{query}'")
        
        return results
    
    def get_statistics(self) -> Dict:
        """Estatísticas do dataset."""
        if not self.abstracts:
            return {}
        
        label_counts = defaultdict(int)
        total_sentences = 0
        sentence_lengths = []
        
        for abstract in self.abstracts:
            total_sentences += len(abstract.sentences)
            for sentence in abstract.sentences:
                label_counts[sentence.label] += 1
                sentence_lengths.append(len(sentence.text))
        
        stats = {
            'total_abstracts': len(self.abstracts),
            'total_sentences': total_sentences,
            'avg_sentences_per_abstract': total_sentences / len(self.abstracts),
            'label_distribution': dict(label_counts),
            'avg_sentence_length': sum(sentence_lengths) / len(sentence_lengths) if sentence_lengths else 0
        }
        
        return stats
    
    def save_processed(self, output_path: str = "data/processed/abstracts_processed.json"):
        """Salva em JSON."""
        if not self.abstracts:
            logger.warning("Nenhum abstract para salvar")
            return
        
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        data = [abstract.to_dict() for abstract in self.abstracts]
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"💾 {len(data)} abstracts salvos em {output_file}")
    
    def filter_by_label(self, label: str) -> List[str]:
        """Retorna todas as sentenças de um label específico."""
        sentences = []
        
        for abstract in self.abstracts:
            sentences.extend(abstract.get_by_label(label))
        
        return sentences


# ============================================================================
# TESTE
# ============================================================================

if __name__ == "__main__":
    from src.utils.logger import setup_logger
    setup_logger()
    
    # Criar loader
    loader = AbstractsLoader()
    
    # Carregar subset (1000 abstracts para teste)
    abstracts = loader.load(split='train', max_abstracts=1000)
    
    # Estatísticas
    stats = loader.get_statistics()
    print("\n📊 ESTATÍSTICAS:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    # DataFrame
    df = loader.to_dataframe()
    print(f"\n📋 DataFrame shape: {df.shape}")
    print("\nPrimeiras 3 linhas:")
    print(df[['abstract_id', 'num_sentences']].head(3))
    
    # Busca
    print("\n🔍 BUSCA: 'diabetes'")
    results = loader.search('diabetes', top_k=3)
    for i, abstract in enumerate(results, 1):
        print(f"\nAbstract {i} ({abstract.abstract_id}):")
        obj = ' '.join(abstract.get_by_label('OBJECTIVE'))
        res = ' '.join(abstract.get_by_label('RESULTS'))
        print(f"  OBJECTIVE: {obj[:100]}...")
        print(f"  RESULTS: {res[:100]}...")
    
    # Salvar
    loader.save_processed()
    
    # Exemplos de cada label
    print("\n🏷️ EXEMPLOS POR LABEL:")
    for label in loader.VALID_LABELS:
        examples = loader.filter_by_label(label)
        if examples:
            print(f"\n{label}:")
            print(f"  Total: {len(examples)}")
            print(f"  Exemplo: {examples[0][:100]}...")
```

**Execute:**

```powershell
python src/data/abstracts_loader.py
```

**Checkpoint:**
- ✅ Arquivo `data/processed/abstracts_processed.json` criado
- ✅ Estatísticas corretas
- ✅ Busca funcionando

### Passo 3.4: Commit do progresso

```powershell
git add .
git commit -m "Feat: Implemented data loaders for both datasets"
```

---

**🎉 PARABÉNS! Você completou os primeiros 3 dias!**

Neste ponto você tem:
- ✅ Ambiente configurado
- ✅ Datasets baixados e explorados
- ✅ Data loaders funcionando
- ✅ Utilitários básicos implementados

**Continue para a Fase 2 (Dias 4-7) onde vamos:**
- Criar embeddings semânticos
- Implementar ferramentas de NLP médico
- Desenvolver classificadores
- Preparar sistema de busca

---

# FASE 2: Ferramentas e NLP (Dias 4-7)

[Continua no próximo bloco - quer que eu continue?]
