r"""REA aracı: G*Power ikilisinde dize araması yapar, bayt offseti ve kısa alıntı üretir.

İkili dosya repoya GİRMEZ; yol argüman olarak verilir. Betik yalnızca
offset + kısa alıntı yazar, decompile/disassembly çıktısı üretmez
(GRUP1_GOREV.md kural 2 ve 4).

Kullanım:
    python tools/rea_strings.py "C:\...\GPowerNT.exe"
    python tools/rea_strings.py "...\GPowerNT.exe" --ara "average group size"
"""
import argparse
import hashlib
import os
import re
import sys

# LEDGER.md [REA] tablosunun aradığı mesaj parçaları. Tam mesaj ikilide tek
# parça halinde DURMUYOR; çalışma anında birleştiriliyor (bkz. REA-08).
PARCALAR = [
    "The total sample size (",
    ") is not a multiple of",
    "the number of groups (",
    "). The analysis was ",
    "based on the average group size.",
    "Total sample size must be greater than",
    "The total sample size must be greater than the number of groups",
    "The size of each group must be greater or equal 1",
]

# Diyalog başlıkları sabit küme mi? (B-10)
BASLIKLAR = ["Input error", "Please note", "Interruption", "Internal math error"]

# Sayı biçimleme yordamını daraltan format dizeleri (B-09 / REA-10).
FORMATLAR = ["%.16g", "%.15g", "%.7g", "%.6g", "%.5g", "%g",
             "%.7f", "%.6f", "%.5f", "%.3f", "%.0f", "%.f", "%ld"]

# Sayısal yordam hakkında ipucu veren dizeler (REA-04 / REA-05).
YORDAM = [
    "BinomialDist-Quantile: input parameter out of range",
    "BinomialDist-Quantile: answer below lower search bound",
    "BinomialDist-Quantile: answer above upper search bound",
]


def bul(veri, metin):
    """metin'i hem ASCII hem UTF-16LE olarak arar, (kodlama, offset) döndürür."""
    sonuc = []
    for ad, kodlama in (("ascii", "ascii"), ("utf16", "utf-16-le")):
        try:
            desen = metin.encode(kodlama)
        except UnicodeEncodeError:
            continue
        sonuc += [(ad, m.start()) for m in re.finditer(re.escape(desen), veri)]
    return sonuc


def alinti(veri, offset, kodlama, uzunluk=64):
    """Offset'teki kısa alıntı. Yalnızca yazdırılabilir karakterler kalır."""
    adim = 2 if kodlama == "utf16" else 1
    ham = veri[offset:offset + uzunluk * adim]
    metin = ham.decode("utf-16-le", "replace") if adim == 2 else ham.decode("latin-1")
    return re.sub(r"[^\x20-\x7e]+", "|", metin)[:uzunluk]


def tablo(veri, baslik, metinler, aciklama=""):
    print(f"\n### {baslik}")
    if aciklama:
        print(f"\n{aciklama}")
    print("\n| aranan | kodlama | bayt offseti | alıntı |")
    print("|---|---|---|---|")
    for metin in metinler:
        vurus = bul(veri, metin)
        if not vurus:
            print(f"| `{metin}` | — | **YOK** | — |")
            continue
        for kodlama, offset in vurus[:3]:
            print(f"| `{metin}` | {kodlama} | `{offset}` | `{alinti(veri, offset, kodlama)}` |")


def main():
    ayirici = argparse.ArgumentParser(description="G*Power ikilisinde REA dize araması")
    ayirici.add_argument("ikili", help="GPowerNT.exe yolu (repoya konmaz)")
    ayirici.add_argument("--ara", action="append", default=[],
                         help="ek olarak aranacak metin; birden çok kez verilebilir")
    arg = ayirici.parse_args()

    try:
        veri = open(arg.ikili, "rb").read()
    except OSError as hata:
        print(f"ikili okunamadı: {hata}", file=sys.stderr)
        return 1

    print("# REA dize araması — çıktı")
    print(f"\n- ikili: `{os.path.basename(arg.ikili)}`")
    print(f"- boyut: {len(veri)} bayt")
    print(f"- SHA-256: `{hashlib.sha256(veri).hexdigest()}`")

    tablo(veri, "Mesaj parçaları (REA-07 / REA-08)", PARCALAR,
          "Tam mesaj tek parça halinde bulunmaz; parçalar bitişik bir dize "
          "tablosunda durur ve çalışma anında birleştirilir.")
    tablo(veri, "Diyalog başlıkları (B-10)", BASLIKLAR)
    tablo(veri, "Sayı biçimleme format dizeleri (B-09 / REA-10)", FORMATLAR)
    tablo(veri, "Sayısal yordam ipuçları (REA-04 / REA-05)", YORDAM)
    if arg.ara:
        tablo(veri, "Ek arama", arg.ara)
    return 0


if __name__ == "__main__":
    sys.exit(main())
