# Análise de Similaridade de Emendas Parlamentares

Este repositório contém um script em Python desenvolvido para otimizar a análise de emendas feitas por parlamentares a um projeto em tramitação no Poder Legislativo. Ele analisa grandes volumes de emendas parlamentares e agrupa propostas semelhantes utilizando técnicas de Processamento de Linguagem Natural (PLN).

Ao invés de ler dezenas ou centenas de emendas manualmente para identificar padrões, o algoritmo identifica automaticamente quais textos possuem a mesma essência ou objetivo, facilitando a análise técnica, o acompanhamento político e a tomada de decisão.

## 🛠️ Bibliotecas Utilizadas

- **Pandas:** Para manipulação da base de dados e geração das planilhas.
- **Scikit-Learn:** Para a extração de características textuais (TF-IDF) e cálculo da Similaridade de Cosseno.
- **NLTK:** Para a remoção de *stop words*.

## ⚙️ Como Funciona

1. **Leitura:** O script consome uma planilha Excel (`.xlsx`) que costuma ser publicada após o encerramento do prazo de apresentação de emendas. O documento contém o número das emendas e seus respectivos teores (textos completos).
2. **Processamento Textual:** Os textos são limpos e vetorizados através do método TF-IDF, que atribui pesos às palavras mais relevantes.
3. **Cálculo de Similaridade:** É aplicada a Similaridade de Cosseno para comparar cada emenda com todas as outras. O sistema agrupa aquelas que atingem um índice de similaridade igual ou superior a 70% (parâmetro ajustável).
4. **Exportação:** O resultado é salvo em uma nova planilha, adicionando uma coluna que classifica cada emenda dentro de um grupo específico ou a rotula como "Única".

## 🚀 Como Executar o Projeto

### Pré-requisitos
Clone este repositório e instale as dependências listadas no arquivo `requirements.txt`:

```bash
git clone [https://github.com/seu-usuario/analise-similaridade-emendas.git](https://github.com/seu-usuario/analise-similaridade-emendas.git)
cd analise-similaridade-emendas
pip install -r requirements.txt
```

### Base de Dados
Baixe o quadro de emendas que deseja analisar. Neste projeto, utilizei como exemplo a MPV 1348/26, disponível no link oficial: [Quadro de Emendas - Congresso Nacional](https://www3.congressonacional.leg.br/editor-emendas/quadro-emendas.html?sigla=MPV&numero=1348&ano=2026&exibir=quadro).

Salve o arquivo no formato `.xlsx` na pasta do projeto e especifique o nome do arquivo nos parâmetros da função dentro do script.

### Execução
Após configurar o arquivo Excel, rode o script com o comando:

```bash
python analise_similaridade.py
```
