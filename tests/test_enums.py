from unittest import TestCase

from abrasileirado import enums


class TestIterableEnum(TestCase):
    def test_description_with_tuple(self):
        class CorEnum(enums.IterableEnum):
            VERMELHO = ("#ff0000", "Vermelho")
            VERDE = ("#00ff00", "Verde")
            AZUL = ("#0000ff", "Azul")

        self.assertEqual(CorEnum.VERMELHO.description, "Vermelho")
        self.assertEqual(CorEnum.VERDE.description, "Verde")
        self.assertEqual(CorEnum.AZUL.description, "Azul")

    def test_description_with_value(self):
        class CorEnum(enums.IterableEnum):
            VERMELHO = "#ff0000"
            VERDE = "#00ff00"
            AZUL = "#0000ff"

        self.assertEqual(CorEnum.VERMELHO.description, "#ff0000")
        self.assertEqual(CorEnum.VERDE.description, "#00ff00")
        self.assertEqual(CorEnum.AZUL.description, "#0000ff")

    def test_as_choices(self):
        class CorEnum(enums.IterableEnum):
            VERMELHO = (1, "Vermelho")
            VERDE = (2, "Verde")

        self.assertEqual(CorEnum.as_choices(), [(1, "Vermelho"), (2, "Verde")])


class TestEnumChoices(TestCase):
    def test_simnaoenum(self):
        self.assertEqual(enums.SimNaoEnum.as_choices(), [(1, "Sim"), (2, "Não"), (9, "Não declarado")])

    def test_simnaostr_enum(self):
        self.assertEqual(enums.SimNaoStrEnum.as_choices(), [("S", "Sim"), ("N", "Não"), ("ND", "Não declarado")])

    def test_estadocivilenum(self):
        self.assertEqual(
            enums.EstadoCivilEnum.as_choices(),
            [
                (1, "Solteiro(a)"),
                (2, "Casado(a)"),
                (3, "Viúvo(a)"),
                (4, "Divorciado(a)"),
                (5, "Separado(a) judicialmente"),
                (6, "Desquitado"),
                (99, "Não declarado"),
            ],
        )

    def test_corracaenum(self):
        self.assertEqual(
            enums.CorRacaEnum.as_choices(),
            [(1, "Branca"), (2, "Preta"), (3, "Parda"), (4, "Amarela"), (5, "Indígena"), (99, "Não declarada")],
        )

    def test_sexoenum(self):
        self.assertEqual(enums.SexoEnum.as_choices(), [(1, "Masculino"), (2, "Feminino"), (9, "Não declarado")])

    def test_sexostr_enum(self):
        self.assertEqual(
            enums.SexoStrEnum.as_choices(), [("M", "Masculino"), ("F", "Feminino"), ("ND", "Não declarado")]
        )

    def test_generoenum(self):
        self.assertEqual(
            enums.GeneroEnum.as_choices(),
            [
                (1, "Mulher cisgênero"),
                (2, "Homem cisgênero"),
                (3, "Mulher trans"),
                (4, "Homem trans"),
                (5, "Travesti"),
                (6, "Não binário"),
                (7, "Outro"),
                (99, "Não declarado"),
            ],
        )

    def test_deficienciaenum(self):
        self.assertEqual(
            enums.DeficienciaEnum.as_choices(),
            [
                (1, "Visão"),
                (2, "Audição"),
                (3, "Mobilidade"),
                (4, "Cognição/comunicação"),
                (5, "Autocuidado"),
                (9, "Não declarada"),
            ],
        )

    def test_zonahabitacaoenum(self):
        self.assertEqual(
            enums.ZonaHabitacaoEnum.as_choices(),
            [(1, "Urbana"), (2, "Rural"), (3, "Área de transição"), (9, "Não declarada")],
        )

    def test_zonahabitacaostr_enum(self):
        self.assertEqual(
            enums.ZonaHabitacaoStrEnum.as_choices(),
            [("U", "Urbana"), ("R", "Rural"), ("T", "Área de transição"), ("ND", "Não declarada")],
        )

    def test_regiaoenum(self):
        self.assertEqual(
            enums.RegiaoEnum.as_choices(),
            [(1, "Norte"), (2, "Nordeste"), (3, "Sudeste"), (4, "Sul"), (5, "Centro-oeste"), (9, "Não declarada")],
        )

    def test_regiaostr_enum(self):
        self.assertEqual(
            enums.RegiaoStrEnum.as_choices(),
            [
                ("N", "Norte"),
                ("NE", "Nordeste"),
                ("SE", "Sudeste"),
                ("S", "Sul"),
                ("CO", "Centro-oeste"),
                ("ND", "Não declarada"),
            ],
        )


class TestUnidadeFederativa(TestCase):
    def test_unidade_federativa_int_enum(self):
        uf = enums.UnidadeFederativaEnum.SP
        self.assertEqual(uf.value, 35)
        self.assertEqual(uf.description, "São Paulo")
        self.assertEqual(uf.region, enums.RegiaoEnum.SUDESTE)

    def test_unidade_federativa_str_enum(self):
        uf = enums.UnidadeFederativaStrEnum.SP
        self.assertEqual(uf.value, "SP")
        self.assertEqual(uf.description, "São Paulo")
        self.assertEqual(uf.code, "35")
        self.assertEqual(uf.region, enums.RegiaoStrEnum.SUDESTE)


class TestRegiaoUfs(TestCase):
    def test_regiao_ufs(self):
        # Testa se todas as UFs de uma região pertencem àquela região
        for regiao in enums.RegiaoEnum:
            for uf in regiao.ufs:
                self.assertEqual(uf.region, regiao)
        for regiao in enums.RegiaoStrEnum:
            for uf in regiao.ufs:
                self.assertEqual(uf.region, regiao)
