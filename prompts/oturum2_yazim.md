# Oturum 2 — temiz oda yazım oturumu kaydı

> **Bu dosya 2026-10-26'da, oturum 2 bittikten sonra yazıldı.**

## 0. Bu dosya ne DEĞİLDİR

Oturum 2'ye (temiz oda yazım oturumu) verilen **prompt metni kaydedilmedi.**
Bu dosya o metin değildir ve o metnin "yeniden üretimi" de değildir —
hatırlanan bir promptu birebir prompt gibi sunmak, `HALLUCINATIONS.md`'nin
kayıt altına aldığı hata türünün aynısı olurdu.

Burada yapılan şey şu: ödev kuralı 2 ("**iki ayrı ajan oturumu: biri inceler,
diğeri yalnızca SPEC.md ile yazar**") için repodan **bağımsız olarak
doğrulanabilen** izleri toplamak, doğrulanamayan kısmı ise beyan olarak
işaretlemek. Kanıt ile beyan aynı kefeye konmaz.

Oturum 1'in prompt metni korunmuştur: `prompts/oturum1_inceleme.md`
(ve `GRUP1_GOREV.md`). Asimetri bilinçli değil, eksikliktir.

---

## 1. Oturumların ayrımı

| oturum | tarih | kim / ne | G*Power'ı gördü mü | oracle'a baktı mı | çıktı | prompt kaydı |
|---|---|---|---|---|---|---|
| 1 — inceleme | 2026-10-22 | Alt Grup 1 + Claude Opus 5 | **evet** (kurulu, 44 ekran görüntüsü) | üretti | `oracle/`, `SPEC.md`, `LEDGER.md` | ✅ `prompts/oturum1_inceleme.md` |
| 2 — yazım | 2026-10-25 | Alt Grup 2 + LLM | **hayır** (beyan) | **hayır** (beyan) | `grup2_python/` motor + testler | ❌ yok — bu dosyanın konusu |
| 3 — REA + bütünleştirme | 2026-10-26 | Claude Opus 5 | ikiliye dize araması; GUI açılmadı | evet | `src/`, `tools/`, MCP, diferansiyel test | ❌ yok |

Kural 2'nin istediği ayrım **1 ↔ 2** arasındadır ve bu ayrım yapılmıştır;
belgelenmesi eksik kalmıştır.

---

## 2. Oturum 2'ye teslim edilen tek girdi

`SPEC.md` — değiştirilmemiş kopyası `grup2_python/SPEC.md` olarak repoda durur.

| ölçüm | değer |
|---|---|
| satır | 451 |
| md5 (satır sonu normalize edilerek) | `49fa5019a96afd70f15c1798d13e24b6` |
| kök kopya ile fark | **yok** — tek fark satır sonu (CRLF ↔ LF) |

Yeniden üretilebilir:

```bash
md5sum <(tr -d '\r' < SPEC.md) <(tr -d '\r' < grup2_python/SPEC.md)
```

İki hash eşit çıkıyor. Yani oturum 2'nin elindeki şartname, oturum 1'in
yazdığı şartnamenin **aynısıdır**; arada düzeltilmiş/zenginleştirilmiş bir
sürüm yoktur.

**Teslim edilmeyenler** (`grup2_python/README.md` ve `TEST_SONUCLARI.md`
bunu kendi ağzından beyan eder):

- `oracle/anova_oneway.csv` (44 satır)
- `oracle/screenshots/` (44 ekran görüntüsü)
- `tests/uyum_raporu.md` (scipy çapraz kontrolü)
- `LEDGER.md` (kanıt defteri)

---

## 3. Doğrulanabilir izler

Aşağıdakiler beyan değil, repodan sınanabilir gözlemlerdir.

**3.1 — Teslim commit'i yalnızca 6 dosya içeriyor, hiçbiri oracle değil.**

```bash
git show --stat --oneline 4326cd9
```

`README.md`, `SPEC.md`, `TEST_SONUCLARI.md`, `anova_power.py`,
`requirements.txt`, `test_anova_power.py` — 747 ekleme, 0 oracle dosyası.

**3.2 — Oturum 2 kodu oracle'a hiç atıf yapmıyor.**

```bash
grep -ric "oracle\|screenshot\|uyum_raporu" grup2_python/anova_power.py grup2_python/test_anova_power.py
```

İkisi de **0**. Testler yalnızca SPEC içindeki vektörleri (6 a priori,
9 post hoc, 6 kritik F) kullanır; 44 satırlık CSV'den tek satır geçmez.

**3.3 — En güçlü dolaylı iz: oturum 2, SPEC'in sustuğu yerlerde *tahmin
etmek zorunda kalmış* ve bunu yazmış.**

`grup2_python/README.md`'den, kendi ifadeleriyle:

- *"SPEC'in doğrulamadığı iki karar: grup başına minimum 2 kişi; tam eşitlikte
  aynı N'de kalma. Bunlar G*Power'dan gözlemlenmiş kurallar değildir."*
- *"Kaynak sınırı toplam N=100.000.000'dur; G*Power davranışından türetilmedi."*
- *"SPEC ekran biçiminin kesin kuralını vermediği için G*Power'ın metinsel
  gösterimi taklit edilmez."*
- *"44 satırın tümü sağlanmadığı için tam oracle regresyonu yapılmamıştır."*

Bu kayıtlar izolasyonun davranışsal kanıtıdır: oracle CSV'si veya ekran
görüntüleri elinde olsaydı bu kararların en az ikisi (grup başına minimum
gözlem, gösterim biçimi) **tahmin edilmek yerine veriden okunabilirdi**.
Bir ajan, elindeki cevaba rağmen "bunu bilemiyorum" diye not düşmez.

**3.4 — Hesap mantığı sonradan tek motora taşındı, kopyası bırakılmadı.**

`grup2_python/anova_power.py` artık `src/anova_power/core.py`'ye yönlendiren
bir kabuktur (ödev kuralı 3). Özgün, el değmemiş hâli git geçmişinde durur:

```bash
git show 4326cd9:grup2_python/anova_power.py
```

Temiz oda kaydı bu yüzden bozulmaz: denetlenecek sürüm commit'te sabittir.

---

## 4. Doğrulanamayan kısım — dürüst sınır

**İzolasyon, "veriye erişim fiziksel olarak imkânsızdı" diye kanıtlanamaz.**

```bash
git merge-base --is-ancestor 1d1e846 4326cd9   # çıkış kodu 0 = evet
```

Oracle verisini ekleyen commit (`1d1e846`), oturum 2 teslim commit'inin
(`4326cd9`) **atasıdır**. Yani oturum 2 çalışırken `oracle/anova_oneway.csv`
ve 44 ekran görüntüsü o dalda **mevcuttu**; bakılmadıkları iddiası
*bakılmadığına dair beyana* ve bölüm 3'teki dolaylı izlere dayanır.

Bunu kesin kanıta çevirecek olan şey yapılmamıştır. Yapılabilecekler:

1. Oturum 2'yi `oracle/` içermeyen **ayrı bir repoda/dalda** çalıştırmak ve o
   dalın commit'ini teslim etmek (en temiz yöntem).
2. Oturum 2'nin prompt metnini ve araç çağrısı dökümünü kaydetmek — hangi
   dosyaların okunduğu oradan görülürdü.
3. Teslimden önce SPEC'in hash'ini, teslimden sonra okunan dosya listesini
   not etmek.

Bu, bilinen ve kapatılmamış bir boşluktur; `EKSIK_VAKALAR.md` mantığıyla
burada açık bırakılıyor.

---

## 5. Tekrar yapılacaksa — oturum 2 sözleşmesi

Bir sonraki temiz oda oturumu için uyulacak kontrol listesi:

- [ ] Yalnızca `SPEC.md` verilir; hash'i teslim öncesi kaydedilir.
- [ ] Oturum, oracle içermeyen ayrı bir çalışma kopyasında açılır.
- [ ] Prompt metni `prompts/` altına **oturum başlamadan** yazılır.
- [ ] G*Power kurulmaz, açılmaz, ekran görüntüsü okunmaz.
- [ ] SPEC'in sustuğu her nokta "SPEC'te yok, kendi kararım" diye not edilir —
      boşluk sessizce doldurulmaz.
- [ ] Motor kodu yazılır; oracle regresyonu **sonraki** oturuma bırakılır
      (doğrulamayı izole etmek gerekmiyor — bkz. `AGENT_COST.md` oturum 2 dersi).
