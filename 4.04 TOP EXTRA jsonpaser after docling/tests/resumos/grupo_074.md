Objetivo: Descrever o tratamento de dados para análise, incluindo normalização, ponderação e cálculo de métricas de erro (MAE) e precisão.

Tópicos Principais:
*   Ponderação de variáveis binárias para balancear sua influência.
*   Normalização de respostas ordinais para escala 0-1.
*   Cálculo da Correlação.
*   Cálculo do MAE para questões numéricas do GSS, com normalização prévia.
*   Cálculo da precisão normalizada, com ressalvas devido a valores de consistência interna iguais a zero.

Informações Relevantes:
*   Variáveis binárias recebem pesos ajustados para evitar influência desproporcional.
*   Respostas ordinais são normalizadas para manter sua ordem e distância.
*   O MAE é calculado após a normalização das respostas para a escala 0-1, utilizando os limites históricos das respostas do GSS.
*   A precisão normalizada é calculada, mas não pode ser usada para o MAE devido a divisões por zero em casos de ausência de variação nas respostas (consistência interna = 0).

Citação Direta: "To calculate the MAE for the numerical GSS questions, we first normalize the participants' responses to a 0 to 1 scale relative to the range of historical responses to the respective question as indicated on the official NORC site for the GSS."