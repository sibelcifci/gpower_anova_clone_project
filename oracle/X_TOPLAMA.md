# X vektörleri — toplama formu (a priori, geçersiz girdiler)

**Toplayan:** GÖNÜL NAZİRE AYDIN · **Tarih:** 2026-10-26 · **Araç:** G*Power 3.1.9.7 (Windows)

Sabit girdiler: `Effect size f = 0.25`, `α err prob = 0.05`,
`Power (1-β err prob) = 0.80`, `Number of groups = 3`.
Her vektörde **yalnızca** belirtilen alan değişir.

G*Power ayarı (bir kez yapılır):

- **Test family:** `F tests`
- **Statistical test:** `ANOVA: Fixed effects, omnibus, one-way`
- **Type of power analysis:** `A priori: Compute required sample size – given α, power, and effect size`

> ## Körleme notu (dürüstlük kaydı)
>
> Bu veriyi toplayan kişi, toplama başlamadan önce **kendi motorumuzun** bu 13
> vektörde hata döndürdüğünü özet olarak biliyordu (ajan bunu önceki turda
> söyledi). Yani toplama *kör değildir*. Buna karşı alınan önlem: her satır
> için **birebir metin + tam pencere ekran görüntüsü** kaydedilir; yorum veya
> hatırlama kaydedilmez. Ekran görüntüsü bağımsız olarak denetlenebilir.
> `tests/gecersiz_girdi_raporu.md` dosyasına toplama sırasında bakılmadı.

---

## Nasıl kaydedilir

Her blokta şu üç şey doldurulur:

1. **sonuç tipi:** `HATA KUTUSU` · `SONUÇ ÜRETTİ` · `ALAN KABUL ETMEDİ`
2. **ne görüldü:** hata kutusunun başlığı + metni **birebir**, ya da altı çıktı
   alanı (`λ`, `Critical F`, `Numerator df`, `Denominator df`,
   `Total sample size`, `Actual power`)
3. **ekran görüntüsü:** `oracle/screenshots/` içine kaydedilen ad

---

## X-01 — f = 0

- **sınanan:** f=0 -> N sonsuza gider mi, hata mi
- **ekran görüntüsü:** `oracle/screenshots/v45.png`
- **sonuç tipi:** `HATA KUTUSU`
- **ne görüldü:** başlık `Input error`, metin birebir: **"Effect size f is outside the admissible range (1e-06, 50)."** Altı çıktı alanının **hepsi `?`**.
- **notlar:** Mesaj, kılavuzda bulunmayan bir **kabul aralığı** açıklıyor: `f ∈ (1e-06, 50)`. Parantez gösterimi aralığın **açık** olduğunu ima eder (uçlar dahil değil) — doğrulanmadı. `Effect size f` alanı hata kutusunun arkasında kaldı, alanda ne yazdığı görünmüyor.

---

## X-02 — f = -0.25

- **sınanan:** negatif etki buyuklugu
- **ekran görüntüsü:** `oracle/screenshots/v46.png`
- **sonuç tipi:** `HATA KUTUSU`
- **ne görüldü:** başlık `Input error`, metin birebir: **"Effect size f is outside the admissible range (1e-06, 50)."** — X-01 ile **aynı mesaj**. Altı çıktı alanının hepsi `?`.
- **notlar:** Eksi işareti alana **girilebildi**; alan tuş seviyesinde reddetmiyor. Doğrulama `Calculate` anında yapılıyor. Negatif f için ayrı bir mesaj yok: aralık dışı sayılıyor.

---

## X-03 — alpha = 0

- **sınanan:** alpha = 0
- **ekran görüntüsü:** `oracle/screenshots/v47.png`
- **sonuç tipi:** `HATA KUTUSU`
- **ne görüldü:** başlık `Input error`, metin birebir: **"Alpha is outside the admissible range (1e-07, 1)."** `α err prob` alanı ekranda `0` gösteriyor. Altı çıktı alanının hepsi `?`.
- **notlar:** İkinci kabul aralığı: `α ∈ (1e-07, 1)`. Üst sınırın **1** olması, X-04 (`α = 1`) vektörünü kritik hale getiriyor: aralık açıksa α=1 de reddedilmeli.

---

## X-04 — alpha = 1

- **sınanan:** alpha = 1
- **ekran görüntüsü:** `oracle/screenshots/v48.png`
- **sonuç tipi:** `HATA KUTUSU`
- **ne görüldü:** `Input error` → **"Alpha is outside the admissible range (1e-07, 1)."** Altı çıktı alanının hepsi `?`. `α err prob` alanı ekranda **`1`** gösteriyor.
- **notlar:** **Aralık açık: üst sınır dahil değil.** α=1 reddedildi, yani `(1e-07, 1)` gösterimi matematiksel açık aralık anlamında kullanılıyor. Görsel tam ekran alındı; pencere kırpılmamış.

---

## X-05 — alpha = -0.05

- **sınanan:** negatif alpha
- **ekran görüntüsü:** `oracle/screenshots/v49.png`
- **sonuç tipi:** `HATA KUTUSU`
- **ne görüldü:** `Input error` → **"Alpha is outside the admissible range (1e-07, 1)."** Altı çıktı alanının hepsi `?`. `α err prob` alanı ekranda **`−0.05`** gösteriyor.
- **notlar:** Eksi işareti alana girilebiliyor; doğrulama `Calculate` anında. Negatif α için ayrı mesaj yok — X-04 ile birebir aynı metin.

---

## X-06 — Power = 1

- **sınanan:** guc = 1, erisilemez
- **ekran görüntüsü:** `oracle/screenshots/v50.png`
- **sonuç tipi:** `HATA KUTUSU`
- **ne görüldü:** `Input error` → **"Power is outside the admissible range (1e-07, 1)."** Altı çıktı alanının hepsi `?`. `Power` alanı ekranda **`1`** gösteriyor.
- **notlar:** **Üçüncü kabul aralığı** ve α ile **birebir aynı sınırlar**: `(1e-07, 1)`. Güç=1 reddedildi.

---

## X-07 — Power = 0

- **sınanan:** guc = 0
- **ekran görüntüsü:** `oracle/screenshots/v51.png`
- **sonuç tipi:** `HATA KUTUSU`
- **ne görüldü:** `Input error` → **"Power is outside the admissible range (1e-07, 1)."** Altı çıktı alanının hepsi `?`. `Power` alanı ekranda **`0`** gösteriyor.
- **notlar:** X-06 ile aynı metin; alt sınır da dahil değil.

---

## X-08 — Power = 1.5

- **sınanan:** guc > 1
- **ekran görüntüsü:** `oracle/screenshots/v52.png`
- **sonuç tipi:** `HATA KUTUSU`
- **ne görüldü:** `Input error` → **"Power is outside the admissible range (1e-07, 1)."** Altı çıktı alanının hepsi `?`. `Power` alanı ekranda **`1.5`** gösteriyor.
- **notlar:** X-06/X-07 ile aynı metin. Güç > 1 için ayrı bir mesaj yok.

---

## X-09 — Number of groups = 1

- **sınanan:** tek grup -> df1 = 0
- **ekran görüntüsü:** `oracle/screenshots/v53.png`
- **sonuç tipi:** `HATA KUTUSU`
- **ne görüldü:** `Input error` → **"There must be at least 2 groups."** Altı çıktı alanının hepsi `?`. `Number of groups` alanı **`1`**.
- **notlar:** **Yeni mesaj kalıbı.** "admissible range" şablonundan farklı, ayrı bir doğrulama yolu.

---

## X-10 — Number of groups = 0

- **sınanan:** sifir grup
- **ekran görüntüsü:** `oracle/screenshots/v54.png`
- **sonuç tipi:** `HATA KUTUSU`
- **ne görüldü:** `Input error` → **"There must be at least 2 groups."** Altı çıktı alanının hepsi `?`. `Number of groups` alanı **`0`**.
- **notlar:** X-09 ile birebir aynı metin.

---

## X-11 — Number of groups = -3

- **sınanan:** negatif grup
- **ekran görüntüsü:** `oracle/screenshots/v55.png`
- **sonuç tipi:** `HATA KUTUSU`
- **ne görüldü:** `Input error` → **"There must be at least 2 groups."** Altı çıktı alanının hepsi `?`. `Number of groups` alanı **`−3`**.
- **notlar:** Eksi girilebiliyor; negatif grup için ayrı mesaj yok.

---

## X-12 — Number of groups = 2.5

- **sınanan:** tam sayi olmayan grup sayisi
- **ekran görüntüsü:** `oracle/screenshots/v56.png`
- **sonuç tipi:** `SONUÇ ÜRETTİ (hata kutusu YOK)`
- **ne görüldü:** Alan **`2.5` değerini kabul etti** ve `Calculate` hesap yaptı: λ=`9.9375000`, Critical F=`3.0540042`, Numerator df=`2`, Denominator df=`156`, Total sample size=`159`, Actual power=`0.8048873`. Grafik de çizildi.
- **notlar:** **En şaşırtıcı bulgu.** Bu çıktı `k=3` sonucunun birebir aynısı (bkz. id 15, id 30). Yani 2.5 sessizce tam sayıya çevrildi — **uyarı kutusu çıkmadan**. `df1 = 2` olduğu için k=3 kullanıldı; k=2 olsaydı df1=1 olurdu. **AÇIK SORU:** yukarı yuvarlama (ceil) mı, en yakına yuvarlama mı? 2.5 ikisinde de 3 verir, ayırt etmiyor. Ayırt edici vektör: `groups = 2.4` → ceil ise N=159, yuvarlama ise N=128.

---

## X-13 — alpha kutusuna 'abc' yaz

- **sınanan:** alfanumerik olmayan girdi
- **ekran görüntüsü:** `oracle/screenshots/v57.png`
- **sonuç tipi:** `HATA KUTUSU`
- **ne görüldü:** `Input error` → **"Alpha is outside the admissible range (1e-07, 1)."** `α err prob` alanı ekranda **`abc`** metnini gösteriyor. Altı çıktı alanının hepsi `?`.
- **notlar:** Alan **harf girişini kabul ediyor**; sayısal olmayan girdi için ayrı mesaj yok, aralık hatasına katlanıyor (metin muhtemelen 0 olarak ayrıştırılıyor).

---

## X-14 — POST HOC, `Effect size f = 60` (N=30, k=3)

- **ekran görüntüsü:** `oracle/screenshots/v58.png`
- **sonuç tipi:** `HATA KUTUSU`
- **ne görüldü:** `Input error` → **"Effect size f is outside the admissible range (0, 50)."**
  Altı çıktı alanının hepsi `?`.
- **notlar:** **Bu turun en değerli bulgusu.** Alt sınır **`0`** — a priori'de (id 45)
  aynı alan için **`1e-06`** yazıyordu. **Aynı alanın kabul aralığı moda göre değişiyor.**
  Üstelik gösterilen aralık açık `(0, 50)` olmasına rağmen oracle'daki **id 43 post hoc
  `f = 0` ile hesap yapıyor** (güç = α = 0.0500000). Yani *gösterilen aralık ile gerçek
  davranış çelişiyor*: mesaj 0'ı dışlıyor, program 0'ı kabul ediyor.

---

## X-15 — POST HOC, `α err prob = 0` (f=0.25, N=30, k=3)

- **ekran görüntüsü:** `oracle/screenshots/v59.png`
- **sonuç tipi:** `HATA KUTUSU`
- **ne görüldü:** `Input error` → **"Alpha is outside the admissible range (1e-07, 1)."**
  Altı çıktı alanının hepsi `?`.
- **notlar:** A priori (id 47) ile **birebir aynı aralık**. Yani moda bağlı farklılık
  α'da **yok**, yalnızca `f` alanında var. Bu, X-14'teki farkın tesadüf olmadığını gösterir.

---

## Toplama bitince

1. Bu form ajana verilir; ajan `oracle/anova_oneway.csv`'ye id 45–57 satırlarını yazar.
2. `oracle/RENAME_MAP.csv`'ye yeni görsellerin eşlemesi eklenir.
3. `tests/diferansiyel_test.py` 57 satırla koşturulur.
4. Uyuşmazlık çıkarsa **G*Power doğru kabul edilir**; motor düzeltilir veya
   `LEDGER.md`'ye uyuşmazlık olarak yazılır. Kâhin G*Power'dır.
