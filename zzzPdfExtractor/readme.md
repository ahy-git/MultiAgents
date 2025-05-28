1 - codigo gerado com chatgpt4o
    PROMPT = """
            Temos um codigo cujo objetivo esta abaixo:
        <Objetivos>
        Ler um pdf e retornar uma estrutura pydantic com informacoes sobre ele.
        </objetivos>
        <fluxo>
        1 - passamos o path do .pdf ao programa
        2 - o pdf e' transformado em texto (criar a funcao, ja que o pdf  e' um artigo cientifico com formatacao especifica). As imagens no pdf devem ser descritas. Recomendar o que fazer, Temos acesso ao tesseract, bibliotecas python e llava.
        3 - a partir do texto um agente organizara a informacao no formato de saida pydantic. Deve-se criar o modelo pydantic com 3 classes, com as informacoes mais relevantes que um artigo cientifico tem.
        4 - a saida sera mostrada no prompt como markdown
        </fluxo>
"""
2 - codigo revisado pelo deepseek
3 - codigo deepsee enviado ao chatgpt para revisao e anexo o artigo de exemplo --- Aqui o fluxo some ---
4 - codigo chatgpt #2 enviado ao deepseek para revisao e anexo o artigo de exemplo.
5 - codigo deepseek #2 enviado ao chatgpt para inclusao do resto to fluxo