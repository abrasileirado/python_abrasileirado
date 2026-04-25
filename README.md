# Python BRfied

![License](https://img.shields.io/badge/License-MIT-lemon.svg)]
[![Python](https://img.shields.io/pypi/pyversions/abrasileirado.svg)](https://pypi.org/project/abrasileirado/)
[![QA](https://github.com/abrasileirado/python_abrasileirado/actions/workflows/qa.yml/badge.svg)](https://github.com/abrasileirado/python_abrasileirado/actions/workflows/qa.yml)
[![Coverage](https://codecov.io/gh/abrasileirado/python_abrasileirado/branch/main/graph/badge.svg)](https://codecov.io/gh/abrasileirado/python_abrasileirado)
[![Publish](https://github.com/abrasileirado/python_abrasileirado/actions/workflows/publish.yml/badge.svg)](https://github.com/abrasileirado/python_abrasileirado/actions/workflows/publish.yml)
[![Docs](https://github.com/abrasileirado/python_abrasileirado/actions/workflows/docs.yml/badge.svg)](https://abrasileirado.github.io/python_abrasileirado/)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)


Python library specific brazilian objects and validations.

> Why I create abrasileirado? Because **this is Brazil** (Toretto, 2020).


## Data types

* ✅ Sim/Não (Enum)
* ✅ Estado Civil (Enum) - Instituto Brasileiro de Geografia e Estatística (IBGE)
* ✅ Cor/Raça (Enum) - IBGE
* ✅ Sexo (Enum) - IBGE
* ✅ Gênero (Enum) - IBGE*
* ✅ Deficiência (Enum) - IBGE
* ✅ Zona de habitação (Enum) - IBGE
* ✅ Região geopolítica (Enum) - IBGE
* ✅ Unidade federativa (Enum) - IBGE
* ✅ CEP - Código de Endereçamento Postal - Empresa de Correio e Telegráfos (ECT)
* ✅ CNES - Cadastro Nacional de Estabelecimento de Saúde - DATASUS
* ✅ CNS - Cadastro Nacional de Saúde (Cartão SUS) - DATASUS
* ✅ CPF - Cadastro de Pessoa Física - Receita Federal do Brasil (RFB)
* ✅ CNPJ - Cadastro Nacional de Pessoa Jurídica - RFB
* 🚫 Modulo11
* 🚫 ProtocoloIntegrado
* 🚫 ProtocoloJustica
* 🚫 PJE
* 🚫 Boleto
* 🚫 NFE
* 🚫 Municipio




## Validações e formatações

* [x] validate_masked_value
* [x] validate_cpf
* [x] validate_cnpj
* [x] validate_mask
* [x] validate_mod11
* [x] validate_dv_by_mask
* [ ] CEP
* [ ] Data
* [ ] Hora
* [ ] Data e hora
* [ ] CNES
* [ ] CNS
* [ ] Protocolo integrado (https://protocolointegrado.gov.br/Protocolo/projeto.jsf)
* [ ] Protocolo justiça (https://www.conjur.com.br/2009-jan-23/cnj-define-padrao-numeracao-processos-todos-tribunais http://www.stf.jus.br/portal/cms/verTexto.asp?servico=processoPeticaoEletronica&pagina=Informacoes_gerais_apos_desligamento_v1)
* [ ] PJe
* [ ] Linha digitável de boleto
* [ ] Código de barra de boleto
* [ ] Linha digitável de título
* [ ] Código de barra de título
* [ ] Nota fiscal eletrônica
* [ ] Código de município do IBGE (https://github.com/chinnonsantos/sql-paises-estados-cidades https://concla.ibge.gov.br/classificacoes/por-tema/codigo-de-areas/codigo-de-areas)
* [ ]  is_only_digits
* [ ]  apply_mask
