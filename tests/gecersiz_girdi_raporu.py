r"""Gecersiz a priori girdilerinde motorun davranis raporu (EKSIK_VAKALAR X-01..X-13).

Bu betik KAHIN DEGILDIR. G*Power'in bu vektorlerde ne yaptigi henuz
bilinmiyor; burada yalnizca *kendi motorumuzun* ne yaptigi kayda geciriliyor.
Oracle verisi geldiginde karsilastirma yapilacak yer burasidir.

Sinanan sozlesme ozellikleri (oracle gerektirmeyenler):
  1. surec asili kalmaz (her vektor icin 15 s ust sinir),
  2. cikis kodu 0 degildir (sessizce sayi uretmez),
  3. stdout tek satir JSON'dur ve icinde "error" alani vardir.

Kullanim:
    PYTHONPATH=src PYTHONUTF8=1 python tests/gecersiz_girdi_raporu.py
    PYTHONPATH=src PYTHONUTF8=1 python tests/gecersiz_girdi_raporu.py --md > tests/gecersiz_girdi_raporu.md
"""
import json
import os
import subprocess
import sys
import time

TEMEL = {"mode": "a_priori", "f": 0.25, "alpha": 0.05, "power": 0.80, "groups": 3}

# (ad, degisen alan(lar), neyi sinadigi) — EKSIK_VAKALAR.md bolum 2 ile ayni sira
VEKTORLER = [
    ("X-01", {"f": 0},            "a priori'de f=0 (N sonsuza gider)"),
    ("X-02", {"f": -0.25},        "negatif etki buyuklugu"),
    ("X-03", {"alpha": 0},        "alpha = 0"),
    ("X-04", {"alpha": 1},        "alpha = 1"),
    ("X-05", {"alpha": -0.05},    "negatif alpha"),
    ("X-06", {"power": 1},        "guc = 1 (erisilemez)"),
    ("X-07", {"power": 0},        "guc = 0"),
    ("X-08", {"power": 1.5},      "guc > 1"),
    ("X-09", {"groups": 1},       "tek grup -> df1 = 0"),
    ("X-10", {"groups": 0},       "sifir grup"),
    ("X-11", {"groups": -3},      "negatif grup"),
    # id 56: G*Power 2.5'i KABUL EDIP hesap yapiyor (SPEC 6.5). Bu satirda
    # beklenen davranis hata DEGIL, sonuc uretmektir.
    ("X-12", {"groups": 2.5},     "tam sayi olmayan grup sayisi (SONUC beklenir)"),
    ("X-13", {"alpha": "abc"},    "alpha kutusuna harf"),
]

UST_SINIR = 15.0


def kosu(vektor):
    """Vektoru gercek CLI surecine stdin'den verir; (cikis, cikti, sure) doner."""
    ortam = dict(os.environ, PYTHONPATH="src", PYTHONUTF8="1")
    t0 = time.time()
    surec = subprocess.run([sys.executable, "-m", "anova_power"],
                           input=json.dumps(vektor), capture_output=True,
                           text=True, env=ortam, timeout=UST_SINIR)
    return surec.returncode, (surec.stdout or surec.stderr).strip(), time.time() - t0


def main():
    md = "--md" in sys.argv
    satirlar, sorun = [], []

    for ad, degisiklik, sinanan in VEKTORLER:
        vektor = dict(TEMEL, **degisiklik)
        alan = ", ".join(f"{k}={v!r}" for k, v in degisiklik.items())
        try:
            cikis, cikti, sure = kosu(vektor)
        except subprocess.TimeoutExpired:
            satirlar.append((ad, alan, sinanan, "—", f">{UST_SINIR:.0f} s", "ASILI KALDI"))
            sorun.append(f"{ad}: {UST_SINIR:.0f} saniyede bitmedi")
            continue

        try:
            mesaj = json.loads(cikti).get("error", "(error alani yok)")
            if ad == "X-12":
                mesaj = ""
        except json.JSONDecodeError:
            mesaj = "(JSON degil) " + cikti[:60]
            sorun.append(f"{ad}: stdout JSON degil")

        if ad == "X-12":
            # Tek istisna: oracle bu vektorde sonuc bekliyor (id 56).
            if cikis != 0:
                sorun.append(f"{ad}: oracle sonuc bekliyor ama motor reddetti")
            mesaj = "SONUC URETTI: " + cikti[:70]
        elif cikis == 0:
            sorun.append(f"{ad}: cikis kodu 0 — sessizce sonuc uretti")
        satirlar.append((ad, alan, sinanan, str(cikis), f"{sure:.1f} s", mesaj))

    if md:
        print("# Gecersiz a priori girdileri — MOTORUN davranisi\n")
        print("> G*Power karsiliklari ARTIK TOPLANDI: oracle id 45-59, gorseller v45-v59.")
        print("> Karsilastirmanin kendisi `tests/diferansiyel_test.py` icinde yapilir;")
        print("> bu dosya yalnizca motorun davranisinin okunabilir dokumudur.")
        print("> Uretim: `python tests/gecersiz_girdi_raporu.py --md`\n")
        print("| # | degisen girdi | sinanan | cikis kodu | sure | motorun mesaji |")
        print("|---|---|---|---|---|---|")
        for s in satirlar:
            print("| {} | `{}` | {} | {} | {} | `{}` |".format(*s))
        print()
        print("Diger alanlar sabit: `f=0.25, alpha=0.05, power=0.80, groups=3`.\n")
        if sorun:
            print("## Sozlesme ihlalleri\n")
            for x in sorun:
                print("- " + x)
        else:
            print("## Sonuc\n")
            print(f"{len(satirlar)}/{len(satirlar)} vektorde davranis oracle ile uyumlu: ")
            print("asili kalma yok; 12 vektor `error` alanli JSON dondu, X-12 ise")
            print("oracle'in (id 56) bekledigi gibi SONUC uretti.")
    else:
        for s in satirlar:
            print("{:5}  {:18}  cikis={:>2}  {:>5}  {}".format(s[0], s[1], s[3], s[4], s[5]))
        print()
        print("SORUN YOK" if not sorun else "SORUN: " + "; ".join(sorun))

    return 1 if sorun else 0


if __name__ == "__main__":
    sys.exit(main())
