from crewai.tools import BaseTool
import matplotlib.pyplot as plt

class CustomGraphTool(BaseTool):
    name: str="Ferramenta de Criação de Gráficos"
    description: str=""" Gera um gráfico com base em uma lista
de valores e um tipo de gráfico especificado (linha , barras
ou pizza ) e salva o gráfico como um arquivo PNG. Recebe uma lista de valores, uma lista de labels e o tipo de grafico: linha, barras, pizza """
    
    def _run(self, values: list, labels: list, chart_type: str = "linha",
             title: str="Chart") -> str:
        
        plt.figure()
        
        if chart_type == "linha":
            plt.plot(values)
            plt.title(title)
        if chart_type == "barras":
            plt.bar(range(len(values)),values, tick_label=labels)
            plt.title(title)
        if chart_type == "pizza":
            if not labels:
                labels = [f"Item {i+1}" for i in range(len(values))]
            plt.pie(values, labels = labels, autopct="%1.1f%%")
            plt.title(title)
        else:
            return "Tipo de grafico invalido. Escolha entrer 'linha', 'barras' ou 'pizza'"
        
        #salvar png
        file_name = f"{title.lower().replace(" ","_")}.png"
        plt.savefig(file_name)
        plt.close()
        
        msg = f"grafico salvo como {file_name}"
        return msg
        