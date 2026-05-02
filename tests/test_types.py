import pytest

from abrasileirado.types import EnderecoBrasil
from abrasileirado.types import CodigoValidavel, CNES, CNS, CEP, CPF, CNPJ, NUP
from abrasileirado.enums import UnidadeFederativaStrEnum


def test_cpf_valido():
    cpf = CPF("12345678909")
    assert str(cpf) == "123.456.789-09"
    assert cpf.digitos == "12345678909"

def test_cpf_valido_com_mascara():
    cpf = CPF("123.456.789-09")
    assert str(cpf) == "123.456.789-09"
    assert cpf.digitos == "12345678909"

def test_cpf_invalido_dv():
    with pytest.raises(ValueError):
        CPF("12345678900")

def test_cpf_invalido_tamanho():
    with pytest.raises(ValueError):
        CPF("12345678")

def test_nup_valido():
    nup = NUP("23520005177202676")
    assert str(nup) == "23520.005177/2026-76"
    assert nup.digitos == "23520005177202676"

def test_nup_valido_com_mascara():
    nup = NUP("23520.005177/2026-76")
    assert str(nup) == "23520.005177/2026-76"
    assert nup.digitos == "23520005177202676"

def test_nup_invalido_dv():
    with pytest.raises(ValueError):
        NUP("23520005177202677")

def test_nup_invalido_tamanho():
    with pytest.raises(ValueError):
        NUP("1234567890123456")

def test_cnes_valid():
    cnes = CNES('1234567')
    assert cnes.digitos == '1234567'
    assert str(cnes) == '1234567'
    assert CNES('0000001').digitos == '0000001'
    assert CNES('0000001').__str__() == '0000001'
    # Inválido: menos de 3 dígitos
    with pytest.raises(ValueError):
        CNES('12')
    # Inválido: todos dígitos iguais
    with pytest.raises(ValueError):
        CNES('1111111')

def test_cns_valid():
    cns = CNS('123456789012345')
    assert cns.digitos == '123456789012345'
    assert str(cns) == '123456789012345'
    # Inválido: menos de 3 dígitos
    with pytest.raises(ValueError):
        CNS('12')
    # Inválido: todos dígitos iguais
    with pytest.raises(ValueError):
        CNS('111111111111111')

def test_cep_valid():
    cep = CEP('12345678')
    assert cep.digitos == '12345678'
    assert str(cep) == '12345-678'
    cep2 = CEP('12.345-678')
    assert cep2.digitos == '12345678'
    assert str(cep2) == '12345-678'
    # Inválido: menos de 3 dígitos
    with pytest.raises(ValueError):
        CEP('12')
    # Inválido: todos dígitos iguais
    with pytest.raises(ValueError):
        CEP('11111111')

def test_cpf_valid():
    # CPF válido: 000.000.001-91
    cpf = CPF('00000000191')
    assert cpf.digitos == '00000000191'
    assert str(cpf) == '000.000.001-91'
    cpf2 = CPF('000.000.001-91')
    assert cpf2.digitos == '00000000191'
    assert str(cpf2) == '000.000.001-91'
    # Inválido: todos dígitos iguais
    with pytest.raises(ValueError):
        CPF('11111111111')
    # Inválido: menos de 3 dígitos
    with pytest.raises(ValueError):
        CPF('1')
    # Inválido: DV errado
    with pytest.raises(ValueError):
        CPF('12345678900')

def test_cnpj_valid():
    # CNPJ válido: 12.345.678/9000-05
    cnpj = CNPJ('12345678900005')
    assert cnpj.digitos == '12345678900005'
    assert str(cnpj) == '12.345.678/9000-05'
    cnpj2 = CNPJ('12.345.678/9000-05')
    assert cnpj2.digitos == '12345678900005'
    assert str(cnpj2) == '12.345.678/9000-05'
    # Inválido: todos dígitos iguais
    with pytest.raises(ValueError):
        CNPJ('11111111111111')
    # Inválido: menos de 3 dígitos
    with pytest.raises(ValueError):
        CNPJ('1')
    # Inválido: DV errado
    with pytest.raises(ValueError):
        CNPJ('12345678900000')

def test_endereco_brasil():
    cep = CEP('12345678')
    uf = UnidadeFederativaStrEnum.SP
    endereco = EnderecoBrasil(
        logradouro='Rua Teste',
        numero='123',
        bairro='Centro',
        municipio='São Paulo',
        uf=uf,
        cep=cep,
        complemento='Apto 1'
    )
    assert endereco.linha_logradouro == 'Rua Teste 123, Apto 1'
    assert 'Centro' in endereco.extendido
    assert 'São Paulo/SP' in endereco.extendido
    assert str(endereco).startswith('Rua Teste 123, Apto 1')
    # Sem complemento
    endereco2 = EnderecoBrasil(
        logradouro='Av. Brasil',
        numero='1000',
        bairro='Jardim',
        municipio='Campinas',
        uf=UnidadeFederativaStrEnum.SP,
        cep=cep
    )
    assert endereco2.linha_logradouro == 'Av. Brasil 1000'


def test_codigo_validavel_basic_validation_missing_coverage():
    # Covering line 69: if code is None: return None
    cv = CodigoValidavel.__new__(CodigoValidavel)
    assert cv._basic_digits_validation(None) is None

    # Covering line 75: if value is None or value.strip() == '': return None
    assert cv._basic_digits_validation("") is None
    assert cv._basic_digits_validation("abc") is None

def test_codigo_validavel_full_digits_default():
    # Covering line 30: return 1 in _full_digits
    cv = CodigoValidavel.__new__(CodigoValidavel)
    assert cv._full_digits == 1

def test_cep_invalid_length_beyond_full_digits():
    # CEP._is_valid is an instance method (no @classmethod)
    # CodigoValidavel.__init__ calls self._is_valid
    with pytest.raises(ValueError):
        CEP("123456789")


class TestNUP:
    def test_nup_valido(self):
        # Exemplo real de NUP válido: 23520005177202676
        # Base: 2352000517720267, DV: 6 (98 - (base % 97))
        nup = NUP("23520005177202676")
        assert str(nup) == "23520.005177/2026-76"
        assert nup.digitos == "23520005177202676"

    def test_nup_valido_com_mascara(self):
        nup = NUP("23520.005177/2026-76")
        assert str(nup) == "23520.005177/2026-76"
        assert nup.digitos == "23520005177202676"

    def test_nup_invalido_dv(self):
        with pytest.raises(ValueError):
            NUP("23520005177202677")  # DV incorreto

    def test_nup_invalido_tamanho(self):
        with pytest.raises(ValueError):
            NUP("1234567890123456")  # Menos de 17 dígitos

    def test_nup_invalido_tamanho_maior(self):
        with pytest.raises(ValueError):
            NUP("123456789012345678")  # Mais de 17 dígitos
