"""SPEC.md tabanlı tek yönlü ANOVA güç analizi. Python 3.10+, SciPy."""
import json
import math
import sys

from scipy.stats import f as central_f, ncf

MAX_N = 100_000_000  # Uygulama kaynak sınırı; G*Power kuralı değildir.


def number(data, key, integer=False):
    value = data.get(key)
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{key}: sayısal değer gerekli")
    try:
        finite = math.isfinite(value)
    except OverflowError:
        finite = False
    if not finite:
        raise ValueError(f"{key}: sonlu değer gerekli")
    if integer and (int(value) != value):
        raise ValueError(f"{key}: tam sayı gerekli")
    return int(value) if integer else float(value)


def statistics(effect, alpha, groups, total_n):
    df1, df2 = groups - 1, total_n - groups
    lam = effect * effect * total_n
    if not math.isfinite(lam):
        raise ValueError("Nonsantralite sayısal aralığı aştı")
    critical = float(central_f.isf(alpha, df1, df2))
    # Merkezi durumda ayrı dal: bazı ncf uygulamaları lambda=0'da
    # survival function için farklı sayısal davranış gösterebilir.
    power = alpha if effect == 0 else float(ncf.sf(critical, df1, df2, lam))
    if not math.isfinite(critical) or not math.isfinite(power) or not 0 <= power <= 1:
        raise ValueError("Bu girdiler için güvenilir sayısal sonuç üretilemedi")
    return {"lambda": lam, "critical_f": critical, "df1": df1,
            "df2": df2, "actual_power": power}


def analyze(data):
    if not isinstance(data, dict):
        raise ValueError("Girdi bir JSON nesnesi olmalı")
    mode = data.get("mode")
    if mode not in ("a_priori", "post_hoc"):
        raise ValueError("mode: a_priori veya post_hoc olmalı")
    allowed = {"mode", "f", "alpha", "groups", "power" if mode == "a_priori" else "total_n"}
    if set(data) - allowed:
        raise ValueError("Bilinmeyen veya bu moda ait olmayan alan var")
    effect = number(data, "f")
    alpha = number(data, "alpha")
    groups = number(data, "groups", True)
    if effect < 0 or not 0 < alpha < 1 or groups < 2:
        raise ValueError("f >= 0, 0 < alpha < 1 ve groups >= 2 gerekli")
    if groups >= MAX_N:
        raise ValueError("groups uygulamanın kaynak sınırını aşıyor")
    if mode == "post_hoc":
        total_n = number(data, "total_n", True)
        if total_n <= groups:
            raise ValueError("total_n grup sayısından büyük olmalı")
        if total_n > MAX_N:
            raise ValueError("total_n uygulamanın kaynak sınırını aşıyor")
        result = statistics(effect, alpha, groups, total_n)
        if total_n % groups:
            result["warning"] = "Toplam N grup sayısının katı değildir; analiz ortalama grup büyüklüğüne dayanır."
    else:
        target = number(data, "power")
        if not 0 < target < 1:
            raise ValueError("power: 0 ile 1 arasında olmalı")
        if target <= alpha:
            raise ValueError("power <= alpha için SPEC belirsiz; bu sürüm desteklemiyor")
        if effect == 0:
            raise ValueError("f=0 iken alpha üzerindeki hedef güce sonlu N ile ulaşılamaz")
        # Seçilen yorum: eşit gruplar, en az iki kişi/grup ve hedefi
        # karşılayan en küçük kat. Eşitlikte bir sonraki kata atlanmaz.
        limit = MAX_N // groups
        if limit < 2:
            raise ValueError("Eşit gruplu minimum N kaynak sınırını aşıyor")
        low, high = 1, 2
        while statistics(effect, alpha, groups, high * groups)["actual_power"] < target:
            low = high
            if high == limit:
                raise ValueError("Hedef güç kaynak sınırı içinde sağlanamıyor")
            high = min(high * 2, limit)
        while high - low > 1:
            mid = (low + high) // 2
            if statistics(effect, alpha, groups, mid * groups)["actual_power"] >= target:
                high = mid
            else:
                low = mid
        total_n = high * groups
        result = statistics(effect, alpha, groups, total_n)
        result["total_n"] = total_n
    # Karşılaştırmalar tam hassasiyetle yapıldıktan sonra çıktı biçimlenir.
    return {key: round(value, 7) if isinstance(value, float) else value
            for key, value in result.items()}


def main():
    # JSON encoding must not depend on Windows locale.
    sys.stdin.reconfigure(encoding="utf-8-sig")
    sys.stdout.reconfigure(encoding="utf-8")
    try:
        data = json.loads(sys.stdin.read(), parse_constant=lambda s: (_ for _ in ()).throw(ValueError(f"Geçersiz JSON sabiti: {s}")))
        result = analyze(data)
        code = 0
    except (ValueError, TypeError, OverflowError, ArithmeticError) as exc:
        result, code = {"error": str(exc)}, 1
    print(json.dumps(result, ensure_ascii=False, allow_nan=False, separators=(",", ":")))
    return code


if __name__ == "__main__":
    sys.exit(main())
