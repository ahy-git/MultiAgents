# Resumo diario de grupos. (Whatsapp Group Controller)
Este projeto é uma **interface web interativa construída com Streamlit** para gerenciamento de grupos e configuração de resumos automatizados via agendamento. Ele é ideal para aplicações em que grupos (como grupos de mensagens, estudo, equipes de trabalho etc.) precisam de resumos periódicos configuráveis.

### Descrição em alto nível:

O sistema permite ao usuário visualizar, selecionar e configurar grupos cadastrados, personalizando opções como:

* **Horário de execução do resumo**
* **Inclusão de nomes e links**
* **Ativação/desativação do resumo automatizado**

Além disso, a interface oferece uma funcionalidade de **agendamento em lote (batch)**, onde múltiplos grupos podem ser configurados automaticamente com horários espaçados, otimizando o tempo de execução de tarefas em sistemas que processam múltiplos grupos sequencialmente.

### Funcionalidades principais:

* Interface intuitiva dividida em colunas: seleção de grupos e configurações detalhadas
* Armazenamento em cache para evitar recarregamentos pesados
* Expansível para integrações com bots, WhatsApp ou outros sistemas de mensagens
* Sistema de controle centralizado para leitura e escrita nas configurações dos grupos
* Execução de scripts Python agendados para geração de resumos
---

Sure! Here's a **technical README-style description in English** for your project:

---

## 📊 Group Summary Scheduler – Streamlit App

This project is a **Streamlit-based web application** designed to manage and schedule summary generation for multiple groups. It provides a user-friendly interface for configuring group-specific settings and batch scheduling automation scripts.

### 🔧 Core Features

* **Group Selection and Display**
  Load and visualize available groups using a cached mapping mechanism for performance optimization.

* **Summary Configuration Panel**
  For each group, users can configure:

  * Execution time (`time_input`)
  * Enable/disable summary generation (`checkbox`)
  * Whether to include links or participant names in the summary
  * Settings are saved to a controller and linked to an executable Python script

* **Batch Scheduling**
  Select multiple groups and automatically stagger the execution times by 10-minute intervals, starting 5 minutes from now. This prevents overload and ensures scheduled tasks run sequentially.

* **Script Integration**
  The system links each group’s configuration to a Python script (e.g., `summary.py`) responsible for generating the summary, making the architecture modular and extendable.

### 🧩 Project Structure (Simplified)

```
.
├── app.py                  # Main Streamlit interface
├── utils/
│   ├── group_controller.py # Backend logic to fetch/update group data
│   ├── groups_util.py      # Utility functions for formatting and display
│   └── summary.py          # Executable script for summary generation
```

### 💡 Use Cases

* Automating WhatsApp group summaries
* Managing team communications in asynchronous environments
* Creating daily/weekly digests for educational or work groups

### 🚀 Requirements

* Python 3.9+
* Streamlit
* Custom backend logic in `GroupController` and `GroupUtils`

### ✅ Highlights

* Modular design — Easily extend summary logic or data sources
* Batch-friendly scheduling — Scalable to large numbers of groups
* Designed for low-friction user interaction with real-time feedback


