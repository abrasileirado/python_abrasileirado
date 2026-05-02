import re

from abrasileirado.enums import UnidadeFederativaStrEnum


class CodigoValidavel:
    def __init__(self, code: str):
        if not self._is_valid(code):
            classname = self.__class__.__name__
            raise ValueError(f"{classname} inválido.")
        self.__clean_code: str = self._only_digits(code).zfill(self._full_digits)
        self.__masked_code: str = self._mask_code(code)

    @property
    def _full_digits(self) -> int:
        return 1

    @property
    def digitos(self) -> str:
        """Retorna apenas os dígitos do código, sem máscara."""
        return self.__clean_code

    def __str__(self) -> str:
        """Retorna o código formatado com máscara, se aplicável."""
        return self.__masked_code

    def _only_digits(self, code: str) -> str:
        """Retorna apenas os dígitos do código, sem máscara."""
        return "".join(c for c in filter(str.isdigit, code))

    def _mask_code(self, code: str) -> str:
        """Retorna o código formatado com máscara, se aplicável. Subclasses devem implementar esse método para aplicar
        a máscara específica do código.

        Arguments:
            code (str): O código a ser formatado com máscara.

        Returns:
            str: O código formatado com máscara.
        """
        return self._only_digits(code).zfill(self._full_digits)

    def _basic_digits_validation(self, code: str) -> str | None:
        """Realiza validações básicas comuns a códigos numéricos, como quantidade de dígitos, não aceitar todos os
        dígitos iguais, etc. Subclasses podem usar esse método para realizar validações básicas antes de implementar
        validações específicasadicionais, como dígitos verificadores, formato, etc.

        Arguments:
            code (str): O código a ser validado.

        Returns:
            str: O código limpo contendo apenas os dígitos, se as validações básicas forem aprovadas.
            bool: False se as validações básicas falharem.
        """
        if code is None:
            return None

        value = self._only_digits(code)

        # Não informou ou informou uma string vazia
        if value is None or value.strip() == "":
            return None

        # Com menos de 3 dígitos não é válido, mesmo que os dígitos verificadores sejam tecnicamente corretos
        if len(value.strip()) < 3 or len(value.strip()) > self._full_digits:
            return None

        # Não aceita todos os dígitos iguais
        if value == (value[0] * self._full_digits):
            return None
        return value

    def _is_valid(self, code: str) -> bool:
        """Verifica se o código é válido, realizando validações básicas como quantidade de dígitos, não aceitar todos
        os dígitos iguais, etc.
        Subclasses devem implementar validações específicas adicionais, como dígitos verificadores, formato, etc.

        Arguments:
            code (str): O código a ser validado.

        Returns:
            bool: True se o código for válido, False caso contrário.
        """
        return len(self._basic_digits_validation(code) or "") == self._full_digits


class CNES(CodigoValidavel):
    """Classe imutável para representar um CNES (Cadastro Nacional de Estabelecimento de Saúde).
    O CNES é um número de identificação utilizado para estabelecimentos de saúde no Brasil, composto por 7 dígitos.
    Essa classe valida o CNES no momento da criação, garantindo que apenas CNES válidos possam ser instanciados.
    O CNES pode ser representado tanto no formato apenas com dígitos (ex: 1234567) quanto no formato com máscara
    (ex: 1234567, sem máscara).
    Examples:
    .. code-block:: python
        cnes1 = CNES("1234567")
        print(cnes1)  # Saída: 1234567 (CNES completo, sem máscara)
        print(cnes1.digitos)  # Saída: 1234567

        # Verificando validade
        print(CNES.is_valid("1234567"))  # Saída: True
        print(CNES.is_valid("123456"))  # Saída: False (menos de 7 dígitos)
        print(CNES.is_valid("12345678"))  # Saída: False (mais de 7 dígitos)
        print(CNES.is_valid("0000000"))  # Saída: False (todos os dígitos iguais)

        # Clonando um CNES
        cnes2 = CNES(str(cnes1))
    """

    MASK = "9999999"
    REGEX = re.compile(r"^(\d{7})$")

    @property
    def _full_digits(self) -> int:
        return 7


class CNS(CodigoValidavel):
    """Classe imutável para representar um CNS (Cartão Nacional de Saúde).
    O CNS é um número de identificação utilizado para cidadãos brasileiros no sistema de saúde, composto por 15 dígitos,
    onde os 11 primeiros são a base do número e os 4 últimos são dígitos verificadores calculados a partir dos 11
    primeiros.
    Essa classe valida o CNS no momento da criação, garantindo que apenas CNS válidos possam ser instanciados.
    O CNS pode ser representado tanto no formato apenas com dígitos (ex: 123456789012345) quanto no formato com máscara
    (ex: 123 4567 8901 2345).

    Examples:
    .. code-block:: python
        cns1 = CNS("123456789012345")
        print(cns1)  # Saída: 123 4567 8901 2345 (CNS completo, DV corretos, sem máscara)
        print(cns1.digitos)  # Saída: 123456789012345

        # Verificando validade
        print(CNS.is_valid("123456789012345"))  # Saída: True
        print(CNS.is_valid("123 4567 8901 2345"))  # Saída: True
        print(CNS.is_valid("12345678901234"))  # Saída: False (menos de 15 dígitos)
        print(CNS.is_valid("1234567890123456"))  # Saída: False (mais de 15 dígitos)
        print(CNS.is_valid("000000000000000"))  # Saída: False (todos os dígitos iguais)

        # Clonando um CNS
        cns2 = CNS(str(cns1))
    """

    MASK = "999 9999 9999 9999"
    REGEX = re.compile(r"^(\d{3}) (\d{4}) (\d{4}) (\d{4})$")

    @property
    def _full_digits(self) -> int:
        return 15


class CEP(CodigoValidavel):
    """Classe para representar um CEP (Código de Endereçamento Postal) brasileiro.
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

    @property
    def _full_digits(self) -> int:
        return 8

    MASK = "99999-999"
    REGEX = r"^\d{5}-\d{3}$"

    def _mask_code(self, code: str) -> str:
        digits = self._only_digits(code)
        return f"{digits[:5]}-{digits[5:]}"


class EnderecoBrasil:
    """Classe para representar um endereço, com atributos comuns como rua, número, bairro, cidade, estado e CEP.
    Pode ser usada para representar endereços residenciais, comerciais ou de correspondência.
    Essa classe é imutável.

    Examples:
    .. code-block:: python
        endereco = EnderecoBrasil(
            logradouro="Rua das Flores",
            numero="123",
            bairro="Jardim Primavera",
            municipio="São Paulo",
            uf=UnidadeFederativaStrEnum.SP,
            cep=CEP("12345678"),
            complemento="Apto 45"
        )
        print(endereco)  # Saída: Rua das Flores 123, Apto 45\nJardim Primavera\n12345-678 São Paulo/SP
        print(endereco.extendido)  # Saída: Rua das Flores 123, Apto 45\nJardim Primavera\nSão Paulo/SP\n12345-678

    """

    def __init__(
        self,
        logradouro: str,
        numero: str,
        bairro: str,
        municipio: str,
        uf: UnidadeFederativaStrEnum,
        cep: CEP,
        complemento: str | None = None,
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
        """Retorna o endereço completo extendido da ECT."""
        endereco = f"{self.linha_logradouro}\n{self.__bairro}\n{self.__municipio}/{self.__uf.value}\n{self.__cep}"
        return endereco

    def __str__(self) -> str:
        """Retorna o endereço formatado no formato padrão da ECT."""
        endereco = f"{self.linha_logradouro}\n{self.__bairro}\n{self.__cep} {self.__municipio}/{self.__uf.value}"
        return endereco


class CPF(CodigoValidavel):
    """Classe imutável para representar um CPF (Cadastro de Pessoas Físicas).
    O CPF é um número de identificação fiscal utilizado no Brasil para pessoas físicas.
    Ele é composto por 11 dígitos, onde os 9 primeiros são a base do número e os 2 últimos são dígitos verificadores
    calculados a partir dos 9 primeiros.
    Essa classe valida o CPF no momento da criação, garantindo que apenas CPFs válidos possam ser instanciados.
    O CPF pode ser representado tanto no formato apenas com dígitos (ex: 12345678901) quanto no formato com máscara
    (ex: 123.456.789-01).

    Examples:
    .. code-block:: python
        cpf1 = CPF("12345678901")
        print(cpf1)  # Saída: 123.456.789-01 (CPF completo, DV corretos, sem máscara)
        print(cpf1.digitos)  # Saída: 12345678901

        # Verificando validade
        print(CPF.is_valid("12345678901"))  # Saída: True
        print(CPF.is_valid("123.456.789-01"))  # Saída: True
        print(CPF.is_valid("1234567890"))  # Saída: False (menos de 11 dígitos)
        print(CPF.is_valid("123456789012"))  # Saída: False (mais de 11 dígitos)
        print(CPF.is_valid("00000000000"))  # Saída: False (todos os dígitos iguais)

        # Clonando um CPF
        cpf2 = CPF(str(cpf1))
    """

    MASK = "99.999.999/9999-00"
    REGEX = re.compile(r"^(\d{2})[.-]?(\d{3})[.-]?(\d{3})/(\d{4})-(\d{2})$")

    @property
    def _full_digits(self) -> int:
        return 11

    def _mask_code(self, code: str) -> str:
        digits = self._only_digits(code).zfill(self._full_digits)
        return f"{digits[:3]}.{digits[3:6]}.{digits[6:9]}-{digits[9:]}"

    def _is_valid(self, code: str) -> bool:
        value = self._basic_digits_validation(code)
        if not value:
            return False
        v = value.zfill(self._full_digits)
        dv1 = sum([int(v[i]) * (10 - i) for i in range(0, 9)]) * 10 % 11
        dv2 = sum([int(v[i]) * (11 - i) for i in range(0, 10)]) * 10 % 11
        dv1 = dv1 if dv1 != 10 else 0
        dv2 = dv2 if dv2 != 10 else 0
        return value[-2:] == f"{dv1}{dv2}"


class CNPJ(CodigoValidavel):
    """Classe imutável para representar um CNPJ (Cadastro Nacional de Pessoa Jurídica).
    O CNPJ é um número de identificação fiscal utilizado no Brasil para pessoas jurídicas.
    Ele é composto por 14 dígitos, onde os 12 primeiros são a base do número e os 2 últimos são dígitos verificadores
    calculados a partir dos 12 primeiros.

    Essa classe valida o CNPJ no momento da criação, garantindo que apenas CNPJs válidos possam ser instanciados.
    O CNPJ pode ser representado tanto no formato apenas com dígitos (ex: 12345678900005) quanto no formato com máscara
    (ex: 12.345.678/9000-05).
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

    MASK = "99.999.999/9999-00"
    REGEX = re.compile(r"^(\d{2})[.-]?(\d{3})[.-]?(\d{3})/(\d{4})-(\d{2})$")

    @property
    def _full_digits(self) -> int:
        return 14

    def _mask_code(self, code: str) -> str:
        digits = self._only_digits(code).zfill(self._full_digits)
        return f"{digits[:2]}.{digits[2:5]}.{digits[5:8]}/{digits[8:12]}-{digits[12:]}"

    def _is_valid(self, code: str) -> bool:
        value = self._basic_digits_validation(code)
        if not value:
            return False
        v = value.zfill(self._full_digits)
        c1 = (5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2)
        c2 = (6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2)
        dv1 = sum([int(v[i]) * c1[i] for i in range(0, 12)])
        dv2 = sum([int(v[i]) * c2[i] for i in range(0, 13)])
        dv1 = 11 - dv1 % 11 if dv1 % 11 > 2 else 0
        dv2 = 11 - dv2 % 11 if dv2 % 11 > 2 else 0
        dvs = f"{dv1}{dv2}"
        return value[-2:] == dvs


class NUP(CodigoValidavel):
    """Classe imutável para representar um NUP (Número Único de Processo).
    O NUP é um número de identificação utilizado para processos judiciais e administrativos no Brasil.
    Ele é composto por 17 dígitos, tem 17 dígitos:
    - 5 para a unidade protocolizadora,
    - 6 para o sequencial anual,
    - 4 para o ano,
    - 2 para o dígito verificador.

    Essa classe valida o NUP no momento da criação, garantindo que apenas NUPs válidos possam ser instanciados.
    O NUP pode ser representado tanto no formato apenas com dígitos (ex: 23520005177202676) quanto no formato
    com máscara (ex: 23520.005177/2026-76).
    """

    MASK = "99999.999999/9999-99"
    REGEX = re.compile(r"^(\d{5})\.?(\d{6})/(\d{4})-(\d{2})$")

    @property
    def _full_digits(self) -> int:
        return 17

    def _mask_code(self, code: str) -> str:
        digits = self._only_digits(code).zfill(self._full_digits)
        return f"{digits[:5]}.{digits[5:11]}/{digits[11:15]}-{digits[15:]}"

    def _is_valid(self, code: str) -> bool:
        digits = self._only_digits(code)
        if len(digits) != 17:
            return False

        base = digits[:15]
        given_dv = digits[15:]

        def calc_dv(number: str, start_weight: int = 2) -> int:
            total = 0
            weight = start_weight
            for ch in reversed(number):
                total += int(ch) * weight
                weight += 1
            dv = 11 - (total % 11)
            return dv % 10

        dv1 = calc_dv(base, 2)
        dv2 = calc_dv(base + str(dv1), 2)

        return given_dv == f"{dv1}{dv2}"


class PIS(CodigoValidavel):
    """Classe imutável para representar um PIS (Programa de Integração Social).
    O PIS é um número de identificação utilizado para trabalhadores no Brasil,
    composto por 11 dígitos, onde os 10 primeiros são a base do número e o último é um dígito verificador
    calculado a partir dos 10 primeiros.
    Essa classe valida o PIS no momento da criação, garantindo que apenas PIS válidos possam ser instanciados.
    O PIS pode ser representado tanto no formato apenas com dígitos (ex: 12345678901) quanto no formato com
    máscara (ex: 123.45678.90-1).

    Examples:
    .. code-block:: python
        pis1 = PIS("12345678901")
        print(pis1)  # Saída: 123.45678.90-1 (PIS completo, DV correto, sem máscara)
        print(pis1.digitos)  # Saída: 12345678901

        # Verificando validade
        print(PIS.is_valid("12345678901"))  # Saída: True
        print(PIS.is_valid("123.45678.90-1"))  # Saída: True
        print(PIS.is_valid("1234567890"))  # Saída: False (menos de 11 dígitos)
        print(PIS.is_valid("123456789012"))  # Saída: False (mais de 11 dígitos)
        print(PIS.is_valid("00000000000"))  # Saída: False (todos os dígitos iguais)

        # Clonando um PIS
        pis2 = PIS(str(pis1))
    """

    MASK = "999.99999.99-9"
    REGEX = re.compile(r"^(\d{3})\.(\d{5})\.(\d{2})-(\d{1})$")

    @property
    def _full_digits(self) -> int:
        return 11

    def _mask_code(self, code: str) -> str:
        digits = self._only_digits(code).zfill(self._full_digits)
        return f"{digits[:3]} {digits[3:6]} {digits[6:9]} {digits[9:]}"


class RENAVAM(CPF):
    def _mask_code(self, code: str) -> str:
        digits = self._only_digits(code).zfill(self._full_digits)
        return f"{digits[:3]} {digits[3:6]} {digits[6:9]} {digits[9:]}"


class TituloEleitoral(CPF):
    def _mask_code(self, code: str) -> str:
        digits = self._only_digits(code).zfill(self._full_digits)
        return f"{digits[:3]} {digits[3:6]} {digits[6:9]} {digits[9:]}"


class CNJ(CPF):
    def _mask_code(self, code: str) -> str:
        digits = self._only_digits(code).zfill(self._full_digits)
        return f"{digits[:3]} {digits[3:6]} {digits[6:9]} {digits[9:]}"


class Telefone(CPF):
    def _mask_code(self, code: str) -> str:
        digits = self._only_digits(code).zfill(self._full_digits)
        return f"{digits[:3]} {digits[3:6]} {digits[6:9]} {digits[9:]}"


class Passaporte(CPF):
    def _mask_code(self, code: str) -> str:
        digits = self._only_digits(code).zfill(self._full_digits)
        return f"{digits[:3]} {digits[3:6]} {digits[6:9]} {digits[9:]}"


class PlacaVeicular(CPF):
    def _mask_code(self, code: str) -> str:
        digits = self._only_digits(code).zfill(self._full_digits)
        return f"{digits[:3]} {digits[3:6]} {digits[6:9]} {digits[9:]}"


class Certidao(CPF):
    """Classe para representar uma certidão, como certidão de nascimento, casamento, óbito, etc.
    O número da certidão tem 11 dígitos, onde os 9 primeiros são a base do número e os 2 últimos
    são dígitos verificadores calculados a partir dos 9 primeiros. Essa classe é imutável.

    Examples:
    .. code-block:: python
        certidao = Certidao("12345678900")
        print(certidao)  # Saída: 123.456.789-00 (Certidão completa, DV corretos, sem máscara)
        print(certidao.digitos)  # Saída: 12345678900

        # Verificando validade
        print(Certidao.is_valid("12345678900"))  # Saída: True
        print(Certidao.is_valid("123.456.789-00"))  # Saída: True
        print(Certidao.is_valid("12345678-900"))  # Saída: False (formato inválido)
        print(Certidao.is_valid("00000000000"))  # Saída: False (todos os dígitos iguais)

        # Clonando uma certidão
        certidao2 = Certidao(str(Certidao("12345678900")))
    """

    def _mask_code(self, code: str) -> str:
        digits = self._only_digits(code).zfill(self._full_digits)
        return f"{digits[:3]} {digits[3:6]} {digits[6:9]} {digits[9:]}"
