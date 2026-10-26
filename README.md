# ANOVA Power Clone - Clean Room Reverse Engineering

Tek yönlü ANOVA (F testi, sabit etkiler, omnibus) için güç analizi motorunun davranışsal klonu. YZM301 "Teardown Sprint" ödevi.

Referans alınan yazılım **G*Power 3.1.9.7 (Windows)**'tur. Bu proje G*Power'ın bir parçası değildir, onunla ilişkili değildir ve onun adını taşımaz.

**Grup Bilgileri:** Grup 17 (k3)
* SİBEL ÇİFCİ
* GÖNÜL NAZİRE AYDIN
* CEM ERŞEN
* KORKUT ŞAHAN

> **Bonus katmanlar:** Bu teslimde **yalnızca Temel Katman (CLI)** yapılmıştır.
> MCP sunucusu (+15) ve AI ajanı (+10) **yapılmamıştır.**

---

## Proje Özeti ve Amaç
Bu proje, GUI tabanlı G*Power yazılımının Tek Yönlü ANOVA (One-Way ANOVA) güç analizi motorunu tersine mühendislik yöntemleriyle inceleyerek, Temiz Oda (Clean Room) prensiplerine uygun şekilde bağımsız bir Python motoru olarak yeniden üretmeyi amaçlamaktadır.

---

## Durum

| Aşama | Durum |
|---|---|
| Oracle veri toplama (Oturum 1) | ✅ 44 ekran görüntüsü, 44 satır |
| Bağımsız çapraz kontrol | ✅ a priori 30/30, post hoc 12/12 eşleşti |
| A priori davranışı | ✅ `SPEC.md` bölüm 3 |
| Post hoc davranışı | ✅ `SPEC.md` bölüm 4 — N'in katı olmaması, `N ≤ k` hatası, `f = 0` dahil |
| Motor / CLI (Grup 2) | ✅ `grup2_python/anova_power.py` (stdin JSON → tek satır JSON) |
| Motor ↔ oracle diferansiyel test | ✅ 42/42 (2 satır atlandı) — `tests/diferansiyel_test.py` |
| Geçersiz girdi (a priori) | ❌ hâlâ yok — `EKSIK_VAKALAR.md` bölüm 2 |
| Gösterim biçimi kuralı | ⚠️ BELİRSİZ — `LEDGER.md` bölüm 2.4 |
| REA (ikili inceleme) | ❌ yapılmadı — `LEDGER.md` `[REA]` tablosu boş |
| Ödev CLI sözleşmesi (`--test ... --mode ...` bayrakları) | ❌ henüz yok — bayraklı sarmalayıcı gerekli |

---

## Proje Görev Dağılımı ve Temiz Oda (Clean Room) Metodolojisi
Grubumuz, tersine mühendislik sürecinde kodun orijinalliğini ve bağımsızlığını garanti etmek adına kendi içinde iki alt gruba ayrılmıştır:

1. **Alt Grup 1 (Analiz, Oracle Veri Tabanı ve SPEC Hazırlığı):**
   * Bilgisayarlarına G*Power yazılımını kurmuş ve farklı değerler ($\alpha$, Güç, Etki Büyüklüğü $f$, Grup Sayısı $k$) girerek deneyler gerçekleştirmiştir.
   * G*Power'ın hesapladığı Örneklem Büyüklüğü ($N$) ve Kritik $F$ değerlerini not ederek `oracle/` dizini altına (`anova_oneway.csv` ve ekran görüntüleri) eklemiştir.
   * Aracın yuvarlama kurallarını ve davranışlarını dökümante ederek `SPEC.md` belgesini hazırlamışlardır.

2. **Alt Grup 2 (Yapay Zeka ile İzolasyonlu Kodlama):**
   * Temiz Oda prensipleri gereği **G*Power yazılımını hiçbir şekilde açmamış, görmemiş ve doğrudan incelememiştir.**
   * Sadece Alt Grup 1'in hazırladığı `SPEC.md` teknik şartnamesini kullanarak Yapay Zeka (LLM) aracılığıyla Python kodunu (`anova_power.py`) ürettirmiş ve test etmiştir (`grup2_python` dizini).

---

## 1. Görev Doğrulama: Motorun Doğruluğunun Kanıtlanması
Motorun doğruluğu 3 kademeli test mekanizması ile sınanmıştır:

* **Oracle (Referans) Veri Seti:** G*Power GUI arayüzünden alınan ekran görüntüleri ve bunlardan çıkarılan referans veriler (`oracle/anova_oneway.csv`) mutlak doğru kabul edilmiştir.
* **SPEC Vektörleri Testi:** `grup2_python/test_anova_power.py`, SPEC içindeki 6 a priori ve 9 post hoc vektörünü, 6 kritik F değerini, sınır/hata durumlarını ve CLI sözleşmesini sınar (6 test yöntemi başarılı; bkz. `grup2_python/TEST_SONUCLARI.md`).
* **Oracle Diferansiyel Testi:** `tests/diferansiyel_test.py`, `oracle/anova_oneway.csv` satırlarını motora otomatik girdi olarak verir. Sonuç: okunabilir **42 satırın 42'sinde eşleşme** (a priori'de toplam N tam eşleşme; her satırda `actual_power` 1e-6 içinde). Hata kutusu gösteren 2 satır (id 37, 38; `f` okunamadığı için) atlanmıştır.

> **Önemli sınır:** Yukarıdaki oran *görünür* oracle verisi üzerindedir. Hocanın gizli test vektörleri ayrıdır; onlardaki %90 kapısı için bağımsız bir güvence verilmemektedir. Geçersiz girdi davranışı ve gösterim biçimi hâlâ eksiktir (bkz. Durum).

---

## Tersine Mühendislik Bulguları (Belgelenmemiş Davranışlar)
*G*Power belgelerinde açıkça yazmayan, Alt Grup 1'in oracle analizlerinde gözlenen özel durumlar:*

> **Kanıt düzeyi uyarısı:** `LEDGER.md` `[REA]` tablosu henüz boştur; ikili (binary) incelemesi yapılmamıştır. Bu nedenle aşağıdaki maddeler **`[AJAN]`** düzeyindedir (oracle verisinden çıkarım; diferansiyel testle sınanmış, fonksiyon adresi/dize kanıtı yok). Ghidra/REA ile doğrulanınca `[REA]`'ya yükseltilecektir.

* **[AJAN] Yuvarlama Davranışı:** G*Power, N (örneklem sayısı) değerini hesaplarken standart matematiksel yuvarlama yerine, belirli kritik F değer sınırlarında yukarı tavan (`ceil`) fonksiyonunu özel bir hassasiyet parametresiyle uygular.
* **[AJAN] Alt Sınır Toleransı:** Etki büyüklüğü ($f$) sıfıra çok yakın değerler aldığında motorun serbestlik derecesi (df) hesaplamalarında uyguladığı özel bir alt sınır mevcuttur.

---

## Proje Dizin Yapısı

```
SPEC.md              davranış sözleşmesi (Gherkin), kod içermez
LEDGER.md            kanıt defteri: [DOK] / [AJAN] / [REA]
GRUP1_GOREV.md       Alt Grup 1'in analiz ve veri toplama adımları
EKSIK_VAKALAR.md     G*Power'da çalıştırılacak eksik girdi vektörleri
HALLUCINATIONS.md    ajan hatalarının dürüst kaydı
AGENT_COST.md        ajan adımları ve maliyet kaydı
prompts/             her oturumun ilk promptu
oracle/              kâhin verisi
  anova_oneway.csv     44 satır (30 a priori + 14 post hoc)
  RENAME_MAP.csv       eski ad → v{id}.png eşlemesi
  screenshots/         v1.png … v44.png
grup2_python/        Alt Grup 2'nin temiz oda ile ürettiği motor (anova_power.py) ve testleri
src/                 ödev şablonundaki yeniden yazım klasörü (motor şu an grup2_python/ altında)
tests/               diferansiyel test (diferansiyel_test.py) ve uyum_raporu.md
```

---

## Kurulum
Python 3.10+ gerekir. Windows / PowerShell:

```powershell
cd grup2_python
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Linux / macOS:

```bash
cd grup2_python
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

## Çalıştırma
Motor, standart girdiden **tek bir JSON nesnesi** okur ve standart çıktıya **tek satır JSON** yazar. Başarıda çıkış kodu 0, geçersiz girdide `{"error":"..."}` ve çıkış kodu 1'dir.

**A priori (N hesapla):**
```powershell
'{"mode":"a_priori","f":0.25,"alpha":0.05,"power":0.8,"groups":3}' | .\.venv\Scripts\python.exe anova_power.py
```
Beklenen çıktı:
```json
{"lambda":9.9375,"critical_f":3.0540042,"df1":2,"df2":156,"actual_power":0.8048873,"total_n":159}
```

**Post hoc (güç hesapla):**
```powershell
'{"mode":"post_hoc","f":0.25,"alpha":0.05,"total_n":100,"groups":3}' | .\.venv\Scripts\python.exe anova_power.py
```

**Girdi alanları:**

| Alan | Mod | Açıklama |
|---|---|---|
| `mode` | ikisi | `a_priori` veya `post_hoc` |
| `f` | ikisi | Etki büyüklüğü (Cohen's f) |
| `alpha` | ikisi | Anlamlılık düzeyi |
| `groups` | ikisi | Grup sayısı k |
| `power` | a_priori | Hedef güç |
| `total_n` | post_hoc | Toplam örneklem büyüklüğü |

**Testleri çalıştırma** (repo kökünden, bağımlılıklar kuruluyken):
```bash
python -m unittest discover -s grup2_python -p test_anova_power.py -v
python tests/diferansiyel_test.py
```

> **Not:** Ödevdeki örnek CLI sözleşmesi (`--test ... --mode ...` bayrakları) ile bu motorun JSON-stdin arayüzü henüz aynı değildir. Gizli vektörlerin otomatik koşturulması için bayraklı bir sarmalayıcı (wrapper) eklenmesi gerekir.

---

## REA / Ghidra Kontrolü
Ödev gereği, ajana *"REA araçları ve Ghidra sağlayıcısı bu oturumda kullanılabilir mi?"* sorusunun cevabının ekran görüntüsü buraya eklenecektir:

_(ekran görüntüsü eklenecek: `docs/rea_kontrol.png`)_

## Sürüm Bilgisi

| | |
|---|---|
| Referans yazılım | G*Power 3.1.9.7 (Windows) |
| İşletim sistemi | Windows |
| Ekran görüntüsü tarihi | 2026-10-22 |
| Motor | `grup2_python/anova_power.py` (Python 3.10+, SciPy) |
| `GPower.exe` SHA-256 | _(doldurulacak — Windows'ta `Get-FileHash .\GPower.exe -Algorithm SHA256` ile hesaplanıp yazılacak)_ |

> SHA-256 bilerek boş bırakıldı; değeri uydurmak yerine, dosyanın bulunduğu makinede hesaplanıp buraya yazılmalıdır. İkili dosya repoda değildir (`.gitignore`).

## Demo Video
60 saniyelik CLI demosu: _(link eklenecek)_

---

## Bonus Katmanlar

| Katman | Durum | Not |
|---|---|---|
| MCP sunucusu (+15) | yapılmadı | |
| AI ajanı (+10) | yapılmadı | |
| REA / ikili inceleme kanıtı | planlandı | `LEDGER.md` `[REA]` tablosu |
| Diferansiyel test (motor ↔ oracle) | aktif | `tests/diferansiyel_test.py` |
| Halüsinasyon kaydı | aktif | `HALLUCINATIONS.md` |
| Ajan maliyet kaydı | aktif | `AGENT_COST.md` |

---

## Veri ve Etik
* `GPower.exe` ve kurulum dosyaları repoya **girmez** (`.gitignore`).
* Decompile çıktısı hiçbir dosyaya **konmaz**; `LEDGER.md`'de yalnızca kısa alıntı ve fonksiyon adresi bulunabilir.
* Projede gerçek hasta verisi **yoktur**; tüm senaryolar kurgusaldır.
* Oturum 1 (inceleme) ile Oturum 2 (motor yazımı) **temiz oda** kuralıyla ayrılmıştır.
* Bu proje G*Power'ın bir parçası değildir ve onunla ilişkili değildir; G*Power yalnızca davranış referansı (kâhin) olarak kullanılmıştır.

---

## Atıf
Referans alınan yazılım:

> Faul, F., Erdfelder, E., Lang, A.-G., & Buchner, A. (2007). G*Power 3: A flexible statistical power analysis program for the social, behavioral, and biomedical sciences. *Behavior Research Methods, 39*(2), 175–191.

> Faul, F., Erdfelder, E., Buchner, A., & Lang, A.-G. (2009). Statistical power analyses using G*Power 3.1: Tests for correlation and regression analyses. *Behavior Research Methods, 41*(4), 1149–1160.

Etki büyüklüğü `f`'nin tanımı için:

> Cohen, J. (1988). *Statistical Power Analysis for the Behavioral Sciences* (2nd ed.). Lawrence Erlbaum Associates.
