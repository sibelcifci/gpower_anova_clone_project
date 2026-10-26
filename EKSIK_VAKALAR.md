# Eksik Vakalar — G*Power'da girilmesi gereken vektörler

Mevcut oracle: **60 satır / 60 ekran görüntüsü**
(44 `a priori` + 16 `post hoc`).

Aşağıdaki vektörler veri setinde **hâlâ yok**. Her satır G*Power'da doğrudan
girilebilecek biçimde yazıldı. Çıktı değerlerini ben dolduramam — kâhin
G*Power'dır.

> "beklenen" sütunu bilerek yoktur. Beklenti yazmak, kâhini ben belirlemek olurdu.

---

## 0. TAMAMLANANLAR ✅

**Post hoc modu (eski bölüm 2, 11 vektör) — TAMAMI TOPLANDI.**
Artık `SPEC.md` bölüm 4 gerçek verilerle dolu. Elde edilen başlıca bilgiler:

| bulgu | kanıt |
|---|---|
| Post hoc'ta N, grup sayısının katı olmak zorunda değil; uyarı verilip hesap yapılıyor | id 32, 35, 39 |
| Uyarı metnindeki "average group size" hesabı değiştirmiyor: `df2 = N − k`, `λ = f²·N` | id 32 (N=100, k=3 → df2=97, λ=6.25) |
| `N ≤ k` → `Input error`, çıktı alanları `?` | id 37 (N=3), id 38 (N=2) |
| `N = k + 1` çalışıyor (df2 = 1) | id 39, 40 |
| `f = 0` hata değil; güç **tam olarak α** | id 43 |
| Çok büyük `f` → güç `1.0000000` | id 44 |
| A priori ↔ post hoc gidiş–dönüş tutarlı | id 15↔31, id 1↔34 |

---

## 1. Kapsam özeti

| Boyut | Veri setinde bulunan | Durum |
|---|---|---|
| Grup sayısı `k` | 2, 3, 4, 5, 6, 8, 10 | istenen 2/3/4/5/10 **tam** |
| Etki büyüklüğü `f` | 0 *(post hoc)*, 0.10 … 0.50, 2.0 *(post hoc)* | **a priori'de uçlar boş** |
| `α` | 0.01, 0.025, 0.05, 0.10 | **uçlar boş** |
| İstenen güç (a priori) | 0.80, 0.85, 0.90, 0.95 | **güç ≤ α hiç yok** |
| Mod | a priori 30, post hoc 14 | **ikisi de var** ✅ |
| Geçersiz girdi | yalnızca `N ≤ k` (post hoc) | **diğerleri boş** |
| Kaynak | 44/44 tek kaynak (`grup1`) | **ikinci kurulum verisi yok** |

---

## 2. TAMAMLANDI ✅ — Geçersiz girdiler (id 45–60)

**16 vektör toplandı** (2026-10-26). Kayıt: `oracle/X_TOPLAMA.md`,
görseller `v45.png` … `v60.png`, kurallar `SPEC.md` bölüm 6.

| bulgu | kanıt |
|---|---|
| Aralık hataları tek kalıptan: `"<Alan> is outside the admissible range (a, b)"` | id 45–52, 58, 59 |
| `α` ve `Power` aralığı `(1e-07, 1)`; üst sınır dahil değil | id 48, 50 |
| **`f` aralığı moda bağlı:** a priori `(1e-06, 50)`, post hoc `(0, 50)` | id 45 ↔ id 58 |
| **Mesaj ile davranış çelişiyor:** post hoc `(0, 50)` der, `f=0`'ı kabul eder | id 58 ↔ id 43 |
| `groups < 2` ayrı metin: `"There must be at least 2 groups."` | id 53, 54, 55 |
| **`groups` kesirli olabilir:** sessizce en yakına yuvarlanır, uyarı yok | id 56 (2.5→3), id 60 (2.4→2) |
| `α` kutusuna harf yazılabilir; ayrı mesaj yok | id 57 |

### Bu bölümden doğan YENİ eksikler

| # | mod | vektör | ne öğreniriz |
|---|---|---|---|
| Y-01 | a priori | `f = 1e-06` | alt sınır dahil mi (mesaj açık aralık diyor) |
| Y-02 | a priori | `f = 50` | üst sınır dahil mi |
| Y-03 | a priori | `α = 1e-07` | alt sınır dahil mi |
| Y-04 | post hoc | `groups = 2.5`, `N = 150` | yuvarlama post hoc'ta da aynı mı |
| Y-05 | a priori | `groups = 3.5` | yarımda yukarı kuralı tek örnekten ibaret değil mi |
| Y-06 | post hoc | `N = 0` ve `N = -5` | N için ayrı mesaj kalıbı var mı |

---

## 3. ÖNCELİK 2 — Gösterim biçimini ayırt eden vektörler

`LEDGER.md` bölüm 2.4'teki iki hipotezi **ayırt eder**. İkisi yeter.

Mod: `Post hoc`.

| # | f | α | N | k | λ ne olacak | ne öğreniriz |
|---|---|---|---|---|---|---|
| D-01 | 0.25 | 0.05 | 128 | 2 | tam **8** | `8` görünürse → gösterim **moda** bağlı. `8.0000000` görünürse → moda bağlı değil |
| D-02 | 1.1 | 0.05 | 102 | 3 | **123.42** (tam sayı değil, 11 karakter) | `123.42` görünürse → **alan genişliğine** bağlı. `123.4200000` görünürse → yalnızca tam sayılar kısalıyor |

Bu iki ekran görüntüsü, `SPEC.md` bölüm 5'teki BELİRSİZ notunu kapatır.

---

## 4. ÖNCELİK 3 — Güç ≤ α bandı (a priori)

Veri setinde **hiç yok**. Güç α'nın altına inemez (id 43 bunu post hoc'ta
gösterdi), dolayısıyla a priori'de ya minimum N'e çakılma ya da hata beklenir.

Mod: `A priori`. f = 0.25, k = 3 sabit.

| # | α | güç |
|---|---|---|
| G-01 | 0.05 | **0.05** (güç = α) |
| G-02 | 0.05 | **0.04** (güç < α) |
| G-03 | 0.05 | 0.01 |
| G-04 | **0.10** | **0.10** (güç = α, farklı α) |
| G-05 | 0.05 | 0.50 |
| G-06 | 0.05 | 0.99 |
| G-07 | 0.05 | **0.999** |

---

## 5. ÖNCELİK 4 — Yuvarlama ve minimum N (a priori)

30 satırın hiçbirinde yuvarlama payı büyük değil ve hiçbiri alt sınıra
değmiyor. "Tavana yuvarlama" ile "sonraki kata atlama" hâlâ **ayırt edilemiyor**.

Mod: `A priori`.

| # | f | α | güç | k | neden |
|---|---|---|---|---|---|
| K-01 | 0.80 | 0.05 | 0.80 | 10 | ham N küçük, k büyük → yuvarlama payı en görünür |
| K-02 | 0.80 | 0.05 | 0.80 | 9 | tek sayı k |
| K-03 | 0.70 | 0.05 | 0.80 | 7 | asal k |
| K-04 | 0.60 | 0.05 | 0.90 | 11 | asal ve büyük k |
| K-05 | 0.25 | 0.05 | 0.80 | 7 | k = 7 veri setinde yok |
| K-06 | 0.25 | 0.05 | 0.80 | 9 | k = 9 veri setinde yok |
| K-07 | 0.50 | 0.05 | 0.80 | 20 | çok gruplu uç |
| K-08 | **1.5** | 0.05 | 0.80 | 10 | **grup başına minimum gözlem 1 mi 2 mi** — en kritik olanı |

---

## 6. ÖNCELİK 5 — Etki büyüklüğünün uçları (a priori)

α = 0.05, güç = 0.80, k = 3 **sabit**, yalnızca `f` değişiyor:

| # | f | not |
|---|---|---|
| F-01 | **0.01** | N on binlere çıkar, taşma davranışı |
| F-02 | 0.02 | |
| F-03 | 0.05 | |
| F-04 | 0.99 | |
| F-05 | **1.0** | tam sınır |
| F-06 | 5.0 | N alt sınırına çakılmalı |
| F-07 | 10.0 | uç |

---

## 7. ÖNCELİK 6 — α'nın eksik değerleri

f = 0.25, güç = 0.80, k = 3 sabit. Mod: `A priori`.

| # | α |
|---|---|
| A-01 | 0.001 |
| A-02 | 0.20 |
| A-03 | 0.50 |

---

## 8. ÖNCELİK 7 — İkinci kurulumdan tekrar görseli

44 görselin tamamı tek kaynaktan geliyor. Tekrar grupları (id 2↔20, 3↔23,
15↔30, 32↔33, 35↔36, 39↔40) aynı kurulumda alındığı için yalnızca
*tekrarlanabilirliği* gösteriyor, **taşınabilirliği göstermiyor**.

| # | mod | f | α | güç | k | özel not |
|---|---|---|---|---|---|---|
| T-01 | a priori | 0.25 | 0.05 | 0.80 | 3 | id 15/30 ile aynı vektör, **başka bir bilgisayarda** |

---

## 9. ÖNCELİK 8 — Post hoc'ta kalan küçük boşluklar

Post hoc büyük ölçüde kapandı; yalnızca α tarafı hiç zorlanmadı.
Mod: `Post hoc`, f = 0.25, N = 150, k = 3 sabit.

| # | α | neden |
|---|---|---|
| P-01 | **0** | post hoc'ta α = 0 |
| P-02 | **1** | post hoc'ta α = 1 |
| P-03 | 0.001 | çok katı α |
| P-04 | 0.50 | uç gevşek α |
| P-05 | — | k = 1 ile post hoc (`Number of groups` = 1) |

---

## 10. Kapsam dışı — KARARLAŞTIRILDI

Motor bunları desteklemeyecek, oracle görseli **toplanmasına gerek yok**:

- `Sensitivity`, `Criterion`, `Compromise` güç analizi türleri
- `Determine =>` düğmesi
- `X–Y plot for a range of values`
- `Protocol of power analyses` sekmesi
