import streamlit as st

# Mock data para teste direto
mock_data = {
    "flights": [
        {
            "tipo": "IDA",
            "companhia": "LATAM",
            "partida": "08:00",
            "chegada": "22:30", 
            "duracao": "14h30m",
            "preco": "R$ 1.650",
            "rota": "São Paulo → Paris",
            "link_compra": "https://www.latam.com/pt_br/apps/personas?fecha1_dia=15&fecha1_anomes=012025&from_city1=São%20Paulo&to_city1=Paris&auAvailability=1&ida_vuelta=ida&tipo_pasajero1=ADT&cantidad_pasajeros=1&cantidad_ninos=0&cantidad_infantes=0",
            "codigo_voo": "LA8084",
            "classe": "Econômica"
        },
        {
            "tipo": "VOLTA",
            "companhia": "LATAM",
            "partida": "10:15",
            "chegada": "16:45",
            "duracao": "12h30m",
            "preco": "R$ 1.540",
            "rota": "Paris → São Paulo",
            "link_compra": "https://www.latam.com/pt_br/apps/personas?fecha1_dia=22&fecha1_anomes=012025&from_city1=Paris&to_city1=São%20Paulo&auAvailability=1&ida_vuelta=ida&tipo_pasajero1=ADT&cantidad_pasajeros=1&cantidad_ninos=0&cantidad_infantes=0",
            "codigo_voo": "LA8185",
            "classe": "Econômica"
        }
    ],
    "stays": [
        {
            "nome": "Hotel Mercure Paris Centre",
            "localizacao": "Centro de Paris - Châtelet",
            "tipo_quarto": "Standard Double",
            "preco_noite": "R$ 825",
            "preco_total": "R$ 3.300",
            "avaliacao": "4.2/5 ⭐⭐⭐⭐",
            "link_reserva": "https://www.booking.com/hotel/fr/mercure-paris-centre.pt-br.html",
            "comodidades": ["Wi-Fi gratuito", "Academia", "Restaurante", "Room Service"],
            "cancelamento": "Cancelamento grátis até 24h antes"
        }
    ],
    "activities": [
        {
            "nome": "Tour pela Torre Eiffel",
            "descricao": "Visita guiada com acesso aos andares superiores e vista panorâmica de Paris",
            "preco": "R$ 275",
            "duracao": "3 horas",
            "categoria": "Turismo Cultural",
            "horario": "09:00 - 12:00",
            "inclui": ["Guia em português", "Acesso aos andares", "Fila prioritária"],
            "link_reserva": "https://www.getyourguide.com.br/paris-l16/torre-eiffel-ingresso-c12/",
            "avaliacao": "4.8/5 ⭐⭐⭐⭐⭐",
            "local_encontro": "Champ de Mars, Paris"
        }
    ]
}

st.set_page_config(
    page_title="Planos de Viagem IA",
    page_icon="✈️",
    layout="wide"
)

st.title("✈️ Planos de Viagem com IA")
st.markdown("**Planeje sua viagem perfeita com nossos agentes inteligentes!**")

with st.form("travel_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        origin = st.text_input("🛫 De onde você vai partir?", value="São Paulo")
        start_date = st.date_input("📅 Data de ida")
        budget = st.number_input("💰 Orçamento total (R$)", min_value=1000, value=10000, step=500)
    
    with col2:
        destination = st.text_input("🛬 Para onde você quer ir?", value="Paris")
        end_date = st.date_input("📅 Data de volta")
    
    submitted = st.form_submit_button("🔍 Buscar Plano de Viagem", use_container_width=True)

if submitted:
    st.success("✅ Plano de viagem gerado com sucesso!")
    data = mock_data
    
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
                
                st.divider()
    
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