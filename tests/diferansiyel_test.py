"""Diferansiyel test: motor ↔ oracle (`oracle/anova_oneway.csv`).

Kâhin G*Power'dır. Bu betik motoru CSV'nin **44 satırının tamamına** karşı
koşturur ve uyuşmazlığı **düzeltmez, raporlar** (GRUP1_GOREV.md adım 4).

- Çıktı üreten 42 satır: `df1`, `df2`, `lambda`, `critical_f`, `actual_power`
  ve a priori'de `total_n` karşılaştırılır. `total_n` ve df'lerde **tam
  eşleşme**, ondalıklarda 5e-7 mutlak tolerans aranır.
- Hata kutusu gösteren 2 satır (id 37, 38): motorun da **reddetmesi** beklenir.
  Bu satırlar atlanmaz; hata davranışı de bir davranıştır.
- Post hoc'ta `N % k != 0` olan satırlarda `warning` alanının **varlığı** da
  kontrol edilir (SPEC 4.2).

Çalıştırma (repo kökünden):

    python tests/diferansiyel_test.py

Tüm satırlar eşleşirse çıkış kodu 0, aksi halde 1 olur.
"""
import csv
import io
import os
import sys

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(KOK, "src"))

from anova_power import analyze  # noqa: E402

CSV_YOLU = os.path.join(KOK, "oracle", "anova_oneway.csv")
TOLERANS = 5e-7

# id 37/38'de `Effect size f` ekran görüntüsünde hata kutusunun arkasında kaldı
# (CSV `notlar` sütunu: "okunamadi"). Bu iki satırın reddi `N <= k` kuralından
# gelmelidir, `f`'nin okunamamasından DEĞİL. Bu yüzden geçerli bir yer tutucu
# veriyoruz ve hatanın gerçekten grup sayısı kuralından geldiğini doğruluyoruz;
# aksi halde test yanlış sebeple "geçmiş" görünürdü.
YER_TUTUCU_F = 0.25
RED_BEKLENEN_METIN = "grup sayısından büyük olmalı"


def satirlari_oku(yol):
    with io.open(yol, encoding="utf-8", newline="") as dosya:
        return list(csv.DictReader(dosya))


def motoru_cagir(satir):
    """CSV satırını motorun girdisine çevirir ve çağırır."""
    ham_f = satir["f"]
    ortak = dict(f=YER_TUTUCU_F if ham_f == "" else float(ham_f),
                 alpha=float(satir["alpha"]),
                 groups=int(satir["groups"]))
    if satir["mod"] == "a_priori":
        return analyze(dict(mode="a_priori", power=float(satir["power"]), **ortak))
    return analyze(dict(mode="post_hoc", total_n=int(satir["total_n"]), **ortak))


def satiri_karsilastir(satir, sonuc):
    """Oracle ile motoru karşılaştırır; farkların listesini döndürür."""
    farklar = []
    tam = [("df1", int(satir["df1"])), ("df2", int(satir["df2"]))]
    if satir["mod"] == "a_priori":
        tam.append(("total_n", int(satir["total_n"])))
    for ad, beklenen in tam:
        if sonuc[ad] != beklenen:
            farklar.append(f"{ad}: oracle={beklenen} motor={sonuc[ad]}")
    for ad in ("lambda", "critical_f", "actual_power"):
        beklenen = float(satir[ad])
        sapma = abs(beklenen - sonuc[ad])
        if sapma > TOLERANS:
            farklar.append(f"{ad}: oracle={beklenen} motor={sonuc[ad]} (d={sapma:.1e})")
    if satir["mod"] == "post_hoc":
        kat_degil = int(satir["total_n"]) % int(satir["groups"]) != 0
        if kat_degil != ("warning" in sonuc):
            farklar.append(
                f"warning: N%k!=0 oldugunda beklenen={kat_degil} motor={'warning' in sonuc}")
    return farklar


def main():
    satirlar = satirlari_oku(CSV_YOLU)
    eslesen = fark = dogru_red = yanlis_red = 0
    sorunlar = []

    print(f"Diferansiyel test — {len(satirlar)} oracle satiri")
    print(f"{'id':>3}  {'mod':9}  durum")
    print("-" * 56)

    for satir in satirlar:
        rid = satir["id"]
        # actual_power bos => G*Power hic cikti uretmedi (hata kutusu)
        hata_bekleniyor = satir["actual_power"] == ""
        try:
            sonuc = motoru_cagir(satir)
        except ValueError as hata:
            if hata_bekleniyor and RED_BEKLENEN_METIN in str(hata):
                dogru_red += 1
                print(f"{rid:>3}  {satir['mod']:9}  N<=k KURALIYLA REDDEDILDI -> {hata}")
            elif hata_bekleniyor:
                yanlis_red += 1
                sorunlar.append((rid, f"red dogru kuraldan gelmedi: {hata}"))
                print(f"{rid:>3}  {satir['mod']:9}  !! YANLIS SEBEPLE RED -> {hata}")
            else:
                yanlis_red += 1
                sorunlar.append((rid, f"beklenmeyen hata: {hata}"))
                print(f"{rid:>3}  {satir['mod']:9}  !! BEKLENMEYEN HATA -> {hata}")
            continue

        if hata_bekleniyor:
            yanlis_red += 1
            sorunlar.append((rid, f"hata beklenirken sonuc uretti: {sonuc}"))
            print(f"{rid:>3}  {satir['mod']:9}  !! HATA BEKLENIYORDU, SONUC URETTI")
            continue

        farklar = satiri_karsilastir(satir, sonuc)
        if farklar:
            fark += 1
            sorunlar.append((rid, "; ".join(farklar)))
            print(f"{rid:>3}  {satir['mod']:9}  FARK -> " + " | ".join(farklar))
        else:
            eslesen += 1
            print(f"{rid:>3}  {satir['mod']:9}  ESLESTI")

    print("-" * 56)
    print(f"ESLESTI: {eslesen}   FARK: {fark}   "
          f"hata dogru reddedildi: {dogru_red}   hata davranisi FARK: {yanlis_red}")

    if sorunlar:
        print("\nUYUSMAZLIKLAR (duzeltilmedi, raporlaniyor):")
        for rid, aciklama in sorunlar:
            print(f"  id {rid}: {aciklama}")
        return 1
    print("\nTum satirlar eslesti. Kahin = G*Power; uyusmazlik yok.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
