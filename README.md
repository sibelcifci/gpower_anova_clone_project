# ANOVA Power Clone - Clean Room Reverse Engineering

Tek yönlü ANOVA (F testi, sabit etkiler, omnibus) için güç analizi motorunun davranışsal klonu. YZM301 "Teardown Sprint" ödevi.

Referans alınan yazılım **G*Power 3.1.9.7 (Windows)**'tur. Bu proje G*Power'ın bir parçası değildir, onunla ilişkili değildir ve onun adını taşımaz.

**Grup Bilgileri:** Grup 17 (k3)
* SİBEL ÇİFCİ
* GÖNÜL NAZİRE AYDIN
* CEM ERŞEN
* KORKUT ŞAHAN

> **Katmanlar:** Temel Katman (CLI) ✅, MCP sunucusu (+15) ✅, AI ajanı (+10) ✅.
> Hesap mantığı tek motordadır (`src/anova_power/core.py`); CLI, MCP ve ajan bu
> motoru çağıran ince katmanlardır (ödev kuralı 3).

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
| Motor (tek kaynak) | ✅ `src/anova_power/core.py` |
| CLI (bayraklı + stdin JSON) | ✅ `src/anova_power/cli.py` — `python -m anova_power --mode ...` |
| MCP sunucusu (+15) | ✅ `src/anova_power/mcp_server.py` — bağımlılıksız stdio JSON-RPC |
| AI ajanı (+10) | ✅ MCP üzerinden doğal dil — `.mcp.json` |
| Motor ↔ oracle diferansiyel test | ✅ 42/42 eşleşme + 2/2 doğru red — `tests/diferansiyel_test.py` |
| Geçersiz girdi (a priori) | ❌ hâlâ yok — `EKSIK_VAKALAR.md` bölüm 2 |
| Gösterim biçimi kuralı | ⚠️ BELİRSİZ — `LEDGER.md` bölüm 2.4 |
| REA (ikili inceleme) | ✅ 5 satır kanıtlandı, 8 TODO — `LEDGER.md` bölüm 4 |
| Ödev CLI sözleşmesi (`--mode ...` bayrakları) | ✅ `src/anova_power/cli.py` |

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

Tam liste ve bayt offsetleri: `LEDGER.md` bölüm 4 (`[REA]`) ve 4.1.
Aşağıdakiler **ikiliden dize aramasıyla** kanıtlanmıştır; araç `tools/rea_strings.py`.

* **[REA] Mesajlar çalışma anında parçalardan birleştiriliyor.** `Please note`
  uyarısı ikilide tek parça hâlinde **yoktur**; beş ayrı sabit (`1856476`–`1856584`)
  birleştirilir. Tam metin araması bu yüzden sonuç vermez — kılavuzda bulunmayacak
  bir uygulama ayrıntısı.
* **[REA] Aynı kısıt için iki ayrı hata metni var.** Ana pencere birleştirmeli
  (`1856161` + `1856536`), etki büyüklüğü diyaloğu ise sabit metin (`1907320`).
* **[REA] Diyalog başlıkları sabit, dört elemanlı bir küme** (`1951204`–`1951488`):
  `Input error`, `Please note`, `Interruption`, `Internal math error`. Yani
  `Input error`/`Please note` ayrımı hesabın durup durmasının sonucu değil,
  çağıranın seçimi.
* **[REA] Kuantiller sınırlı iteratif aramayla çözülüyor**, kapalı formla değil:
  `answer below lower search bound` / `above upper search bound` (`1846184`, `1846240`).
* **[REA] Sayı biçimleme** `%.7f` (`1943636`) ve `%.5g` (`1846016`) dizelerini
  kullanıyor; `%.6f`/`%.5f`/`%.3f` ikilide **yok**. Ekrandaki 7 ondalıklı gösterim
  `%.7f` ile, `LEDGER.md` 2.4'teki üç karşı örnek (`0`, `120`, `199.5`) `%.5g` ile
  uyumlu. İkisi arasında **seçimi yapan koşul** hâlâ kanıtlanmadı (B-09 kısmen).

> **Kanıt düzeyi dürüstlüğü:** Yukarıdakiler dize kanıtına dayanır. Hesap
> mantığının kendisi (`lambda = f^2 * N`, en küçük N araması, `f = 0` dalı) **kod
> akışı incelemesi** gerektirir ve hâlâ `[AJAN]` düzeyindedir; `LEDGER.md` bölüm
> 4'te REA-01, REA-02, REA-03, REA-09 olarak **TODO** işaretlidir. Kanıtsız
> `[REA]` yazılmamıştır.

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
src/anova_power/     TEK MOTOR ve ince katmanlar
  core.py              hesap motoru (başka hiçbir yerde hesap yok)
  cli.py               CLI katmanı: bayraklı + stdin JSON
  mcp_server.py        MCP sunucusu (stdio JSON-RPC, bağımlılıksız)
tools/rea_strings.py REA aracı: ikilide dize araması (ikili repoya girmez)
grup2_python/        Alt Grup 2'nin temiz oda teslimi; anova_power.py artık
                     src/'teki motora yönlendiren kabuk (özgün hâli: 4326cd9)
tests/               diferansiyel_test.py (motor ↔ oracle) ve uyum_raporu.md
.mcp.json            MCP sunucusunun Claude Code/Desktop kaydı
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

### Bayraklı CLI (ödev sözleşmesi)

Gizli vektörlerin otomatik koşturulması için bayraklı giriş yolu eklendi. Aynı
motoru çağırır, çıktı biçimi birebir aynıdır:

```bash
python -m anova_power --test anova --mode a_priori --f 0.25 --alpha 0.05 --power 0.80 --groups 3
python -m anova_power --mode post_hoc --f 0.25 --alpha 0.05 --total-n 100 --groups 3
```

`PYTHONPATH=src` gerekir (veya repo kökünden `src` çalışma yoluna eklenir).
`--total_n`, `-n`, `-k`, `--type`, `--effect-size` eşanlamlıları da kabul edilir.

### MCP sunucusu (+15)

```bash
echo '{"jsonrpc":"2.0","id":1,"method":"tools/list"}' | PYTHONPATH=src python -m anova_power.mcp_server
```

İki araç sunar: `anova_a_priori` ve `anova_post_hoc`. Üçüncü parti bağımlılık
yoktur. Claude Code / Claude Desktop için kayıt `.mcp.json` dosyasındadır.

### AI ajanı (+10)

`.mcp.json` yüklü bir istemcide doğal dil yeterlidir; ajan MCP araçlarını çağırır:

> "Üç gruplu bir çalışma planlıyorum, orta büyüklükte etki bekliyorum,
> %80 güç istiyorum. Kaç denek gerekir?"

Ajan `anova_a_priori` aracını `f=0.25, alpha=0.05, power=0.80, groups=3` ile
çağırır ve `total_n = 159` döner. Örnek döküm: `docs/ajan_demo.md`.

---

## REA / Ghidra Kontrolü

Bu oturumda **Ghidra kullanılmadı**; REA, standart kütüphaneyle yazılmış bir dize
arama aracıyla yapıldı: `tools/rea_strings.py`. Gerekçe: aranan kanıt (hata/uyarı
metinleri, biçimleme format dizeleri, diyalog başlıkları) `.rdata` bölümündeki
sabit dizelerdir; bunlara ulaşmak için disassembly gerekmez ve decompile çıktısı
üretilmediği için **kural 4** kendiliğinden korunur.

```
python tools/rea_strings.py "<GPowerNT.exe yolu>"
```

Çıktı doğrudan `LEDGER.md` bölüm 4'teki tabloyu üretir. Kod akışı gerektiren
iddialar (REA-01, REA-02, REA-03, REA-09) bu araçla **kanıtlanamaz** ve bilerek
TODO bırakılmıştır — Ghidra ile ileri inceleme gerekir.

_(ödev gereği ekran görüntüsü: `docs/rea_kontrol.png` — eklenecek)_

## Sürüm Bilgisi

| | |
|---|---|
| Referans yazılım | G*Power 3.1.9.7 (Windows) |
| İşletim sistemi | Windows |
| Ekran görüntüsü tarihi | 2026-10-22 |
| Motor | `grup2_python/anova_power.py` (Python 3.10+, SciPy) |
| İncelenen ikili | `GPowerNT.exe` (2.287.616 bayt, 32-bit) |
| `GPowerNT.exe` SHA-256 | `c63e6a133eb6372932f810c08cc33dc35a06d1ddb658f897bd6c34a754efc812` |

> SHA-256, REA oturumunda ikilinin bulunduğu makinede hesaplandı. Kurulumun
> dağıttığı dosyanın adı `GPower.exe` değil **`GPowerNT.exe`**'dir. İkili dosya
> repoda değildir (`.gitignore`); yeniden üretmek için:
>
> ```powershell
> Get-FileHash .\GPowerNT.exe -Algorithm SHA256
> ```

## Demo Video
60 saniyelik CLI demosu: _(link eklenecek)_

---

## Bonus Katmanlar

| Katman | Durum | Not |
|---|---|---|
| MCP sunucusu (+15) | ✅ | `src/anova_power/mcp_server.py`, bağımlılıksız stdio JSON-RPC |
| AI ajanı (+10) | ✅ | MCP üzerinden doğal dil; `.mcp.json`, `docs/ajan_demo.md` |
| REA / ikili inceleme kanıtı | ✅ kısmen | 5 satır kanıtlandı, 8 TODO — `LEDGER.md` bölüm 4 |
| Diferansiyel test (motor ↔ oracle) | aktif | `tests/diferansiyel_test.py` |
| Halüsinasyon kaydı | aktif | `HALLUCINATIONS.md` |
| Ajan maliyet kaydı | aktif | `AGENT_COST.md` |

---

## Veri ve Etik
* `GPower.exe` ve kurulum dosyaları repoya **girmez** (`.gitignore`).
* Decompile çıktısı hiçbir dosyaya **konmaz**; `LEDGER.md`'de yalnızca kısa alıntı ve fonksiyon adresi bulunabilir.
* Projede gerçek hasta verisi **yoktur**; tüm senaryolar kurgusaldır.
* Oturum 1 (inceleme) ile Oturum 2 (motor yazımı) **temiz oda** kuralıyla ayrılmıştır.
* Oturum 3 (REA) motor yazıldıktan **sonra** yapılmıştır; ikiliden elde edilen hiçbir
  bilgi hesap mantığına geri beslenmemiştir. REA bulguları yalnızca `LEDGER.md`'de
  belgelenmiştir.
* Bu proje G*Power'ın bir parçası değildir ve onunla ilişkili değildir; G*Power yalnızca davranış referansı (kâhin) olarak kullanılmıştır.

---

## Atıf
Referans alınan yazılım:

> Faul, F., Erdfelder, E., Lang, A.-G., & Buchner, A. (2007). G*Power 3: A flexible statistical power analysis program for the social, behavioral, and biomedical sciences. *Behavior Research Methods, 39*(2), 175–191.

> Faul, F., Erdfelder, E., Buchner, A., & Lang, A.-G. (2009). Statistical power analyses using G*Power 3.1: Tests for correlation and regression analyses. *Behavior Research Methods, 41*(4), 1149–1160.

Etki büyüklüğü `f`'nin tanımı için:

> Cohen, J. (1988). *Statistical Power Analysis for the Behavioral Sciences* (2nd ed.). Lawrence Erlbaum Associates.
