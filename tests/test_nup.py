import pytest
from abrasileirado.types import NUP

class TestNUP:
    def test_nup_valido(self):
        # Exemplo real de NUP válido: 23520005177202676
        # Base: 2352000517720267, DV: 6 (98 - (base % 97))
        nup = NUP("23520005177202676")
    #     assert str(nup) == "23520.005177/2026-76"
    #     assert nup.digitos == "23520005177202676"

    # def test_nup_valido_com_mascara(self):
    #     nup = NUP("23520.005177/2026-76")
    #     assert str(nup) == "23520.005177/2026-76"
    #     assert nup.digitos == "23520005177202676"

    # def test_nup_invalido_dv(self):
    #     with pytest.raises(ValueError):
    #         NUP("23520005177202677")  # DV incorreto

    # def test_nup_invalido_tamanho(self):
    #     with pytest.raises(ValueError):
    #         NUP("1234567890123456")  # Menos de 17 dígitos
