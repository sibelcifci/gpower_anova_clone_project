# anova-power-clone

Tek yönlü ANOVA (F testi, sabit etkiler, omnibus) için güç analizi motorunun
davranışsal klonu. YZM301 "teardown sprint" ödevi.

Referans alınan yazılım **G*Power 3.1.9.7 (Windows)**'tur. Bu proje G*Power'ın
bir parçası değildir, onunla ilişkili değildir ve onun adını taşımaz.

---

## Durum

| Aşama | Durum |
|---|---|
| Oracle veri toplama (Oturum 1) | ✅ 44 ekran görüntüsü, 44 satır |
| Bağımsız çapraz kontrol | ✅ a priori 30/30, post hoc 12/12 eşleşti |
| A priori davranışı | ✅ `SPEC.md` bölüm 3 |
| Post hoc davranışı | ✅ `SPEC.md` bölüm 4 — N'in katı olmaması, `N ≤ k` hatası, `f = 0` dahil |
| Geçersiz girdi (a priori) | ❌ hâlâ yok — `EKSIK_VAKALAR.md` bölüm 2 |
| Gösterim biçimi kuralı | ⚠️ BELİRSİZ — `LEDGER.md` bölüm 2.4 |
| REA (ikili inceleme) | ❌ yapılmadı — `LEDGER.md` `[REA]` tablosu boş |
| Motor / CLI | ❌ yazılmadı (Grup 2'nin işi) |

---

## Dizin yapısı

```
SPEC.md              davranış sözleşmesi (Gherkin), kod içermez
LEDGER.md            kanıt defteri: [DOK] / [AJAN] / [REA]
EKSIK_VAKALAR.md     G*Power'da çalıştırılacak eksik girdi vektörleri
HALLUCINATIONS.md    ajan hatalarının dürüst kaydı
AGENT_COST.md        ajan maliyet kaydı
prompts/             her oturumun ilk promptu
oracle/              kâhin verisi
  anova_oneway.csv     44 satır (30 a priori + 14 post hoc)
  RENAME_MAP.csv       eski ad → v{id}.png eşlemesi
  screenshots/         v1.png … v44.png
src/                 motor (Grup 2 dolduracak)
tests/               uyum_raporu.md ve testler
```

---

## Kurulum

```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

`requirements.txt` henüz yok; Grup 2 motoru yazarken oluşturacak.

## Çalıştırma

CLI henüz yazılmadı. Sözleşmesi `SPEC.md` bölüm 2'de tanımlıdır:
tek satır JSON çıktı, geçersiz girdide `{"error":"..."}` ve sıfırdan farklı
çıkış kodu.

---

## Sürüm bilgisi

| | |
|---|---|
| Referans yazılım | G*Power 3.1.9.7 |
| İşletim sistemi | Windows |
| Ekran görüntüsü tarihi | 2026-10-22 |
| `GPower.exe` SHA-256 | _(doldurulacak — ikili dosya repoda değil)_ |

> SHA-256 bilerek boş bırakıldı. Değeri uydurmak yerine, dosyanın bulunduğu
> makinede hesaplanıp buraya yazılmalıdır.

## Demo video

_(link eklenecek)_

---

## Bonus katmanlar

| Katman | Durum | Not |
|---|---|---|
| REA / ikili inceleme kanıtı | planlandı | `LEDGER.md` `[REA]` tablosu |
| Diferansiyel test (motor ↔ oracle) | planlandı | `tests/` |
| Property-based test | planlandı | sınır değerler |
| Halüsinasyon kaydı | aktif | `HALLUCINATIONS.md` |
| Ajan maliyet kaydı | aktif | `AGENT_COST.md` |

---

## Veri ve etik

- `GPower.exe` ve kurulum dosyaları repoya **girmez** (`.gitignore`).
- Decompile çıktısı hiçbir dosyaya **konmaz**; `LEDGER.md`'de yalnızca kısa
  alıntı ve fonksiyon adresi bulunabilir.
- Projede gerçek hasta verisi **yoktur**; tüm senaryolar kurgusaldır.
- Oturum 1 (inceleme) ile Oturum 2 (motor yazımı) **temiz oda** kuralıyla
  ayrılmıştır: bu oturumda hiçbir motor kodu yazılmamıştır.

---

## Atıf

Referans alınan yazılım:

> Faul, F., Erdfelder, E., Lang, A.-G., & Buchner, A. (2007). G*Power 3:
> A flexible statistical power analysis program for the social, behavioral,
> and biomedical sciences. *Behavior Research Methods, 39*(2), 175–191.

> Faul, F., Erdfelder, E., Buchner, A., & Lang, A.-G. (2009). Statistical power
> analyses using G*Power 3.1: Tests for correlation and regression analyses.
> *Behavior Research Methods, 41*(4), 1149–1160.

Etki büyüklüğü `f`'nin tanımı için:

> Cohen, J. (1988). *Statistical Power Analysis for the Behavioral Sciences*
> (2nd ed.). Lawrence Erlbaum Associates.
