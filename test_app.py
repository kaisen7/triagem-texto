import unittest
from app import Classificador, tokens

class TestTriagem(unittest.TestCase):
    def setUp(self):
        self.modelo = Classificador([
            {'categoria': 'entrega', 'texto': 'entrega pedido atrasado'},
            {'categoria': 'pagamento', 'texto': 'cartão pagamento pix'}])
    def test_normalizacao(self): self.assertEqual(tokens('CARTÃO!'), ['cartao'])
    def test_desconhecido(self): self.assertEqual(self.modelo.prever('xyz')[0], None)
    def test_pesos(self):
        categoria, pesos = self.modelo.prever('pagar cartão pix')
        self.assertEqual(categoria, 'pagamento')
        self.assertAlmostEqual(sum(pesos.values()), 1)
    def test_repeticao_longa(self):
        self.assertEqual(self.modelo.prever('pix ' * 10000)[0], 'pagamento')
    def test_treino_vazio(self):
        with self.assertRaises(ValueError): Classificador([])

if __name__ == '__main__': unittest.main()
