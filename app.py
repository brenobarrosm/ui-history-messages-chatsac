import os
from datetime import datetime

import streamlit as st
import requests

# Define o token de acesso
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')


# Função para fazer a requisição GET para a API
def get_messages(id_message):
    url = f'https://api.chatsac.com/core/v2/api/chats/{id_message}'
    headers = {
        'access-token': ACCESS_TOKEN
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        st.error('Erro na requisição: ' + response.text)
        return None

# Função para formatar a data e hora
def format_datetime(dt_str):
    dt = datetime.strptime(dt_str.split('.')[0], '%Y-%m-%dT%H:%M:%S')
    return dt.strftime("%d/%m - %H:%M")

# Configura a página do Streamlit
st.title('Histórico de Mensagens')

# Campo de texto para o ID da mensagem
id_message = st.text_input('Informe o ID do chat')

# Botão para fazer a requisição
if st.button('Buscar Mensagens'):
    if id_message:
        data = get_messages(id_message)

        if data and 'messages' in data:
            messages = data['messages']
            for message in messages:
                # Ignorar mensagens específicas
                if message['text'] == "Chat iniciado por: CLIENTE":
                    continue

                # Formatar a data e hora
                formatted_datetime = format_datetime(message['dhMessage'])

                # Exibir mensagens estilo chat
                if message['isSentByMe']:
                    # Mensagem enviada por mim
                    st.markdown(f"""
                    <div style='display: flex; justify-content: flex-start;'>
                        <div style='background-color: #3f1bee; padding: 10px; margin: 10px; border-radius: 10px; max-width: 70%;'>
                            <p style='font-size: 18px; color: white'><strong>{message['text']}</strong></p>
                            <span style='color: white'>{formatted_datetime}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    # Mensagem enviada pelo cliente
                    st.markdown(f"""
                    <div style='display: flex; justify-content: flex-end;'>
                        <div style='background-color: #ff1380; padding: 10px; margin: 10px; border-radius: 10px; max-width: 70%;'>
                            <p style='font-size: 18px; color: white'><strong>{message['text']}</strong></p>
                            <span style='color: white'>{formatted_datetime}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.warning('Nenhuma mensagem encontrada.')
    else:
        st.warning('Por favor, informe um ID de mensagem.')
