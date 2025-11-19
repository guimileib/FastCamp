import streamlit as st
import pandas as pd
from coordinator import CoordinatorAgent

# Configuração da Página
st.set_page_config(
    page_title="Medical AI Agents",
    page_icon="🩺",
    layout="wide"
)

# Título e Descrição
st.title("🩺 Sistema Multi-Agentes de Apoio Médico")
st.markdown("""
Este sistema utiliza uma arquitetura de **Agentes Inteligentes** (powered by Google Gemini) para auxiliar na análise clínica.
O fluxo de trabalho é dividido entre agentes especialistas: **Triagem**, **Diagnóstico** e **Tratamento**.
""")

# Sidebar para Configurações e Seleção
with st.sidebar:
    st.header("⚙️ Configurações")
    st.info("Certifique-se de que o arquivo .env contém sua GOOGLE_API_KEY.")
    
    st.divider()
    
    st.header("📂 Seleção de Caso")
    try:
        df = pd.read_csv('data/mtsamples.csv')
        st.success(f"Base de dados carregada: {len(df)} registros.")
        
        # Filtros
        specialties = df['medical_specialty'].unique()
        selected_specialty = st.selectbox("Filtrar por Especialidade:", ["Todas"] + list(specialties))
        
        if selected_specialty != "Todas":
            filtered_df = df[df['medical_specialty'] == selected_specialty]
        else:
            filtered_df = df
            
        # Seleção do Caso Específico
        case_options = filtered_df.apply(lambda x: f"ID {x.name}: {x['description'][:50]}...", axis=1)
        selected_case_index = st.selectbox("Escolha um caso para analisar:", filtered_df.index, format_func=lambda x: f"ID {x}: {df.loc[x, 'description'][:60]}...")
        
        if st.button("🎲 Caso Aleatório"):
            selected_case_index = filtered_df.sample(1).index[0]
            st.rerun()
            
    except FileNotFoundError:
        st.error("Arquivo 'data/mtsamples.csv' não encontrado.")
        st.stop()

# Carregar o caso selecionado
case = df.loc[selected_case_index]

# Exibir Detalhes do Caso (Input)
st.subheader("📄 Detalhes do Caso Clínico")
col1, col2 = st.columns([1, 3])
with col1:
    st.metric("ID do Caso", case.name)
    st.metric("Especialidade", case['medical_specialty'])
with col2:
    st.text_area("Transcrição Médica (Input para os Agentes)", case['transcription'], height=200)

# Botão de Ação
if st.button("🚀 Iniciar Análise Multi-Agente", type="primary"):
    coordinator = CoordinatorAgent()
    
    with st.spinner('Os agentes estão analisando o caso...'):
        # Executar o Coordenador
        results = coordinator.process_case(case['transcription'], case['description'])
    
    st.success("Análise concluída com sucesso!")
    
    # Exibir Resultados em Abas
    tab1, tab2, tab3 = st.tabs(["🚑 Triagem", "🔍 Diagnóstico", "💊 Tratamento"])
    
    with tab1:
        st.header("Relatório de Triagem")
        st.markdown(results['triage'])
        
    with tab2:
        st.header("Análise Diagnóstica")
        st.markdown(results['diagnostic'])
        
    with tab3:
        st.header("Plano de Tratamento")
        st.markdown(results['treatment'])

    # Expander para ver o JSON bruto (opcional)
    with st.expander("Ver dados brutos da resposta"):
        st.json(results)

# Rodapé
st.divider()
st.caption("Nota: Este é um protótipo de IA para fins educacionais e de demonstração. Não substitui o aconselhamento médico profissional.")
