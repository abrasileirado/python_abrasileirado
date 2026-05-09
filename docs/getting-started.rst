Getting Started
===============

Install
-------

.. code-block:: bash

   pip install abrasileirado

Typed values
------------

The package exposes immutable typed objects for Brazilian-specific data.
Objects validate their input when created and expose both a formatted string
representation and raw digits through ``.digitos``.

.. code-block:: python

   from abrasileirado.types import CPF, CEP, EnderecoBrasil
   from abrasileirado.enums import UnidadeFederativaStrEnum

   cpf = CPF("12345678909")
   print(cpf)          # 123.456.789-09
   print(cpf.digitos)  # 12345678909

   cep = CEP("59015300")
   print(cep)          # 59015-300
   print(cep.digitos)  # 59015300

   endereco = EnderecoBrasil(
       logradouro="Rua Dr. Nilo Bezerra Ramalho",
       numero="1692",
       bairro="Tirol",
       municipio="Natal",
       uf=UnidadeFederativaStrEnum.RN,
       cep=cep,
       complemento="Sala 001",
   )
   print(endereco)

Validate without exceptions
---------------------------

All classes derived from ``CodigoValidavel`` provide ``is_valid`` for cases
where you only need a boolean result.

.. code-block:: python

   from abrasileirado.types import CPF, PIS, CertidaoRCPN

   CPF.is_valid("123.456.789-09")  # True
   CPF.is_valid("123.456.789-00")  # False

   PIS.is_valid("12044568103")  # True

   CertidaoRCPN.is_valid("123456.01.55.2024.1.00001.001.0000001-67")  # True

Available types
---------------

Core typed objects include:

* ``CEP``
* ``EnderecoBrasil``
* ``CPF``
* ``CNPJ``
* ``CNES``
* ``CNS``
* ``NUP``
* ``PIS``
* ``RENAVAM``
* ``TituloEleitoral``
* ``CertidaoRCPN``
* ``Telefone``
* ``Passaporte``
* ``PlacaVeicular``
