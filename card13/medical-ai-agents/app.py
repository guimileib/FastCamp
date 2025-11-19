import streamlit as st
from agents.host_agent.agent import HostAgent

st.set_page_config(page_title="Medical AI System", layout="wide", page_icon="🏥")

st.title("🏥 Medical AI Multi-Agent System")
st.markdown("---")

@st.cache_resource
def get_host_agent():
    return HostAgent()

try:
    host_agent = get_host_agent()
except Exception as e:
    st.error(f"Erro ao inicializar os agentes: {e}")
    st.stop()

col_input, col_output = st.columns([1, 1.5])

with col_input:
    st.subheader("📝 Dados do Paciente")
    # recebe a transcrição, dados do kaggle são inseridos aqui
    transcription = st.text_area(
        "Transcrição ou Descrição do Caso",
        height=300,
        placeholder="Ex: Paciente sexo masculino, 45 anos, relata dor torácica..."
    )
    
    analyze_btn = st.button("Iniciar Análise Multi-Agente", type="primary", use_container_width=True)

with col_output:
    st.subheader("📊 Resultados da Análise")

    if analyze_btn:
        if not transcription:
            st.warning("Por favor, insira a descrição do caso.")
        else:
            with st.spinner("Os agentes estão trabalhando..."):
                try:
                    # chamamos o método do Python diretamente, sem requests/HTTP
                    results = host_agent.process_case(transcription)
                    
                    st.success("Análise concluída com sucesso!")
                
                    tab1, tab2, tab3 = st.tabs(["🚑 Triagem", "🩺 Diagnóstico", "💊 Tratamento"]) # cada aba exibe uma informação
                    
                    with tab1:
                        st.markdown("### Relatório de Triagem")
                        st.write(results.get("triage", "Sem dados"))
                        
                    with tab2:
                        st.markdown("### Hipóteses Diagnósticas")
                        st.write(results.get("diagnostic", "Sem dados"))
                        
                    with tab3:
                        st.markdown("### Plano de Tratamento")
                        st.write(results.get("treatment", "Sem dados"))

                except Exception as e:
                    st.error(f"Ocorreu um erro durante o processamento: {e}")

st.markdown("---")
st.caption("Sistema executando localmente via Streamlit Direct-Call")