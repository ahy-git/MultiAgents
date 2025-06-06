### ✈️ **FlightSearcher Agent – 

**FlightSearcher** is an autonomous browser agent powered by GPT-4o that attempts to search for the cheapest round-trip flights. It uses the `browser-use` framework to interact with real web interfaces like Google Flights by reading the screen (`use_vision=True`) and executing input actions like typing and clicking.

---

### 🔍 **Key Insights**

1. **LLM Limitations in Dynamic UI**

   * Despite using GPT-4o with vision, the agent fails to reliably complete the flight search task due to challenges in understanding dynamic DOM changes, autocomplete dropdowns, and context-specific UI behavior.

2. **Instruction Following vs Execution**

   * Even with precise task prompts and multiple agents (vision, executor, verifier), the LLM tends to either execute prematurely or get stuck due to lack of structured memory and true environment feedback.

3. **State Management Gap**

   * The browser agent lacks a persistent notion of “task progress” or “UI state”, causing it to misinterpret when a goal is completed or how to backtrack.

4. **Research-Only Maturity**

   * While promising for demos and research, tools like `browser-use` are not production-ready for real-world tasks involving unpredictable web interfaces.

---
