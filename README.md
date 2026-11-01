# Triagem Texto
Experimento de aprendizado de máquina para sugerir categorias de mensagens: entrega, pagamento ou produto.

## Problema explorado
Organizar mensagens de atendimento usando exemplos rotulados, sem depender de uma API externa.

## Demonstração
```sh
python app.py "Quero estorno do pagamento no cartão"
python app.py "O pedido não chegou no meu endereço"
python app.py --avaliar avaliacao.json
```
Saída esperada para o primeiro exemplo: sugestão `pagamento`, seguida dos pesos relativos de cada classe.

## Como funciona
1. Normaliza letras e acentos e separa o texto em palavras.
2. Conta exemplos e palavras de cada categoria.
3. Calcula a probabilidade das palavras por categoria com suavização de Laplace.
4. Soma logaritmos para evitar multiplicar muitos números muito pequenos.
5. Retorna a categoria de maior peso relativo.

É um Naive Bayes multinomial implementado para estudo, não um chatbot nem um LLM. Leia `tokens`, depois `Classificador.__init__`, e por último `prever`.

## Dados e avaliação
`treino.json` tem 18 mensagens sintéticas criadas para o exercício. `avaliacao.json` contém 6 mensagens separadas, também sintéticas. Esses arquivos pequenos demonstram o fluxo, mas não medem qualidade no mundo real. Não há comparação com dados reais nem validação independente. Alterar os exemplos de avaliação após observar erros pode favorecer artificialmente o resultado.

## Limitações importantes
Não compreende contexto ou negação de forma confiável. Pode errar com sarcasmo, novos assuntos ou mensagens sobre mais de uma categoria. Os percentuais são pesos normalizados do modelo, **não confiança calibrada**. Quando nenhuma palavra é conhecida, pede revisão humana. Mesmo com palavras conhecidas, as sugestões precisam de revisão; não automatize decisões reais com este protótipo.

## Sua próxima melhoria
Crie uma categoria `cancelamento`, acrescente exemplos variados de treino e escreva exemplos novos de avaliação. Compare erros antes e depois, sem treinar com os exemplos de avaliação.

## Para explicar numa entrevista
- Qual a diferença entre treino e avaliação?
- Por que usamos suavização e logaritmos?
- Por que 100% em seis frases não significa qualidade em produção?

## Requisitos
Python 3.10 ou superior. Usa apenas a biblioteca padrão: não precisa instalar pacotes nem configurar chaves de API.
No Windows, se `python` não funcionar, use `py` nos mesmos comandos.
Abra a pasta do projeto no VS Code e escolha Terminal > Novo Terminal.

## Origem e aprendizado
Projeto de estudo preparado com apoio do ChatGPT. A versão inicial foi gerada com assistência de IA; este repositório serve como base para leitura, testes e melhorias próprias. Não representa experiência profissional nem um sistema em produção.
Antes de apresentar numa entrevista, execute os exemplos e implemente uma melhoria que consiga explicar.

## Testes
```sh
python -m unittest -v
```
