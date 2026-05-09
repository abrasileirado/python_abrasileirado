from unittest import TestCase

from abrasileirado.enums import TipoLivroRcpnEnum, UnidadeFederativaStrEnum
from abrasileirado.types import (
    CEP,
    CNES,
    CNPJ,
    CNS,
    CPF,
    NUP,
    PIS,
    RENAVAM,
    CertidaoRCPN,
    CodigoValidavel,
    EnderecoBrasil,
    Passaporte,
    PlacaVeicular,
    Telefone,
    TituloEleitoral,
)


class TestCEP(TestCase):
    def test_cep_valido(self):
        cep = CEP("59015300")
        self.assertEqual(cep.digitos, "59015300")
        self.assertEqual(str(cep), "59015-300")
        cep2 = CEP("59.015-300")
        self.assertEqual(cep2.digitos, "59015300")
        self.assertEqual(str(cep2), "59015-300")

    def test_cep_invalido(self):
        # Inválido: menos de 8 dígitos
        with self.assertRaises(ValueError):
            CEP("12")
        # Inválido: mais de 8 dígitos
        with self.assertRaises(ValueError):
            CEP("123456789")
        # Inválido: todos dígitos iguais
        with self.assertRaises(ValueError):
            CEP("11111111")


class TestEnderecoBrasil(TestCase):
    def test_endereco_brasil(self):

        # Com complemento
        e = EnderecoBrasil(
            logradouro="Rua Dr. Nilo Bezerra Ramalho",
            numero="1692",
            bairro="Tirol",
            municipio="Natal",
            uf=UnidadeFederativaStrEnum.RN,
            cep=CEP("59015-300"),
            complemento="Sala 001",
        )
        self.assertEqual(e.logradouro, "Rua Dr. Nilo Bezerra Ramalho")
        self.assertEqual(e.numero, "1692")
        self.assertEqual(e.bairro, "Tirol")
        self.assertEqual(e.municipio, "Natal")
        self.assertEqual(e.uf, UnidadeFederativaStrEnum.RN)
        self.assertEqual(e.cep, CEP("59015-300"))
        self.assertEqual(e.complemento, "Sala 001")
        self.assertEqual("Rua Dr. Nilo Bezerra Ramalho 1692, Sala 001\nTirol\n59015-300 Natal/RN", e.ect_padrao)
        self.assertEqual("Rua Dr. Nilo Bezerra Ramalho 1692, Sala 001\nTirol\nNatal/RN\n59015-300", e.ect_extendido)
        self.assertEqual(str(e), e.ect_padrao)

        # Sem complemento
        e = EnderecoBrasil(
            logradouro="Rua Dr. Nilo Bezerra Ramalho",
            numero="1692",
            bairro="Tirol",
            municipio="Natal",
            uf=UnidadeFederativaStrEnum.RN,
            cep=CEP("59015-300"),
        )
        self.assertIsNone(e.complemento)
        self.assertEqual("Rua Dr. Nilo Bezerra Ramalho 1692\nTirol\n59015-300 Natal/RN", e.ect_padrao)
        self.assertEqual("Rua Dr. Nilo Bezerra Ramalho 1692\nTirol\nNatal/RN\n59015-300", e.ect_extendido)

    def test_endereco_brasil_equality_and_hash_use_fields(self):
        endereco = EnderecoBrasil(
            logradouro="Rua Dr. Nilo Bezerra Ramalho",
            numero="1692",
            bairro="Tirol",
            municipio="Natal",
            uf=UnidadeFederativaStrEnum.RN,
            cep=CEP("59015300"),
            complemento="Sala 001",
        )
        same_endereco = EnderecoBrasil(
            logradouro="Rua Dr. Nilo Bezerra Ramalho",
            numero="1692",
            bairro="Tirol",
            municipio="Natal",
            uf=UnidadeFederativaStrEnum.RN,
            cep=CEP("59015-300"),
            complemento="Sala 001",
        )
        other_endereco = EnderecoBrasil(
            logradouro="Rua Dr. Nilo Bezerra Ramalho",
            numero="1692",
            bairro="Tirol",
            municipio="Natal",
            uf=UnidadeFederativaStrEnum.RN,
            cep=CEP("59015-300"),
        )

        self.assertEqual(endereco, same_endereco)
        self.assertEqual(hash(endereco), hash(same_endereco))
        self.assertEqual({endereco, same_endereco}, {endereco})
        self.assertNotEqual(endereco, other_endereco)
        self.assertNotEqual(endereco, "Rua Dr. Nilo Bezerra Ramalho")


class TestCPF(TestCase):
    def test_cpf_valido(self):
        cpf = CPF("12345678909")
        self.assertEqual(str(cpf), "123.456.789-09")
        self.assertEqual(cpf.digitos, "12345678909")

    def test_cpf_valido_leading_zeros(self):
        # CPF válido sem máscara (caso distinto de test_cpf_valido)
        cpf = CPF("00000000191")
        self.assertEqual(cpf.digitos, "00000000191")
        self.assertEqual(str(cpf), "000.000.001-91")

    def test_cpf_valido_com_mascara(self):
        cpf = CPF("123.456.789-09")
        self.assertEqual(str(cpf), "123.456.789-09")
        self.assertEqual(cpf.digitos, "12345678909")

    def test_cpf_invalido_dv(self):
        with self.assertRaises(ValueError):
            CPF("12345678900")

    def test_cpf_invalido_tamanho(self):
        with self.assertRaises(ValueError):
            CPF("12345678")


class TestNUP(TestCase):
    def test_nup_valido(self):
        nup = NUP("23520005177202676")
        self.assertEqual(str(nup), "23520.005177/2026-76")
        self.assertEqual(nup.digitos, "23520005177202676")

    def test_nup_valido_com_mascara(self):
        nup = NUP("23520.005177/2026-76")
        self.assertEqual(str(nup), "23520.005177/2026-76")
        self.assertEqual(nup.digitos, "23520005177202676")

    def test_nup_invalido_dv(self):
        with self.assertRaises(ValueError):
            NUP("23520005177202677")

    def test_nup_invalido_tamanho(self):
        with self.assertRaises(ValueError):
            NUP("1234567890123456")


class TestCNES(TestCase):
    def test_cnes_valido(self):
        cnes = CNES("2079305")
        self.assertEqual(cnes.digitos, "2079305")
        self.assertEqual(str(cnes), "2079305")
        self.assertEqual(CNES("0000001").digitos, "0000001")
        self.assertEqual(CNES("0000001").__str__(), "0000001")

    def test_cnes_invalido_tamanho(self):
        # Inválido: menos de 3 dígitos
        with self.assertRaises(ValueError):
            CNES("12")

    def test_cnes_invalido_digitos_iguais(self):
        # Inválido: todos dígitos iguais
        with self.assertRaises(ValueError):
            CNES("1111111")


class TestCNS(TestCase):
    def test_cns_valido(self):
        cns = CNS("898001160444643")
        self.assertEqual(cns.digitos, "898001160444643")
        self.assertEqual(str(cns), "898001160444643")

    def test_cns_valido_definitivo(self):
        cns = CNS("123456789010000")
        self.assertEqual(cns.digitos, "123456789010000")
        self.assertEqual(str(cns), "123456789010000")

    def test_cns_valido_definitivo_com_dv_especial(self):
        cns = CNS("100000000060018")
        self.assertEqual(cns.digitos, "100000000060018")
        self.assertEqual(str(cns), "100000000060018")

    def test_cns_invalido_tamanho(self):
        # Inválido: menos de 15 dígitos
        with self.assertRaises(ValueError):
            CNS("12")

    def test_cns_invalido_digitos_iguais(self):
        # Inválido: todos dígitos iguais
        with self.assertRaises(ValueError):
            CNS("111111111111111")

    def test_cns_invalido_dv(self):
        with self.assertRaises(ValueError):
            CNS("898001160444648")

    def test_cns_invalido_prefixo(self):
        with self.assertRaises(ValueError):
            CNS("398001160444643")


class TestCNPJ(TestCase):
    def test_cnpj_valido(self):
        # CNPJ válido: 12.345.678/9000-05
        cnpj = CNPJ("12345678900005")
        self.assertEqual(cnpj.digitos, "12345678900005")
        self.assertEqual(str(cnpj), "12.345.678/9000-05")
        cnpj2 = CNPJ("12.345.678/9000-05")
        self.assertEqual(cnpj2.digitos, "12345678900005")
        self.assertEqual(str(cnpj2), "12.345.678/9000-05")

    def test_cnpj_invalido(self):
        # Inválido: todos dígitos iguais
        with self.assertRaises(ValueError):
            CNPJ("11111111111111")
        # Inválido: menos de 14 dígitos
        with self.assertRaises(ValueError):
            CNPJ("1")
        # Inválido: DV errado
        with self.assertRaises(ValueError):
            CNPJ("12345678900000")


class TestCodigoValidavel(TestCase):
    def test_codigo_validavel_base_mask_and_str(self):
        class CodigoSempreValido(CodigoValidavel):
            def _is_valid(self, code: str) -> bool:
                return True

        codigo = CodigoSempreValido("1")

        self.assertEqual(codigo.digitos, "1")
        self.assertEqual(str(codigo), "1")

    def test_codigo_validavel_basic_validation_with_none_empty_and_nondigit_input(self):
        # Validate behavior through public APIs (no private method calls)
        with self.assertRaises(ValueError):
            CPF(None)

        with self.assertRaises(ValueError):
            CPF("")

        with self.assertRaises(ValueError):
            CPF("abc")

    def test_codigo_validavel_full_digits_default(self):
        # Validate default digit handling through observable behavior
        cpf = CPF("12345678909")
        self.assertEqual(cpf.digitos, "12345678909")
        self.assertEqual(str(cpf), "123.456.789-09")

    def test_codigo_validavel_equality_and_hash_use_type_and_digits(self):
        cep = CEP("59015300")
        masked_cep = CEP("59015-300")

        self.assertEqual(cep, masked_cep)
        self.assertEqual(hash(cep), hash(masked_cep))
        self.assertEqual({cep, masked_cep}, {cep})
        self.assertNotEqual(cep, "59015300")

    def test_codigo_validavel_is_valid_classmethod(self):
        self.assertTrue(CEP.is_valid("59015-300"))
        self.assertFalse(CEP.is_valid("123"))
        self.assertTrue(CPF.is_valid("123.456.789-09"))
        self.assertFalse(CPF.is_valid("123.456.789-00"))
        self.assertTrue(CertidaoRCPN.is_valid("123456.01.55.2024.1.00001.001.0000001-67"))
        self.assertFalse(CertidaoRCPN.is_valid("123456.01.55.2024.1.00001.001.0000001-00"))


class TestCEPInvalid(TestCase):
    def test_cep_invalid_length_beyond_full_digits(self):
        # CEP._is_valid is an instance method (no @classmethod)
        # CodigoValidavel.__init__ calls self._is_valid
        with self.assertRaises(ValueError):
            CEP("123456789")


class TestNUPExtra(TestCase):
    def test_nup_invalido_tamanho_maior(self):
        with self.assertRaises(ValueError):
            NUP("123456789012345678")  # Mais de 17 dígitos


class TestPIS(TestCase):
    def test_pis_uses_own_mask(self):
        pis = PIS("12044568103")

        self.assertEqual(pis.digitos, "12044568103")
        self.assertEqual(str(pis), "120 445 681 03")

    def test_pis_invalido_dv(self):
        with self.assertRaises(ValueError):
            PIS("123")

        with self.assertRaises(ValueError):
            PIS("12044568104")


class TestRENAVAM(TestCase):
    def test_renavam_valido(self):
        renavam = RENAVAM("63988496249")

        self.assertEqual(renavam.digitos, "63988496249")
        self.assertEqual(str(renavam), "63988496249")

    def test_renavam_invalido(self):
        with self.assertRaises(ValueError):
            RENAVAM("123")

        with self.assertRaises(ValueError):
            RENAVAM("63988496240")


class TestTituloEleitoral(TestCase):
    def test_titulo_eleitoral_valido(self):
        titulo = TituloEleitoral("123456780191")

        self.assertEqual(titulo.digitos, "123456780191")
        self.assertEqual(str(titulo), "123456780191")

    def test_titulo_eleitoral_invalido(self):
        with self.assertRaises(ValueError):
            TituloEleitoral("123")

        with self.assertRaises(ValueError):
            TituloEleitoral("123456782490")

        with self.assertRaises(ValueError):
            TituloEleitoral("123456782496")


class TestTelefone(TestCase):
    def test_telefone_valido(self):
        telefone = Telefone("(84) 98765-4321")

        self.assertEqual(telefone.digitos, "84987654321")
        self.assertEqual(str(telefone), "(84) 98765-4321")

    def test_telefone_invalido(self):
        with self.assertRaises(ValueError):
            Telefone("00 98765-4321")


class TestPassaporte(TestCase):
    def test_passaporte_valido(self):
        passaporte = Passaporte("12345678")

        self.assertEqual(passaporte.digitos, "12345678")
        self.assertEqual(str(passaporte), "12345678")

    def test_passaporte_invalido(self):
        with self.assertRaises(ValueError):
            Passaporte("1234567")


class TestPlacaVeicular(TestCase):
    def test_placa_veicular_valida(self):
        placa = PlacaVeicular("1234567")

        self.assertEqual(placa.digitos, "1234567")
        self.assertEqual(str(placa), "1234567")

    def test_placa_veicular_invalida(self):
        with self.assertRaises(ValueError):
            PlacaVeicular("1111111")


class TestCertidaoRCPN(TestCase):
    def test_rcpn_valido(self):
        rcpn = CertidaoRCPN("12345601552024100001001000000167")

        self.assertEqual(rcpn.digitos, "12345601552024100001001000000167")
        self.assertEqual(str(rcpn), "123456.01.55.2024.1.00001.001.0000001-67")
        self.assertEqual(rcpn.codigo_serventia, "123456")
        self.assertEqual(rcpn.codigo_acervo, "01")
        self.assertEqual(rcpn.registro_civil, "55")
        self.assertEqual(rcpn.ano_registro, "2024")
        self.assertEqual(rcpn.tipo_livro, TipoLivroRcpnEnum.NASCIMENTO)
        self.assertEqual(rcpn.numero_livro, "00001")
        self.assertEqual(rcpn.numero_folha, "001")
        self.assertEqual(rcpn.numero_termo, "0000001")
        self.assertEqual(rcpn.dv, "67")

        masked_rcpn = CertidaoRCPN("123456.01.55.2024.1.00001.001.0000001-67")
        self.assertEqual(masked_rcpn, rcpn)

    def test_rcpn_invalido(self):
        with self.assertRaises(ValueError):
            CertidaoRCPN(None)

        with self.assertRaises(ValueError):
            CertidaoRCPN("123")

        with self.assertRaises(ValueError):
            CertidaoRCPN("12345600552024100001001000000171")

        with self.assertRaises(ValueError):
            CertidaoRCPN("12345601552024100001001000000100")
