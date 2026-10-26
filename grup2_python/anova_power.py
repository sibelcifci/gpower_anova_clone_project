"""Oturum 2 (temiz oda) teslimi — artık tek motora yönlendiren kabuk.

Bu dosya başlangıçta motorun kendisiydi: yalnızca `SPEC.md` okunarak, G*Power
hiç açılmadan üretildi. Ödev kuralı 3 ("hesap mantığı tek motordadır; CLI, MCP
ve ajan bu motoru çağıran ince katmanlardır") gereği hesap mantığı
`src/anova_power/core.py`'ye taşındı ve burada kopyası bırakılmadı.

Özgün, el değmemiş hâli git geçmişinde durur:

    git show 4326cd9:grup2_python/anova_power.py

Temiz oda kaydı bozulmaz; bu dosya yalnızca `grup2_python/test_anova_power.py`
testlerinin aynı arayüzle çalışmaya devam etmesi için vardır.

Paket yol üzerinden ve `gpower_motor` takma adıyla yüklenir: bu dosyanın kendi
adı da `anova_power` olduğu için düz `import` paketi değil kendisini bulurdu.
"""
import importlib
import importlib.util
import os
import sys

_PAKET = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src", "anova_power")
_ALIAS = "gpower_motor"

if _ALIAS not in sys.modules:
    _spec = importlib.util.spec_from_file_location(
        _ALIAS, os.path.join(_PAKET, "__init__.py"),
        submodule_search_locations=[_PAKET])
    _motor = importlib.util.module_from_spec(_spec)
    sys.modules[_ALIAS] = _motor          # göreli import'lar için önce kaydedilir
    _spec.loader.exec_module(_motor)
else:
    _motor = sys.modules[_ALIAS]

MAX_N = _motor.MAX_N
analyze = _motor.analyze
number = _motor.number
statistics = _motor.statistics
main = importlib.import_module(f"{_ALIAS}.cli").main

__all__ = ["MAX_N", "analyze", "main", "number", "statistics"]

if __name__ == "__main__":
    sys.exit(main())
