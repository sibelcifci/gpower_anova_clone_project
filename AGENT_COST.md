# AGENT_COST — ajan maliyet kaydı

Her ajan oturumunun ne kadar tükettiğinin kaydı. Jeton ve ücret sayılarını
ajan kendisi ölçemez; bu alanlar **arayüzden okunup elle** doldurulmalıdır.
Uydurulmuş bir sayı yazmak, boş bırakmaktan kötüdür.

---

## Özet tablo

| # | Oturum | Tarih | Model | Girdi jetonu | Çıktı jetonu | Ücret | Süre |
|---|---|---|---|---|---|---|---|
| 1 | İnceleme / oracle | 2026-10-22 | Claude Opus 5 | _(doldurulacak)_ | _(doldurulacak)_ | _(doldurulacak)_ | _(doldurulacak)_ |
| 2 | Motor yazımı | — | — | — | — | — | — |
| 3 | REA / ikili inceleme | — | — | — | — | — | — |

---

## Oturum 1 — İnceleme / oracle verisi

- **Tarih:** 2026-10-22
- **Model:** Claude Opus 5 (Claude Code, Windows)
- **Amaç:** Ekran görüntülerinden oracle CSV üretmek, çapraz kontrol etmek,
  SPEC/LEDGER taslaklarını yazmak. Motor kodu yazılmadı.

### Ölçülebilen iş hacmi

| metrik | değer |
|---|---|
| Okunan ekran görüntüsü | 52 okuma (44 benzersiz görsel + 8 doğrulama amaçlı tekrar okuma) |
| Üretilen oracle satırı | 44 (30 a priori + 14 post hoc) |
| Kopyalanan / dönüştürülen görsel | 44 (29 kopya + 15 JPEG→PNG dönüşümü) |
| Çalıştırılan bağımsız kontrol | 8 (a priori N, post hoc güç, kritik F, actual power, minimallik, λ, df kuralları, eşleme) |
| Yakalanan ajan hatası | 2 (H1-01, H1-02) — ikisi de kayda geçti ve düzeltildi |
| Yazılan belge | 8 |
| Yazılan motor kodu satırı | **0** (temiz oda kuralı) |

### Maliyetin büyük kısmı nerede

En pahalı kalem **44 görselin okunması**. Her ekran görüntüsü tek tek
modele verildi; metin olarak özetlenmiş hâlleri kullanılmadı, çünkü
değerlerin ekrandaki basamak sayısıyla okunması gerekiyordu. Ayrıca 8 görsel,
`v{id}.png` eşlemesini ve şüpheli bir gösterim biçimini doğrulamak için
**ikinci kez** okundu — bu tekrar okumalar H1-02'nin yakalanmasını sağladı,
yani maliyeti karşılığını verdi.

Bu maliyeti düşürmenin yolu, G*Power'ın `Protocol of power analyses`
sekmesinden metin çıktısı almak olurdu; o sekmenin içeriği elimizdeki
görsellerde yok. **Öneri:** sonraki ölçümlerde ekran görüntüsünün yanında
protokol metni de kaydedilsin.

### Doldurulacak alanlar

```
Girdi jetonu   : ____
Çıktı jetonu   : ____
Toplam ücret   : ____
Duvar saati    : ____
```

---

## Oturum 2 — Motor yazımı

_(henüz başlamadı)_

## Oturum 3 — REA / ikili inceleme

_(henüz başlamadı)_
