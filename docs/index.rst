Home
====

Python library specific brazilian objects and validations.

.. image:: https://img.shields.io/badge/GitHub-Repository-blue?logo=github
   :target: https://github.com/abrasileirado/python_abrasileirado
   :alt: GitHub Repository

.. image:: https://img.shields.io/badge/License-MIT-lemon.svg
   :target: https://opensource.org/licenses/MIT
   :alt: License

.. image:: https://img.shields.io/pypi/pyversions/abrasileirado.svg
   :target: https://pypi.org/project/abrasileirado/
   :alt: Python

.. image:: https://github.com/abrasileirado/python_abrasileirado/actions/workflows/qa.yml/badge.svg
   :target: https://github.com/abrasileirado/python_abrasileirado/actions/workflows/qa.yml
   :alt: QA

.. image:: https://codecov.io/gh/abrasileirado/python_abrasileirado/branch/main/graph/badge.svg
   :target: https://codecov.io/gh/abrasileirado/python_abrasileirado
   :alt: Coverage

.. image:: https://github.com/abrasileirado/python_abrasileirado/actions/workflows/publish.yml/badge.svg
   :target: https://github.com/abrasileirado/python_abrasileirado/actions/workflows/publish.yml
   :alt: Publish

.. image:: https://github.com/abrasileirado/python_abrasileirado/actions/workflows/docs.yml/badge.svg
   :target: https://abrasileirado.github.io/python_abrasileirado/
   :alt: Docs

.. image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit
   :target: https://github.com/pre-commit/pre-commit
   :alt: pre-commit


> Why I create abrasileirado? Because **this is Brazil** (Toretto, 2020).

> Why are classes, properties, and methods in Portuguese? (Toretto, 2020) already answered.


Compare with others packages
----------------------------

There are several Python packages for Brazilian data validation and utilities. Here’s how **abrasileirado** compares to some popular alternatives:

====================  ==================  ==================  ==================  ==================
Feature               abrasileirado       validate-docbr      pycpfcnpj           brutils
====================  ==================  ==================  ==================  ==================
CPF validation        Yes                 Yes                 Yes                 Yes
CNPJ validation       Yes                 Yes                 Yes                 Yes
Other docs (RG, CNH)  Yes                 Yes                 No                  Yes
Enums/types           Yes                 No                  No                  No
Typed objects         Yes                 No                  No                  No
Date/time support     Yes                 No                  No                  No
File parsing          Yes                 No                  No                  No
Serialization         Yes                 No                  No                  No
Test coverage         100%                Unknown             Unknown             Unknown
Python 3.10+          Yes                 Yes                 Yes                 Yes
====================  ==================  ==================  ==================  ==================

**abrasileirado** focuses on typed objects, enums, and validations for Brazilian-specific data, while others are more focused on document validation only.

Features
--------

- Typed objects for CPF, CNPJ, RG, CNH, and Brazilian addresses.
- Enums for Brazilian states, genders, and zones of habitation.

Installation
------------

.. code-block:: bash
   pip install abrasileirado

Requires Python 3.10+.

Quick example
-------------

To do

.. toctree::
   :maxdepth: 1

   getting-started
   contribute
   abrasileirado
