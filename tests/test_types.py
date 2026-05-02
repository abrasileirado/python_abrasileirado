from unittest import TestCase

from abrasileirado.enums import UnidadeFederativaStrEnum
from abrasileirado.types import (
    CEP,
    CNES,
    CNJ,
    CNPJ,
    CNS,
    CPF,
    NUP,
    PIS,
    RENAVAM,
    Certidao,
    CodigoValidavel,
    EnderecoBrasil,
    Passaporte,
    PlacaVeicular,
    Telefone,
    TituloEleitoral,
)


class TestCPF(TestCase):
    def test_cpf_valido(self):
        cpf = CPF("12345678909")
        self.assertEqual(str(cpf), "123.456.789-09")
        self.assertEqual(cpf.digitos, "12345678909")

    def test_cpf_valid(self):
        # CPF válido: 000.000.001-91
        cpf = CPF("00000000191")
        self.assertEqual(cpf.digitos, "00000000191")
        self.assertEqual(str(cpf), "000.000.001-91")
        cpf2 = CPF("000.000.001-91")
        self.assertEqual(cpf2.digitos, "00000000191")
        self.assertEqual(str(cpf2), "000.000.001-91")
        # Inválido: todos dígitos iguais
        with self.assertRaises(ValueError):
            CPF("11111111111")
        # Inválido: menos de 3 dígitos
        with self.assertRaises(ValueError):
            CPF("1")
        # Inválido: DV errado
        with self.assertRaises(ValueError):
            CPF("12345678900")

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
    def test_cnes_valid(self):
        cnes = CNES("1234567")
        self.assertEqual(cnes.digitos, "1234567")
        self.assertEqual(str(cnes), "1234567")
        self.assertEqual(CNES("0000001").digitos, "0000001")
        self.assertEqual(CNES("0000001").__str__(), "0000001")
        # Inválido: menos de 3 dígitos
        with self.assertRaises(ValueError):
            CNES("12")
        # Inválido: todos dígitos iguais
        with self.assertRaises(ValueError):
            CNES("1111111")


class TestCNS(TestCase):
    def test_cns_valid(self):
        cns = CNS("123456789012345")
        self.assertEqual(cns.digitos, "123456789012345")
        self.assertEqual(str(cns), "123456789012345")
        # Inválido: menos de 3 dígitos
        with self.assertRaises(ValueError):
            CNS("12")
        # Inválido: todos dígitos iguais
        with self.assertRaises(ValueError):
            CNS("111111111111111")


class TestCEP(TestCase):
    def test_cep_valid(self):
        cep = CEP("12345678")
        self.assertEqual(cep.digitos, "12345678")
        self.assertEqual(str(cep), "12345-678")
        cep2 = CEP("12.345-678")
        self.assertEqual(cep2.digitos, "12345678")
        self.assertEqual(str(cep2), "12345-678")
        # Inválido: menos de 3 dígitos
        with self.assertRaises(ValueError):
            CEP("12")
        # Inválido: todos dígitos iguais
        with self.assertRaises(ValueError):
            CEP("11111111")


class TestCNPJ(TestCase):
    def test_cnpj_valid(self):
        # CNPJ válido: 12.345.678/9000-05
        cnpj = CNPJ("12345678900005")
        self.assertEqual(cnpj.digitos, "12345678900005")
        self.assertEqual(str(cnpj), "12.345.678/9000-05")
        cnpj2 = CNPJ("12.345.678/9000-05")
        self.assertEqual(cnpj2.digitos, "12345678900005")
        self.assertEqual(str(cnpj2), "12.345.678/9000-05")
        # Inválido: todos dígitos iguais
        with self.assertRaises(ValueError):
            CNPJ("11111111111111")
        # Inválido: menos de 3 dígitos
        with self.assertRaises(ValueError):
            CNPJ("1")
        # Inválido: DV errado
        with self.assertRaises(ValueError):
            CNPJ("12345678900000")


class TestEnderecoBrasil(TestCase):
    def test_endereco_brasil(self):
        cep = CEP("12345678")
        uf = UnidadeFederativaStrEnum.SP
        endereco = EnderecoBrasil(
            logradouro="Rua Teste",
            numero="123",
            bairro="Centro",
            municipio="São Paulo",
            uf=uf,
            cep=cep,
            complemento="Apto 1",
        )
        self.assertEqual(endereco.linha_logradouro, "Rua Teste 123, Apto 1")
        self.assertIn("Centro", endereco.extendido)
        self.assertIn("São Paulo/SP", endereco.extendido)
        self.assertTrue(str(endereco).startswith("Rua Teste 123, Apto 1"))
        # Sem complemento
        endereco2 = EnderecoBrasil(
            logradouro="Av. Brasil",
            numero="1000",
            bairro="Jardim",
            municipio="Campinas",
            uf=UnidadeFederativaStrEnum.SP,
            cep=cep,
        )
        self.assertEqual(endereco2.linha_logradouro, "Av. Brasil 1000")


class TestCodigoValidavel(TestCase):
    def test_codigo_validavel_basic_validation_with_none_empty_and_nondigit_input(self):
        # Covering line 69: if code is None: return None
        cv = CodigoValidavel.__new__(CodigoValidavel)
        self.assertIsNone(cv._basic_digits_validation(None))

        # Covering line 75: if value is None or value.strip() == '': return None
        self.assertIsNone(cv._basic_digits_validation(""))
        self.assertIsNone(cv._basic_digits_validation("abc"))

    def test_codigo_validavel_full_digits_default(self):
        # Validate default digit handling through observable behavior
        cpf = CPF("12345678909")
        self.assertEqual(cpf.digitos, "12345678909")
        self.assertEqual(str(cpf), "123.456.789-09")


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


class TestCPFDerivedMasks(TestCase):
    def test_cpf_derived_codes_use_grouped_mask(self):
        expected_formats = {
            PIS: "123 456 789 09",
            RENAVAM: "123 456 789 09",
            TituloEleitoral: "123 456 789 09",
            CNJ: "123 456 789 09",
            Telefone: "123 456 789 09",
            Passaporte: "123 456 789 09",
            PlacaVeicular: "123 456 789 09",
            Certidao: "123 456 789 09",
        }

        for code_class, expected_mask in expected_formats.items():
            with self.subTest(code_class=code_class.__name__):
                code = code_class("12345678909")
                self.assertEqual(code.digitos, "12345678909")
                self.assertEqual(str(code), expected_mask)
