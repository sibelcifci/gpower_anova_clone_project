# AGENT_COST — ajan maliyet kaydı

Her ajan oturumunun ne kadar tükettiğinin kaydı. Jeton ve ücret sayılarını
ajan kendisi ölçemez; bu alanlar **arayüzden okunup elle** doldurulmalıdır.
Uydurulmuş bir sayı yazmak, boş bırakmaktan kötüdür.

---

## Özet tablo

| # | Oturum | Tarih | Model | Girdi jetonu | Çıktı jetonu | Ücret | Süre |
|---|---|---|---|---|---|---|---|
| 1 | İnceleme / oracle | 2026-10-22 | Claude Opus 5 | _(doldurulacak)_ | _(doldurulacak)_ | _(doldurulacak)_ | _(doldurulacak)_ |
| 2 | Motor yazımı (temiz oda) | 2026-10-25 | LLM (Grup 2) | _(doldurulacak)_ | _(doldurulacak)_ | _(doldurulacak)_ | _(doldurulacak)_ |
| 3 | REA + bütünleştirme | 2026-10-26 | Claude Opus 5 | _(doldurulacak)_ | _(doldurulacak)_ | _(doldurulacak)_ | _(doldurulacak)_ |

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

## Oturum 2 — Motor yazımı (temiz oda)

- **Tarih:** 2026-10-25
- **Amaç:** Yalnızca `SPEC.md` okunarak motor + test yazmak. G*Power açılmadı.

| metrik | değer |
|---|---|
| Okunan belge | 1 (`SPEC.md`, değiştirilmemiş kopya) |
| Yazılan motor satırı | ~114 |
| Yazılan test satırı | ~83 |
| Test yöntemi | 6, tamamı geçti |
| Okunan ekran görüntüsü | **0** (temiz oda) |
| Oracle CSV erişimi | **yok** — bu yüzden tam oracle regresyonu Oturum 3'e kaldı |

**Maliyet notu:** Bu oturum ucuzdu çünkü görsel okuma yok. Ancak oracle CSV
verilmediği için motorun 44 satıra karşı doğrulanması yapılamadı; o iş Oturum
3'te 1 dakikalık bir koşuya dönüştü. **Ders:** temiz oda, SPEC'i izole eder;
*doğrulamayı* izole etmek gerekmiyordu.

## Oturum 3 — REA + bütünleştirme

- **Tarih:** 2026-10-26
- **Model:** Claude Opus 5 (Claude Code, Windows)
- **Amaç:** REA kanıtı üretmek, tek motor yapısına geçmek, MCP + ajan katmanını
  eklemek, belgeleri gerçeğe uydurmak.

| metrik | değer |
|---|---|
| İncelenen ikili | 1 (`GPowerNT.exe`, 2.287.616 bayt) |
| Kanıtlanan `[REA]` satırı | 5 (REA-07, 08, 10, 12, 13) |
| TODO kalan `[REA]` satırı | 8 (kod akışı gerektiriyor) |
| Kılavuzda olmayan davranış | 7 (U-01 … U-07) |
| Okunan ekran görüntüsü | **0** |
| Yazılan kaynak dosya | 7 (`core`, `cli`, `__main__`, `__init__`, `mcp_server`, `rea_strings`, 2 test) |
| Koşturulan test | 6 (SPEC) + 5 (MCP) + 44 satır diferansiyel |
| Yakalanan hata | 3 (H3-01, H3-02, H3-03) |

### Maliyetin büyük kısmı nerede

Oturum 1'in tersi: en pahalı kalem **görsel okuma değil, belge çapraz
kontrolü**. REA'nın kendisi şaşırtıcı biçimde ucuzdu — dize araması saniyeler
sürdü ve 5 kanıtlı satır üretti. Buna karşılık README ↔ LEDGER tutarsızlığını
bulmak (H3-01) her iki belgeyi satır satır okumayı gerektirdi.

**Öneri:** REA'ya erken başlanmalıydı. Oturum 1 "REA aracı çalıştırılmadı" diye
kapanmıştı; oysa aradığı iki metin zaten elindeydi ve araç 110 satır. Oturum 1'in
en büyük belirsizliklerinden ikisi (B-09, B-10) bu araçla kapanırdı.

### Doldurulacak alanlar

```
Girdi jetonu   : ____
Çıktı jetonu   : ____
Toplam ücret   : ____
Duvar saati    : ____
```
