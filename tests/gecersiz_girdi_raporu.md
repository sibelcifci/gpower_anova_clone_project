# Gecersiz a priori girdileri — MOTORUN davranisi

> G*Power karsiliklari ARTIK TOPLANDI: oracle id 45-59, gorseller v45-v59.
> Karsilastirmanin kendisi `tests/diferansiyel_test.py` icinde yapilir;
> bu dosya yalnizca motorun davranisinin okunabilir dokumudur.
> Uretim: `python tests/gecersiz_girdi_raporu.py --md`

| # | degisen girdi | sinanan | cikis kodu | sure | motorun mesaji |
|---|---|---|---|---|---|
| X-01 | `f=0` | a priori'de f=0 (N sonsuza gider) | 1 | 0.8 s | `f: (1e-06, 50) aralığında olmalı` |
| X-02 | `f=-0.25` | negatif etki buyuklugu | 1 | 0.7 s | `f: (1e-06, 50) aralığında olmalı` |
| X-03 | `alpha=0` | alpha = 0 | 1 | 0.8 s | `alpha: (1e-07, 1) aralığında olmalı` |
| X-04 | `alpha=1` | alpha = 1 | 1 | 0.7 s | `alpha: (1e-07, 1) aralığında olmalı` |
| X-05 | `alpha=-0.05` | negatif alpha | 1 | 0.7 s | `alpha: (1e-07, 1) aralığında olmalı` |
| X-06 | `power=1` | guc = 1 (erisilemez) | 1 | 0.7 s | `power: (1e-07, 1) aralığında olmalı` |
| X-07 | `power=0` | guc = 0 | 1 | 0.7 s | `power: (1e-07, 1) aralığında olmalı` |
| X-08 | `power=1.5` | guc > 1 | 1 | 0.7 s | `power: (1e-07, 1) aralığında olmalı` |
| X-09 | `groups=1` | tek grup -> df1 = 0 | 1 | 0.7 s | `En az 2 grup olmalı` |
| X-10 | `groups=0` | sifir grup | 1 | 0.7 s | `En az 2 grup olmalı` |
| X-11 | `groups=-3` | negatif grup | 1 | 0.7 s | `En az 2 grup olmalı` |
| X-12 | `groups=2.5` | tam sayi olmayan grup sayisi (SONUC beklenir) | 0 | 0.7 s | `SONUC URETTI: {"lambda":9.9375,"critical_f":3.0540042,"df1":2,"df2":156,"actual_powe` |
| X-13 | `alpha='abc'` | alpha kutusuna harf | 1 | 0.7 s | `alpha: sayısal değer gerekli` |

Diger alanlar sabit: `f=0.25, alpha=0.05, power=0.80, groups=3`.

## Sonuc

13/13 vektorde davranis oracle ile uyumlu: 
asili kalma yok; 12 vektor `error` alanli JSON dondu, X-12 ise
oracle'in (id 56) bekledigi gibi SONUC uretti.
