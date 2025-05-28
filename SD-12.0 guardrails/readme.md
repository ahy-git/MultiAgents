# 🤖 CrewAI + Guardrails: Validação de JSON com Reescrita Inteligente

Este projeto demonstra como usar o **CrewAI (Flow)** em conjunto com **Guardrails.ai** para gerar, validar e corrigir automaticamente JSONs estruturados com base em um schema pré-definido.

A arquitetura implementa um ciclo completo de agentes que:

1. Geram perfis em formato JSON (com campos `name`, `age`, `profession`)
2. Validam a saída usando um `Guardrails` schema (Pydantic)
3. Em caso de falha, usam outro agente para **reescrever o prompt** com base no erro retornado
4. Repetem o ciclo até obter uma saída válida ou atingir o número máximo de tentativas (`max_retries=10`)

---

## 🧩 Componentes

- **`crew_profile_generator.py`**  
  Agente responsável por gerar o JSON a partir do prompt fornecido.

- **`tool_guardrails_validator.py`**  
  Tool que valida a saída usando `Guardrails` e um schema definido via `Pydantic`.

- **`crew_prompt_rewriter.py`**  
  Agente que recebe a mensagem de erro do Guardrails e reescreve o prompt para nova tentativa.

- **`main_flow.py`**  
  Orquestrador com `CrewAI.Flow`, controlando a execução do ciclo com `@start`, `@router`, e `@listen`.

---

## ⚙️ Fluxo de Execução

```mermaid
flowchart TD
    Start([Start])
    Gen[🔁 Geração de Perfil]
    Validate[✅ Validação com Guardrails]
    Success[🎉 Validação OK]
    Rewrite[✍️ Reescrita de Prompt]
    Retry[🔁 Retenta com Novo Prompt]
    Fail[❌ Máx. Tentativas Atingido]

    Start --> Gen
    Gen --> Validate
    Validate -->|Válido| Success
    Validate -->|Inválido| Rewrite
    Rewrite --> Retry
    Retry --> Gen
    Validate -->|10 tentativas| Fail
````

---

## 🚀 Como Executar

1. Instale as dependências (recomenda-se usar virtualenv):

```bash
pip install -r requirements.txt
```

2. Execute o fluxo principal:

```bash
python main_flow.py
```

---

## 🎯 Objetivo Educacional

Este projeto serve como base para entender:

* Integração de validação estrutural com LLMs
* Controle de fluxo orientado a agentes com `CrewAI`
* Reescrita iterativa de prompts com base em falhas reais
* Uso prático de `Guardrails` com `Pydantic schemas`

---