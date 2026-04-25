
import pytest
from abrasileirado import enums

class TestIterableEnum:
    def test_description_with_tuple(self):
        class CorEnum(enums.IterableEnum):
            VERMELHO = ("#ff0000", "Vermelho")
            VERDE = ("#00ff00", "Verde")
            AZUL = ("#0000ff", "Azul")
        assert CorEnum.VERMELHO.description == "Vermelho"
        assert CorEnum.VERDE.description == "Verde"
        assert CorEnum.AZUL.description == "Azul"

    def test_description_with_value(self):
        class CorEnum(enums.IterableEnum):
            VERMELHO = "#ff0000"
            VERDE = "#00ff00"
            AZUL = "#0000ff"
        assert CorEnum.VERMELHO.description == "#ff0000"
        assert CorEnum.VERDE.description == "#00ff00"
        assert CorEnum.AZUL.description == "#0000ff"

    def test_as_choices(self):
        class CorEnum(enums.IterableEnum):
            VERMELHO = (1, "Vermelho")
            VERDE = (2, "Verde")
        assert CorEnum.as_choices() == [(1, "Vermelho"), (2, "Verde")]


@pytest.mark.parametrize("enum_cls, expected", [
    (enums.SimNaoIntEnum, [(1, "Sim"), (2, "Não"), (9, "Não informado")]),
    (enums.SimNaoStrEnum, [("S", "Sim"), ("N", "Não"), ("I", "Não informado")]),
    (enums.EstadoCivilEnum, [
        (1, "Solteiro(a)"), (2, "Casado(a)"), (3, "Viúvo(a)"), (4, "Divorciado(a)"),
        (5, "Separado(a) judicialmente"), (6, "Desquitado"), (99, "Não informado")]),
    (enums.CorRacaEnum, [
        (1, "Branca"), (2, "Preta"), (3, "Parda"), (4, "Amarela"), (5, "Indígena"), (99, "Não informada")]),
    (enums.SexoEnum, [(1, "Masculino"), (2, "Feminino"), (9, "Não informado")]),
    (enums.SexoStrEnum, [("M", "Masculino"), ("F", "Feminino"), ("N", "Não informado")]),
    (enums.GeneroEnum, [
        (1, "Mulher cisgênero"), (2, "Homem cisgênero"), (3, "Mulher trans"), (4, "Homem trans"),
        (5, "Travesti"), (6, "Não binário"), (7, "Outro"), (99, "Não informado")]),
    (enums.DeficienciaEnum, [
        (1, "Visão"), (2, "Audição"), (3, "Mobilidade"), (4, "Cognição/comunicação"), (5, "Autocuidado"), (9, "Não declarado")]),
    (enums.ZonaHabitacaoEnum, [(1, "Urbana"), (2, "Rural"), (3, "Área de transição"), (9, "Não informada")]),
    (enums.ZonaHabitacaoStrEnum, [("U", "Urbana"), ("R", "Rural"), ("T", "Área de transição"), ("N", "Não informada")]),
    (enums.RegiaoIntEnum, [
        (1, "Norte"), (2, "Nordeste"), (3, "Sudeste"), (4, "Sul"), (5, "Centro-oeste"), (9, "Não declarado")]),
    (enums.RegiaoStrEnum, [
        ("N", "Norte"), ("NE", "Nordeste"), ("SE", "Sudeste"), ("S", "Sul"), ("CO", "Centro-oeste"), ("N", "Não declarado")]),
])
def test_as_choices_parametrized(enum_cls, expected):
    assert enum_cls.as_choices() == expected

def test_unidade_federativa_int_enum():
    uf = enums.UnidadeFederativaIntEnum.SP
    assert uf.value == 35
    assert uf.description == "São Paulo"
    assert uf.region == enums.RegiaoIntEnum.SUDESTE

def test_unidade_federativa_str_enum():
    uf = enums.UnidadeFederativaStrEnum.SP
    assert uf.value == "SP"
    assert uf.description == "São Paulo"
    assert uf.code == "35"
    assert uf.region == enums.RegiaoStrEnum.SUDESTE

def test_regiao_ufs():
    # Testa se todas as UFs de uma região pertencem àquela região
    for regiao in enums.RegiaoIntEnum:
        for uf in regiao.ufs:
            assert uf.region == regiao
    for regiao in enums.RegiaoStrEnum:
        for uf in regiao.ufs:
            assert uf.region == regiao
