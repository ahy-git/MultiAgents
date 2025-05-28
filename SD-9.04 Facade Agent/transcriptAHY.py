import os
import base64
from faster_whisper import WhisperModel


class Transcript:
    
    def __init__(self, save_dir="audio"):
        # Diretório para salvar os áudios
        self.save_dir = save_dir
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

    def fix_base64_padding(self, base64_string):
        """
        Corrige padding de base64 se necessário
        """
        missing_padding = len(base64_string) % 4
        if missing_padding != 0:
            base64_string += "=" * (4 - missing_padding)
        return base64_string
    
    def transcribe_audio_with_whisper(self, audio_file):
        """
        Transcreve o áudio usando faster-whisper.
        """
        try:
            # Carrega o modelo (use "base", "small", etc. – e use GPU se disponível)
            model = WhisperModel("medium", device="cpu", compute_type="int8")  # Altere para "cuda" se tiver GPU
            
            segments, _ = model.transcribe(audio_file, beam_size=5)
            
            # Concatena o texto de todos os segmentos
            text = " ".join([segment.text for segment in segments])
            return text

        except Exception as e:
            print(f"Erro durante a transcrição: {e}")
            return None

    def get_text(self, data) -> str:
        """
        Recebe o objeto de dados com áudio em base64, salva o arquivo, transcreve e retorna o texto.
        """
        try:
            code_base64 = self.fix_base64_padding(data.audio_base64_bytes)
            audio_data = base64.b64decode(code_base64)

            output_file = os.path.join(self.save_dir, "output_audio.wav")
            with open(output_file, "wb") as audio_file:
                audio_file.write(audio_data)

            print(f"Áudio salvo com sucesso em {output_file}")
            
            transcription = self.transcribe_audio_with_whisper(output_file)

            os.remove(output_file)

            return transcription

        except base64.binascii.Error as e:
            print(f"Erro de decodificação Base64: {e}")
            return None
        except Exception as e:
            print(f"Erro geral: {e}")
            return None
