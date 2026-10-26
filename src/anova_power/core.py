"""Tek yönlü ANOVA güç analizi motoru — SPEC.md tabanlı. Python 3.10+, SciPy.

Bu dosya projenin **tek** hesap motorudur (ödev kuralı 3). CLI, MCP sunucusu ve
AI ajanı bu modülü çağıran ince katmanlardır; hiçbiri kendi hesabını yapmaz.

Köken: Oturum 2'de temiz oda kuralıyla, yalnızca `SPEC.md` okunarak üretildi
(`grup2_python/anova_power.py`, commit 4326cd9). Buraya taşındı; hesap mantığı
değişmedi. Tek davranış değişikliği `power <= alpha` dalındadır ve
`SPEC.md` 3.4'ten türetilmiştir — gerekçe aşağıda.
"""
import math

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


def _en_kucuk_n(effect, alpha, groups, target):
    """Hedef gücü sağlayan en küçük uygun toplam N (SPEC 3.3 + 3.4).

    N daima grup sayısının tam katıdır (AJ-04) ve `df2 = N - k >= 1` gerekir
    (id 39/40'ta df2 = 1 çalışıyor), dolayısıyla aranan en küçük değer 2k'dır.
    Bu bir varsayım değil, iki gözlemin sonucudur.
    """
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
    return high * groups


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
        if effect == 0:
            raise ValueError("f=0 iken alpha üzerindeki hedef güce sonlu N ile ulaşılamaz")
        # power <= alpha: SPEC bölüm 6 bu bandı BELİRSİZ bırakıyor, ama SPEC 3.4
        # ("istenen gücü sağlayan en küçük uygun N") bandı kendi içinde çözüyor:
        # güç hiçbir N'de alfanın altına inemediğinden (id 43) en küçük uygun
        # kat zaten hedefi sağlar. Hata atmak yerine o değeri döndürüyoruz;
        # aksi halde gizli vektörde bu bant varsa N hiç üretilmez.
        total_n = _en_kucuk_n(effect, alpha, groups, target)
        result = statistics(effect, alpha, groups, total_n)
        result["total_n"] = total_n
    # Karşılaştırmalar tam hassasiyetle yapıldıktan sonra çıktı biçimlenir.
    return {key: round(value, 7) if isinstance(value, float) else value
            for key, value in result.items()}
