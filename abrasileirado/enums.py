from enum import Enum
from typing import Any

from isort import code


class IterableEnum(Enum):
    """ Enum base que permite iterar sobre seus membros e acessar suas descrições.
        Cada membro do enum pode ter um atributo 'description' que fornece uma descrição legível do membro.
        Se o atributo 'description' não estiver presente, a descrição será o valor do membro convertido para string.
    """

    def __init__(self, value: Any, description: Any = None) -> None:
        """ Inicializa o membro do enum com um valor e uma descrição opcional.
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
        """ Retorna uma lista de tuplas contendo o valor e a descrição de cada membro do enum.
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
        if getattr(cls, '__local_cache', None) is not None:
            return cls.__local_cache

        cls.__local_cache = [(x.value, getattr(x, 'description', str(x))) for x in cls]
        return cls.__local_cache


class SimNaoIntEnum(IterableEnum):
    SIM = (1, 'Sim')
    NAO = (2, 'Não')
    NAO_INFORMADO = (9, 'Não informado')


class SimNaoStrEnum(IterableEnum):
    SIM = ('S', 'Sim')
    NAO = ('N', 'Não')
    NAO_INFORMADO = ('I', 'Não informado')


class EstadoCivilEnum(IterableEnum):
    """ Enum para representar os estados civis de uma pessoa.
        Fonte: IBGE, usado no PNAD Contínua e PNS.
    """
    SOLTEIRO = (1, 'Solteiro(a)')
    CASADO = (2, 'Casado(a)')
    VIUVO = (3, 'Viúvo(a)')
    DIVORCIADO = (4, 'Divorciado(a)')
    SEPARADO = (5, 'Separado(a) judicialmente')
    UNIAO_ESTAVEL = (6, 'Desquitado')
    NAO_INFORMADO = (99, 'Não informado')


class CorRacaEnum(IterableEnum):
    """ Enum para representar as cores/raças de uma pessoa.
        Fonte: IBGE, usado no PNAD Contínua e PNS.
    """
    BRANCA = (1, 'Branca')
    PRETA = (2, 'Preta')
    PARDA = (3, 'Parda')
    AMARELA = (4, 'Amarela')
    INDIGENA = (5, 'Indígena')
    NAO_INFORMADA = (99, 'Não informada')


class SexoEnum(IterableEnum):
    """ Enum para representar os sexos de uma pessoa.
        Fonte: IBGE, usado no PNAD Contínua e PNS.
    """
    MASCULINO = (1, 'Masculino')
    FEMININO = (2, 'Feminino')
    NAO_INFORMADO = (9, 'Não informado')


class SexoStrEnum(IterableEnum):
    """ Enum para representar os sexos de uma pessoa, com valores string."""
    MASCULINO = ('M', 'Masculino')
    FEMININO = ('F', 'Feminino')
    NAO_INFORMADO = ('N', 'Não informado')


class GeneroEnum(IterableEnum):
    """ Enum para representar os gêneros de uma pessoa
        Fonte: IBGE, usado no PNAD Contínua e PNS.
    """
    MULHER_CISGENERO = (1, 'Mulher cisgênero')
    HOMEM_CISGENERO = (2, 'Homem cisgênero')
    MULHER_TRANS = (3, 'Mulher trans')
    HOMEM_TRANS = (4, 'Homem trans')
    TRAVESTI = (5, 'Travesti')
    NAO_BINARIO = (6, 'Não binário')
    OUTRO = (7, 'Outro')
    NAO_INFORMADO = (99, 'Não informado')


class DeficienciaEnum(IterableEnum):
    """ Enum para representar as deficiências de uma pessoa, com valores inteiros.
        Fonte: IBGE, usado no PNAD Contínua e PNS
    """
    VISAO = (1, 'Visão')
    AUDICAO = (2, 'Audição')
    MOBILIDADE = (3, 'Mobilidade')
    COGNICAO_COMUNICACAO = (4, 'Cognição/comunicação')
    AUTOCUIDADO = (5, 'Autocuidado')
    NAO_DECLARADO = (9, 'Não declarado')


class ZonaHabitacaoEnum(IterableEnum):
    """ Enum para representar as zonas de habitação.
        Fonte: IBGE, classificação domiciliar do Censo.
    """
    URBANA = (1, 'Urbana')
    RURAL = (2, 'Rural')
    TRANSICAO = (3, 'Área de transição')
    NAO_INFORMADA = (9, 'Não informada')


class ZonaHabitacaoStrEnum(IterableEnum):
    """ Enum para representar as zonas de habitação, em string.
        Fonte: IBGE, classificação domiciliar do Censo.
    """
    URBANA = ('U', 'Urbana')
    RURAL = ('R', 'Rural')
    TRANSICAO = ('T', 'Área de transição')
    NAO_INFORMADA = ('N', 'Não informada')


class RegiaoIntEnum(IterableEnum):
    """ Enum para representar as regiões do Brasil, com valores inteiros.
        Fonte: IBGE, usado no PNAD Contínua e PNS
    """
    NORTE = (1, 'Norte')
    NORDESTE = (2, 'Nordeste')
    SUDESTE = (3, 'Sudeste')
    SUL = (4, 'Sul')
    CENTRO_OESTE = (5, 'Centro-oeste')
    NAO_DECLARADO = (9, 'Não declarado')

    @property
    def ufs(self) -> list['UnidadeFederativaIntEnum']:
        return [uf for uf in UnidadeFederativaIntEnum if uf.region == self]


class RegiaoStrEnum(IterableEnum):
    """ Enum para representar as regiões do Brasil, com valores string.
        Fonte: IBGE, usado no PNAD Contínua e PNS
    """
    NORTE = ('N', 'Norte')
    NORDESTE = ('NE', 'Nordeste')
    SUDESTE = ('SE', 'Sudeste')
    SUL = ('S', 'Sul')
    CENTRO_OESTE = ('CO', 'Centro-oeste')
    NAO_DECLARADO = ('N', 'Não declarado')

    @property
    def ufs(self) -> list['UnidadeFederativaStrEnum']:
        return [uf for uf in UnidadeFederativaStrEnum if uf.region == self]


class UnidadeFederativaIntEnum(IterableEnum):
    """ Enum para representar as unidades federativas do Brasil, com valores inteiros.
        Fonte: IBGE, usado no PNAD Contínua e PNS
    """
    AC = (12, 'Acre', RegiaoIntEnum.NORTE)
    AL = (27, 'Alagoas', RegiaoIntEnum.NORDESTE)
    AP = (16, 'Amapá', RegiaoIntEnum.NORTE)
    AM = (13, 'Amazonas', RegiaoIntEnum.NORTE)
    BA = (29, 'Bahia', RegiaoIntEnum.NORDESTE)
    CE = (23, 'Ceará', RegiaoIntEnum.NORDESTE)
    DF = (53, 'Distrito Federal', RegiaoIntEnum.CENTRO_OESTE)
    ES = (32, 'Espírito Santo', RegiaoIntEnum.SUDESTE)
    GO = (52, 'Goiás', RegiaoIntEnum.CENTRO_OESTE)
    MA = (21, 'Maranhão', RegiaoIntEnum.NORDESTE)
    MT = (51, 'Mato Grosso', RegiaoIntEnum.CENTRO_OESTE)
    MS = (50, 'Mato Grosso do Sul', RegiaoIntEnum.CENTRO_OESTE)
    MG = (31, 'Minas Gerais', RegiaoIntEnum.SUDESTE)
    PA = (15, 'Pará', RegiaoIntEnum.NORTE)
    PB = (25, 'Paraíba', RegiaoIntEnum.NORDESTE)
    PR = (41, 'Paraná', RegiaoIntEnum.SUL)
    PE = (26, 'Pernambuco', RegiaoIntEnum.NORDESTE)
    PI = (22, 'Piauí', RegiaoIntEnum.NORDESTE)
    RJ = (33, 'Rio de Janeiro', RegiaoIntEnum.SUDESTE)
    RN = (24, 'Rio Grande do Norte', RegiaoIntEnum.NORDESTE)
    RS = (43, 'Rio Grande do Sul', RegiaoIntEnum.SUL)
    RO = (11, 'Rondônia', RegiaoIntEnum.NORTE)
    RR = (14, 'Roraima', RegiaoIntEnum.NORTE)
    SC = (42, 'Santa Catarina', RegiaoIntEnum.SUL)
    SP = (35, 'São Paulo', RegiaoIntEnum.SUDESTE)
    SE = (28, 'Sergipe', RegiaoIntEnum.NORDESTE)
    TO = (17, 'Tocantins', RegiaoIntEnum.NORTE)

    def __init__(self, value: Any, description: str, region: RegiaoIntEnum) -> None:
        super().__init__(value, description)
        self.region = region


class UnidadeFederativaStrEnum(IterableEnum):
    """ Enum para representar as unidades federativas do Brasil, com valores string.
        Fonte: IBGE, usado no PNAD Contínua e PNS
    """
    AC = ('AC', 'Acre', '12', RegiaoStrEnum.NORTE)
    AL = ('AL', 'Alagoas', '27', RegiaoStrEnum.NORDESTE)
    AP = ('AP', 'Amapá', '16', RegiaoStrEnum.NORTE)
    AM = ('AM', 'Amazonas', '13', RegiaoStrEnum.NORTE)
    BA = ('BA', 'Bahia', '29', RegiaoStrEnum.NORDESTE)
    CE = ('CE', 'Ceará', '23', RegiaoStrEnum.NORDESTE)
    DF = ('DF', 'Distrito Federal', '53', RegiaoStrEnum.CENTRO_OESTE)
    ES = ('ES', 'Espírito Santo', '32', RegiaoStrEnum.SUDESTE)
    GO = ('GO', 'Goiás', '52', RegiaoStrEnum.CENTRO_OESTE)
    MA = ('MA', 'Maranhão', '21', RegiaoStrEnum.NORDESTE)
    MT = ('MT', 'Mato Grosso', '51', RegiaoStrEnum.CENTRO_OESTE)
    MS = ('MS', 'Mato Grosso do Sul', '50', RegiaoStrEnum.CENTRO_OESTE)
    MG = ('MG', 'Minas Gerais', '31', RegiaoStrEnum.SUDESTE)
    PA = ('PA', 'Pará', '15', RegiaoStrEnum.NORTE)
    PB = ('PB', 'Paraíba', '25', RegiaoStrEnum.NORDESTE)
    PR = ('PR', 'Paraná', '41', RegiaoStrEnum.SUL)
    PE = ('PE', 'Pernambuco', '26', RegiaoStrEnum.NORDESTE)
    PI = ('PI', 'Piauí', '22', RegiaoStrEnum.NORDESTE)
    RJ = ('RJ', 'Rio de Janeiro', '33', RegiaoStrEnum.SUDESTE)
    RN = ('RN', 'Rio Grande do Norte', '24', RegiaoStrEnum.NORDESTE)
    RS = ('RS', 'Rio Grande do Sul', '43', RegiaoStrEnum.SUL)
    RO = ('RO', 'Rondônia', '11', RegiaoStrEnum.NORTE)
    RR = ('RR', 'Roraima', '14', RegiaoStrEnum.NORTE)
    SC = ('SC', 'Santa Catarina', '42', RegiaoStrEnum.SUL)
    SP = ('SP', 'São Paulo', '35', RegiaoStrEnum.SUDESTE)
    SE = ('SE', 'Sergipe', '28', RegiaoStrEnum.NORDESTE)
    TO = ('TO', 'Tocantins', '17', RegiaoStrEnum.NORTE)

    def __init__(self, value: Any, description: str, _code: str, region: RegiaoStrEnum) -> None:
        super().__init__(value, description)
        self.code = _code
        self.region = region
