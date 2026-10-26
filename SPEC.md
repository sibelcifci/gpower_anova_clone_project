# SPEC — Tek yönlü ANOVA güç analizi (F testi, sabit etkiler, omnibus)

Bu belge **davranış** tanımıdır. İçinde kod, algoritma adımları veya decompile
çıktısı **yoktur** ve olmayacaktır. Motoru nasıl yazacağı Grup 2'nin kararıdır.

- **Kâhin:** G*Power 3.1.9.7 (Windows) ekran görüntüleri.
- **Kanıt tabanı:** `oracle/anova_oneway.csv` — **44 satır**
  (30 `a priori`, 14 `post hoc` — 12'si sonuç üretti, 2'si hata verdi).
- **Kapsam:** F testi ailesi → `ANOVA: Fixed effects, omnibus, one-way`,
  `a priori` ve `post hoc`.
- `id N` yazan her yer, o CSV satırına ve `oracle/screenshots/v{N}.png`
  görseline atıftır.

> Doğrulanmamış her kuralın başında **`TODO: REA ile doğrulanacak`** notu vardır.

---

## 1. Alanlar

### Girdiler

| alan | tip | a priori | post hoc |
|---|---|---|---|
| `f` (effect size f) | ondalık | gerekli | gerekli |
| `alpha` (α err prob) | ondalık | gerekli | gerekli |
| `power` (1−β err prob) | ondalık | **gerekli (girdi)** | — *(çıktıdır)* |
| `groups` (number of groups, `k`) | tam sayı | gerekli | gerekli |
| `total_n` (total sample size, `N`) | tam sayı | — *(çıktıdır)* | **gerekli (girdi)** |

İki mod arasındaki tek yapısal fark budur: `power` ile `total_n` yer değiştirir
(id 31 ↔ id 15, id 34 ↔ id 1).

### Çıktılar

| alan | tip | a priori | post hoc |
|---|---|---|---|
| `lambda` (λ) | ondalık | ✓ | ✓ |
| `critical_f` | ondalık | ✓ | ✓ |
| `df1` / `df2` | tam sayı | ✓ | ✓ |
| `total_n` | tam sayı | ✓ *(hesaplanır)* | — |
| `actual_power` | ondalık | ✓ | ✓ *(ana çıktı)* |

---

## 2. CLI sözleşmesi

Bu sözleşme **bizim tasarım kararımızdır**, G*Power'dan türetilmemiştir.
G*Power'ın komut satırı arayüzü yoktur; buradaki kurallar ödev gereğidir.

- Program **tek satır JSON** yazar ve sonlanır.
- Başarılı çalışmada çıkış kodu **0**.
- Geçersiz girdide çıktı `{"error":"<mesaj>"}` olur, çıkış kodu **sıfırdan farklı**.
- Hata durumunda çıktıda `error` dışında alan bulunmaz.

```gherkin
Feature: CLI sözleşmesi

  Scenario: Başarılı çalışma tek satır JSON ve sıfır çıkış kodu üretir
    Given geçerli bir girdi kümesi
    When program çalıştırılır
    Then çıktı tek satır JSON olur
    And çıkış kodu 0 olur
    And çıktıda "error" alanı bulunmaz

  Scenario: Geçersiz girdi hata sözleşmesini izler
    Given geçersiz bir girdi kümesi
    When program çalıştırılır
    Then çıktı yalnızca "error" alanını içeren tek satır JSON olur
    And çıkış kodu sıfırdan farklı olur

  Scenario: Uyarı, hata değildir
    Given post hoc modda toplam N grup sayısının katı değildir
    When program çalıştırılır
    Then program normal sonucu üretir
    And çıkış kodu 0 olur
    And çıktıda ayrıca bir "warning" alanı bulunur
    # TASARIM KARARI: G*Power burada bilgi kutusu gösterip hesabı yapıyor
    # (id 32, 35, 39). "warning" alanı bu davranışı CLI'ya taşımak içindir.
    # Alternatif, uyarıyı hiç iletmemekti; bilgi kaybı olmasın diye seçilmedi.
```

---

## 3. A priori modu

30 a priori satırının **tamamında** tutar (bkz. `tests/uyum_raporu.md`).

### 3.1 Serbestlik dereceleri

```gherkin
Feature: Serbestlik dereceleri

  Scenario Outline: df1 grup sayısının bir eksiği, df2 ise N eksi grup sayısıdır
    Given grup sayısı <k>
    And toplam örneklem <N>
    When analiz yapılır
    Then numerator df <df1> olur
    And denominator df <df2> olur

    Examples: gerçek oracle satırları
      | id | k  | N   | df1 | df2 |
      | 4  | 2  | 128 | 1   | 126 |
      | 15 | 3  | 159 | 2   | 156 |
      | 1  | 4  | 280 | 3   | 276 |
      | 5  | 5  | 200 | 4   | 195 |
      | 10 | 6  | 330 | 5   | 324 |
      | 13 | 8  | 304 | 7   | 296 |
      | 6  | 10 | 260 | 9   | 250 |
```

### 3.2 Nonsantralite parametresi

```gherkin
Feature: Nonsantralite parametresi

  Scenario Outline: λ, etki büyüklüğünün karesi ile toplam örneklemin çarpımıdır
    Given etki büyüklüğü <f>
    And toplam örneklem <N>
    When analiz yapılır
    Then nonsantralite parametresi <lambda> olur

    Examples: gerçek oracle satırları
      | id | f    | N    | lambda     |
      | 15 | 0.25 | 159  | 9.9375000  |
      | 3  | 0.40 | 66   | 10.5600000 |
      | 29 | 0.50 | 42   | 10.5000000 |
      | 19 | 0.10 | 1548 | 15.4800000 |
      | 8  | 0.30 | 237  | 21.3300000 |
      | 14 | 0.45 | 76   | 15.3900000 |
```

### 3.3 Toplam örneklem grup sayısının katıdır

```gherkin
Feature: Örneklem büyüklüğünün gruplara bölünmesi

  Scenario Outline: A priori'de toplam N daima grup sayısının tam katıdır
    Given grup sayısı <k>
    When a priori analiz yapılır
    Then toplam örneklem <N> olur
    And <N> sayısı <k> ile tam bölünür
    And grup başına <n_per_group> gözlem düşer

    Examples: gerçek oracle satırları
      | id | k  | N   | n_per_group |
      | 15 | 3  | 159 | 53          |
      | 1  | 4  | 280 | 70          |
      | 5  | 5  | 200 | 40          |
      | 10 | 6  | 330 | 55          |
      | 13 | 8  | 304 | 38          |
      | 6  | 10 | 260 | 26          |

  # DİKKAT: Bu kural YALNIZCA a priori'ye aittir.
  # Post hoc'ta N, k'nın katı olmak zorunda değildir (bölüm 4.2).

  # TODO: REA ile doğrulanacak.
  # Mevcut 30 satır, "tavana yuvarlama" ile "bir sonraki kata atlama"
  # kurallarını AYIRT EDEMEZ; ikisi de aynı sonucu verir.
  # Ayırt edici vektörler: EKSIK_VAKALAR.md bölüm 6.
```

### 3.4 Örneklem büyüklüğü en küçük yeterli değerdir

```gherkin
Feature: Minimal örneklem

  Scenario Outline: Bulunan N, istenen gücü sağlayan en küçük uygun değerdir
    Given etki büyüklüğü <f>, alfa <alpha>, istenen güç <power>, grup sayısı <k>
    When a priori analiz yapılır
    Then toplam örneklem <N> olur
    And gerçekleşen güç istenen güçten küçük olmaz
    And <N> değerinden bir kat küçük örneklem istenen gücü sağlamaz

    Examples: gerçek oracle satırları
      | id | f    | alpha | power | k | N   | actual_power |
      | 15 | 0.25 | 0.05  | 0.80  | 3 | 159 | 0.8048873    |
      | 1  | 0.25 | 0.05  | 0.95  | 4 | 280 | 0.9509908    |
      | 9  | 0.50 | 0.05  | 0.90  | 3 | 54  | 0.9015607    |
      | 11 | 0.25 | 0.10  | 0.80  | 3 | 126 | 0.8008668    |
      | 14 | 0.45 | 0.025 | 0.85  | 4 | 76  | 0.8501249    |
      | 7  | 0.15 | 0.01  | 0.90  | 4 | 864 | 0.9012454    |
```

### 3.5 Kritik F

```gherkin
Feature: Kritik F

  Scenario Outline: Kritik F yalnızca alfa ve serbestlik derecelerine bağlıdır
    Given alfa <alpha>, numerator df <df1>, denominator df <df2>
    When analiz yapılır
    Then kritik F <critical_f> olur

    Examples: gerçek oracle satırları
      | id | alpha | df1 | df2 | critical_f |
      | 15 | 0.05  | 2   | 156 | 3.0540042  |
      | 16 | 0.01  | 2   | 225 | 4.7007255  |
      | 11 | 0.10  | 2   | 123 | 2.3462330  |
      | 14 | 0.025 | 3   | 72  | 3.3034207  |
      | 6  | 0.05  | 9   | 250 | 1.9174493  |

  Scenario: Kritik F etki büyüklüğünden bağımsızdır
    Given id 41 ve id 42 satırları aynı alfa ve aynı serbestlik derecelerine sahiptir
    And etki büyüklükleri farklıdır
    Then iki satırın kritik F değerleri birebir aynıdır
    # id 41: f=0.40 ve id 42: f=0.10, ikisinde de kritik F = 3.3541308
```

### 3.6 Determinizm

```gherkin
Feature: Determinizm

  Scenario Outline: Aynı girdi daima aynı çıktıyı verir
    Given <id_a> ve <id_b> satırları aynı girdi vektörüne sahiptir
    When her ikisi de analiz edilir
    Then tüm çıktı alanları 7 ondalık basamağa kadar birebir aynı olur

    Examples: gerçek tekrar grupları
      | id_a | id_b | mod      |
      | 2    | 20   | a priori |
      | 3    | 23   | a priori |
      | 15   | 30   | a priori |
      | 32   | 33   | post hoc |
      | 35   | 36   | post hoc |
      | 39   | 40   | post hoc |

  # BELİRSİZ: farklı makine/kurulumlarda da aynı sonucun çıkıp çıkmadığı
  # bilinmiyor. 44 görselin tamamı TEK kaynaktan (grup1) gelmektedir.
  # TODO: ikinci bir kurulumdan tekrar görseli alınacak (EKSIK_VAKALAR T-01)
```

---

## 4. Post hoc modu

12 post hoc satırının tamamında tutar; 2 satır da hata davranışını belgeler.

### 4.1 Temel hesap

```gherkin
Feature: Post hoc güç hesabı

  Scenario Outline: Verilen örneklem için gerçekleşen güç hesaplanır
    Given etki büyüklüğü <f>, alfa <alpha>, toplam örneklem <N>, grup sayısı <k>
    When post hoc analiz yapılır
    Then nonsantralite parametresi <lambda> olur
    And numerator df <df1>, denominator df <df2> olur
    And kritik F <critical_f> olur
    And güç <power> olur

    Examples: gerçek oracle satırları
      | id | f    | alpha | N   | k | lambda     | df1 | df2 | critical_f | power     |
      | 31 | 0.25 | 0.05  | 159 | 3 | 9.9375000  | 2   | 156 | 3.0540042  | 0.8048873 |
      | 34 | 0.25 | 0.05  | 280 | 4 | 17.5000000 | 3   | 276 | 2.6373109  | 0.9509908 |
      | 41 | 0.40 | 0.05  | 30  | 3 | 4.8000000  | 2   | 27  | 3.3541308  | 0.4420732 |
      | 42 | 0.10 | 0.05  | 30  | 3 | 0.3000000  | 2   | 27  | 3.3541308  | 0.0707888 |
```

### 4.2 Toplam N, grup sayısının katı olmak zorunda DEĞİLDİR

Bu, a priori ile post hoc arasındaki en önemli davranış farkıdır.

```gherkin
Feature: Bölünmeyen örneklem büyüklüğü

  Scenario Outline: Katı olmayan N kabul edilir, uyarı verilir, hesap yapılır
    Given toplam örneklem <N> ve grup sayısı <k>
    And <N> sayısı <k> ile tam bölünmez
    When post hoc analiz yapılır
    Then bir bilgi kutusu gösterilir
    And kutunun başlığı "Please note" olur
    And kutunun metni toplam N'nin grup sayısının katı olmadığını söyler
    And metin analizin ortalama grup büyüklüğüne dayandığını belirtir
    And hesap yine de yapılır
    And denominator df <df2> olur
    And nonsantralite parametresi <lambda> olur
    And güç <power> olur

    Examples: gerçek oracle satırları
      | id | f    | N   | k | df2 | lambda    | power     |
      | 32 | 0.25 | 100 | 3 | 97  | 6.2500000 | 0.5885389 |
      | 35 | 0.25 | 101 | 4 | 97  | 6.3125000 | 0.5228374 |
      | 39 | 0.25 | 4   | 3 | 1   | 0.2500000 | 0.0530691 |

  Scenario: Uyarı metni hesabı DEĞİŞTİRMEZ
    Given id 32 satırında toplam N 100 ve grup sayısı 3'tür
    And kutu "analysis was based on the average group size" demektedir
    Then denominator df yine de 97 olur, yani N eksi grup sayısı
    And nonsantralite parametresi yine de 6.25 olur, yani f kare çarpı 100
    # Yani "ortalama grup büyüklüğü" ifadesi yalnızca açıklamadır;
    # hesaba yuvarlanmış veya düzeltilmiş bir N girmez.
```

### 4.3 Örneklem grup sayısından büyük olmalıdır

```gherkin
Feature: Post hoc alt sınırı

  Scenario Outline: N grup sayısından büyük değilse hesap yapılmaz
    Given toplam örneklem <N> ve grup sayısı <k>
    And <N> değeri <k> değerinden büyük değildir
    When post hoc analiz yapılır
    Then bir hata kutusu gösterilir
    And kutunun başlığı "Input error" olur
    And kutunun metni örneklemin grup sayısından büyük olması gerektiğini söyler
    And bütün çıktı alanları soru işareti gösterir
    And hiçbir sonuç üretilmez

    Examples: gerçek oracle satırları
      | id | N | k |
      | 37 | 3 | 3 |
      | 38 | 2 | 3 |

  Scenario: Sınırın hemen üstü çalışır
    Given toplam örneklem 4 ve grup sayısı 3'tür
    When post hoc analiz yapılır
    Then denominator df 1 olur
    And hesap başarıyla tamamlanır
    # id 39/40: df2 = 1 ile hesap yapılıyor, kritik F = 199.5
```

### 4.4 Etki büyüklüğünün uçları

```gherkin
Feature: Etki büyüklüğünün uç değerleri

  Scenario: Sıfır etki büyüklüğü hata değildir ve güç tam olarak alfaya eşittir
    Given etki büyüklüğü 0, alfa 0.05, toplam örneklem 150, grup sayısı 3
    When post hoc analiz yapılır
    Then nonsantralite parametresi 0 olur
    And güç 0.0500000 olur
    And hiçbir hata gösterilmez
    # id 43. Bu, gücün alfanın altına inemeyeceğinin de kanıtıdır.

  Scenario: Çok büyük etki büyüklüğünde güç bire yuvarlanır
    Given etki büyüklüğü 2.0, alfa 0.05, toplam örneklem 30, grup sayısı 3
    When post hoc analiz yapılır
    Then nonsantralite parametresi 120 olur
    And güç 1.0000000 olur
    # id 44
```

### 4.5 İki mod arasında gidiş–dönüş tutarlılığı

```gherkin
Feature: Modlar arası tutarlılık

  Scenario Outline: A priori'nin bulduğu N, post hoc'a verilince aynı gücü verir
    Given <f>, <alpha>, <k> ve istenen güç <hedef> ile a priori analiz yapılır
    And toplam örneklem <N> bulunur ve gerçekleşen güç <guc> olur
    When aynı <f>, <alpha>, <k> ve bulunan <N> ile post hoc analiz yapılır
    Then güç yine <guc> olur

    Examples: gerçek oracle satırları
      | a_priori_id | post_hoc_id | f    | alpha | k | hedef | N   | guc       |
      | 15          | 31          | 0.25 | 0.05  | 3 | 0.80  | 159 | 0.8048873 |
      | 1           | 34          | 0.25 | 0.05  | 4 | 0.95  | 280 | 0.9509908 |
```

---

## 5. Gösterim biçimi

```gherkin
Feature: Gösterim biçimi

  Scenario: Tam sayı alanlar her zaman tam sayı gösterilir
    Given herhangi bir başarılı analiz
    Then toplam örneklem, numerator df ve denominator df tam sayı gösterilir
    # 42/42 satırda tutuyor.

  Scenario: Ondalık alanlar genellikle yedi basamakla gösterilir
    Given herhangi bir başarılı analiz
    Then λ, kritik F ve güç çoğunlukla yedi ondalık basamakla gösterilir
    # DİKKAT: Bu kuralın istisnaları vardır ve kesin kuralı BİLİNMİYOR.
    #   id 43 → λ "0"      (7 ondalık olsaydı "0.0000000")
    #   id 44 → λ "120"    (7 ondalık olsaydı "120.0000000")
    #   id 39 → kritik F "199.5" (7 ondalık olsaydı "199.5000000")
    # Ama a priori'de tam sayı λ'lar yedi ondalıkla gösteriliyor:
    #   id 4 → "8.0000000", id 13 → "19.0000000", id 18 → "21.0000000"
    # İki aday hipotez ve ayırt edici vektörler: LEDGER.md bölüm 2.4
    # TODO: REA ile doğrulanacak

  Scenario: Grafik etiketi alandan daha az basamak gösterir
    Given id 8 satırında kritik F alanı 4.6970018 değerindedir
    Then grafik başlığındaki etiket 4.697 olarak görünür
    # Etiket, altı anlamlı basamağa yuvarlanır ve sondaki sıfırlar atılır.
    # 42/42 satırda tutuyor. TODO: REA ile doğrulanacak.
```

---

## 6. Girdi sınırları — ARTIK DOĞRULANDI

> Bu bölüm 2026-10-26'da **baştan yazıldı.** Önceki sürümü oracle verisi
> olmadan yazılmıştı ve bir kuralı **yanlıştı**: "`groups = 2.5` hata üretir"
> diyordu; G*Power hesabı yapıyor (id 56). Kanıt: id 45–59, görseller v45–v59.

### 6.1 Kabul aralıkları

G*Power üç alan için **tek kalıptan** üretilen bir hata verir:

```
"<Alan> is outside the admissible range (<alt>, <üst>)."
```

| alan | a priori | post hoc | kanıt |
|---|---|---|---|
| `Effect size f` | `(1e-06, 50)` | `(0, 50)` | id 45, 46 ↔ id 58 |
| `α err prob` | `(1e-07, 1)` | `(1e-07, 1)` | id 47, 48, 49 ↔ id 59 |
| `Power` | `(1e-07, 1)` | — (çıktıdır) | id 50, 51, 52 |

**Üst sınır dahil değildir:** `α = 1` ve `Power = 1` reddedildi (id 48, 50).
Alt sınırların tam değerleri (`f = 1e-06`, `α = 1e-07`) **denenmedi** — gösterim
açık aralık olduğu için motor da açık kabul eder; bu bir varsayımdır.

```gherkin
Feature: Kabul aralıkları

  Scenario Outline: Aralık dışı girdi hata üretir, çıktı alanları "?" olur
    Given mod <mod> seçilir
    And <alan> alanına <deger> verilir
    When hesap istenir
    Then "Input error" kutusu çıkar
    And altı çıktı alanının hepsi "?" gösterir

    Examples:
      | mod      | alan  | deger | id |
      | a_priori | f     | 0     | 45 |
      | a_priori | f     | -0.25 | 46 |
      | a_priori | alpha | 0     | 47 |
      | a_priori | alpha | 1     | 48 |
      | a_priori | alpha | -0.05 | 49 |
      | a_priori | power | 1     | 50 |
      | a_priori | power | 0     | 51 |
      | a_priori | power | 1.5   | 52 |
      | post_hoc | f     | 60    | 58 |
      | post_hoc | alpha | 0     | 59 |
```

### 6.2 `f` alanının aralığı MODA BAĞLIDIR

A priori alt sınırı `1e-06`, post hoc alt sınırı `0`'dır (id 45 ↔ id 58).
Aynı alan, aynı testte, yalnızca analiz türü değiştiği için farklı doğrulanır.
**Kılavuzda böyle bir ayrım yazmaz.**

### 6.3 Gösterilen aralık ile gerçek davranış ÇELİŞİR (post hoc)

Post hoc mesajı aralığı **açık** gösterir: `(0, 50)`. Buna rağmen id 43'te
`f = 0` **kabul edilir** ve güç tam olarak α çıkar (`0.0500000`).

```gherkin
  Scenario: Post hoc f = 0 kabul edilir, mesajın dediğinin aksine
    Given mod post_hoc ve f = 0 verilir
    When hesap istenir
    Then hata çıkmaz
    And güç alfaya eşit olur   # id 43: alpha=0.05 -> 0.0500000
```

Motor **davranışı** izler, mesajı değil: post hoc'ta `0 <= f < 50`.

### 6.4 Grup sayısı: ayrı bir mesaj kalıbı

`groups < 2` için aralık kalıbı **kullanılmaz**; ayrı bir metin çıkar:

```
"There must be at least 2 groups."
```

id 53 (`groups=1`), id 54 (`groups=0`), id 55 (`groups=-3`) — üçünde de birebir
aynı metin.

### 6.5 Tam sayı olmayan grup sayısı SESSİZCE kabul edilir

```gherkin
  Scenario: groups = 2.5 hata vermez, hesap yapılır
    Given a priori modda f=0.25, alpha=0.05, power=0.80 verilir
    And groups alanına 2.5 yazılır
    When hesap istenir
    Then hata kutusu ÇIKMAZ
    And uyarı kutusu da ÇIKMAZ
    And sonuç k=3 ile birebir aynı olur   # id 56 = id 15/30
    # lambda 9.9375000, critical F 3.0540042, df1 2, df2 156,
    # total N 159, actual power 0.8048873
```

Bu, G*Power'ın **sessiz veri dönüşümü** yaptığı tek yerdir: `N`'in `k`'nın katı
olmaması durumunda bir `Please note` kutusu gösterilirken (bölüm 4.2), burada
hiçbir uyarı yoktur.

**Yuvarlama yönü ÇÖZÜLDÜ (id 60).** `groups = 2.4` verildiğinde N=128 çıktı
ve `df1 = 1` oldu, yani **k=2** kullanıldı. Yukarı yuvarlama olsaydı k=3 ve
N=159 çıkardı. Kural: **en yakına yuvarlama**.

```gherkin
  Scenario Outline: Kesirli grup sayısı en yakın tam sayıya yuvarlanır
    Given a priori modda f=0.25, alpha=0.05, power=0.80 verilir
    And groups alanına <giris> yazılır
    Then hesap <k> ile yapılır ve toplam N <n> olur

    Examples:
      | giris | k | n   | id |
      | 2.4   | 2 | 128 | 60 |
      | 2.5   | 3 | 159 | 56 |
```

İki satır birlikte yönü belirler: 2.4 aşağı, 2.5 yukarı gider. Yarım
değerinin yukarı mı en yakın çifte mi gittiği (banker yuvarlaması) ayrıca
sınanmadı; 2.5 → 3 yukarı yuvarlamayla uyumludur, banker yuvarlaması 2
verirdi — yani **yarımda yukarı**.

### 6.6 Sayısal olmayan metin ayrı mesaj almaz

`α` kutusuna `abc` yazılabilir; `Calculate` basıldığında "geçersiz sayı" diye
ayrı bir hata **yoktur**, aralık hatasına katlanır (id 57). Metin büyük
olasılıkla `0` olarak ayrıştırılıyor — doğrulanmadı.

### 6.7 Hâlâ bilinmeyenler

| soru | durum |
|---|---|
| `power <= alpha` bandı (a priori) | BELİRSİZ — EKSIK_VAKALAR G-01…G-04 |
| A priori'de grup başına minimum gözlem | BELİRSİZ — EKSIK_VAKALAR K-08 |
| Alt sınırların tam değerleri (`f=1e-06`, `α=1e-07`) | denenmedi |
| Post hoc'ta `power` alanı girdi değil, sınırı yok | doğrulandı (id 58, 59) |
| `groups` üst sınırı | denenmedi |

---

## 7. Kapsam dışı

Bu sürümde desteklenmeyecek, G*Power'ın aynı ekranında bulunan özellikler
(karar alındı):

- `Sensitivity`, `Criterion`, `Compromise` güç analizi türleri
- `Determine =>` paneli (ortalama ve standart sapmadan `f` türetme)
- `X–Y plot for a range of values` grafiği
- `Protocol of power analyses` sekmesi
- Dengesiz (eşit olmayan) grup büyüklükleri
