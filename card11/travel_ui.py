import streamlit as st
import requests
import json


st.set_page_config(page_title="Planejador de Viagens com IA", page_icon="✈️")
st.title("🌍 Planejador de Viagens com IA")

with st.sidebar:
    st.header("🔧 Status dos Agentes")
    
    # Só verifica status quando o usuário clicar no botão
    if st.button("🔄 Verificar Status"):
        def verificar_agente(nome, porta):
            try:
                response = requests.get(f"http://localhost:{porta}/docs", timeout=2)
                return "🟢" if response.status_code == 200 else "🔴"
            except:
                return "🔴"
        
        st.write(f"{verificar_agente('Host', 8000)} Host Agent (8000)")
        st.write(f"{verificar_agente('Voos', 8001)} Flight Agent (8001)")
        st.write(f"{verificar_agente('Hospedagem', 8002)} Stay Agent (8002)")
        st.write(f"{verificar_agente('Atividades', 8003)} Activities Agent (8003)")
        
        st.markdown("---")
        st.caption("🟢 Online | 🔴 Offline")
    else:
        st.info("Clique para verificar se os agentes estão online")
        st.caption("Host: 8000 | Voos: 8001 | Hospedagem: 8002 | Atividades: 8003")

# Formulário principal
origin = st.text_input("🛫 De onde você está saindo?", placeholder="Ex: São Paulo")
destination = st.text_input("🛬 Para onde você vai?", placeholder="Ex: Paris")
start_date = st.date_input("📅 Data de ida")
end_date = st.date_input("📅 Data de volta")
budget = st.number_input("💰 Orçamento (em USD)", min_value=100, step=50, value=1000)

if st.button("🚀 Planejar Minha Viagem"):
    if not all([origin, destination, start_date, end_date, budget]):
        st.warning("⚠️ Por favor, preencha todos os campos.")
    else:
        with st.spinner("🔄 Planejando sua viagem... Isso pode levar alguns segundos."):
            payload = {
                "origin": origin,
                "destination": destination,
                "start_date": str(start_date),
                "end_date": str(end_date),
                "budget": budget
            }
            
            try:
                response = requests.post(
                    "http://localhost:8000/run", 
                    json=payload, 
                    timeout=120
                )
                
                if response.ok:
                    data = response.json()
                    
                    st.success("✅ Plano de viagem gerado com sucesso!")
                    
                    # Exibir Voos
                    st.subheader("✈️ Voos Disponíveis")
                    if isinstance(data.get("flights"), list):
                        # Separar voos de ida e volta
                        voos_ida = [flight for flight in data["flights"] if flight.get('tipo') == 'IDA']
                        voos_volta = [flight for flight in data["flights"] if flight.get('tipo') == 'VOLTA']
                        
                        # Voos de IDA
                        st.markdown("### 🛫 **VOOS DE IDA**")
                        for i, flight in enumerate(voos_ida, 1):
                            with st.expander(f"✈️ {flight.get('companhia', 'Companhia')} - {flight.get('preco', 'Preço não disponível')}"):
                                col1, col2 = st.columns(2)
                                
                                with col1:
                                    st.write(f"**🛫 Partida:** {flight.get('partida', 'N/A')}")
                                    st.write(f"**🛬 Chegada:** {flight.get('chegada', 'N/A')}")
                                    st.write(f"**⏱️ Duração:** {flight.get('duracao', 'N/A')}")
                                    if flight.get('promocao'):
                                        st.warning(flight['promocao'])
                                
                                with col2:
                                    st.write(f"**🎫 Código:** {flight.get('codigo_voo', 'N/A')}")
                                    st.write(f"**💺 Classe:** {flight.get('classe', 'N/A')}")
                                    st.write(f"**🗺️ Rota:** {flight.get('rota', 'N/A')}")
                                
                                # Botão de compra
                                if flight.get('link_compra'):
                                    st.markdown(f"### 🛒 [COMPRAR PASSAGEM DE IDA]({flight['link_compra']})")
                                
                                st.divider()
                        
                        # Voos de VOLTA
                        st.markdown("### 🛬 **VOOS DE VOLTA**")
                        for i, flight in enumerate(voos_volta, 1):
                            with st.expander(f"✈️ {flight.get('companhia', 'Companhia')} - {flight.get('preco', 'Preço não disponível')}"):
                                col1, col2 = st.columns(2)
                                
                                with col1:
                                    st.write(f"**🛫 Partida:** {flight.get('partida', 'N/A')}")
                                    st.write(f"**🛬 Chegada:** {flight.get('chegada', 'N/A')}")
                                    st.write(f"**⏱️ Duração:** {flight.get('duracao', 'N/A')}")
                                    if flight.get('promocao'):
                                        st.warning(flight['promocao'])
                                
                                with col2:
                                    st.write(f"**🎫 Código:** {flight.get('codigo_voo', 'N/A')}")
                                    st.write(f"**💺 Classe:** {flight.get('classe', 'N/A')}")
                                    st.write(f"**🗺️ Rota:** {flight.get('rota', 'N/A')}")
                                
                                # Botão de compra
                                if flight.get('link_compra'):
                                    st.markdown(f"### 🛒 [COMPRAR PASSAGEM DE VOLTA]({flight['link_compra']})")
                                
                                st.divider()
                    else:
                        st.info(str(data.get("flights", "Nenhum voo disponível")))
                    
                    # Exibir Hospedagens
                    st.subheader("🏨 Hospedagens Disponíveis")
                    if isinstance(data.get("stays"), list):
                        for i, stay in enumerate(data["stays"], 1):
                            with st.expander(f"🏨 {stay.get('nome', 'Hotel')} - {stay.get('preco_total', 'Preço não disponível')}"):
                                col1, col2 = st.columns(2)
                                
                                with col1:
                                    st.write(f"**📍 Localização:** {stay.get('localizacao', 'N/A')}")
                                    st.write(f"**🛏️ Quarto:** {stay.get('tipo_quarto', 'N/A')}")
                                    st.write(f"**💰 Por noite:** {stay.get('preco_noite', 'N/A')}")
                                    st.write(f"**⭐ Avaliação:** {stay.get('avaliacao', 'N/A')}")
                                    if stay.get('promocao'):
                                        st.success(stay['promocao'])
                                
                                with col2:
                                    st.write(f"**💳 Total:** {stay.get('preco_total', 'N/A')}")
                                    st.write(f"**❌ Cancelamento:** {stay.get('cancelamento', 'Consulte o hotel')}")
                                    
                                    if stay.get('comodidades'):
                                        st.write("**🎯 Comodidades:**")
                                        for comodidade in stay['comodidades']:
                                            st.write(f"• {comodidade}")
                                
                                # Botão de reserva
                                if stay.get('link_reserva'):
                                    st.markdown(f"### 🏨 [RESERVAR HOTEL]({stay['link_reserva']})")
                                    st.markdown(f"**Link direto:** {stay['link_reserva']}")
                                
                                st.divider()
                    else:
                        st.info(str(data.get("stays", "Nenhuma hospedagem disponível")))
                    
                    # Exibir Atividades
                    st.subheader("🗺️ Atividades Sugeridas")
                    if isinstance(data.get("activities"), list):
                        for i, activity in enumerate(data["activities"], 1):
                            with st.expander(f"🗺️ {activity.get('nome', 'Atividade')} - {activity.get('preco', 'Preço não disponível')}"):
                                col1, col2 = st.columns(2)
                                
                                with col1:
                                    st.write(f"**📝 Descrição:** {activity.get('descricao', 'N/A')}")
                                    st.write(f"**⏰ Duração:** {activity.get('duracao', 'N/A')}")
                                    st.write(f"**🕐 Horário:** {activity.get('horario', 'Consulte disponibilidade')}")
                                    st.write(f"**🏷️ Categoria:** {activity.get('categoria', 'N/A')}")
                                    if activity.get('promocao'):
                                        st.warning(activity['promocao'])
                                
                                with col2:
                                    st.write(f"**💰 Preço:** {activity.get('preco', 'N/A')}")
                                    st.write(f"**⭐ Avaliação:** {activity.get('avaliacao', 'N/A')}")
                                    st.write(f"**📍 Encontro:** {activity.get('local_encontro', 'A definir')}")
                                    
                                    if activity.get('inclui'):
                                        st.write("**✅ Inclui:**")
                                        for item in activity['inclui']:
                                            st.write(f"• {item}")
                                
                                # Botão de reserva
                                if activity.get('link_reserva'):
                                    st.markdown(f"### 🎫 [RESERVAR ATIVIDADE]({activity['link_reserva']})")
                                
                                st.divider()
                    else:
                        st.info(str(data.get("activities", "Nenhuma atividade encontrada")))
                    
                    # Resposta completa (debug)
                    with st.expander("📄 Ver resposta completa (JSON)"):
                        st.json(data)
                        
                else:
                    st.error(f"❌ Falha ao buscar plano de viagem. Código: {response.status_code}")
                    st.error(f"Detalhes: {response.text}")
                    
            except requests.exceptions.ConnectionError:
                st.error("❌ **Erro de Conexão!**")
                st.warning("⚠️ Os agentes não estão rodando.")
                
            except requests.exceptions.Timeout:
                st.error("⏱️ **Timeout!**")
                st.warning("A requisição demorou muito tempo. Tente novamente.")
                
            except Exception as e:
                st.error(f"❌ **Erro inesperado:** {str(e)}")
                st.exception(e)