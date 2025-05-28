## 📄 `README.md`

# 🧠 PDF Summarizer with Docling + CrewAI + LLM

Este projeto automatiza a leitura e o resumo de documentos PDF com uso de modelos de linguagem (LLMs) e o conversor multimodal [Docling](https://docling-project.github.io/).

> Ideal para relatórios, artigos científicos, apresentações e documentos com texto e imagens. Ele extrai as seções, resume individualmente e gera um resumo executivo final.

---

## 🚀 Funcionalidades

- ✅ Conversão de PDF para JSON com enriquecimento visual (imagens, descrições)
- ✅ Extração de seções estruturadas via `Docling`
- ✅ Geração de resumos por seção com LLMs (CrewAI)
- ✅ Síntese final automática (com suporte a blocos longos e recursividade)
- ✅ Robustez contra falhas: reinício a partir do último arquivo processado
- ✅ Limpeza automática de arquivos temporários
- ✅ Renomeia o resultado final com o nome do PDF original

---

## 🛠️ Requisitos

- Python 3.10+
- [Docling](https://github.com/docling-project/docling) (`pip install docling`)
- crewai (`pip install crewai`)
- pymupdf (`pip install pymupdf`)
- dotenv (`pip install python-dotenv`)
- Um modelo LLM configurado (Gemini, OpenAI, OpenRouter, etc.)

---

## ⚙️ Como usar

### 1. Coloque seu PDF na raiz do projeto

```bash
sample.pdf
```

### 2. Execute o script principal:

```bash
python main.py
```

O script irá:
- Converter o PDF com `docling.document_converter`
- Extrair as seções do JSON
- Resumir cada seção e salvar como `resumos/grupo_###.md`
- Consolidar todos os resumos em `resumo_final.md`
- Renomear para `sample.md`

---

## 📂 Estrutura gerada (antes da limpeza)

```
├── sample.pdf
├── sample.json
├── resumos/
│   ├── grupo_001.md
│   ├── grupo_002.md
│   └── ...
├── resumo_final.md
```

Após a execução, você terá apenas:

```
sample.md
```

---

## 🧠 Tecnologias

- **Docling**: converte PDF para estrutura JSON rica (com imagens, OCR, tabelas)
- **CrewAI**: gerencia agentes LLM com ferramentas integradas
- **LLM (via LiteLLM/OpenRouter/OpenAI)**: gera resumos reais por seção
- **Python**: automação e controle de fluxo

---

## ✅ Reexecução segura

Se o processo for interrompido, ao rodar novamente:

- O script detecta o último `.md` salvo
- Recomeça exatamente dali
- Evita duplicidade ou sobrecarga desnecessária da LLM

---

## 📌 Configuração LLM

Você pode usar qualquer LLM que suporte `function calling` com CrewAI:
- Google Gemini (via Vertex AI)
- OpenAI GPT-3.5/4
- Claude 3 Haiku (via Poe API ou OpenRouter)
- Mistral, LLaMA, Mixtral (via Together.ai, OpenRouter, Ollama local)

---

## 🧹 Pós-processamento automático

Ao final da execução:

- `sample.json` é deletado
- Pasta `resumos/` é removida
- `resumo_final.md` é renomeado para `sample.md`

---

## 📄 Licença

Este projeto é livre para uso pessoal ou acadêmico. Compartilhe melhorias!

---

## 🤝 Contribuições

Pull requests são bem-vindos! Para sugestões, abra uma [issue](https://github.com/seu-repo/issues) ou envie uma mensagem.

---

## ✨ Exemplo de uso

Veja um exemplo de output final:
```
## Resumo Parcial

Este documento aborda diversos aspectos relacionados a agentes de IA generativa, arquiteturas cognitivas e o uso de ferramentas e extensões para ampliar as capacidades dos modelos de linguagem.

### Objetivos Gerais

*   Explicar o conceito de agentes de IA generativa e seus componentes.
*   Descrever o papel de modelos de linguagem e arquiteturas cognitivas em agentes.
*   Ilustrar o uso de ferramentas e extensões para interação com o mundo real.
*   Apresentar frameworks e técnicas de engenharia de prompts, como ReAct, Chain-of-Thought (CoT) e Tree-of-Thoughts (ToT).

### Principais Temas

*   **Agentes de IA Generativa:** Conceito, componentes (autonomia, proatividade), arquitetura cognitiva.
*   **Modelos de Linguagem (LMs):** Papel nos agentes, tipos de modelos, seleção de modelos adequados.
*   **Ferramentas (Tools):** Extensão da funcionalidade dos LLMs, ponte para o mundo externo, uso em RAG.
*   **Camada de Orquestração:** Processo cíclico de tomada de decisão dos agentes.
*   **Arquiteturas Cognitivas:** Modelagem da cognição de agentes inteligentes (percepção, raciocínio, aprendizado, ação).
*   **Engenharia de Prompts:** Chain-of-Thought (CoT), Tree-of-Thoughts (ToT) e ReAct.
*   **Extensões:** Ferramentas para interação com APIs.

### Conclusões

*   Agentes de IA generativa combinam raciocínio, lógica e acesso a informações externas.
*   Ferramentas e extensões são essenciais para que os agentes interajam com o mundo real.
*   Arquiteturas cognitivas fornecem estruturas para construir agentes inteligentes.
*   Frameworks de engenharia de prompts, como ReAct, podem melhorar o desempenho e a confiabilidade dos LLMs.
*   Extensões facilitam a interação com APIs.

### Recomendações

*   Utilizar modelos de linguagem que se adequem à aplicação desejada e às ferramentas a serem usadas.
*   Empregar ferramentas para superar as limitações dos modelos base.
*   Considerar o uso de frameworks como ReAct para aprimorar o raciocínio e a ação dos agentes.
*   Implementar extensões para facilitar a interação com APIs e simplificar a execução de tarefas.

## Resumo Parcial

### Objetivos Gerais

*   Descrever aplicações que utilizam busca vetorial, agentes de IA e diferentes estratégias de aprendizado para otimizar o desempenho de modelos de linguagem.
*   Apresentar exemplos práticos de agentes em ação e arquiteturas de produção.
*   Discutir os componentes-chave e as futuras tendências em agentes de IA generativa.

### Principais Temas

*   **Busca Vetorial:** Utilização para encontrar informações relevantes em data stores e responder a consultas.
*   **Estratégias de Aprendizado:**
    *   Geração Aumentada por Recuperação (RAG).
    *   Ajuste fino com dados específicos da tarefa.
    *   Engenharia de Prompt.
    *   In-context learning.
    *   Aprendizado baseado em fine-tuning.
*   **Arquitetura de Agentes:**
    *   Camada de orquestração.
    *   Ferramentas (Extensões, Funções, Data Stores).
    *   Integração com Vertex AI e outras plataformas.
*   **Aplicações em Produção:** Construção de aplicações robustas com Vertex AI, incluindo interfaces de usuário e mecanismos de avaliação.
*   **Avanços Futuros:** Agent chaining e melhorias nas ferramentas e capacidades de raciocínio.

### Conclusões

*   Agentes de IA estendem as capacidades dos modelos de linguagem, permitindo o acesso a informações em tempo real, a sugestão de ações e a execução de tarefas complexas de forma autônoma.
*   A combinação de diferentes abordagens de aprendizado e técnicas de agente, pode levar a soluções mais robustas e adaptáveis.
*   A plataforma Vertex AI simplifica a construção e o gerenciamento de agentes em produção.
*   A experimentação e o aprimoramento são cruciais para o desenvolvimento de arquiteturas de agentes complexas.

### Recomendações

*   Explorar a combinação de diferentes técnicas de aprendizado (RAG, fine-tuning, etc.) para maximizar o desempenho do modelo.
*   Utilizar ferramentas de orquestração e frameworks (LangChain, LangGraph) para construir agentes.
*   Considerar o uso de plataformas como Vertex AI para simplificar o processo de implantação e gerenciamento de agentes.
*   Focar em agentes iterativos e no refino das soluções para casos de uso específicos.

### Citações Diretas Representativas

*   "The end result is an application that allows the agent to match a user's query to a known data store through vector search, retrieve the original content, and provide it to the orchestration layer and model for further processing."
*   "Each approach has its own strengths and limitations, and the best choice depends on the specific application and the resources available."
*   "However, by combining these techniques in an agent framework, we can leverage the various strengths and minimize their weaknesses, allowing for a more robust and adaptable solution."
*   "In order to provide a real-world executable example of an agent in action, we'll build a quick prototype with the LangChain and LangGraph libraries."
*   "This allows developers to focus on building and refining their agents while the complexities of infrastructure, deployment and maintenance are managed by the platform itself."
*   "The architecture includes many of the various components necessary for a production ready application."
*   "At the heart of an agent's operation is the orchestration layer, a cognitive architecture that structures reasoning, planning, decision-making and guides its actions."
```

