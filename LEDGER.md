# LEDGER — kanıt defteri

Her iddia bir etiket taşır:

| Etiket | Anlamı | Puan |
|---|---|---|
| `[DOK]` | Resmî belgede/kılavuzda yazıyor | yok |
| `[AJAN]` | Ajanın oracle verisinden çıkarımı — **binary kanıtı yok** | yok |
| `[REA]` | İkili (binary) incelemesiyle kanıtlanmış | **var** |

> **Bu oturumda hiçbir `[REA]` satırı doldurulmamıştır.** REA aracı çalıştırılmadı,
> `GPower.exe` açılmadı. `[REA]` tablosu boş şablon olarak bırakılmıştır.
> Kanıtsız `[REA]` yazmak kural ihlalidir.

**Kanıt tabanı:** `oracle/anova_oneway.csv` — **44 satır / 44 ekran görüntüsü**

| mod | satır | benzersiz girdi vektörü |
|---|---|---|
| `a_priori` | 30 | 27 |
| `post_hoc` | 14 (12'si çıktı üretti, 2'si hata) | 11 |

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
| AJ-10 | Grafik başlığındaki `critical F = …` etiketi, alandaki değerin **6 anlamlı basamağa** yuvarlanmış ve sondaki sıfırları atılmış hâlidir | **42/42** | etiket ↔ alan karşılaştırması |
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
| B-09 | **YENİ:** ondalık gösterim kuralı (bölüm 2.4) | hâlâ bilinmiyor |
| B-10 | **YENİ:** `Input error` ile `Please note` kutularının ayrım ölçütü | kısmen: biri hesabı durduruyor, diğeri durdurmuyor; tam kural bilinmiyor |

---

## 4. `[REA]` — ikili inceleme kanıtı (BOŞ ŞABLON)

Bu tablo kasten boştur. Decompile çıktısı bu dosyaya **konmayacak**;
yalnızca kısa alıntı + fonksiyon adresi yazılacaktır.

| id | iddia | fonksiyon adresi / dize ref | alıntı | durum |
|---|---|---|---|---|
| REA-01 | AJ-03 (`λ = f² · N`) motorda böyle hesaplanıyor | | | TODO |
| REA-02 | AJ-04 (a priori'de N, k'nın katına yuvarlanıyor) | | | TODO |
| REA-03 | AJ-05 (en küçük N araması) — arama mı, kapalı form mu | | | TODO |
| REA-04 | AJ-07 (kritik F yordamı) | | | TODO |
| REA-05 | AJ-08 (merkezî olmayan F kuyruk olasılığı yordamı) | | | TODO |
| REA-06 | B-05 (a priori'de grup başına minimum gözlem sabiti) | | | TODO |
| REA-07 | AJ-16 — `"Sample size must be greater than the number of groups"` dizesi | **dize araması: bu metin** | | TODO |
| REA-08 | AJ-14/AJ-15 — `"not a multiple of the number of groups"` dizesi ve sonrasındaki dal | **dize araması: bu metin** | | TODO |
| REA-09 | AJ-17 (`f = 0` özel durumu mu, yoksa formülün doğal sonucu mu) | | | TODO |
| REA-10 | B-09 (sayı biçimlendirme yordamı) | | | TODO |
| REA-11 | B-08 (kayan nokta tipi ve yakınsama toleransı) | | | TODO |

> REA-07 ve REA-08 için **somut başlangıç noktası var**: iki hata/uyarı
> metninin tam İngilizce hâli elimizde. İkilide dize araması yapıp bu
> metinlere ulaşan dalı bulmak, REA'ya girmenin en kolay yolu.

---

## 5. Oturum 1'de yapılmayanlar (dürüstlük notu)

- `GPower.exe` indirilmedi, çalıştırılmadı, incelenmedi.
- Hiçbir decompile/disassembly yapılmadı.
- Kılavuz veya makaleler okunmadı → `[DOK]` bölümü boş.
- Motor/CLI kodu yazılmadı (temiz oda kuralı).
- scipy çapraz kontrol betiği **bilerek repoya konmadı**; yalnızca raporu
  (`tests/uyum_raporu.md`) repoda.
- İki satırda (id 37, 38) `Effect size f` hata kutusunun arkasında kaldı;
  değer **tahmin edilmedi**, boş bırakıldı.
