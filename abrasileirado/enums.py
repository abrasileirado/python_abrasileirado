from enum import Enum
from typing import Any


class IterableEnum(Enum):
    """Enum base que permite iterar sobre seus membros e acessar suas descrições.
    Cada membro do enum pode ter um atributo 'description' que fornece uma descrição legível do membro.
    Se o atributo 'description' não estiver presente, a descrição será o valor do membro convertido para string.
    """

    def __init__(self, value: Any, description: Any = None) -> None:
        """Inicializa o membro do enum com um valor e uma descrição opcional.
        Se a descrição não for fornecida, ela será definida como o valor do membro convertido para string.
        Args:
            value (Any): O valor do membro do enum.
            description (Any, optional): A descrição legível do membro do enum. Defaults to None.
        Returns:
            None

        Examples:
            .. code-block:: python
                class CorEnum(IterableEnum):
                    VERMELHO = ('#ff0000', 'Vermelho')
                    VERDE = ('#00ff00', 'Verde')
                    AZUL = ('#0000ff', 'Azul')

                print(CorEnum.VERMELHO.description)  # Output: Vermelho
                print(CorEnum.VERDE.description)     # Output: Verde
                print(CorEnum.AZUL.description)     # Output: Azul

            .. code-block:: python
                class CorEnum(IterableEnum):
                    VERMELHO = '#ff0000'
                    VERDE = '#00ff00'
                    AZUL = '#0000ff'

                print(CorEnum.VERMELHO.description)  # Output: #ff0000
                print(CorEnum.VERDE.description)     # Output: #00ff00
                print(CorEnum.AZUL.description)     # Output: #0000ff
        """
        super().__init__()
        self.description = description if description else value
        self._value_ = value

    @classmethod
    def as_choices(cls) -> tuple[Any, str]:
        """Retorna uma lista de tuplas contendo o valor e a descrição de cada membro do enum.
        A descrição é obtida a partir do atributo 'description' de cada membro, se existir, ou do valor do membro
        caso contrário.

        Returns:
            list[tuple[Any, str]]: Lista de tuplas contendo o valor e a descrição de cada membro do enum.

        Examples:

            .. code-block:: python
                class CorEnum(IterableEnum):
                    VERMELHO = ('#ff0000', 'Vermelho')
                    VERDE = ('#00ff00', 'Verde')
                    AZUL = ('#0000ff', 'Azul')

                print(CorEnum.as_choices())
                # Output: [('#ff0000', 'Vermelho'), ('#00ff00', 'Verde'), ('#0000ff', 'Azul')]

            .. code-block:: python
                class CorEnum(IterableEnum):
                    VERMELHO = '#ff0000'
                    VERDE = '#00ff00'
                    AZUL = '#0000ff'
                print(CorEnum.as_choices())
                # Output: [('#ff0000', '#ff0000'), ('#00ff00', '#00ff00'), ('#0000ff', '#0000ff')]

            .. code-block:: python
                class CorEnum(IterableEnum):
                    VERMELHO = 16711680
                    VERDE = 65280
                    AZUL = 255
                print(CorEnum.as_choices())
                # Output: [(16711680, '16711680'), (65280, '65280'), (255, '255')]
        """
        return [(x.value, getattr(x, "description", str(x))) for x in cls]


class SimNaoEnum(IterableEnum):
    SIM = (1, "Sim")
    NAO = (2, "Não")
    NAO_INFORMADO = (9, "Não informado")


class SimNaoStrEnum(IterableEnum):
    SIM = ("S", "Sim")
    NAO = ("N", "Não")
    NAO_INFORMADO = ("I", "Não informado")


class EstadoCivilEnum(IterableEnum):
    """Enum para representar os estados civis de uma pessoa.
    Fonte: IBGE, usado no PNAD Contínua e PNS.
    """

    SOLTEIRO = (1, "Solteiro(a)")
    CASADO = (2, "Casado(a)")
    VIUVO = (3, "Viúvo(a)")
    DIVORCIADO = (4, "Divorciado(a)")
    SEPARADO = (5, "Separado(a) judicialmente")
    UNIAO_ESTAVEL = (6, "Desquitado")
    NAO_INFORMADO = (99, "Não informado")


class CorRacaEnum(IterableEnum):
    """Enum para representar as cores/raças de uma pessoa.
    Fonte: IBGE, usado no PNAD Contínua e PNS.
    """

    BRANCA = (1, "Branca")
    PRETA = (2, "Preta")
    PARDA = (3, "Parda")
    AMARELA = (4, "Amarela")
    INDIGENA = (5, "Indígena")
    NAO_INFORMADA = (99, "Não informada")


class SexoEnum(IterableEnum):
    """Enum para representar os sexos de uma pessoa.
    Fonte: IBGE, usado no PNAD Contínua e PNS.
    """

    MASCULINO = (1, "Masculino")
    FEMININO = (2, "Feminino")
    NAO_INFORMADO = (9, "Não informado")


class SexoStrEnum(IterableEnum):
    """Enum para representar os sexos de uma pessoa, com valores string."""

    MASCULINO = ("M", "Masculino")
    FEMININO = ("F", "Feminino")
    NAO_INFORMADO = ("N", "Não informado")


class GeneroEnum(IterableEnum):
    """Enum para representar os gêneros de uma pessoa
    Fonte: IBGE, usado no PNAD Contínua e PNS.
    """

    MULHER_CISGENERO = (1, "Mulher cisgênero")
    HOMEM_CISGENERO = (2, "Homem cisgênero")
    MULHER_TRANS = (3, "Mulher trans")
    HOMEM_TRANS = (4, "Homem trans")
    TRAVESTI = (5, "Travesti")
    NAO_BINARIO = (6, "Não binário")
    OUTRO = (7, "Outro")
    NAO_INFORMADO = (99, "Não informado")


class DeficienciaEnum(IterableEnum):
    """Enum para representar as deficiências de uma pessoa, com valores inteiros.
    Fonte: IBGE, usado no PNAD Contínua e PNS
    """

    VISAO = (1, "Visão")
    AUDICAO = (2, "Audição")
    MOBILIDADE = (3, "Mobilidade")
    COGNICAO_COMUNICACAO = (4, "Cognição/comunicação")
    AUTOCUIDADO = (5, "Autocuidado")
    NAO_DECLARADO = (9, "Não declarado")


class ZonaHabitacaoEnum(IterableEnum):
    """Enum para representar as zonas de habitação.
    Fonte: IBGE, classificação domiciliar do Censo.
    """

    URBANA = (1, "Urbana")
    RURAL = (2, "Rural")
    TRANSICAO = (3, "Área de transição")
    NAO_INFORMADA = (9, "Não informada")


class ZonaHabitacaoStrEnum(IterableEnum):
    """Enum para representar as zonas de habitação, em string.
    Fonte: IBGE, classificação domiciliar do Censo.
    """

    URBANA = ("U", "Urbana")
    RURAL = ("R", "Rural")
    TRANSICAO = ("T", "Área de transição")
    NAO_INFORMADA = ("N", "Não informada")


class RegiaoEnum(IterableEnum):
    """Enum para representar as regiões do Brasil, com valores inteiros.
    Fonte: IBGE, usado no PNAD Contínua e PNS
    """

    NORTE = (1, "Norte")
    NORDESTE = (2, "Nordeste")
    SUDESTE = (3, "Sudeste")
    SUL = (4, "Sul")
    CENTRO_OESTE = (5, "Centro-oeste")
    NAO_DECLARADO = (9, "Não declarado")

    @property
    def ufs(self) -> list["UnidadeFederativaEnum"]:
        return [uf for uf in UnidadeFederativaEnum if uf.region == self]


class RegiaoStrEnum(IterableEnum):
    """Enum para representar as regiões do Brasil, com valores string.
    Fonte: IBGE, usado no PNAD Contínua e PNS
    """

    NORTE = ("N", "Norte")
    NORDESTE = ("NE", "Nordeste")
    SUDESTE = ("SE", "Sudeste")
    SUL = ("S", "Sul")
    CENTRO_OESTE = ("CO", "Centro-oeste")
    NAO_DECLARADO = ("N", "Não declarado")

    @property
    def ufs(self) -> list["UnidadeFederativaStrEnum"]:
        return [uf for uf in UnidadeFederativaStrEnum if uf.region == self]


class UnidadeFederativaEnum(IterableEnum):
    """Enum para representar as unidades federativas do Brasil, com valores inteiros.
    Fonte: IBGE, usado no PNAD Contínua e PNS
    """

    AC = (12, "Acre", RegiaoEnum.NORTE)
    AL = (27, "Alagoas", RegiaoEnum.NORDESTE)
    AP = (16, "Amapá", RegiaoEnum.NORTE)
    AM = (13, "Amazonas", RegiaoEnum.NORTE)
    BA = (29, "Bahia", RegiaoEnum.NORDESTE)
    CE = (23, "Ceará", RegiaoEnum.NORDESTE)
    DF = (53, "Distrito Federal", RegiaoEnum.CENTRO_OESTE)
    ES = (32, "Espírito Santo", RegiaoEnum.SUDESTE)
    GO = (52, "Goiás", RegiaoEnum.CENTRO_OESTE)
    MA = (21, "Maranhão", RegiaoEnum.NORDESTE)
    MT = (51, "Mato Grosso", RegiaoEnum.CENTRO_OESTE)
    MS = (50, "Mato Grosso do Sul", RegiaoEnum.CENTRO_OESTE)
    MG = (31, "Minas Gerais", RegiaoEnum.SUDESTE)
    PA = (15, "Pará", RegiaoEnum.NORTE)
    PB = (25, "Paraíba", RegiaoEnum.NORDESTE)
    PR = (41, "Paraná", RegiaoEnum.SUL)
    PE = (26, "Pernambuco", RegiaoEnum.NORDESTE)
    PI = (22, "Piauí", RegiaoEnum.NORDESTE)
    RJ = (33, "Rio de Janeiro", RegiaoEnum.SUDESTE)
    RN = (24, "Rio Grande do Norte", RegiaoEnum.NORDESTE)
    RS = (43, "Rio Grande do Sul", RegiaoEnum.SUL)
    RO = (11, "Rondônia", RegiaoEnum.NORTE)
    RR = (14, "Roraima", RegiaoEnum.NORTE)
    SC = (42, "Santa Catarina", RegiaoEnum.SUL)
    SP = (35, "São Paulo", RegiaoEnum.SUDESTE)
    SE = (28, "Sergipe", RegiaoEnum.NORDESTE)
    TO = (17, "Tocantins", RegiaoEnum.NORTE)

    def __init__(self, value: Any, description: str, region: RegiaoEnum) -> None:
        super().__init__(value, description)
        self.region = region


class UnidadeFederativaStrEnum(IterableEnum):
    """Enum para representar as unidades federativas do Brasil, com valores string.
    Fonte: IBGE, usado no PNAD Contínua e PNS
    """

    AC = ("AC", "Acre", "12", RegiaoStrEnum.NORTE)
    AL = ("AL", "Alagoas", "27", RegiaoStrEnum.NORDESTE)
    AP = ("AP", "Amapá", "16", RegiaoStrEnum.NORTE)
    AM = ("AM", "Amazonas", "13", RegiaoStrEnum.NORTE)
    BA = ("BA", "Bahia", "29", RegiaoStrEnum.NORDESTE)
    CE = ("CE", "Ceará", "23", RegiaoStrEnum.NORDESTE)
    DF = ("DF", "Distrito Federal", "53", RegiaoStrEnum.CENTRO_OESTE)
    ES = ("ES", "Espírito Santo", "32", RegiaoStrEnum.SUDESTE)
    GO = ("GO", "Goiás", "52", RegiaoStrEnum.CENTRO_OESTE)
    MA = ("MA", "Maranhão", "21", RegiaoStrEnum.NORDESTE)
    MT = ("MT", "Mato Grosso", "51", RegiaoStrEnum.CENTRO_OESTE)
    MS = ("MS", "Mato Grosso do Sul", "50", RegiaoStrEnum.CENTRO_OESTE)
    MG = ("MG", "Minas Gerais", "31", RegiaoStrEnum.SUDESTE)
    PA = ("PA", "Pará", "15", RegiaoStrEnum.NORTE)
    PB = ("PB", "Paraíba", "25", RegiaoStrEnum.NORDESTE)
    PR = ("PR", "Paraná", "41", RegiaoStrEnum.SUL)
    PE = ("PE", "Pernambuco", "26", RegiaoStrEnum.NORDESTE)
    PI = ("PI", "Piauí", "22", RegiaoStrEnum.NORDESTE)
    RJ = ("RJ", "Rio de Janeiro", "33", RegiaoStrEnum.SUDESTE)
    RN = ("RN", "Rio Grande do Norte", "24", RegiaoStrEnum.NORDESTE)
    RS = ("RS", "Rio Grande do Sul", "43", RegiaoStrEnum.SUL)
    RO = ("RO", "Rondônia", "11", RegiaoStrEnum.NORTE)
    RR = ("RR", "Roraima", "14", RegiaoStrEnum.NORTE)
    SC = ("SC", "Santa Catarina", "42", RegiaoStrEnum.SUL)
    SP = ("SP", "São Paulo", "35", RegiaoStrEnum.SUDESTE)
    SE = ("SE", "Sergipe", "28", RegiaoStrEnum.NORDESTE)
    TO = ("TO", "Tocantins", "17", RegiaoStrEnum.NORTE)

    def __init__(self, value: Any, description: str, _code: str, region: RegiaoStrEnum) -> None:
        super().__init__(value, description)
        self.code = _code
        self.region = region


class GrupoNaturezaJuridicaEnum(IterableEnum):
    ADMINISTRACAO_PUBLICA = ("1", "ADMINISTRAÇÃO PÚBLICA")
    ENTIDADES_EMPRESARIAIS = ("2", "ENTIDADES EMPRESARIAIS")
    ENTIDADES_SEM_FINS_LUCRATIVOS = ("3", "ENTIDADES SEM FINS LUCRATIVOS")
    PESSOAS_FISICAS = ("4", "PESSOAS FÍSICAS")
    ORGANIZACOES_INTERNACIONAIS = ("5", "ORGANIZAÇÕES INTERNACIONAIS E OUTRAS INSTITUIÇÕES EXTRATERRITORIAIS")


class NaturezaJuridicaEnum(IterableEnum):
    # 1. ADMINISTRAÇÃO PÚBLICA
    ORGAO_EXECUTIVO_FEDERAL = (
        "1015",
        "Órgão Público do Poder Executivo Federal",
        GrupoNaturezaJuridicaEnum.ADMINISTRACAO_PUBLICA,
    )
    ORGAO_EXECUTIVO_ESTADUAL = (
        "1023",
        "Órgão Público do Poder Executivo Estadual ou do Distrito Federal",
        GrupoNaturezaJuridicaEnum.ADMINISTRACAO_PUBLICA,
    )
    ORGAO_EXECUTIVO_MUNICIPAL = (
        "1031",
        "Órgão Público do Poder Executivo Municipal",
        GrupoNaturezaJuridicaEnum.ADMINISTRACAO_PUBLICA,
    )
    ORGAO_LEGISLATIVO_FEDERAL = (
        "1040",
        "Órgão Público do Poder Legislativo Federal",
        GrupoNaturezaJuridicaEnum.ADMINISTRACAO_PUBLICA,
    )
    ORGAO_LEGISLATIVO_ESTADUAL = (
        "1058",
        "Órgão Público do Poder Legislativo Estadual ou do Distrito Federal",
        GrupoNaturezaJuridicaEnum.ADMINISTRACAO_PUBLICA,
    )
    ORGAO_LEGISLATIVO_MUNICIPAL = (
        "1066",
        "Órgão Público do Poder Legislativo Municipal",
        GrupoNaturezaJuridicaEnum.ADMINISTRACAO_PUBLICA,
    )
    ORGAO_JUDICIARIO_FEDERAL = (
        "1074",
        "Órgão Público do Poder Judiciário Federal",
        GrupoNaturezaJuridicaEnum.ADMINISTRACAO_PUBLICA,
    )
    ORGAO_JUDICIARIO_ESTADUAL = (
        "1082",
        "Órgão Público do Poder Judiciário Estadual",
        GrupoNaturezaJuridicaEnum.ADMINISTRACAO_PUBLICA,
    )
    AUTARQUIA_FEDERAL = ("1104", "Autarquia Federal", GrupoNaturezaJuridicaEnum.ADMINISTRACAO_PUBLICA)
    AUTARQUIA_ESTADUAL = (
        "1112",
        "Autarquia Estadual ou do Distrito Federal",
        GrupoNaturezaJuridicaEnum.ADMINISTRACAO_PUBLICA,
    )
    AUTARQUIA_MUNICIPAL = ("1120", "Autarquia Municipal", GrupoNaturezaJuridicaEnum.ADMINISTRACAO_PUBLICA)
    FUNDACAO_FEDERAL = ("1139", "Fundação Federal", GrupoNaturezaJuridicaEnum.ADMINISTRACAO_PUBLICA)
    FUNDACAO_ESTADUAL = (
        "1147",
        "Fundação Estadual ou do Distrito Federal",
        GrupoNaturezaJuridicaEnum.ADMINISTRACAO_PUBLICA,
    )
    FUNDACAO_MUNICIPAL = ("1155", "Fundação Municipal", GrupoNaturezaJuridicaEnum.ADMINISTRACAO_PUBLICA)
    ORGAO_AUTONOMO_UNIAO = ("1163", "Órgão Público Autônomo da União", GrupoNaturezaJuridicaEnum.ADMINISTRACAO_PUBLICA)
    ORGAO_AUTONOMO_ESTADUAL = (
        "1171",
        "Órgão Público Autônomo Estadual ou do Distrito Federal",
        GrupoNaturezaJuridicaEnum.ADMINISTRACAO_PUBLICA,
    )
    ORGAO_AUTONOMO_MUNICIPAL = (
        "1180",
        "Órgão Público Autônomo Municipal",
        GrupoNaturezaJuridicaEnum.ADMINISTRACAO_PUBLICA,
    )

    # 2. ENTIDADES EMPRESARIAIS
    EMPRESA_PUBLICA = ("2011", "Empresa Pública", GrupoNaturezaJuridicaEnum.ENTIDADE_EMPRESARIAL)
    SOCIEDADE_ECONOMIA_MISTA = ("2038", "Sociedade de Economia Mista", GrupoNaturezaJuridicaEnum.ENTIDADE_EMPRESARIAL)
    SOCIEDADE_ANONIMA_ABERTA = ("2046", "Sociedade Anônima Aberta", GrupoNaturezaJuridicaEnum.ENTIDADE_EMPRESARIAL)
    SOCIEDADE_ANONIMA_FECHADA = ("2054", "Sociedade Anônima Fechada", GrupoNaturezaJuridicaEnum.ENTIDADE_EMPRESARIAL)
    SOCIEDADE_EMPRESARIA_LIMITADA = (
        "2062",
        "Sociedade Empresária Limitada",
        GrupoNaturezaJuridicaEnum.ENTIDADE_EMPRESARIAL,
    )
    SOCIEDADE_EMPRESARIA_NOME_COLETIVO = (
        "2076",
        "Sociedade Empresária em Nome Coletivo",
        GrupoNaturezaJuridicaEnum.ENTIDADE_EMPRESARIAL,
    )
    SOCIEDADE_EMPRESARIA_COMANDITA_SIMPLES = (
        "2089",
        "Sociedade Empresária em Comandita Simples",
        GrupoNaturezaJuridicaEnum.ENTIDADE_EMPRESARIAL,
    )
    SOCIEDADE_EMPRESARIA_COMANDITA_ACOES = (
        "2097",
        "Sociedade Empresária em Comandita por Ações",
        GrupoNaturezaJuridicaEnum.ENTIDADE_EMPRESARIAL,
    )
    SOCIEDADE_MERCANTIL_EXTINTA = (
        "2100",
        "Sociedade Mercantil de Capital e Indústria (extinta pelo NCC/2002)",
        GrupoNaturezaJuridicaEnum.ENTIDADE_EMPRESARIAL,
    )
    SOCIEDADE_EMPRESARIA_CONTA_PARTICIPACAO = (
        "2127",
        "Sociedade Empresária em Conta de Participação",
        GrupoNaturezaJuridicaEnum.ENTIDADE_EMPRESARIAL,
    )
    EMPRESARIO_INDIVIDUAL = ("2135", "Empresário (Individual)", GrupoNaturezaJuridicaEnum.ENTIDADE_EMPRESARIAL)
    COOPERATIVA = ("2143", "Cooperativa", GrupoNaturezaJuridicaEnum.ENTIDADE_EMPRESARIAL)
    CONSORCIO_SOCIEDADES = ("2151", "Consórcio de Sociedades", GrupoNaturezaJuridicaEnum.ENTIDADE_EMPRESARIAL)
    GRUPO_SOCIEDADES = ("2160", "Grupo de Sociedades", GrupoNaturezaJuridicaEnum.ENTIDADE_EMPRESARIAL)
    ESTABELECIMENTO_SOCIEDADE_ESTRANGEIRA = (
        "2178",
        "Estabelecimento, no Brasil, de Sociedade Estrangeira",
        GrupoNaturezaJuridicaEnum.ENTIDADE_EMPRESARIAL,
    )
    ESTABELECIMENTO_EMPRESA_BINACIONAL = (
        "2194",
        "Estabelecimento, no Brasil, de Empresa Binacional Argentino-Brasileira",
        GrupoNaturezaJuridicaEnum.ENTIDADE_EMPRESARIAL,
    )
    ENTIDADE_BINACIONAL_ITAIPU = ("2208", "Entidade Binacional Itaipu", GrupoNaturezaJuridicaEnum.ENTIDADE_EMPRESARIAL)
    EMPRESA_DOMICILIADA_EXTERIOR = (
        "2216",
        "Empresa Domiciliada no Exterior",
        GrupoNaturezaJuridicaEnum.ENTIDADE_EMPRESARIAL,
    )
    CLUBE_FUNDO_INVESTIMENTO = ("2224", "Clube/Fundo de Investimento", GrupoNaturezaJuridicaEnum.ENTIDADE_EMPRESARIAL)
    SOCIEDADE_SIMPLES_PURA = ("2232", "Sociedade Simples Pura", GrupoNaturezaJuridicaEnum.ENTIDADE_EMPRESARIAL)
    SOCIEDADE_SIMPLES_LIMITADA = ("2240", "Sociedade Simples Limitada", GrupoNaturezaJuridicaEnum.ENTIDADE_EMPRESARIAL)
    SOCIEDADE_NOME_COLETIVO = ("2259", "Sociedade em Nome Coletivo", GrupoNaturezaJuridicaEnum.ENTIDADE_EMPRESARIAL)
    SOCIEDADE_COMANDITA_SIMPLES = (
        "2267",
        "Sociedade em Comandita Simples",
        GrupoNaturezaJuridicaEnum.ENTIDADE_EMPRESARIAL,
    )
    SOCIEDADE_SIMPLES_CONTA_PARTICIPACAO = (
        "2275",
        "Sociedade Simples em Conta de Participação",
        GrupoNaturezaJuridicaEnum.ENTIDADE_EMPRESARIAL,
    )
    EMPRESA_INDIVIDUAL_LIMITADA = (
        "2305",
        "Empresa Individual de Responsabilidade Limitada",
        GrupoNaturezaJuridicaEnum.ENTIDADE_EMPRESARIAL,
    )

    # 3. ENTIDADES SEM FINS LUCRATIVOS
    SERVICO_NOTARIAL_REGISTRAL = (
        "3034",
        "Serviço Notarial e Registral (Cartório)",
        GrupoNaturezaJuridicaEnum.ENTIDADE_SEM_FINS_LUCRATIVOS,
    )
    ORGANIZACAO_SOCIAL = ("3042", "Organização Social", GrupoNaturezaJuridicaEnum.ENTIDADE_SEM_FINS_LUCRATIVOS)
    OSCIP = (
        "3050",
        "Organização da Sociedade Civil de Interesse Público (Oscip)",
        GrupoNaturezaJuridicaEnum.ENTIDADE_SEM_FINS_LUCRATIVOS,
    )
    FUNDACAO_PRIVADA = (
        "3069",
        "Outras Formas de Fundações Mantidas com Recursos Privados",
        GrupoNaturezaJuridicaEnum.ENTIDADE_SEM_FINS_LUCRATIVOS,
    )
    SERVICO_SOCIAL_AUTONOMO = (
        "3077",
        "Serviço Social Autônomo",
        GrupoNaturezaJuridicaEnum.ENTIDADE_SEM_FINS_LUCRATIVOS,
    )
    CONDOMINIO_EDILICIOS = ("3085", "Condomínio Edilícios", GrupoNaturezaJuridicaEnum.ENTIDADE_SEM_FINS_LUCRATIVOS)
    UNIDADE_EXECUTORA = (
        "3093",
        "Unidade Executora (Programa Dinheiro Direto na Escola)",
        GrupoNaturezaJuridicaEnum.ENTIDADE_SEM_FINS_LUCRATIVOS,
    )
    COMISSAO_CONCILIACAO_PREVIA = (
        "3107",
        "Comissão de Conciliação Prévia",
        GrupoNaturezaJuridicaEnum.ENTIDADE_SEM_FINS_LUCRATIVOS,
    )
    ENTIDADE_MEDIACAO_ARBITRAGEM = (
        "3115",
        "Entidade de Mediação e Arbitragem",
        GrupoNaturezaJuridicaEnum.ENTIDADE_SEM_FINS_LUCRATIVOS,
    )
    PARTIDO_POLITICO = ("3123", "Partido Político", GrupoNaturezaJuridicaEnum.ENTIDADE_SEM_FINS_LUCRATIVOS)
    ENTIDADE_SINDICAL = ("3131", "Entidade Sindical", GrupoNaturezaJuridicaEnum.ENTIDADE_SEM_FINS_LUCRATIVOS)
    ESTABELECIMENTO_FUNDACAO_ASSOCIACAO_ESTRANGEIRAS = (
        "3204",
        "Estabelecimento, no Brasil, de Fundação ou Associação Estrangeiras",
        GrupoNaturezaJuridicaEnum.ENTIDADE_SEM_FINS_LUCRATIVOS,
    )
    FUNDACAO_ASSOCIACAO_EXTERIOR = (
        "3212",
        "Fundação ou Associação Domiciliada no Exterior",
        GrupoNaturezaJuridicaEnum.ENTIDADE_SEM_FINS_LUCRATIVOS,
    )
    OUTRAS_ASSOCIACOES = ("3999", "Outras Formas de Associação", GrupoNaturezaJuridicaEnum.ENTIDADE_SEM_FINS_LUCRATIVOS)
    # 4. PESSOAS FÍSICAS
    EMPRESA_INDIVIDUAL_IMOBILIARIA = ("4014", "Empresa Individual Imobiliária", GrupoNaturezaJuridicaEnum.PESSOA_FISICA)
    SEGURADO_ESPECIAL = ("4022", "Segurado Especial", GrupoNaturezaJuridicaEnum.PESSOA_FISICA)
    CONTRIBUINTE_INDIVIDUAL = ("4081", "Contribuinte individual", GrupoNaturezaJuridicaEnum.PESSOA_FISICA)
    # 5. ORGANIZAÇÕES INTERNACIONAIS E OUTRAS INSTITUIÇÕES EXTRATERRITORIAIS
    ORGANIZACAO_INTERNACIONAL = (
        "5002",
        "Organização Internacional e Outras Instituições Extraterritoriais",
        GrupoNaturezaJuridicaEnum.ORGANIZACAO_INTERNACIONAL,
    )

    def __init__(self, value: Any, description: str, grupo: GrupoNaturezaJuridica) -> None:
        super().__init__(value, description)
        self.grupo = grupo
