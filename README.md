# CHASSI (QUI-28)

Aplicação web para planejar experimentos com planejamento fatorial e analisar os resultados com um modelo quadrático.

O usuário informa os parâmetros do experimento (nome, unidade, valor central, limites e delta) e o valor de alfa. O backend gera um delineamento composto central: 3 repetições do ponto central, 2^k pontos cúbicos e 2k pontos axiais, em valores codificados e reais. Depois o usuário preenche a resposta medida em cada ensaio e o backend devolve:

- coeficientes do modelo quadrático com erros-padrão;
- tabela ANOVA (regressão, resíduos, falta de ajuste, erro puro, total);
- teste F a 95% de confiança, com o texto da conclusão;
- ponto ótimo (máximo ou mínimo) dentro da faixa dos dados, calculado com `scipy.optimize.minimize`;
- gráfico da superfície de resposta, gráfico dos pontos do planejamento e gráfico de resíduos por resposta prevista.

## Estrutura

```txt
frontend/vite-project/
├── src/                    React (Vite)
│   ├── Parametros/         formulário de parâmetros e tabela do planejamento
│   └── Modelagem/          entrada das respostas e exibição dos resultados
└── backend/
    ├── app.py              Flask, rotas /submit_param e /submit_quadratic_model
    └── logica/
        ├── Entregando_perifericos.py   Parameter, FatorialPlan, validação das entradas
        └── Processando_dados.py        QuadraticModel, ANOVA, teste F, ponto ótimo, gráficos
logica/                     protótipos anteriores, não usados pelo app
```

## Como executar

Requisitos: Python 3.11 e Node.js 16 ou superior.

Backend (porta 5000):

```bash
cd frontend/vite-project/backend
pip install flask flask-cors numpy pandas scipy matplotlib
python app.py
```

O comando precisa rodar dentro de `backend/`, porque `app.py` importa `logica.*` por caminho relativo.

Frontend (porta 5173):

```bash
cd frontend/vite-project
npm install
npm run dev
```

Abra `http://localhost:5173`. O frontend chama o backend em `http://localhost:5000`, endereço fixo em `Parametros.jsx` e `Modelagem.jsx`.

## API

`POST /submit_param` recebe os parâmetros e devolve o planejamento como DataFrame em `orient="split"`. Se as entradas forem inválidas, devolve HTTP 400 com `{"errors": [...]}`. Exemplos de entrada inválida: valor central fora dos limites, delta maior que a distância até um limite, alfa menor que 1 ou maior que a raiz do número de parâmetros.

```json
{
  "alpha": 1.41,
  "has_integer": false,
  "variables": [
    {"name": "T", "unit": "C", "value": 50, "minValue": 0, "maxValue": 100, "delta": 10},
    {"name": "P", "unit": "bar", "value": 5, "minValue": 0, "maxValue": 10, "delta": 1}
  ]
}
```

`POST /submit_quadratic_model` recebe as colunas reais dos parâmetros mais a coluna `Resposta`, e `maximize` (`true` para máximo, `false` para mínimo). Devolve `tabela_coeficientes`, `anovaTable`, `fTable`, `fstring`, `maxPoint` e os gráficos `plot`, `data_plot` e `residuals_parameters` como PNG em base64.

## Limitações

- A tela de modelagem só funciona com 2 parâmetros. `Modelagem.jsx` envia as colunas de índice 3 e 4 da tabela, que são os valores reais quando há 2 parâmetros. O backend aceita 1 a 3 parâmetros nos gráficos.
- O número de repetições do ponto central é fixo em 3.
- Parâmetros inteiros não são suportados pela interface: `app.py` cria todo `Parameter` com `is_integer=False`.
- `QuadraticModel` calcula `number_of_levels` como o número de valores distintos da primeira coluna, e não como o número de pontos distintos do planejamento. Com 2 parâmetros e alfa diferente de 1, isso dá 5 em vez de 9, e os graus de liberdade de falta de ajuste e erro puro na tabela ANOVA ficam errados.
- `LinearModel` existe em `Processando_dados.py`, mas não tem rota e não executa sem erro.
- O backend roda com `debug=True` e CORS aberto. Use apenas localmente.
- Não há `requirements.txt` nem testes automatizados.

## Autores

Projeto desenvolvido entre agosto e novembro de 2023 por [@vicentemarciot27](https://github.com/vicentemarciot27), [@thiagoufrota](https://github.com/thiagoufrota), [@matheusdnascimentols](https://github.com/matheusdnascimentols) e [@Trevilato-ITA](https://github.com/Trevilato-ITA).
