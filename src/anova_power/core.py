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

# --- Kabul aralıkları (SPEC 6.1) -------------------------------------------
# Kâhinden doğrudan okundu: "<Alan> is outside the admissible range (a, b)."
# id 45-59, görseller v45-v59. Üst sınırların dahil olmadığı id 48 ve id 50
# ile kanıtlandı; alt sınırların tam değerleri denenmedi (SPEC 6.1 notu).
F_UST = 50.0
F_ALT_A_PRIORI = 1e-06        # id 45: f=0 reddedildi
F_ALT_POST_HOC = 0.0          # id 58 mesajı (0, 50) der; id 43 f=0'ı KABUL eder
ALFA_ALT, ALFA_UST = 1e-07, 1.0
GUC_ALT, GUC_UST = 1e-07, 1.0

# SPEC 6.5 — tam sayı olmayan grup sayısı sessizce tam sayıya çevrilir.
# Yön iki oracle satırıyla belirlendi: id 60 (2.4 -> k=2, N=128) ve
# id 56 (2.5 -> k=3, N=159). Aşağı/yukarı ayrımı 2.4'te, yarımın yukarı
# gittiği 2.5'te görüldü. Python'un round() fonksiyonu KULLANILAMAZ:
# banker yuvarlaması yapar ve round(2.5) = 2 verir, bu id 56 ile çelişir.
def _grup_sayisi(ham):
    """Grup sayısını en yakın tam sayıya yuvarlar, yarımda yukarı (SPEC 6.5)."""
    return int(math.floor(ham + 0.5))


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


def _araliklari_dogrula(mode, effect, alpha, target=None):
    """SPEC 6.1-6.4: G*Power'ın kabul aralıklarını birebir uygular.

    `f` alanının alt sınırı MODA BAĞLIDIR (SPEC 6.2): a priori'de 1e-06,
    post hoc'ta 0. Post hoc'ta sınır **kapalı** alınır çünkü gösterilen
    aralık (0, 50) olmasına rağmen id 43 f=0'ı kabul eder (SPEC 6.3) —
    davranış, mesaja göre önceliklidir.
    """
    if mode == "a_priori":
        if not F_ALT_A_PRIORI < effect < F_UST:
            raise ValueError(f"f: ({F_ALT_A_PRIORI:g}, {F_UST:g}) aralığında olmalı")
    elif not F_ALT_POST_HOC <= effect < F_UST:
        raise ValueError(f"f: [{F_ALT_POST_HOC:g}, {F_UST:g}) aralığında olmalı")
    if not ALFA_ALT < alpha < ALFA_UST:
        raise ValueError(f"alpha: ({ALFA_ALT:g}, {ALFA_UST:g}) aralığında olmalı")
    if target is not None and not GUC_ALT < target < GUC_UST:
        raise ValueError(f"power: ({GUC_ALT:g}, {GUC_UST:g}) aralığında olmalı")


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
    # SPEC 6.5: tam sayı olmayan grup sayısı reddedilmez, çevrilir (id 56).
    groups = _grup_sayisi(number(data, "groups"))
    if groups < 2:
        # SPEC 6.4: G*Power burada aralık kalıbını değil ayrı bir metin kullanır.
        raise ValueError("En az 2 grup olmalı")
    if groups >= MAX_N:
        raise ValueError("groups uygulamanın kaynak sınırını aşıyor")
    if mode == "post_hoc":
        _araliklari_dogrula(mode, effect, alpha)
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
        _araliklari_dogrula(mode, effect, alpha, target)
        # SPEC 6.8 / REA-19: G*Power "Power must be greater than or equal to
        # alpha." der (ikilide 1856032) ve bu kural tek yönlü ANOVA a priori
        # yolunda GERÇEKTEN tetikleniyor (id 61). Eşitlik serbesttir.
        if target < alpha:
            raise ValueError("power: alfadan küçük olamaz")
        # NOT: power == alpha hâlâ geçerlidir ve en küçük uygun N'i döndürür;
        # kâhinin kuralı "greater than OR EQUAL" diyor. Yalnızca power < alpha
        # reddedilir. Önceki sürüm ikisini de kabul ediyordu (id 61 çürüttü).
        total_n = _en_kucuk_n(effect, alpha, groups, target)
        result = statistics(effect, alpha, groups, total_n)
        result["total_n"] = total_n
    # Karşılaştırmalar tam hassasiyetle yapıldıktan sonra çıktı biçimlenir.
    return {key: round(value, 7) if isinstance(value, float) else value
            for key, value in result.items()}
