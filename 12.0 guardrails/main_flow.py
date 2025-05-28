# main_flow.py
from crewai.flow.flow import Flow, start, listen, router
from pydantic import BaseModel
from crew_profile_generator import ProfileGeneratorCrew
from tool_guardrails_validator import GuardrailsValidatorTool
from crew_prompt_rewriter import PromptRewriterCrew  # Novo import

class ProfileState(BaseModel):
    prompt: str = (
        "PROMPT VIRA PELO INPUT DO FLOW"
    )
    raw_output: str = ""
    validated_output: str = ""
    error: str = ""
    tentativas: int = 0
    logs: str = ""

class ProfileFlow(Flow[ProfileState]):

    @start()
    def inicio(self):
        self.state.logs += f"\n🔁 Iniciando tentativa {self.state.tentativas + 1}\n"
        return self.state

    @listen(inicio)
    def gerar_perfil(self):
        crew = ProfileGeneratorCrew()
        result = crew.kickoff(self.state.prompt)
        self.state.raw_output = result.raw.strip()
        self.state.logs += f"📤 Output gerado:\n{self.state.raw_output}\n"
        return self.state

    @router(gerar_perfil)
    def validar_perfil(self):
        validator = GuardrailsValidatorTool()
        validation = validator._run(self.state.raw_output)
        self.state.tentativas += 1

        if validation["valid"]:
            self.state.validated_output = validation["output"]
            self.state.logs += f"✅ Validação OK na tentativa {self.state.tentativas}\n"
            return "finalizado"

        self.state.error = validation["error"]
        self.state.logs += (
            f"❌ Validação falhou:\n{self.state.error}\n"
        )

        if self.state.tentativas >= 10:
            return "falhou"

        return "reescrever"

    @listen("reescrever")
    def reescrever_prompt(self):
        rewriter = PromptRewriterCrew()
        prompt_corrigido = rewriter.kickoff(
            original_prompt=self.state.prompt,
            error_message=self.state.error
        )
        self.state.prompt = prompt_corrigido.raw.strip()
        self.state.logs += "✍️ Prompt reescrito com base no erro.\n"
        return "inicio"

    @listen("finalizado")
    def sucesso(self):
        print("🎉 Perfil validado com sucesso:")
        print(self.state.validated_output)
        return self.state

    @listen("falhou")
    def erro_final(self):
        print("🚨 Máximo de tentativas atingido. Validação não foi possível.")
        print(f"Último output:\n{self.state.raw_output}")
        print(f"Erro:\n{self.state.error}")
        return self.state


## TEST
flow = ProfileFlow()
final_state = flow.kickoff(inputs={
    "prompt": (
        "Gere um perfil com os campos: erro (str), idade (int), profession (str). "
        "O resultado deve ser um JSON válido com esses campos. "
        "Evite valores nulos ou vazios. Apenas retorne o JSON, sem explicações."
    )
})
print("\n📋 LOG FINAL:\n" + final_state.logs)

