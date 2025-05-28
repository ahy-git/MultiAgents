
# main_guardrails_retry.py
from crew_profile_generator import ProfileGeneratorCrew
from crew_prompt_rewriter import PromptRewriterCrew
from tool_guardrails_validator import GuardrailsValidatorTool

MAX_RETRIES = 3

profile_gen = ProfileGeneratorCrew()
prompt_rewriter = PromptRewriterCrew()
validator = GuardrailsValidatorTool()

original_prompt = "Gere um JSON com os campos: erro (str), age (int)"
prompt = original_prompt

for attempt in range(1, MAX_RETRIES + 1):
    print(f"\n🔁 Tentativa {attempt} com prompt:\n{prompt}\n")

    result = profile_gen.kickoff(prompt)
    output = result.raw if hasattr(result, 'raw') else result

    validation = validator._run(output)

    if validation['valid']:
        print("\n✅ Saída válida:")
        print(validation['output'])
        break
    else:
        print(f"\n❌ Validação falhou: {validation['error']}")
        rewrite_result = prompt_rewriter.kickoff(prompt, validation['error'])
        prompt = rewrite_result.raw if hasattr(rewrite_result, 'raw') else rewrite_result
else:
    print("\n⛔ Todas as tentativas falharam. Último erro:")
    print(validation['error'])
