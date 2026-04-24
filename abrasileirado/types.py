import re
from abrasileirado.enums import UnidadeFederativaStrEnum


class CodigoValidavel:
    """ Classe base para representar códigos que podem ser validados, como CPF, CNPJ, CEP, etc.
        Essa classe é imutável e serve como base para outras classes de tipos específicos.
        Subclasses devem implementar o método is_valid para validar o código específico.

        Attributes:
            __clean_code (str): O código limpo, contendo apenas os dígitos.
            __masked_code (str): O código formatado com máscara, se aplicável.

        Methods:
            digitos: Retorna apenas os dígitos do código, sem máscara.
            __str__: Retorna o código formatado com máscara.
            is_valid: Método de classe que deve ser implementado pelas subclasses para validar o código específico.
            __only_digits: Método de classe que retorna apenas os dígitos do código, sem máscara.
        """

    __full_digits = 1  # Deve ser definido pelas subclasses para indicar o nº total de dígitos esperados (sem máscara)

    def __init__(self, code: str):
        if not self.is_valid(code):
            classname = self.__class__.__name__
            raise ValueError(f"{classname} inválido: O {classname} tem que ser válido.")
        self.__clean_code: str = self.__only_digits(code).zfill(self.__full_digits)
        self.__masked_code: str = self.__mask_code(code)

    @property
    def digitos(self) -> str:
        """ Retorna apenas os dígitos do código, sem máscara. """
        return self.__clean_code

    def __str__(self) -> str:
        """ Retorna o código formatado com máscara, se aplicável. """
        return self.__masked_code

    @classmethod
    def __only_digits(cls, code: str) -> str:
        """ Retorna apenas os dígitos do código, sem máscara. """
        return ''.join(c for c in filter(str.isdigit, code))

    @classmethod
    def __mask_code(cls, code: str) -> str:
        """ Retorna o código formatado com máscara, se aplicável. Subclasses devem implementar esse método para aplicar 
            a máscara específica do código.

            Arguments:
                code (str): O código a ser formatado com máscara.

            Returns:
                str: O código formatado com máscara.
        """
        return cls.__only_digits(code).zfill(cls.__full_digits)

    @classmethod
    def _basic_digits_validation(cls, code: str) -> str | None:
        """ Realiza validações básicas comuns a códigos numéricos, como quantidade de dígitos, não aceitar todos os dígitos iguais, etc.
            Subclasses podem usar esse método para realizar validações básicas antes de implementar validações específicas adicionais, como dígitos verificadores, formato, etc.

            Arguments:
                code (str): O código a ser validado.

            Returns:
                str: O código limpo contendo apenas os dígitos, se as validações básicas forem aprovadas.
                bool: False se as validações básicas falharem.
        """
        value = cls.__only_digits(code)

        # Não informou ou informou uma string vazia
        if value is None or value.strip() == '':
            return None

        # Com menos de 3 dígitos não é válido, mesmo que os dígitos verificadores sejam tecnicamente corretos
        if len(value.strip()) < 3 or len(value.strip()) > cls.__full_digits:
            return None

        # Não aceita todos os dígitos iguais
        if value == (value[0] * cls.__full_digits):
            return None
        return value

    @classmethod
    def is_valid(cls, code: str) -> bool:
        """ Verifica se o código é válido, realizando validações básicas como quantidade de dígitos, não aceitar todos os dígitos iguais, etc.
            Subclasses devem implementar validações específicas adicionais, como dígitos verificadores, formato, etc.

            Arguments:
                code (str): O código a ser validado.

            Returns:
                bool: True se o código for válido, False caso contrário.
        """
        return len(cls._basic_digits_validation(code) or "") == cls.__full_digits


class CNES(CodigoValidavel):
    """Classe imutável para representar um CNES (Cadastro Nacional de Estabelecimento de Saúde)."""
    __full_digits = 7


class CNS(CodigoValidavel):
    """Classe imutável para representar um CNS (Cartão Nacional de Saúde)."""
    __full_digits = 15


class CEP(CodigoValidavel):
    """ Classe para representar um CEP (Código de Endereçamento Postal) brasileiro.
        O CEP é um código numérico de 8 dígitos que identifica uma área geográfica
        específica no Brasil, usado para facilitar a entrega de correspondências e encomendas.
        Essa classe é imutável.

        Examples:
        .. code-block:: python
            cep1 = CEP("12345678")
            print(cep1)  # Saída: 12345-678
            print(cep1.digitos)  # Saída: 12345678

            # Verificando validade
            print(CEP.is_valid("12345678"))  # Saída: True
            print(CEP.is_valid("12345-678"))  # Saída: True
            print(CEP.is_valid("1234-5678"))  # Saída: True
            print(CEP.is_valid("12.345-678"))  # Saída: True
            print(CEP.is_valid("12345"))  # Saída: False

            # Clonando um CEP
            cep2 = CEP(str(cep1))
            print(cep2)  # Saída: 12345-678
    """

    __full_digits = 8

    MASK = '99999-999'
    REGEX = r'^\d{5}-\d{3}$'

    @classmethod
    def __mask_code(cls, code: str) -> str:
        digits = cls.__only_digits(code)
        return f"{digits[:5]}-{digits[5:]}"


class EnderecoBrasil:
    """ Classe para representar um endereço, com atributos comuns como rua, número, bairro, cidade, estado e CEP.
        Pode ser usada para representar endereços residenciais, comerciais ou de correspondência.
        Essa classe é imutável.
    """
    def __init__(
        self,
        logradouro: str,
        numero: str,
        bairro: str,
        municipio: str,
        uf: UnidadeFederativaStrEnum,
        cep: CEP,
        complemento: str|None = None
    ):
        self.__logradouro = logradouro
        self.__numero = numero
        self.__bairro = bairro
        self.__municipio = municipio
        self.__uf = uf
        self.__cep = cep
        self.__complemento = complemento

    @property
    def linha_logradouro(self) -> str:
        _complemento = f", {self.__complemento}" if self.__complemento else ""
        return f"{self.__logradouro} {self.__numero}{_complemento}"

    @property
    def extendido(self) -> str:
        """ Retorna o endereço completo extendido da ECT."""
        endereco = f"{self.linha_logradouro}\n{self.__bairro}\n{self.__municipio}/{self.__uf.value}\n{self.__cep}"
        return endereco

    def __str__(self) -> str:
        """ Retorna o endereço formatado no formato padrão da ECT."""
        endereco = f"{self.linha_logradouro}\n{self.__bairro}\n{self.__cep} {self.__municipio}/{self.__uf.value}"
        return endereco


class CPF(CodigoValidavel):
    """ Classe imutável para representar um CPF (Cadastro de Pessoa Física).
        O CPF é um número de identificação fiscal utilizado no Brasil para pessoas físicas.
        Ele é composto por 11 dígitos, onde os 9 primeiros são a base do número e os 2 últimos são dígitos verificadores calculados a partir dos 9 primeiros.
        Essa classe valida o CPF no momento da criação, garantindo que apenas CPFs válidos possam ser instanciados.
        O CPF pode ser representado tanto no formato apenas com dígitos (ex: 12345678909) quanto no formato com máscara (ex: 123.456.789-09).

        Examples:

        .. code-block:: python
            print(CPF("00000000191"))  # Saída: 000.000.001-91 (CPF completo, DV corretos, sem máscara)
            print(CPF("000.000.001-91"))  # Saída: 000.000.001-91 (CPF completo, DV corretos, máscara perfeita)
            print(CPF("191"))  # Saída: 000.000.191-00 (CPF parcial, DV corretos, sem máscara)
            print(CPF("1-91").apenas_digitos)  # Saída: 0000000191 (CPF parcial, DV corretos, máscara imperfeita)

            # Verificando validade (True)
            print(CPF.is_valid("00000000191")) # CPF válido, DV corretos, sem máscara
            print(CPF.is_valid("000.000.001-91")) # CPF válido, DV corretos, com máscara perfeita
            print(CPF.is_valid("000000001-91")) # CPF válido, DV corretos, máscara imperfeita
            print(CPF.is_valid("191")) # CPF parcial, 3 dígitos, DV corretos, máscara imperfeita

            # Verificando validade (False)
            print(CPF.is_valid("11111111111")) # CPF com todos os dígitos iguais é inválido
            print(CPF.is_valid("1")) # CPF com menos de 3 dígitos é inválido
            print(CPF.is_valid("123"))  # CPF parcial, 3 dígitos, DV inválidos

            # Clonando um CPF
            cpf2 = CPF(str(CPF("12345678909")))
    """

    __full_digits = 11

    MASK = '999.999.999-00'
    REGEX = re.compile(r'^(\d{3})\.(\d{3})\.(\d{3})-(\d{2})$')

    @classmethod
    def __mask_code(cls, code: str) -> str:
        digits = cls.__only_digits(code).zfill(cls.__full_digits)
        return f"{digits[:3]}.{digits[3:6]}.{digits[6:9]}-{digits[9:]}"

    @classmethod
    def is_valid(cls, code: str):
        value = cls._basic_digits_validation(code)
        if not value:
            return False
        v = value.zfill(cls.__full_digits)
        dv1 = sum([int(v[i]) * (10-i) for i in range(0, 9)]) * 10 % 11
        dv2 = sum([int(v[i]) * (11-i) for i in range(0, 10)]) * 10 % 11
        dv1 = dv1 if dv1 != 10 else 0
        dv2 = dv2 if dv2 != 10 else 0
        return value[-2:] == f"{dv1}{dv2}"


class CNPJ(CodigoValidavel):
    """ Classe imutável para representar um CNPJ (Cadastro Nacional de Pessoa Jurídica).
        O CNPJ é um número de identificação fiscal utilizado no Brasil para pessoas jurídicas.
        Ele é composto por 14 dígitos, onde os 12 primeiros são a base do número e os 2 últimos são dígitos verificadores calculados a partir dos 12 primeiros.

        Essa classe valida o CNPJ no momento da criação, garantindo que apenas CNPJs válidos possam ser instanciados.
        O CNPJ pode ser representado tanto no formato apenas com dígitos (ex: 12345678900005) quanto no formato com máscara (ex: 12.345.678/9000-05).
        Examples:
        .. code-block:: python
            print(CNPJ("12345678900005"))  # Saída: 12.345.678/9000-05 (CNPJ completo, DV corretos, sem máscara)
            print(CNPJ("12.345.678/9000-05"))  # Saída: 12.345.678/9000-05 (CNPJ completo, DV corretos, máscara perfeita)
            print(CNPJ("12345678/9000-05"))  # Saída: 00.000.000/1234-56 (CNPJ parcial, DV corretos, máscara imperfeita)

            # Verificando validade (True)
            print(CNPJ.is_valid("12345678900005"))  # CNPJ válido, DV corretos, sem máscara
            print(CNPJ.is_valid("12.345.678/9000-05"))  # CNPJ válido, DV corretos, com máscara perfeita
            print(CNPJ.is_valid("12345678/9000-05"))  # CNPJ parcial, DV corretos, máscara imperfeita
            print(CNPJ.is_valid("00000000000108"))  # CNPJ válido, DV corretos, sem máscara, com zeros à esquerda

            # Verificando validade (False)
            print(CNPJ.is_valid("12345678900000"))  # CNPJ com DVs incorretos
            print(CNPJ.is_valid("1234567890000"))  # CNPJ com menos de 14 dígitos
            print(CNPJ.is_valid("123456789000000"))  # CNPJ com mais de 14 dígitos
            print(CNPJ.is_valid("00.000.000/0000-00"))  # CNPJ com todos os dígitos iguais é inválido

            # Clonando um CNPJ
            cnpj2 = CNPJ(str(CNPJ("12345678900005")))
        """ 

    __full_digits = 14

    MASK = '99.999.999/9999-00'
    REGEX = re.compile('^(\d{2})[.-]?(\d{3})[.-]?(\d{3})/(\d{4})-(\d{2})$')

    @classmethod
    def __mask_code(cls, code: str) -> str:
        digits = cls.__only_digits(code).zfill(cls.__full_digits)
        return f"{digits[:2]}.{digits[2:5]}.{digits[5:8]}/{digits[8:12]}-{digits[12:]}"

    @classmethod
    def is_valid(cls, code: str) -> bool:
        value = cls._basic_digits_validation(code)
        if not value:
            return False
        v = value.zfill(cls.__full_digits)
        c1 = (5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2)
        c2 = (6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2)
        dv1 = sum([int(v[i]) * c1[i] for i in range(0, 12)])
        dv2 = sum([int(v[i]) * c2[i] for i in range(0, 13)])
        dv1 = 11 - dv1 % 11 if dv1 % 11 > 2 else 0
        dv2 = 11 - dv2 % 11 if dv2 % 11 > 2 else 0
        dvs = f"{dv1}{dv2}"
        return value[-2:] == dvs
