"""Classificador didático de texto com Naive Bayes multinomial."""
import argparse
import json
import math
import re
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path


def tokens(texto):
    normal = unicodedata.normalize('NFKD', texto.lower())
    normal = ''.join(c for c in normal if not unicodedata.combining(c))
    return re.findall(r'[a-z]+', normal)


class Classificador:
    def __init__(self, exemplos):
        self.documentos = Counter()
        self.palavras = defaultdict(Counter)
        self.vocabulario = set()
        if not exemplos:
            raise ValueError('É necessário fornecer exemplos de treinamento.')
        for item in exemplos:
            categoria, texto = item['categoria'], item['texto']
            termos = tokens(texto)
            if not categoria or not termos:
                raise ValueError('Cada exemplo precisa de categoria e texto.')
            self.documentos[categoria] += 1
            self.palavras[categoria].update(termos)
            self.vocabulario.update(termos)

    def prever(self, texto):
        termos = [t for t in tokens(texto) if t in self.vocabulario]
        if not termos:
            return None, {}
        scores = {}
        total = sum(self.documentos.values())
        for categoria, documentos in self.documentos.items():
            contagem = self.palavras[categoria]
            denominador = sum(contagem.values()) + len(self.vocabulario)
            score = math.log(documentos / total)
            for termo in termos:
                score += math.log((contagem[termo] + 1) / denominador)
            scores[categoria] = score
        maior = max(scores.values())
        pesos = {c: math.exp(s - maior) for c, s in scores.items()}
        soma = sum(pesos.values())
        pesos = {c: p / soma for c, p in pesos.items()}
        return max(pesos, key=pesos.get), pesos


def carregar(arquivo):
    return json.loads(Path(arquivo).read_text(encoding='utf-8'))


def main():
    parser = argparse.ArgumentParser(description='Triagem experimental de mensagens de atendimento.')
    parser.add_argument('texto', nargs='?')
    parser.add_argument('--treino', default=str(Path(__file__).with_name('treino.json')))
    parser.add_argument('--avaliar', metavar='ARQUIVO_JSON')
    args = parser.parse_args()
    try:
        modelo = Classificador(carregar(args.treino))
        if args.avaliar:
            itens = carregar(args.avaliar)
            if not itens: raise ValueError('Arquivo de avaliação vazio.')
            acertos = 0
            for item in itens:
                prevista, _ = modelo.prever(item['texto'])
                acertos += prevista == item['categoria']
                print(f'Esperado: {item["categoria"]} | Previsto: {prevista} | {item["texto"]}')
            print(f'Acertos: {acertos}/{len(itens)} ({acertos / len(itens):.0%}) — amostra didática, não valida uso real.')
        else:
            if not args.texto: parser.error('Informe uma mensagem ou use --avaliar.')
            categoria, pesos = modelo.prever(args.texto)
            if categoria is None:
                print('Sem vocabulário conhecido. Encaminhar para análise humana.')
            else:
                print(f'Sugestão experimental: {categoria}')
                for nome, peso in sorted(pesos.items(), key=lambda x: x[1], reverse=True):
                    print(f'  {nome}: {peso:.1%} (peso relativo, não confiança calibrada)')
    except (ValueError, OSError, KeyError, TypeError) as error:
        parser.exit(1, f'Erro: {error}\n')

if __name__ == '__main__':
    main()
