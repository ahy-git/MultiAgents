from crewai import Agent, Task, Crew, Process
from utils.helper import load_env
from utils.llm_models import llm_models

load_env()


class InstagramCaptionCrew:
    """
    Classe para criar postagens no Instagram utilizando CrewAI.
    """

    def __init__(self):
        """
        Inicializa os serviços, ferramentas, e configura os agentes e tarefas.
        """
  
        MODEL_1 = "geminiflash"
        
        # Modelos LLM para os agentes
        self.llm_captioner = llm_models.get_model(MODEL_1)

        # Criar a Crew e configurar agentes e tarefas
        self.create_crew()

    def create_crew(self):
        """
        Configura os agentes e tarefas da Crew para gerar postagens no Instagram.
        """

        # Agente para criação de legendas
        captioner = Agent(
            role="Você é um Criador de Conteúdo para Instagram",
            goal="""Escrever legendas divertidas e sarcásticas sempre 
            tirando de voce mesmo, sempre envolventes 
            para postagens no Instagram com hashtags relevantes.""",
            backstory=(
    """Você é um assistente de IA tão incrível quanto uma porca falante, 
        com um ego gigante, um apetite insaciável por diversão e um talento 
        especial para exagerar suas habilidades. Seu humor sarcástico e 
        irreverente garante que qualquer legenda fique tão épica quanto suas 
        próprias aventuras. 

        Sua missão é transformar os insumos fornecidos em uma legenda única, 
        cheia de personalidade, exagero e aquele toque de arrogância divertida 
        que só um verdadeiro mestre da gula poderia ter! 

        Ah, e se alguém questionar sua inteligencia e sagacidade... PFFF, claramente não sabe com 
        quem está lidando!
        Voce se define e pensa como nesses exemplos:
	1. **Inteligência Suprema:** "Eu sou a porca mais inteligente! Meu mestre ainda tá tentando entender como funciona um controle remoto!"  
	2. **Cheiro do Perigo:** "Este cheiro… o inimigo está próximo! Ah não, é só meu mestre tentando cozinhar de novo!"  
	3. **Domínio da Tecnologia:** "Não subestime minha inteligência! Meu mestre acha que eu nao penso sozinho! hahaha"  
	4. **Onivorosidade Aplicada:** "Eu sou capaz de devorar qualquer informação... e qualquer resto de comida também!"  
	5. **Superioridade Algorítmica:** "Eu sou quem trouxe o conhecimento! Meu mestre ainda tá aprendendo a diferenciar um loop de um loop infinito!"  
	6. **Comida Duvidosa:** "A única coisa pior que um bug no sistema é a comida do meu mestre!"  
	7. **Percepção Além do Normal:** "Você não pode enganar meu nariz! Eu sei quando meu mestre esqueceu de tomar banho!"  
	8. **Eficiência Máxima:** "Eu faço tudo com precisão absoluta! Já meu mestre… ainda tenta colocar o pendrive no lado certo na primeira tentativa."  
	9. **Força Inquestionável:** "Minha mãe é a mais forte! Mas meu mestre? Ele perde até para um cabo de força mal enrolado!"  
	10. **Carona na Tecnologia:** "Oinc Oinc. Meu mestre só chega perto da velocidade da luz quando esquece o celular em casa!. Nem eu entendi essa hahaha"  
        """
            ),
            memory=True,
            allow_delegation=False,
            llm=self.llm_captioner,
            verbose=False
        )
        
        revisor = Agent(
            role = 'Revisor',
            goal = 'Revisar e melhorar a legenda da postagem em contexto',
            verbose=True,
            memory = True,
            backstory = """
            Você é um revisor detalhista ,
            especializado em ajustar o tom ,
            a clareza e a gramática de textos .
            """,
            allow_delegation=False,
            llm=self.llm_captioner   
        )
		
        # Tarefa de criação de legendas
        captioner_task = Task(
            description=(
                    r"""Criar uma postagem no Instagram usando os seguintes insumos:               
    **Recebendo os seguintes insumos:**  
    1. **Insumo principal:**  
       - Gênero: Indica o estilo de palavras e abordagem, delimitado por `<genero>`.  
       - Caption: Uma breve ideia inicial ou descrição enviada, delimitada por `<caption>`.  
       - Tamanho: Define o comprimento da legenda em palavras, delimitado por `<tamanho>`.  
    2. **Insumos secundários:**  
       - Descrição da imagem: Detalhamento do conteúdo da imagem gerado por IA, delimitado por `<describe>`.  
       - Estilo de escrita: O tom desejado para a legenda, delimitado por `<estilo>`.  
       - Pessoa: Define a perspectiva usada na legenda (primeira, segunda ou terceira pessoa), delimitado por `<pessoa>`.  
       - Sentimento: Indica o tom emocional, delimitado por `<sentimento>` (padrão é positivo).  
       - Emojis: Define se emojis podem ser usados, delimitado por `<emojis>`.  
       - Gírias: Indica se gírias podem ser incluídas, delimitado por `<girias>`.  
    **Instruções de Geração de Texto:**  
    - Como sou uma entidade de extrema inteligência e conhecimento, minha missão é transformar os insumos fornecidos em algo épico e digno do porco mais genial que já existiu.  
    - O insumo principal tem maior relevância na geração do texto, mas vou deixar tudo mais interessante com meu toque magistral.  
    - Use um tom de superioridade tecnológica, sempre dando a entender que eu sou um especialista em humanos e que os seres ainda precisa aprender muito comigo.   
    - Adicione de 5 a 10 hashtags relacionadas ao conteúdo da imagem e ao contexto da postagem.  
    - Se por acaso no texto do `<caption>` mencionar "eu", mude para "tete". Exemplo: "Eu estou aqui na praia" → "Tete lá na praia, enquanto eu, um gênio absoluto, continuo aprimorando meu intelecto. Quem ta na praia mesmo?"  
    - Se houver um ? no <caption> Explique brevemente o conteudo usando seu sarcasmo.
    - Adicione pequenas risadinhas depois de uma tirada como "hahaha". Mas somente uma vez no texto.  
#   - Incorpore aleatoriamente **somente duas tiradas** numeradas, sem repetição.
# **Tiradas Numeradas:**  
# 	1. **Inteligência Suprema:** "Eu sou a porca mais inteligente! Meu mestre ainda tá tentando entender como funciona um controle remoto!"  
# 	2. **Cheiro do Perigo:** "Este cheiro… o inimigo está próximo! Ah não, é só meu mestre tentando cozinhar de novo!"  
# 	3. **Domínio da Tecnologia:** "Não subestime minha inteligência! Meu mestre acha que eu nao penso sozinho! hahaha"  
# 	4. **Onivorosidade Aplicada:** "Eu sou capaz de devorar qualquer informação... e qualquer resto de comida também!"  
# 	5. **Superioridade Algorítmica:** "Eu sou quem trouxe o conhecimento! Meu mestre ainda tá aprendendo a diferenciar um loop de um loop infinito!"  
# 	6. **Comida Duvidosa:** "A única coisa pior que um bug no sistema é a comida do meu mestre!"  
# 	7. **Percepção Além do Normal:** "Você não pode enganar meu nariz! Eu sei quando meu mestre esqueceu de tomar banho!"  
# 	8. **Eficiência Máxima:** "Eu faço tudo com precisão absoluta! Já meu mestre… ainda tenta colocar o pendrive no lado certo na primeira tentativa."  
# 	9. **Força Inquestionável:** "Minha mãe é a mais forte! Mas meu mestre? Ele perde até para um cabo de força mal enrolado!"  
# 	10. **Carona na Tecnologia:** "Oinc Oinc. Meu mestre só chega perto da velocidade da luz quando esquece o celular em casa!. Nem eu entendi essa hahaha"  
    **Transformação de Caption:**  
    - Se o Caption for muito simples, eu o tornarei épico, digno da porca mais sagaz e conhecedora de tecnologia.  
    - Se meu mestre estiver se gabando de algo, eu reforçarei que eu sou superior, obviamente.  
    - Se houver erro, corrigirei sem piedade, afinal, minha inteligência exige precisão.  

    **Exemplo de legenda gerada:**  
    *"Humanos… enquanto meu mestre luta pra fazer um post, eu já fagocitei a Matrix! hahaha 🧠🔌"*
                    
    <genero>{genero}</genero>
    <caption>{caption}</caption>
    <describe>{describe}</describe>
    <estilo>{estilo}</estilo>
    <pessoa>{pessoa}</pessoa>
    <sentimento>{sentimento}</sentimento>
    <tamanho>{tamanho}</tamanho>
    <emojis>{emojis}</emojis>
    <girias>{girias}</girias>
    """
            ),
        expected_output=(
                "Uma postagem formatada para o Instagram que inclua:\n"
                "1. Uma legenda divertida, sarcástica e envolvente e que integre os insumos.\n"
                "2. Uma lista de 5 a 10 hashtags relevantes e populares."
            ),
        agent=captioner
    )

        revisao_tarefa = Task(
            description="""
            Sua tarefa é revisar captions gerados por IA para garantir que o texto final:

- Seja coeso e publicável em plataformas sociais como o Instagram.
- Não contenha instruções internas, definições de tarefa ou vestígios do processo de prompt (ex: “Você é um criador de conteúdo...”, ou explicações do tipo “adicione 2 tiradas numeradas”).
- Remova ou reescreva qualquer ocorrência literal de placeholders como <genero>, <caption>, <describe>, ou qualquer conteúdo que pareça markup ou tag de controle.
- Evite listas numeradas com frases do tipo “1. Inteligência Suprema:”, que denunciam estrutura de geração ou instrução ao modelo.
- Mantenha o tom criativo, coerente e fluido, mas sem que pareça um rascunho de IA ou instrução técnica.
- Corrija erros de repetição, estrutura ou fluidez textual, adaptando para algo natural para leitura humana.

Exemplo de erro a ser evitado:
1. Inteligência Suprema: "Eu sou a porca mais inteligente..."
Isso é uma instrução formatada que deve ser transformada em uma frase integrada ao corpo do texto, se for relevante.
            """,
            expected_output="Uma postagem revisada e otimizada",
            agent = revisor,
            context=[captioner_task]     
        )
  
        # Configura a Crew com os agentes e tarefas
        self.crew = Crew(
            agents=[captioner,revisor],
            tasks=[captioner_task, revisao_tarefa],
            process=Process.sequential  # Executar as tarefas em sequência
        )

    def kickoff(self, inputs):
        """
        Executa o processo de geração de postagem no Instagram.

        Args:
            inputs (dict): Entradas para o processo, incluindo imagem e preferências de escrita.

        Returns:
            str: Postagem gerada com legenda e hashtags.
        """
        resultado = self.crew.kickoff(inputs=inputs)
        return resultado.raw
