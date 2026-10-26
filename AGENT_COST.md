# AGENT_COST — ajan maliyet kaydı

Her ajan oturumunun ne kadar tükettiğinin kaydı. Jeton ve ücret sayılarını
ajan kendisi ölçemez; bu alanlar **arayüzden okunup elle** doldurulmalıdır.
Uydurulmuş bir sayı yazmak, boş bırakmaktan kötüdür.

## Boş alanlar nereden okunur

Aşağıdaki tabloda `_(okunacak)_` yazan her hücre, oturumun koştuğu arayüzden
alınmalıdır. Ajanın kendi bağlam penceresinden bu sayıya erişimi yoktur:
jeton sayımı ve ücretlendirme ajanın dışında, istemci/API tarafında tutulur.

| arayüz | nereye bakılır |
|---|---|
| Claude Code (terminal) | oturum içinde `/cost` — o oturumun jeton ve ücret dökümünü verir; `/status` modeli ve oturum bilgisini gösterir |
| Claude Desktop / claude.ai | Ayarlar → kullanım (Usage) sayfası, tarih filtresiyle |
| API / SDK | yanıtların `usage` alanı (`input_tokens`, `output_tokens`) toplanır |

**Kapanmış oturumlar için:** oturum sonlandıysa `/cost` artık o oturumu
göstermez; sayı yalnızca kullanım sayfasından **tarih bazında** okunabilir ve
o gün başka iş de yapıldıysa oturuma izole edilemez. Böyle bir durumda hücre
`_(oturum kapandı, izole edilemiyor)_` yazılmalı — tahmini bir sayı değil.

Bu, ölçüm disiplininin bir parçası: `HALLUCINATIONS.md` mantığıyla, **bilinmeyen
bir sayının yerine makul görünen bir sayı yazmak** en pahalı hata türüdür.

---

## Özet tablo

| # | Oturum | Tarih | Model | Girdi jetonu | Çıktı jetonu | Ücret | Süre |
|---|---|---|---|---|---|---|---|
| 1 | İnceleme / oracle | 2026-10-22 | Claude Opus 5 | _(okunacak)_ | _(okunacak)_ | _(okunacak)_ | _(okunacak)_ |
| 2 | Motor yazımı (temiz oda) | 2026-10-25 | LLM (Grup 2) | _(okunacak)_ | _(okunacak)_ | _(okunacak)_ | _(okunacak)_ |
| 3 | REA + bütünleştirme | 2026-10-26 | Claude Opus 5 | _(okunacak)_ | _(okunacak)_ | _(okunacak)_ | _(okunacak)_ |
| 4 | Eksik taraması / teslim denetimi | 2026-10-26 | Claude Opus 5 | _(okunacak)_ | _(okunacak)_ | _(okunacak)_ | _(okunacak)_ |

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

### Arayüzden okunacak alanlar

```
Girdi jetonu   : ____    <- /cost veya kullanim sayfasi
Cikti jetonu   : ____
Toplam ucret   : ____
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
| Ortam | Windows, Python 3.14, SciPy 1.18.1, NumPy 2.5.4 |
| Test koşu süresi | 13,119 s (`grup2_python/TEST_SONUCLARI.md`) |

> Not: yukarıdaki süre **testlerin** koşu süresidir, oturumun duvar saati
> değildir. İkisi karıştırılmamalı; duvar saati hâlâ okunacak alanlardadır.

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

### Arayüzden okunacak alanlar

```
Girdi jetonu   : ____    <- /cost veya kullanim sayfasi
Cikti jetonu   : ____
Toplam ucret   : ____
Duvar saati    : ____
```

---

## Oturum 4 — eksik taraması / teslim denetimi

- **Tarih:** 2026-10-26
- **Model:** Claude Opus 5 (Claude Code, Windows)
- **Amaç:** Teslimi ödev isterleriyle karşılaştırmak, eksikleri önceliklendirmek,
  ucuz olanları kapatmak. **Motor koduna dokunulmadı.**

### Ölçülebilen iş hacmi

| metrik | değer |
|---|---|
| Okunan proje belgesi | 12 (README, LEDGER, HALLUCINATIONS, EKSIK_VAKALAR, uyum raporu, AGENT_COST, ajan demo, SPEC başlıkları, GRUP1_GOREV, grup2 README + TEST_SONUCLARI, .mcp.json) |
| Okunan ekran görüntüsü | **0** |
| Koşturulan test paketi | 3 — diferansiyel (42/42 + 2/2 doğru red), MCP (5 OK), SPEC (6 OK) + CLI duman testi |
| Git doğrulaması | 5 (remote, push durumu, SPEC md5 eşitliği, teslim commit içeriği, oracle↔grup2 ata ilişkisi) |
| Tespit edilen eksik | 8, öncelik sırasına dizildi |
| Kapatılan eksik | 3 (`requirements.txt`, `prompts/oturum2_yazim.md`, bu kayıt) |
| Yazılan motor satırı | **0** |

### Maliyetin büyük kısmı nerede

En pahalı kalem **belge okuma** (12 dosya); testleri koşturmak ve git
sorgulamak toplamda bir dakikanın altında kaldı ve asıl bulguları onlar
verdi. 8 eksiğin 5'i belgelerin kendi durum tablolarından okunabiliyordu;
ama **3'ü yalnızca komut çalıştırarak** ortaya çıktı:

1. Kökte `requirements.txt` olmaması — hiçbir belgede yazmıyor, `ls` ile görüldü.
2. Oturum 2'nin prompt kaydının olmaması — `ls prompts/` ile görüldü.
3. Oracle commit'inin grup 2 teslim commit'inin **atası** olması — yani temiz
   oda izolasyonunun "veri yoktu" diye kanıtlanamayacağı. Bu, belgelerin
   hiçbirinde yazmıyordu ve yalnızca `git merge-base --is-ancestor` ile çıktı.

**Ders:** teslim denetimi belge okumakla bitmiyor. Belgeler projenin kendi
anlattığı hâlini verir; eksikler çoğunlukla **anlatılmayan** yerdedir ve
onları ancak çalıştırmak gösterir. Üç bulgunun üçü de ucuz komutlardan geldi;
bu oturumun en verimli kalemi buydu.

### Arayüzden okunacak alanlar

```
Girdi jetonu   : ____    <- /cost veya kullanim sayfasi
Cikti jetonu   : ____
Toplam ucret   : ____
Duvar saati    : ____
```
