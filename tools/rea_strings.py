r"""REA aracı: G*Power ikilisinde dize araması yapar, bayt offseti ve kısa alıntı üretir.

İkili dosya repoya GİRMEZ; yol argüman olarak verilir. Betik yalnızca
offset + kısa alıntı yazar, decompile/disassembly çıktısı üretmez
(GRUP1_GOREV.md kural 2 ve 4).

Kullanım:
    python tools/rea_strings.py "C:\...\GPowerNT.exe"
    python tools/rea_strings.py "...\GPowerNT.exe" --ara "average group size"
    python tools/rea_strings.py "...\GPowerNT.exe" --tara > rea_kesif.md
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

# --- KESIF MODU (--tara) ---------------------------------------------------
# Bilinen metni aramak yerine ikilideki TUM dizeleri tarar ve desene uyanlari
# listeler. Amaci LEDGER.md'deki TODO kalan REA satirlarini kapatmak: aranacak
# metni tahmin etmek gerekmez, ikili kendi sozlugunu gosterir.
#
# Her desen bir REA satirina baglidir; eslesme BULUNMAMASI da bir bulgudur
# (ornegin hicbir "search bound" dizesi yoksa, kuantil kapali formdur).
KESIF = {
    "Sayısal yordam adları ve arama sınırları (REA-03 / REA-04 / REA-05)":
        "[A-Za-z]{2,}Dist-[A-Za-z ]{3,}|search bound|quantile|iteration|"
        "converg|tolerance|epsilon|bisect|newton",
    "Kısıt ve doğrulama mesajları (REA-02 / REA-06)":
        "must be|multiple of|greater or equal|at least|be an integer|"
        "number of groups|per group|group size",
    "Nonsantralite ve etki büyüklüğü sözlüğü (REA-01 / REA-09)":
        "noncentral|non-central|noncentrality|lambda|effect size|"
        "variance explained|partial eta",
    "Kayan nokta tipi ipuçları (REA-11)":
        "long double|extended|float80|denormal|_fpreset|"
        "overflow|underflow|"
        # NAN/INF/FPU buyuk harfe duyarli: aksi halde "trustInfo" gibi
        # alakasiz dizeler yanlis pozitif veriyor (python.exe uzerinde gorulduy).
        "(?-i:NAN|INF(?![A-Z])|FPU|isnan|_finite)",
}

# Yazdirilabilir ASCII araligi: bosluk (0x20) ile tilde (0x7e) arasi.
# Kacis dizisi yerine karakterlerin kendisi yazildi.
YAZDIRILABILIR = b"[ -~]"
SIFIR = bytes([0])


def dizeler(veri, en_az=6):
    """Ikilideki yazdirilabilir dizeleri (kodlama, offset, metin) olarak uretir.

    ASCII ve UTF-16LE ayri taranir; G*Power mesajlarinin bir kismi ascii,
    bir kismi utf16 (bkz. REA-07'nin iki varyanti).
    """
    tekrar = b"{%d,}" % en_az
    for m in re.finditer(YAZDIRILABILIR + tekrar, veri):
        yield "ascii", m.start(), m.group().decode("latin-1")
    for m in re.finditer(b"(?:" + YAZDIRILABILIR + SIFIR + b")" + tekrar, veri):
        yield "utf16", m.start(), m.group().decode("utf-16-le", "replace")


def tara(veri, en_fazla=25):
    """KESIF desenlerine uyan dizeleri tabloya doker."""
    havuz = list(dizeler(veri))
    print("")
    print("## Keşif taraması")
    print("")
    print("Taranan dize: %d" % len(havuz))
    for baslik, desen in KESIF.items():
        kural = re.compile(desen, re.IGNORECASE)
        gorulen, vurus = set(), []
        for kodlama, offset, metin in havuz:
            if kural.search(metin) and metin not in gorulen:
                gorulen.add(metin)
                vurus.append((kodlama, offset, metin))
        print("")
        print("### " + baslik)
        print("")
        if not vurus:
            print("**Eşleşme yok.** (Yokluk da bulgudur — LEDGER'a böyle yazılır.)")
            continue
        print("Toplam %d benzersiz dize; ilk %d tanesi:"
              % (len(vurus), min(en_fazla, len(vurus))))
        print("")
        print("| kodlama | bayt offseti | dize |")
        print("|---|---|---|")
        for kodlama, offset, metin in vurus[:en_fazla]:
            kisa = re.sub("[^ -~]+", "|", metin)[:70]
            print("| %s | `%d` | `%s` |" % (kodlama, offset, kisa))


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
    ayirici.add_argument("--tara", action="store_true",
                         help="keşif modu: ikilideki tüm dizeleri desenlere göre tarar")
    ayirici.add_argument("--en-fazla", type=int, default=25, dest="en_fazla",
                         help="keşif modunda desen başına yazılacak satır sayısı")
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
    if arg.tara:
        tara(veri, arg.en_fazla)
    return 0


if __name__ == "__main__":
    sys.exit(main())
