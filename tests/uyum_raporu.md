# Uyum Raporu — bağımsız çapraz kontrol (scipy)

**Bu rapor kâhin DEĞİLDİR.** Kâhin yalnızca G*Power 3.1.9.7 ekran görüntüleridir.
Uyuşmazlık çıkarsa **G*Power değeri geçerlidir**; düzeltilmez, raporlanır.

Kapsam: **44 satır / 44 ekran görüntüsü**.

## Kullanılan bağımsız model

- `df1 = k − 1`, `df2 = N − k`, `λ = f² · N`
- kritik F = `scipy.stats.f.isf(α, df1, df2)`
- güç = `scipy.stats.ncf.sf(kritik F, df1, df2, λ)`
- a priori N araması: `2k`'dan başlar, `k` adımla büyür, `güç ≥ hedef` olunca durur

Betik repoya konmadı (temiz oda kuralı: güç hesabı Grup 2'nin işi).

## 1. A priori satırları

| id | f | α | hedef güç | k | G*Power N | scipy N | fark | durum |
|---|---|---|---|---|---|---|---|---|
| 1 | 0.25 | 0.05 | 0.95 | 4 | 280 | 280 | 0 | EŞLEŞTİ |
| 2 | 0.10 | 0.05 | 0.80 | 3 | 969 | 969 | 0 | EŞLEŞTİ |
| 3 | 0.40 | 0.05 | 0.80 | 3 | 66 | 66 | 0 | EŞLEŞTİ |
| 4 | 0.25 | 0.05 | 0.80 | 2 | 128 | 128 | 0 | EŞLEŞTİ |
| 5 | 0.25 | 0.05 | 0.80 | 5 | 200 | 200 | 0 | EŞLEŞTİ |
| 6 | 0.25 | 0.05 | 0.80 | 10 | 260 | 260 | 0 | EŞLEŞTİ |
| 7 | 0.15 | 0.01 | 0.90 | 4 | 864 | 864 | 0 | EŞLEŞTİ |
| 8 | 0.30 | 0.01 | 0.95 | 3 | 237 | 237 | 0 | EŞLEŞTİ |
| 9 | 0.50 | 0.05 | 0.90 | 3 | 54 | 54 | 0 | EŞLEŞTİ |
| 10 | 0.20 | 0.05 | 0.80 | 6 | 330 | 330 | 0 | EŞLEŞTİ |
| 11 | 0.25 | 0.10 | 0.80 | 3 | 126 | 126 | 0 | EŞLEŞTİ |
| 12 | 0.35 | 0.05 | 0.95 | 5 | 160 | 160 | 0 | EŞLEŞTİ |
| 13 | 0.25 | 0.05 | 0.90 | 8 | 304 | 304 | 0 | EŞLEŞTİ |
| 14 | 0.45 | 0.025 | 0.85 | 4 | 76 | 76 | 0 | EŞLEŞTİ |
| 15 | 0.25 | 0.05 | 0.80 | 3 | 159 | 159 | 0 | EŞLEŞTİ |
| 16 | 0.25 | 0.01 | 0.80 | 3 | 228 | 228 | 0 | EŞLEŞTİ |
| 17 | 0.25 | 0.05 | 0.95 | 3 | 252 | 252 | 0 | EŞLEŞTİ |
| 18 | 0.25 | 0.01 | 0.95 | 3 | 336 | 336 | 0 | EŞLEŞTİ |
| 19 | 0.10 | 0.05 | 0.95 | 3 | 1548 | 1548 | 0 | EŞLEŞTİ |
| 20 | 0.10 | 0.05 | 0.80 | 3 | 969 | 969 | 0 | EŞLEŞTİ |
| 21 | 0.10 | 0.05 | 0.90 | 3 | 1269 | 1269 | 0 | EŞLEŞTİ |
| 22 | 0.10 | 0.01 | 0.80 | 3 | 1395 | 1395 | 0 | EŞLEŞTİ |
| 23 | 0.40 | 0.05 | 0.80 | 3 | 66 | 66 | 0 | EŞLEŞTİ |
| 24 | 0.40 | 0.05 | 0.90 | 3 | 84 | 84 | 0 | EŞLEŞTİ |
| 25 | 0.40 | 0.05 | 0.95 | 3 | 102 | 102 | 0 | EŞLEŞTİ |
| 26 | 0.40 | 0.01 | 0.80 | 3 | 93 | 93 | 0 | EŞLEŞTİ |
| 27 | 0.15 | 0.01 | 0.80 | 3 | 624 | 624 | 0 | EŞLEŞTİ |
| 28 | 0.30 | 0.05 | 0.85 | 3 | 126 | 126 | 0 | EŞLEŞTİ |
| 29 | 0.50 | 0.05 | 0.80 | 3 | 42 | 42 | 0 | EŞLEŞTİ |
| 30 | 0.25 | 0.05 | 0.80 | 3 | 159 | 159 | 0 | EŞLEŞTİ |

**A priori özeti: 30 satır — EŞLEŞTİ 30, FARK 0.**

## 2. Post hoc satırları

Post hoc'ta N **girdidir**, güç **çıktıdır**. Karşılaştırma doğrudan güç üzerinden.

| id | f | α | N | k | N, k'nın katı mı | ekrandaki güç | scipy güç | mutlak fark | durum |
|---|---|---|---|---|---|---|---|---|---|
| 31 | 0.25 | 0.05 | 159 | 3 | evet | 0.8048873 | 0.8048873 | 1.5e-08 | EŞLEŞTİ |
| 32 | 0.25 | 0.05 | 100 | 3 | **HAYIR** | 0.5885389 | 0.5885389 | 4.1e-08 | EŞLEŞTİ |
| 33 | 0.25 | 0.05 | 100 | 3 | **HAYIR** | 0.5885389 | 0.5885389 | 4.1e-08 | EŞLEŞTİ |
| 34 | 0.25 | 0.05 | 280 | 4 | evet | 0.9509908 | 0.9509908 | 9.1e-09 | EŞLEŞTİ |
| 35 | 0.25 | 0.05 | 101 | 4 | **HAYIR** | 0.5228374 | 0.5228374 | 3.0e-08 | EŞLEŞTİ |
| 36 | 0.25 | 0.05 | 101 | 4 | **HAYIR** | 0.5228374 | 0.5228374 | 3.0e-08 | EŞLEŞTİ |
| 39 | 0.25 | 0.05 | 4 | 3 | **HAYIR** | 0.0530691 | 0.0530691 | 1.6e-08 | EŞLEŞTİ |
| 40 | 0.25 | 0.05 | 4 | 3 | **HAYIR** | 0.0530691 | 0.0530691 | 1.6e-08 | EŞLEŞTİ |
| 41 | 0.40 | 0.05 | 30 | 3 | evet | 0.4420732 | 0.4420732 | 2.9e-08 | EŞLEŞTİ |
| 42 | 0.10 | 0.05 | 30 | 3 | evet | 0.0707888 | 0.0707888 | 6.5e-10 | EŞLEŞTİ |
| 43 | 0 | 0.05 | 150 | 3 | evet | 0.0500000 | 0.0500000 | 2.8e-17 | EŞLEŞTİ |
| 44 | 2.0 | 0.05 | 30 | 3 | evet | 1.0000000 | 1.0000000 | 6.7e-16 | EŞLEŞTİ |

**Post hoc özeti: 12 satır — EŞLEŞTİ 12, FARK 0.**

> Not: id 43 (`f = 0`) için `scipy.stats.ncf.sf` nonsantralite tam **0** iken
> **−0.95** döndürüyor — bu scipy'nin sınır durumu hatasıdır, G*Power'ın değil.
> λ = 0 olduğunda merkezî olmayan F, merkezî F'ye indirgenir ve kritik F'nin
> üstünde kalan kütle tam olarak α'dır. `scipy.stats.f.sf` ile hesaplandığında
> **0.05** çıkıyor, yani G*Power'ın gösterdiği `0.0500000` doğrudur.
> Tabloda bu satır için merkezî F kullanıldı.

## 3. Hata üreten satırlar

2 satır hiç çıktı üretmedi; karşılaştırılacak sayı yok.

| id | mod | N | k | ne oldu |
|---|---|---|---|---|
| 37 | post_hoc | 3 | 3 | `Input error` kutusu, çıktı alanları `?` |
| 38 | post_hoc | 2 | 3 | `Input error` kutusu, çıktı alanları `?` |

## 4. Yapısal değişmezler

| kontrol | kapsam | sonuç |
|---|---|---|
| `df1 = k − 1` | 42 satır | 42/42 |
| `df2 = N − k` | 42 satır | 42/42 |
| `λ = f² · N` | 42 satır | 42/42 |
| `N mod k = 0` (**yalnızca a priori**) | 30 satır | 30/30 |
| post hoc'ta `N mod k = 0` **gerekmiyor** | 12 satır | 6 satırda N katı değil, hesap yine yapıldı |
| kritik F ↔ `f.isf(α, df1, df2)` | 42 satır | 42/42 |

## 5. İki mod arasında tutarlılık (gidiş–dönüş)

A priori ile bulunan N, post hoc'a geri verildiğinde aynı gücü üretiyor mu?

| a priori id | post hoc id | f | α | k | N | a priori `actual power` | post hoc `Power` | aynı mı |
|---|---|---|---|---|---|---|---|---|
| 15 | 31 | 0.25 | 0.05 | 3 | 159 | 0.8048873 | 0.8048873 | **evet, birebir** |
| 1 | 34 | 0.25 | 0.05 | 4 | 280 | 0.9509908 | 0.9509908 | **evet, birebir** |

## 6. Okunamayan alanlar

2 satırda `Effect size f` alanı hata kutusunun arkasında kaldığı için okunamadı: id 37, 38.
Bu alanlar CSV'de **boş** bırakıldı ve `notlar` sütununa `okunamadi` yazıldı.
Değer başka bir kaynaktan tahmin edilmedi.

Diğer tüm alanlar 44 görüntünün tamamında net okundu.
