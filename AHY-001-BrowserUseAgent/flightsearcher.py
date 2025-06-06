import asyncio
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from browser_use import Agent, BrowserProfile, BrowserSession

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise EnvironmentError("OPENAI_API_KEY precisa estar definido no .env")

# Modelo unico com GPT-4o
gpt4o_llm = ChatOpenAI(model="gpt-4o")

# Configuracao do navegador
browser_profile = BrowserProfile(
    headless=False,
    highlight_elements=True,
    keep_alive=True,
    user_data_dir="~/.config/browseruse/profiles/solo-flight"
)
browser_session = BrowserSession(browser_profile=browser_profile)

async def run_single_agent():
    await browser_session.start()
    await browser_session.create_new_tab("https://www.google.com/flights")
    await asyncio.sleep(3)

    agent = Agent(
        task="""
Acesse o site aberto (https://www.google.com/flights) e busque os 5 voos mais baratos de EZE para JFK,
com ida entre 1 e 30 de setembro e volta entre 1 e 31 de outubro.

- Preencha corretamente os campos de origem e destino.
- Selecione as datas conforme solicitado.
- Aguarde os resultados e extraia os 5 mais baratos.

Para cada voo extraído, informe:
- Nome da companhia aérea
- Datas de ida e volta
- Preço total
- Duração total
- Número de escalas

Liste os voos em ordem crescente de preço.
""",
        llm=gpt4o_llm,
        browser_session=browser_session,
        use_vision=True
    )

    await agent.run(max_steps=25)
    input("🔚 Pressione Enter para encerrar...")
    await browser_session.stop()

if __name__ == "__main__":
    asyncio.run(run_single_agent())
