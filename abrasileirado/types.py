import re

from abrasileirado.enums import TipoLivroRcpnEnum, UnidadeFederativaStrEnum


class CodigoValidavel:
    """Classe base para códigos brasileiros validáveis.

    A classe centraliza normalização de dígitos, representação mascarada, igualdade por valor e validação básica.
    Subclasses devem definir o tamanho total esperado e, quando necessário, implementar máscara e regras específicas
    da autoridade responsável pelo padrão.

    Examples:
    .. code-block:: python
        class CodigoSempreValido(CodigoValidavel):
            def _is_valid(self, code: str) -> bool:
                return True

        codigo = CodigoSempreValido("1")
        print(codigo)  # Saída: 1
        print(codigo.digitos)  # Saída: 1
    """

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

    def __eq__(self, other: object) -> bool:
        if other.__class__ is not self.__class__:
            return NotImplemented
        return self.digitos == other.digitos

    def __hash__(self) -> int:
        return hash((self.__class__, self.digitos))

    @classmethod
    def is_valid(cls, code: str) -> bool:
        try:
            cls(code)
        except ValueError:
            return False
        return True

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


class CEP(CodigoValidavel):
    """Classe imutável para representar um CEP (Código de Endereçamento Postal).

    O CEP é um código numérico de 8 dígitos usado para identificar áreas de entrega no Brasil.
    O padrão é definido e utilizado pela Empresa Brasileira de Correios e Telégrafos (ECT).
    A classe aceita o valor com ou sem máscara e normaliza a saída no formato 99999-999.

    Examples:
    .. code-block:: python
        cep1 = CEP("59015300")
        print(cep1)  # Saída: 59015-300
        print(cep1.digitos)  # Saída: 59015300

        cep2 = CEP("59015-300")
        print(cep2)  # Saída: 59015-300
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
    """Classe imutável para representar um endereço postal brasileiro.

    O endereço reúne logradouro, número, bairro, município, UF, CEP e complemento opcional.
    A saída segue formatos postais usados pela Empresa Brasileira de Correios e Telégrafos (ECT).

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
        print(endereco.ect_extendido)  # Saída: Rua das Flores 123, Apto 45\nJardim Primavera\nSão Paulo/SP\n12345-678
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
    def logradouro(self) -> str:
        return self.__logradouro

    @property
    def numero(self) -> str:
        return self.__numero

    @property
    def bairro(self) -> str:
        return self.__bairro

    @property
    def municipio(self) -> str:
        return self.__municipio

    @property
    def uf(self) -> UnidadeFederativaStrEnum:
        return self.__uf

    @property
    def cep(self) -> CEP:
        return self.__cep

    @property
    def complemento(self) -> str | None:
        return self.__complemento

    @property
    def ect_extendido(self) -> str:
        """Retorna o endereço completo extendido da ECT."""
        return f"{self.linha_logradouro}\n{self.__bairro}\n{self.__municipio}/{self.__uf.value}\n{self.__cep}"

    @property
    def ect_padrao(self) -> str:
        """Retorna o endereço formatado no formato padrão da ECT."""
        return f"{self.linha_logradouro}\n{self.__bairro}\n{self.__cep} {self.__municipio}/{self.__uf.value}"

    def __str__(self) -> str:
        return self.ect_padrao

    def __eq__(self, other: object) -> bool:
        if other.__class__ is not self.__class__:
            return NotImplemented
        return (
            self.logradouro,
            self.numero,
            self.bairro,
            self.municipio,
            self.uf,
            self.cep,
            self.complemento,
        ) == (
            other.logradouro,
            other.numero,
            other.bairro,
            other.municipio,
            other.uf,
            other.cep,
            other.complemento,
        )

    def __hash__(self) -> int:
        return hash(
            (
                self.__class__,
                self.logradouro,
                self.numero,
                self.bairro,
                self.municipio,
                self.uf,
                self.cep,
                self.complemento,
            )
        )


class CPF(CodigoValidavel):
    """Classe imutável para representar um CPF (Cadastro de Pessoas Físicas).

    O CPF é um número de identificação fiscal utilizado no Brasil para pessoas físicas.
    Ele é composto por 11 dígitos, onde os 9 primeiros são a base do número e os 2 últimos são dígitos verificadores
    calculados a partir dos 9 primeiros.
    O padrão é definido pela Receita Federal do Brasil (RFB).
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
    O padrão é definido pela Receita Federal do Brasil (RFB).
    Essa classe valida o CNPJ no momento da criação, garantindo que apenas CNPJs válidos possam ser instanciados.
    O CNPJ pode ser representado tanto no formato apenas com dígitos (ex: 12345678900005) quanto no formato com máscara
    (ex: 12.345.678/9000-05).

    Examples:
    .. code-block:: python
        cnpj = CNPJ("12345678900005")
        print(cnpj)  # Saída: 12.345.678/9000-05
        print(cnpj.digitos)  # Saída: 12345678900005

        cnpj2 = CNPJ("12.345.678/9000-05")
        print(cnpj2)  # Saída: 12.345.678/9000-05
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


class CNES(CodigoValidavel):
    """Classe imutável para representar um CNES (Cadastro Nacional de Estabelecimento de Saúde).

    O CNES é um número de identificação utilizado para estabelecimentos de saúde no Brasil.
    O cadastro é mantido pelo Ministério da Saúde/DATASUS.
    A classe representa o código numérico de 7 dígitos sem máscara.

    Examples:
    .. code-block:: python
        cnes = CNES("2079305")
        print(cnes)  # Saída: 2079305
        print(cnes.digitos)  # Saída: 2079305
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
    O padrão é utilizado pelo Sistema Único de Saúde (SUS), sob gestão do Ministério da Saúde/DATASUS.
    A classe representa o código numérico sem máscara.

    Examples:
    .. code-block:: python
        cns = CNS("898001160444648")
        print(cns)  # Saída: 898001160444648
        print(cns.digitos)  # Saída: 898001160444648
    """

    MASK = "999 9999 9999 9999"
    REGEX = re.compile(r"^(\d{3}) (\d{4}) (\d{4}) (\d{4})$")

    @property
    def _full_digits(self) -> int:
        return 15

    def _is_valid(self, code: str) -> bool:
        digits = self._basic_digits_validation(code)
        if not digits or len(digits) != self._full_digits:
            return False

        if digits[0] in ("1", "2"):
            base = digits[:11]
            total = sum(int(digit) * weight for digit, weight in zip(base, range(15, 4, -1)))
            dv = 11 - (total % 11)
            dv = 0 if dv == 11 else dv

            if dv == 10:
                total += 2
                dv = 11 - (total % 11)
                expected = f"{base}001{dv}"
            else:
                expected = f"{base}000{dv}"

            return digits == expected

        if digits[0] in ("7", "8", "9"):
            total = sum(int(digit) * weight for digit, weight in zip(digits, range(15, 0, -1)))
            return total % 11 == 0

        return False


class NUP(CodigoValidavel):
    """Classe imutável para representar um NUP (Número Único de Processo).

    O NUP é um número de identificação utilizado para processos judiciais e administrativos no Brasil.
    O padrão é usado pelo Conselho Nacional de Justiça (CNJ) e pela Administração Pública para protocolo e tramitação.
    Ele é composto por 17 dígitos:

    - 5 para a unidade protocolizadora,
    - 6 para o sequencial anual,
    - 4 para o ano,
    - 2 para o dígito verificador.

    Examples:
    .. code-block:: python
        nup = NUP("23520005177202676")
        print(nup)  # Saída: 23520.005177/2026-76
        print(nup.digitos)  # Saída: 23520005177202676

        nup2 = NUP("23520.005177/2026-76")
        print(nup2)  # Saída: 23520.005177/2026-76
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

    O PIS é um número de identificação utilizado para trabalhadores no Brasil.
    O cadastro é associado a políticas trabalhistas e sociais do Governo Federal.
    A classe representa o código de 11 dígitos e normaliza a saída em grupos.

    Examples:
    .. code-block:: python
        pis = PIS("12044568103")
        print(pis)  # Saída: 120 445 681 03
        print(pis.digitos)  # Saída: 12044568103
    """

    MASK = "999.99999.99-9"
    REGEX = re.compile(r"^(\d{3})\.(\d{5})\.(\d{2})-(\d{1})$")

    @property
    def _full_digits(self) -> int:
        return 11

    def _mask_code(self, code: str) -> str:
        digits = self._only_digits(code).zfill(self._full_digits)
        return f"{digits[:3]} {digits[3:6]} {digits[6:9]} {digits[9:]}"

    def _is_valid(self, code: str) -> bool:
        digits = self._basic_digits_validation(code)
        if not digits or len(digits) != self._full_digits:
            return False

        weights = (3, 2, 9, 8, 7, 6, 5, 4, 3, 2)
        dv = 11 - (sum(int(digit) * weight for digit, weight in zip(digits[:10], weights)) % 11)
        dv = 0 if dv in (10, 11) else dv
        return digits[-1] == str(dv)


class RENAVAM(CodigoValidavel):
    """Classe imutável para representar um RENAVAM.

    O RENAVAM é o Registro Nacional de Veículos Automotores, usado para identificar veículos no Brasil.
    O padrão é mantido pela Secretaria Nacional de Trânsito (Senatran).
    A classe representa o código numérico de 11 dígitos e valida seu dígito verificador.

    Examples:
    .. code-block:: python
        renavam = RENAVAM("63988496249")
        print(renavam)  # Saída: 63988496249
        print(renavam.digitos)  # Saída: 63988496249
    """

    MASK = "99999999999"
    REGEX = re.compile(r"^\d{11}$")

    @property
    def _full_digits(self) -> int:
        return 11

    def _mask_code(self, code: str) -> str:
        digits = self._only_digits(code).zfill(self._full_digits)
        return digits

    def _is_valid(self, code: str) -> bool:
        digits = self._basic_digits_validation(code)
        if not digits or len(digits) != self._full_digits or not self.REGEX.fullmatch(digits):
            return False
        weights = (3, 2, 9, 8, 7, 6, 5, 4, 3, 2)
        dv = 11 - (sum(int(digit) * weight for digit, weight in zip(digits[:10], weights)) % 11)
        dv = 0 if dv >= 10 else dv
        return digits[-1] == str(dv)


class TituloEleitoral(CodigoValidavel):
    """Classe imutável para representar um Título Eleitoral.

    O Título Eleitoral identifica pessoas aptas ao cadastro eleitoral brasileiro.
    O padrão é definido pela Justiça Eleitoral, sob responsabilidade do Tribunal Superior Eleitoral (TSE).
    A classe representa o código numérico de 12 dígitos e valida seus dígitos verificadores.

    Examples:
    .. code-block:: python
        titulo = TituloEleitoral("123456780191")
        print(titulo)  # Saída: 123456780191
        print(titulo.digitos)  # Saída: 123456780191
    """

    MASK = "999999999999"
    REGEX = re.compile(r"^\d{12}$")

    @property
    def _full_digits(self) -> int:
        return 12

    def _mask_code(self, code: str) -> str:
        digits = self._only_digits(code).zfill(self._full_digits)
        return digits

    def _is_valid(self, code: str) -> bool:
        digits = self._basic_digits_validation(code)
        if not digits or len(digits) != self._full_digits or not self.REGEX.fullmatch(digits):
            return False

        if digits[8:10] not in {f"{uf:02d}" for uf in range(1, 12)} | {"99"}:
            return False

        dv1 = sum(int(digit) * weight for digit, weight in zip(digits[:8], range(2, 10))) % 11
        dv1 = 0 if dv1 == 10 else dv1
        dv2 = sum(int(digit) * weight for digit, weight in zip(digits[8:10] + str(dv1), range(7, 10))) % 11
        dv2 = 0 if dv2 == 10 else dv2
        return digits[-2:] == f"{dv1}{dv2}"


class CertidaoRCPN(CodigoValidavel):
    """Classe imutável para representar uma certidão RCPN.

    A matrícula RCPN identifica certidões do Registro Civil das Pessoas Naturais.
    O padrão é regulado pelo Conselho Nacional de Justiça (CNJ) e usa 32 dígitos, incluindo códigos de serventia,
    acervo, tipo de livro, livro, folha, termo e dígitos verificadores.

    Examples:
    .. code-block:: python
        certidao = CertidaoRCPN("12345601552024100001001000000167")
        print(certidao)  # Saída: 123456.01.55.2024.1.00001.001.0000001-67
        print(certidao.digitos)  # Saída: 12345601552024100001001000000167
        print(certidao.tipo_livro.description)  # Saída: Nascimento
    """

    MASK = "999999.99.99.9999.9.99999.999.9999999-00"
    REGEX = rcpn_pattern = re.compile(
        r"^\d{6}"  # Código Nacional da Serventia (6 dígitos)
        r"(0[1-9]|[1-9]\d)"  # Código do acervo (07-08: 01-99)
        r"55"  # Código fixo RCPN (09-10)
        r"\d{4}"  # Ano (11-14: ex. 2009-2026)
        r"[1-7]"  # Tipo de livro (15: 1 a 7)
        r"\d{5}"  # Número do livro (16-20: 00000-99999)
        r"\d{3}"  # Folha (21-23: 001-999)
        r"\d{7}"  # Termo (24-30: 0000001-9999999)
        r"\d{2}$"  # Dígitos verificadores (31-32)
    )

    @property
    def _full_digits(self) -> int:
        return 32

    def _mask_code(self, code: str) -> str:
        digits = self._only_digits(code).zfill(self._full_digits)
        return (
            f"{digits[:6]}.{digits[6:8]}.{digits[8:10]}.{digits[10:14]}.{digits[14]}."
            f"{digits[15:20]}.{digits[20:23]}.{digits[23:30]}-{digits[30:]}"
        )

    def _is_valid(self, code: str) -> bool:
        if code is None:
            return False

        digits = self._only_digits(code)
        if len(digits) != self._full_digits:
            return False

        return bool(self.REGEX.fullmatch(digits)) and int(digits) % 97 == 1

    @property
    def codigo_serventia(self) -> str:
        """1º ao 6º: Código da Serventia (Cartório)."""
        return self.digitos[:6]

    @property
    def codigo_acervo(self) -> str:
        """7º e 8º: Código do Acervo."""
        return self.digitos[6:8]

    @property
    def registro_civil(self) -> str:
        """9º e 10º: Registro Civil."""
        return self.digitos[8:10]

    @property
    def ano_registro(self) -> str:
        """11º ao 14º: Ano do registro."""
        return self.digitos[10:14]

    @property
    def tipo_livro(self) -> TipoLivroRcpnEnum:
        """15º: Tipo de Livro."""
        codigo = int(self.digitos[14])
        return next(tipo_livro for tipo_livro in TipoLivroRcpnEnum if tipo_livro.value == codigo)

    @property
    def numero_livro(self) -> str:
        """16º ao 20º: Número do Livro."""
        return self.digitos[15:20]

    @property
    def numero_folha(self) -> str:
        """21º ao 23º: Número da Folha."""
        return self.digitos[20:23]

    @property
    def numero_termo(self) -> str:
        """24º ao 30º: Número do Termo."""
        return self.digitos[23:30]

    @property
    def dv(self) -> str:
        """31º e 32º: Dígitos Verificadores."""
        return self.digitos[30:]


class Telefone(CodigoValidavel):
    """Classe imutável para representar um telefone brasileiro.

    O telefone é representado com DDD de 2 dígitos e número de 9 dígitos.
    A numeração telefônica brasileira é regulada pela Agência Nacional de Telecomunicações (Anatel).
    A classe normaliza a saída no formato (99) 99999-9999.

    Examples:
    .. code-block:: python
        telefone = Telefone("(84) 98765-4321")
        print(telefone)  # Saída: (84) 98765-4321
        print(telefone.digitos)  # Saída: 84987654321
    """

    MASK = "(99) 99999-9999"
    REGEX = re.compile(r"^\(?[1-9]{2}\)? ?9?\d{4}-?\d{4}$")

    @property
    def _full_digits(self) -> int:
        return 11

    def _mask_code(self, code: str) -> str:
        digits = self._only_digits(code).zfill(self._full_digits)
        return f"({digits[:2]}) {digits[2:7]}-{digits[7:]}"

    def _is_valid(self, code: str) -> bool:
        digits = self._basic_digits_validation(code)
        return bool(digits and len(digits) == self._full_digits and self.REGEX.fullmatch(code))


class Passaporte(CodigoValidavel):
    """Classe imutável para representar um passaporte brasileiro.

    O passaporte é um documento de viagem emitido pela Polícia Federal.
    Nesta classe, o código é representado como uma sequência numérica de 8 dígitos.

    Examples:
    .. code-block:: python
        passaporte = Passaporte("12345678")
        print(passaporte)  # Saída: 12345678
        print(passaporte.digitos)  # Saída: 12345678
    """

    MASK = "99999999"
    REGEX = re.compile(r"^\d{8}$")

    @property
    def _full_digits(self) -> int:
        return 8

    def _mask_code(self, code: str) -> str:
        return self._only_digits(code).zfill(self._full_digits)

    def _is_valid(self, code: str) -> bool:
        digits = self._basic_digits_validation(code)
        return bool(digits and len(digits) == self._full_digits and self.REGEX.fullmatch(digits))


class PlacaVeicular(CodigoValidavel):
    """Classe imutável para representar uma placa veicular.

    A placa veicular identifica veículos automotores no Brasil.
    O padrão de emplacamento é definido pelo Conselho Nacional de Trânsito (CONTRAN) e operacionalizado pelo
    Sistema Nacional de Trânsito.
    Nesta classe, a placa é representada como uma sequência numérica de 7 dígitos.

    Examples:
    .. code-block:: python
        placa = PlacaVeicular("1234567")
        print(placa)  # Saída: 1234567
        print(placa.digitos)  # Saída: 1234567
    """

    MASK = "9999999"
    REGEX = re.compile(r"^\d{7}$")

    @property
    def _full_digits(self) -> int:
        return 7

    def _mask_code(self, code: str) -> str:
        return self._only_digits(code).zfill(self._full_digits)

    def _is_valid(self, code: str) -> bool:
        digits = self._basic_digits_validation(code)
        return bool(digits and len(digits) == self._full_digits and self.REGEX.fullmatch(digits))
