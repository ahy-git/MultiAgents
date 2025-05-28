import streamlit as st

from utils.sendWhatsapp import SendWhatsapp

sender = SendWhatsapp()

st.title('Envio de Mensagem com EvoAPI')
st.subheader("Preencha os campos")

number = st.text_input("telefone")
message = st.text_area("Mensagem")
send_bt= st.button("Enviar Mensagem")

if send_bt:
    if number and message:
        try:
            response = sender.textMessage(number,message)
            st.success(f"sucesso: {response}")
        except Exception as e:
            st.error(f"Erro: {e}")
    else:
        st.warning("Preencha os campos")
        