# AGENTS.md

## Ambiente

- Este projeto usa o virtualenv local em `.venv`.
- Para rodar testes, use:

```powershell
.\.venv\Scripts\python.exe -m pytest
```

- Para rodar testes com cobertura, use:

```powershell
.\.venv\Scripts\python.exe -m pytest --cov=abrasileirado --cov-report=term-missing --cov-report=xml
```
