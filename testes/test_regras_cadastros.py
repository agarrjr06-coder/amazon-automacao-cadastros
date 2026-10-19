import unittest
from src.regras_cadastros import (
    sku_pai_interno, recuperar_sku_convertido_em_data,
    validar_ean, classificar_categoria, triar_produto, atributos_propostos
)


class TesteRegras(unittest.TestCase):
    def test_sku_pai(self):
        self.assertEqual(sku_pai_interno("1234-ABC-39"), "1234")

    def test_sku_preservado(self):
        self.assertEqual(sku_pai_interno("ABC-1234"), "")

    def test_data_suspeita(self):
        self.assertEqual(
            recuperar_sku_convertido_em_data("31/08/1234", "1234"),
            ("1234-08-31", "SUGESTAO_REQUER_CONFERENCIA")
        )

    def test_data_sem_confirmacao(self):
        self.assertEqual(
            recuperar_sku_convertido_em_data("31/08/1234", "5678"),
            ("31/08/1234", "ORIGINAL")
        )

    def test_ean_invalido_em_notacao_cientifica(self):
        self.assertEqual(validar_ean("1.2345E+12")[1], "NOTACAO_CIENTIFICA_OU_DECIMAL")

    def test_ean_valido(self):
        self.assertEqual(validar_ean("4006381333931"), ("4006381333931", "VALIDO"))

    def test_categoria_em_portugues(self):
        self.assertEqual(classificar_categoria("Calçados"), "CALCADOS")

    def test_categoria_nao_inferida_do_nome(self):
        self.assertEqual(triar_produto("1234-39", "").status, "CATEGORIA_NAO_INFORMADA")

    def test_nao_copiar_exemplos(self):
        self.assertEqual(atributos_propostos({"sku": "1234-39", "marca": ""}), {"SKU": "1234-39"})


if __name__ == "__main__":
    unittest.main()
