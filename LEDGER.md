# LEDGER — kanıt defteri

Her iddia bir etiket taşır:

| Etiket | Anlamı | Puan |
|---|---|---|
| `[DOK]` | Resmî belgede/kılavuzda yazıyor | yok |
| `[AJAN]` | Ajanın oracle verisinden çıkarımı — **binary kanıtı yok** | yok |
| `[REA]` | İkili (binary) incelemesiyle kanıtlanmış | **var** |

> **Oturum 3 (REA) yapıldı.** `tools/rea_strings.py` ile `GPowerNT.exe` üzerinde
> dize araması çalıştırıldı: 5 `[REA]` satırı kanıtlandı, 8'i TODO kaldı (kod akışı
> incelemesi gerektiriyor). Decompile/disassembly yapılmadı, ikili repoya konmadı.
> Kanıtsız `[REA]` yazmak kural ihlalidir; TODO satırları bilerek TODO.

**Kanıt tabanı:** `oracle/anova_oneway.csv` — **59 satır / 59 ekran görüntüsü**
(2026-10-26'da 15 satır eklendi: geçersiz girdi vektörleri, id 45–59, `oracle/X_TOPLAMA.md`)

| mod | satır | benzersiz girdi vektörü |
|---|---|---|
| `a_priori` | 43 | 40 |
| `post_hoc` | 16 (12'si çıktı üretti, 4'ü hata) | 13 |

Çapraz kontrol: `tests/uyum_raporu.md` — a priori 30/30, post hoc 12/12 eşleşti.

---

## 1. `[DOK]` — belgeye dayalı iddialar

**Bu oturumda doldurulmadı.** G*Power kılavuzu / Faul, Erdfelder, Lang ve
Buchner (2007, 2009) makaleleri açılmadı, dolayısıyla belgeye atıf yapılamaz.
Hafızadan "kılavuzda şöyle yazıyor" demek uydurma olurdu.

| # | kontrol edilecek iddia | nereye bakılacak | durum |
|---|---|---|---|
| DOK-01 | Tek yönlü ANOVA için nonsantralite `λ = f² · N` | Faul vd. (2007), ANOVA bölümü | TODO |
| DOK-02 | `f` ile `η²` arasındaki ilişki ve `f` tanımı | Cohen (1988) / kılavuz | TODO |
| DOK-03 | A priori modda toplam N'nin gruplara eşit dağıtıldığı | kılavuz | TODO |
| DOK-04 | Grup başına minimum gözlem sayısı kuralı | kılavuz | TODO |
| DOK-05 | Post hoc'ta "average group size" ifadesinin tam anlamı | kılavuz | TODO |

---

## 2. `[AJAN]` — oracle verisinden gözlenen desenler

Hepsi **yalnızca gözlemdir**. Motorun içeride bu formülü kullandığının değil,
girdi–çıktı davranışının bu formülle **tutarlı olduğunun** kanıtıdır.
Her biri **diferansiyel testle sınanmalı** ve REA ile doğrulanmalıdır.

### 2.1 Her iki modda da geçerli

| # | iddia | tuttuğu satır | nasıl ölçüldü |
|---|---|---|---|
| AJ-01 | `df1 = k − 1` | **42/42** | CSV `assert` (çıktı üreten tüm satırlar) |
| AJ-02 | `df2 = N − k` | **42/42** | CSV `assert`. N, k'nın katı olmasa bile tutuyor (id 32, 35, 39) |
| AJ-03 | `λ = f² · N` | **42/42** | `\|λ_ekran − f²N\| < 5e−7`. Post hoc'ta **girilen N** kullanılır, yuvarlanmış bir N değil |
| AJ-07 | Kritik F = merkezî F dağılımının üst-α kuantili, `(df1, df2)` ile | **42/42** | `scipy.stats.f.isf`, en büyük sapma 4.8e−08 |
| AJ-08 | Güç = merkezî olmayan F'nin kritik F üstünde kalan kütlesi | **42/42** | `scipy.stats.ncf.sf`, en büyük sapma 4.8e−08 |
| AJ-10 | Grafik başlığındaki `critical F = …` etiketi, alandaki değerin **6 anlamlı basamağa** yuvarlanmış ve sondaki sıfırları atılmış hâlidir (`%.6g`) | **42/42** | etiket ↔ alan karşılaştırması; **REA-14 ile ikilide doğrulandı** |
| AJ-11 | Ekranda **grup başına n alanı yoktur** | **44/44** | yokluk gözlemi; `n_per_group` sütunu türetilmiştir |
| AJ-12 | Aynı girdi vektörü daima aynı çıktıyı verir (determinizm) | **6/6 tekrar grubu** | id 2↔20, 3↔23, 15↔30 (a priori); 32↔33, 35↔36, 39↔40 (post hoc) |

### 2.2 Yalnızca a priori

| # | iddia | tuttuğu satır | nasıl ölçüldü |
|---|---|---|---|
| AJ-04 | Toplam N daima grup sayısının tam katıdır (`N mod k = 0`) | **30/30** | CSV `assert`. **Bu kural post hoc'ta geçerli DEĞİLDİR** (aşağı bak) |
| AJ-05 | N, hedef gücü sağlayan **en küçük** katıdır (`N − k` hedefin altında kalır) | **30/30** | `tests/uyum_raporu.md` |
| AJ-06 | `actual power ≥ istenen güç` | **30/30** | `tests/uyum_raporu.md` |

### 2.3 Yalnızca post hoc — YENİ

| # | iddia | tuttuğu satır | nasıl ölçüldü |
|---|---|---|---|
| AJ-13 | Post hoc'ta `Power` bir **çıktıdır**, `Total sample size` ise **girdidir**; ekranda `Power` kutusu girdi bölümünden çıkıp çıktı bölümüne geçer | **14/14** | doğrudan okuma |
| AJ-14 | Post hoc, N grup sayısının katı olmasa bile **hesabı yapar**; bir `Please note` bilgi kutusu gösterir ama sonucu üretir | **3/3** (id 32, 35, 39) | kutu metni okundu |
| AJ-15 | O bilgi kutusu "analysis was based on the average group size" dese de **hesap değişmez**: `df2 = N − k` ve `λ = f² · N` girilen N ile aynen kullanılır | **3/3** | id 32: N=100, k=3 → df2=97, λ=6.25 = 0.0625·100 |
| AJ-16 | `N ≤ k` olduğunda hesap **yapılmaz**: `Input error` kutusu çıkar ve **bütün çıktı alanları `?` olur** | **2/2** (id 37: N=3, id 38: N=2) | doğrudan okuma |
| AJ-17 | `f = 0` **hata değildir**: λ = 0 olur ve güç **tam olarak α'ya eşit** çıkar | **1/1** (id 43: α=0.05 → güç `0.0500000`) | doğrudan okuma |
| AJ-18 | Çok büyük etki büyüklüğünde güç `1.0000000` olarak gösterilir (1'e yuvarlanır) | **1/1** (id 44: f=2.0, N=30) | doğrudan okuma |
| AJ-19 | **Gidiş–dönüş tutarlılığı:** a priori'nin bulduğu N post hoc'a verildiğinde, a priori'nin `actual power` değeri **birebir** geri gelir | **2/2** | id 15→31 (159 → 0.8048873), id 1→34 (280 → 0.9509908) |

### AJ-04 hakkında — önemli düzeltme

"Toplam N, grup sayısının katıdır" kuralı **modun kendisine ait değildir**;
yalnızca a priori'nin *ürettiği* N için geçerlidir. Post hoc'ta kullanıcı
istediği N'i girebilir ve program bunu kabul eder (id 32: N=100, k=3).
Motor bu ayrımı yapmazsa post hoc'ta yanlış davranır.

### AJ-05 hakkında — hâlâ ayırt edilemiyor

30 a priori satırının hiçbirinde yuvarlama payı büyük değil ve hiçbiri alt
sınıra değmiyor. Dolayısıyla:

- **Grup başına minimum gözlem sayısı (a priori) hâlâ bilinmiyor.**
- "Tavana yuvarlama" ile "bir sonraki kata atlama" bu veriyle **ayırt edilemez**.

Ayırt edici vektörler: `EKSIK_VAKALAR.md` → bölüm 6.

> Post hoc tarafında alt sınır **biliniyor**: `N > k` (AJ-16). Bu, a priori'nin
> alt sınırı hakkında bilgi vermez; iki mod ayrı doğrulama yapıyor olabilir.

### AJ-12 hakkında uyarı

44 görselin tamamı **tek kaynaktan** (grup1, tek kurulum) gelmektedir.
AJ-12 yalnızca *aynı kurulumda tekrarlanabilirliği* gösterir;
**farklı makine/kurulumlarda aynı sonucun çıkacağının kanıtı değildir.**

---

## 2.5 Girdi doğrulama — YENİ (id 45–59)

2026-10-26'da toplanan 15 vektör. Hepsi `[AJAN]`: ekrandan okunan davranış,
ikili kanıtı henüz yok. `[REA]` adayları bölüm 4.2'de.

| # | iddia | tuttuğu satır | nasıl ölçüldü |
|---|---|---|---|
| AJ-20 | Aralık hataları **tek kalıptan** üretilir: `"<Alan> is outside the admissible range (<alt>, <üst>)."` | **10/10** | id 45–52, 58, 59 |
| AJ-21 | `α` ve `Power` için aralık **`(1e-07, 1)`**; üst sınır **dahil değil** | **6/6** | id 47–52; `α=1` (id 48) ve `Power=1` (id 50) reddedildi |
| AJ-22 | **`f` alanının aralığı moda bağlıdır:** a priori `(1e-06, 50)`, post hoc `(0, 50)` | **3/3** | id 45, 46 (a priori) ↔ id 58 (post hoc) |
| AJ-23 | **Gösterilen aralık ile davranış çelişir:** post hoc mesajı `(0, 50)` der ama `f = 0` kabul edilir | **1 çelişki** | id 58 mesajı ↔ id 43 sonucu (güç = α = 0.0500000) |
| AJ-24 | `groups < 2` aralık kalıbını **kullanmaz**, ayrı metin verir: `"There must be at least 2 groups."` | **3/3** | id 53 (k=1), 54 (k=0), 55 (k=−3) |
| AJ-25 | **Tam sayı olmayan grup sayısı sessizce kabul edilir:** hata ve **uyarı kutusu olmadan** hesap yapılır | **2/2** | id 56 (`2.5` → k=3, N=159) ve id 60 (`2.4` → k=2, N=128) |
| AJ-27 | Yuvarlama **en yakına, yarımda yukarı**dır — ceil değildir | **2/2** | id 60'ta `df1=1` (k=2); ceil olsaydı k=3, N=159 çıkardı |
| AJ-26 | `α` kutusuna **harf yazılabilir**; sayısal olmayan girdi için ayrı mesaj yoktur, aralık hatasına katlanır | **1/1** | id 57 (`abc`) |

### Neden bu satırlar kıymetli

- **AJ-22 ve AJ-23 kılavuzda yazamaz.** Biri aynı alanın iki moda göre farklı
  doğrulandığını, diğeri programın **kendi hata mesajıyla tutarsız** olduğunu
  gösteriyor. İkincisi bir uygulama kusurudur; belgeye girmesi beklenmez.
- **AJ-25 sessiz veri dönüşümüdür.** G*Power, `N`'in `k`'nın katı olmadığı
  durumda kullanıcıyı `Please note` ile uyarır (AJ-14); burada ise hiç
  uyarmaz. Aynı programda iki farklı politika.
- **AJ-21'in yönü ölçüldü:** aralık gösterimi açık ve gerçekten açık.
  Alt sınırların tam değerleri (`1e-06`, `1e-07`) **denenmedi** — kapsam
  burada bitiyor, genelleme yapılmadı (H1-02'nin dersi).

> **ÇÖZÜLDÜ (id 60).** `groups = 2.4` → N=128, `df1 = 1`, yani k=2. Yukarı
> yuvarlama olsaydı k=3 / N=159 çıkardı. Kural: en yakına yuvarlama, yarımda
> yukarı (AJ-27). Motor bunu uyguluyor; `core.py`'deki TODO kaldırıldı.
> Yan bulgu: id 60'ta λ tam sayı **8** olmasına rağmen `8.0000000` diye
> 7 ondalıkla gösterildi — bölüm 2.4'teki gösterim tartışmasını a priori
> tarafında destekler (karşı örnekler hâlâ post hoc'tan geliyor).

## 2.4 Gösterim biçimi — ESKİ İDDİA ÇÜRÜDÜ, ŞU AN BELİRSİZ

Önceki sürümde "λ, kritik F ve güç alanları **daima** 7 ondalık basamakla
gösterilir (29/29)" yazıyordu. **Bu genelleme yanlıştı.** 29 a priori satırda
tutuyordu ama yeni veride üç karşı örnek çıktı:

| id | alan | gösterilen | 7 ondalık olsaydı |
|---|---|---|---|
| 43 | λ | `0` | `0.0000000` |
| 44 | λ | `120` | `120.0000000` |
| 39, 40 | kritik F | `199.5` | `199.5000000` |

Ama tam sayı olmak tek başına yeterli değil — a priori'de tam sayı λ'lar
**7 ondalıkla** gösteriliyor:

| id | λ | gösterilen |
|---|---|---|
| 4 | 8 | `8.0000000` |
| 13 | 19 | `19.0000000` |
| 18 | 21 | `21.0000000` |

**Kesin kuralı bu veriden çıkaramıyorum.** İki aday açıklama:

| hipotez | açıkladığı | açıklayamadığı |
|---|---|---|
| **H-A: moda bağlı** — post hoc'ta tam sayılar sade gösterilir | id 43 (`0`), id 44 (`120`) | id 39/40: `199.5` tam sayı değil, yine de kısaldı |
| **H-B: alan genişliğine bağlı** — 10 karakteri aşan değer kısaltılır | `199.5000000` (11 krk), `120.0000000` (11 krk) kısaldı; `17.5000000` (10 krk) kısalmadı | id 43: `0.0000000` 9 karakter, kısalmamalıydı (sıfır özel durum olabilir) |

H-B daha çok gözlemi açıklıyor ama **ikisi de doğrulanmadı**.
Ayırt edici iki vektör `EKSIK_VAKALAR.md` → bölüm 10'da.

**Kesin olarak bilinen:** `Total sample size`, `Numerator df` ve
`Denominator df` **her zaman** tam sayı gösterilir — 42/42.

---

## 3. Hâlâ BELİRSİZ olanlar

| # | belirsizlik | durum |
|---|---|---|
| B-01 | Post hoc modun davranışı | **büyük ölçüde ÇÖZÜLDÜ** — AJ-13…AJ-19. Kalan: post hoc'ta α sınırları denenmedi |
| B-02 | Geçersiz girdide ne olur | **kısmen çözüldü** — `N ≤ k` için biliniyor (AJ-16). α=0/1, güç=1, k=1, negatif değerler **hâlâ denenmedi** |
| B-03 | `f = 0` durumunda güç | **ÇÖZÜLDÜ** — güç tam olarak α (AJ-17) |
| B-04 | Güç ≤ α istendiğinde (a priori) ne olur | **hâlâ bilinmiyor** |
| B-05 | A priori'de grup başına minimum gözlem | **hâlâ bilinmiyor** |
| B-06 | Post hoc'ta N, k'nın katı değilken df2 | **ÇÖZÜLDÜ** — `df2 = N − k`, hesap değişmiyor (AJ-15) |
| B-07 | Girdi alanlarının kabul ettiği basamak sayısı / iç yuvarlama | hâlâ bilinmiyor |
| B-08 | Sayıların iç gösterimi (double mu, long double mu) | yalnızca REA ile görülebilir |
| B-09 | ondalık gösterim kuralı (bölüm 2.4) | **KISMEN ÇÖZÜLDÜ** — `%.7f` ve `%.5g` ikilide bulundu (REA-10); seçim koşulu açık |
| B-10 | `Input error` ile `Please note` kutularının ayrım ölçütü | **ÇÖZÜLDÜ** — sabit başlık kümesi, çağıran seçiyor (REA-12) |

---

## 4. `[REA]` — ikili inceleme kanıtı

**Araç:** `tools/rea_strings.py` — dize araması. Decompile/disassembly **yapılmaz**.
**İkili:** `GPowerNT.exe` (dikkat: dosya adı `GPower.exe` **değil**), 2.287.616 bayt, 32-bit MSVC.
**SHA-256:** `c63e6a133eb6372932f810c08cc33dc35a06d1ddb658f897bd6c34a754efc812`

İkili repoda **yok** (`.gitignore`). Tablo yeniden üretilebilir:

```
python tools/rea_strings.py "<GPowerNT.exe yolu>"
```

Kural gereği burada yalnızca **bayt offseti + kısa alıntı** vardır.

| id | iddia | offset (kodlama) | durum |
|---|---|---|---|
| REA-07 | AJ-16 — `N <= k` hata metni | `1856161`, `1856400` (ascii); `1907320` (utf16) | **KANITLANDI** |
| REA-08 | AJ-14/AJ-15 — `Please note` uyarı metni | `1856476`–`1856584` (ascii, 5 parça) | **KANITLANDI** |
| REA-10 | B-09 — sayı biçimleme yordamı | `1846000`–`1846016`, `1943636` | **KISMEN** |
| REA-12 | B-10 — diyalog başlığı ayrımı | `1951204`–`1951488` (utf16) | **KANITLANDI** |
| REA-13 | REA-04/05 — kuantil yordamının biçimi | `1846132`–`1846240` (ascii) | **KANITLANDI (dolaylı)** |
| REA-14 | AJ-10 — grafik etiketi 6 anlamlı basamak | `1872531` (ascii `%.6g`) | **KANITLANDI** |
| REA-01 | AJ-03 (`lambda = f^2 * N`) motorda böyle hesaplanıyor | — | TODO (kod akışı gerekir) |
| REA-02 | AJ-04 (a priori'de N, k'nın katına yuvarlanıyor) | — | TODO (kod akışı gerekir) |
| REA-03 | AJ-05 (en küçük N araması) — arama mı, kapalı form mu | — | TODO (kod akışı gerekir) |
| REA-04 | AJ-07 (kritik F yordamı) | kısmen REA-13 | TODO |
| REA-05 | AJ-08 (merkezî olmayan F kuyruk olasılığı) | kısmen REA-13 | TODO |
| REA-06 | B-05 (a priori'de grup başına minimum gözlem sabiti) | — | TODO |
| REA-09 | AJ-17 (`f = 0` özel durum mu) | — | TODO (kod akışı gerekir) |
| REA-11 | B-08 (kayan nokta tipi) | — | TODO |

### 4.2 Yeni `[REA]` adayları (id 45–59'dan)

Aşağıdaki dizeler ekranda **birebir okundu**; ikilide aranmaları hâlinde
doğrudan `[REA]` kanıtına dönüşürler. Araç hazır: `--ara` veya `--tara`.

| id | aranacak dize | hangi iddiayı kanıtlar | durum |
|---|---|---|---|
| REA-15 | `is outside the admissible range` | AJ-20 — kalıp tek parça mı, çalışma anında mı birleşiyor (REA-08'deki gibi) | TODO |
| REA-16 | `1e-06`, `1e-07`, `50` sabitleri | AJ-21/AJ-22 — sınırlar sabit mi, moda göre iki ayrı sabit mi | TODO |
| REA-17 | `There must be at least 2 groups` | AJ-24 — ayrı doğrulama yolu | TODO |
| REA-18 | `Effect size f`, `Alpha`, `Power` alan adları | AJ-20 — alan adı mesaja çalışma anında mı yerleştiriliyor | TODO |

Çalıştırma:

```
python tools/rea_strings.py "<GPowerNT.exe yolu>" --ara "is outside the admissible range" --ara "There must be at least 2 groups"
python tools/rea_strings.py "<GPowerNT.exe yolu>" --tara --en-fazla 40 > rea_kesif.md
```

### REA-07 — hata metninin İKİ varyantı var

| offset | kodlama | alıntı |
|---|---|---|
| `1856161` | ascii | `Sample size must be greater than` |
| `1856400` | ascii | `Total sample size must be greater than` |
| `1856536` | ascii | `the number of groups (` |
| `1907320` | utf16 | `The total sample size must be greater than the number of groups` |
| `1896904` | utf16 | `The size of each group must be greater or equal 1` |

Ana pencere metni **birleştirmeli**: `Sample size must be greater than` +
` the number of groups (` + k + `)`. id 37/38'de ekrandan okunan
`Sample size must be greater than the number of groups (3).` metni bununla
**birebir doğrulandı** — CSV kaydı doğru, okuma hatası yok.

UTF-16 varyantı (`1907320`) sabittir ve komşu dizelerine göre farklı bir
diyaloğa (etki büyüklüğü paneli) aittir. **Aynı kısıt için iki ayrı metin**
bulunması kılavuzda yazmayan bir uygulama ayrıntısıdır.

### REA-08 — `Please note` mesajı çalışma anında birleştiriliyor

| offset | parça |
|---|---|
| `1856584` | `The total sample size (` |
| `1856560` | `) is not a multiple of` |
| `1856536` | `the number of groups (` |
| `1856512` | `). The analysis was ` |
| `1856476` | `based on the average group size.` |

Beş sabit, **~110 bayt içinde bitişik** bir dize tablosunda. Tam mesaj ikilide
**tek parça halinde yoktur**; bu yüzden tam metin araması sonuç vermez.
Bu tablonun önceki sürümü "dize araması: bu metin" diyordu — o yöntem
başarısız olurdu; yöntemin kendisi düzeltildi.

Bulgu **AJ-15'i güçlendirir**: `based on the average group size.` bağımsız bir
metin sabitidir, hesap yoluna giren bir parametre değildir. Uyarı metni
gerçekten yalnızca açıklama.

### REA-10 — biçimleme: kısmen çözüldü, seçim kuralı hâlâ açık

Bitişik format tablosu; hemen ardından `Input error (illegal character?)`
(`1846036`). Bu blok sayı ayrıştırma/biçimleme modülü:

| offset | format |
|---|---|
| `1846000` | `%ld` |
| `1846004` | `%.16g` |
| `1846012` | `%.f` |
| `1846016` | `%.5g` |

Başka yerlerde: `%.7f` -> `1943636` (utf16), `%.7g` -> `1925748`,
`%.6g` -> `1872531`, `%.15g` -> `1886544`.
**Bulunmayanlar:** `%.6f`, `%.5f`, `%.3f`, `%.0f`.

**Kanıtlanan:** ekrandaki 7 ondalıklı gösterim (`0.8048873`, `9.9375000`,
`17.5000000`) `%.7f` ile uyumludur ve bu dize ikilide **mevcuttur**. Tam sayı
alanlar (`Total sample size`, `df1`, `df2`) `%.f` / `%ld` ile uyumludur.
Bölüm 2.4'teki üç karşı örnek (lambda `0`, lambda `120`, kritik F `199.5`)
`%.5g` çıktısıyla **birebir** uyumludur.

**Kanıtlanmayan:** `%.7f` ile `%.5g` arasında **seçimi yapan koşul**. Dize
araması dal koşulunu göstermez; bunun için kod akışı incelemesi gerekir.
B-09 bu yüzden "kısmen" kalıyor — ama artık iki *hipotez* yerine iki *gerçek
format dizesi* arasında seçim aranıyor.

### REA-12 — B-10 ÇÖZÜLDÜ: başlıklar sabit bir küme

| offset (utf16) | başlık |
|---|---|
| `1951204` | `Input error` |
| `1951228` | `Please note` |
| `1951280` | `Interruption` |
| `1951488` | `Internal math error` |

Dördü bitişik. `Input error` ile `Please note` ayrımı hesabın durup durmasının
bir *sonucu* değildir; çağıran taraf hangi başlık sabitini seçtiğine göre
kutuyu kurar. B-10 kapandı.

### REA-13 — kuantil hesabı sınırlı iteratif arama

| offset (ascii) | dize |
|---|---|
| `1846132` | `BinomialDist-Quantile: input parameter out of range` |
| `1846184` | `BinomialDist-Quantile: answer below lower search bound` |
| `1846240` | `BinomialDist-Quantile: answer above upper search bound` |

`lower/upper search bound` ifadeleri **kapalı form değil, alt/üst sınırlı
iteratif arama** anlamına gelir. Bu dizeler binom dağılımına aittir; **F
kuantili için aynı altyapının kullanıldığı kanıtlanmadı.** Ancak aynı modülde
(`1846000` format tablosuyla komşu) durmaları, dağılım yordamlarının ortak bir
arama iskeleti paylaştığına dair güçlü işarettir.

### REA-14 — AJ-10 doğrulandı: grafik etiketi `%.6g`

AJ-10 "grafik başlığındaki `critical F = ...` etiketi, alandaki değerin
**6 anlamlı basamağa** yuvarlanmış ve sondaki sıfırları atılmış hâlidir"
diyordu. Bu iddia **42/42** tutuyordu ama doğrulamada kullanılan örnek
(id 8: alan `4.6970018`, etiket `4.697`) `%.5g` ile `%.6g` arasında
**ayırt edici değildi** — ikisi de `4.697` verir.

Ayırt edici örnek `v6.png` (id 6):

| alan | etiket | `%.5g` | `%.6g` |
|---|---|---|---|
| `1.9174493` | **`1.91745`** | `1.9174` | `1.91745` |

Etiket `1.91745` olduğuna göre kural **`%.6g`**'dir. Ve bu format dizesi
ikilide mevcuttur: ascii offset `1872531`.

Böylece AJ-10 `[AJAN]` düzeyinden **`[REA]` düzeyine** yükseldi: hem gözlem
(42/42) hem de ikilide format dizesi var. Aynı ekran görüntüsü `%.7f`
gözlemini de destekler: alanlar `16.2500000` ve `1.9174493` olarak, yani
yedi ondalıkla gösteriliyor.

> Dikkat: bu, B-09'u **kapatmaz**. REA-14 yalnızca **grafik etiketini**
> açıklar (`%.6g`). Çıktı **alanlarındaki** `%.7f` ↔ `%.5g` seçimi hâlâ açıktır
> (bölüm 2.4'teki üç karşı örnek). İki ayrı biçimleme yolu olduğu artık kesin.

---

## 4.1 Kılavuzda OLMAYAN davranışlar (Kural 1)

Ödev "kılavuzda yazanı değil, kılavuzda OLMAYAN davranışı bulun" diyor.
Dize aramasıyla ortaya çıkan, kılavuzda bulunmayacak uygulama ayrıntıları:

| # | bulgu | kanıt |
|---|---|---|
| U-01 | Uyarı/hata mesajları **çalışma anında parçalardan birleştiriliyor** | REA-08 |
| U-02 | Aynı kısıt için **iki ayrı metin varyantı** (ana pencere birleştirmeli, diyalog sabit) | REA-07 |
| U-03 | Etki büyüklüğü diyaloğu ile ana pencere arasında **senkron uyarısı**: `...(%ld) is different from that given in the main window (%ld)! Do you want to adjust the value in the main window?` | utf16 `1897116`, `1897224` |
| U-04 | Grup büyüklüğü alt sınırı diyalogda **ayrı bir dizeyle** zorlanıyor: `The size of each group must be greater or equal 1` | utf16 `1896904` |
| U-05 | Diyalog başlıkları **sabit, dört elemanlı küme** | REA-12 |
| U-06 | Dağılım kuantilleri **sınırlı iteratif aramayla** çözülüyor | REA-13 |
| U-07 | Yapı yolları ikilide kalmış (`\Debug\`, `\Release\`); arayüz yazı tipi `Lucida sans unicode` gömülü | utf16 `1951204` civarı |

> U-04 hakkında dikkat: bu dize **etki büyüklüğü diyaloğuna** aittir (komşu
> dizeler onu gösteriyor), a priori aramasının alt sınırı değildir. B-05 hâlâ
> açıktır. Ancak a priori alt sınırı **türetilebilir**: N, k'nın katıdır (AJ-04)
> ve `df2 = N - k >= 1` gerekir (id 39/40'ta df2 = 1 çalışıyor), dolayısıyla
> k'dan büyük en küçük kat **2k**'dır. Bu bir varsayım değil, iki gözlemin
> sonucudur. Motor bu türetmeyi kullanır.

## 5. Oturum 1'de yapılmayanlar (dürüstlük notu)

- `GPower.exe` indirilmedi, çalıştırılmadı, incelenmedi.
- Hiçbir decompile/disassembly yapılmadı.
- Kılavuz veya makaleler okunmadı → `[DOK]` bölümü boş.
- Motor/CLI kodu yazılmadı (temiz oda kuralı).
- scipy çapraz kontrol betiği **bilerek repoya konmadı**; yalnızca raporu
  (`tests/uyum_raporu.md`) repoda.
- İki satırda (id 37, 38) `Effect size f` hata kutusunun arkasında kaldı;
  değer **tahmin edilmedi**, boş bırakıldı.
