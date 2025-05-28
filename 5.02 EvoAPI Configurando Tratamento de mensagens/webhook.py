from flask import Flask, request
from receiveWhatsapp import MessageWhatsapp
from sendWhatsapp import SendWhatsapp

app = Flask(__name__)

@app.route("/message-upsert",methods=['POST'])

def eco():
    data = request.get_json()
    msg = MessageWhatsapp(data)
    sender = SendWhatsapp()
    
    sender.textMessage(number=msg.phone, msg=msg.get_text())
    
    return ""

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
    
    
    
    
    
    
    
    
    
    
    
