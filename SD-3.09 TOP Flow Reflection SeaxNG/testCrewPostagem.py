from crewPostagem import CrewPostagem  # nome do seu arquivo .py sem o .py
import os

# Certifique-se de que as variáveis de ambiente do .env foram carregadas
# Se necessário, adicione seu próprio arquivo .env no mesmo diretório com as variáveis corretas

# Criando a instância do analisador
analisador = CrewPostagem()

# Dados de entrada simulados para teste
inputs = {
    "topic": "Importância da Inteligência Artificial na Educação",
    "ideia": "A IA pode ajudar a melhorar o aprendizado dos alunos com sistemas personalizados.",
    "critica": "O texto anterior estava muito vago e não explicava como a IA atuaria.",
    "objetivo": "Convencer gestores escolares a investir em soluções baseadas em IA."
}

# Executando o fluxo
resultado = analisador.kickoff(inputs=inputs)

# Exibindo o resultado da análise
print("Resultado da Análise:\n")
print(resultado)
