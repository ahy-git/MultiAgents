from flask import Flask, request
from receiveWhatsapp import MessageWhatsapp as Message
from sendWhatsapp import SendWhatsapp
from generate import TextToSpeech
from transcriptAHY import Transcript
from fluxo_audio_origin import FluxoAudio

app = Flask(__name__)

@app.route("/messages-upsert", methods=['POST'])
def webhook():
    send = SendWhatsapp()
    
    try:
        raw_data = request.get_json()

        # Proteção contra estrutura inesperada
        if isinstance(raw_data, list):
            data = raw_data[0]
        elif isinstance(raw_data, dict):
            data = raw_data
        else:
            raise ValueError("Formato inesperado de JSON.")

        msg = Message(data)
        if not msg.data:
            print("[INFO] Nenhuma mensagem válida no update, ignorando.")
            return "ignorado"


        if msg.phone == "5511984617987":
            if msg.message_type == Message.TYPE_TEXT:
                text = msg.get_text()
            elif msg.message_type == Message.TYPE_AUDIO:
                tsc = Transcript()
                text = tsc.get_text(msg)
            else:
                text = "[Tipo de mensagem não suportado]"

            fluxo = FluxoAudio()
            resposta = fluxo.kickoff(inputs={'text': text})

            speech = TextToSpeech()
            speech.synthesize_speech(text=resposta, output_file="output.mp3")

            send.textMessage(msg.phone, resposta)
            send.audio(msg.phone, audio_file="output.mp3")

    except Exception as e:
        print(f"[Erro no processamento da mensagem]: {e}")
        phone = "5511984617987"
     #   send.textMessage(phone, f"Erro no envio da msg: {e}")

    return "resposta"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6565, debug=True)
