# HALLUCINATIONS — ajan hatalarının dürüst kaydı

Amaç: ajanın ürettiği yanlış, uydurma veya doğrulanmamış iddiaların kaydı.
Bir şey yakalandığında **silinmez**, buraya yazılır. Boş bir dosya "hata
olmadı" demek değildir; "henüz yakalanmadı" demektir.

Her kayıt şu alanları taşır:

| alan | ne yazılır |
|---|---|
| **ne dedi** | ajanın iddiası, mümkünse birebir |
| **nasıl fark edildi** | hangi adımda ortaya çıktı |
| **hangi kontrol yakaladı** | çapraz kontrol / insan incelemesi / assert / kural |
| **sonuç** | düzeltildi mi, nasıl |

---

## Oturum 1 — 2026-10-22 (inceleme/analiz, Claude Opus 5)

### H1-01 — Görsellerin iki ayrı kaynaktan geldiği çıkarımı (YANLIŞ)

- **ne dedi:** Ajan, 29 görselin iki kişiden geldiğini çıkardı: *"PNG'ler
  grup1'in (temiz pencere yakalaması, doğrudan klasöre kaydedilmiş), jpeg'ler
  grup2'nin (altlarında masaüstü sızıyor, biri açıkça WhatsApp dosyası)."*
  Bu çıkarımı kullanıcıya **"önerilen" seçenek** olarak sundu.
- **dayanağı neydi:** dosya biçimi (PNG/JPEG), kaydedilme saatleri
  (20:18–20:28 ↔ 20:36–20:38), görsellerin altında görünen masaüstü ve
  "WhatsApp Image" dosya adı. Hepsi gerçek gözlem, ama **çıkarım yanlış**:
  bu izler dosyaların nasıl *aktarıldığını* gösteriyor, kimin *ürettiğini* değil.
- **nasıl fark edildi:** kullanıcıya soruldu; cevap **"hepsi grup1"** oldu.
- **hangi kontrol yakaladı:** **insan incelemesi.** Hiçbir otomatik kontrol
  bunu yakalayamazdı — scipy çapraz kontrolü satırın kendi içindeki sayısal
  tutarlılığına bakar, görselin kime ait olduğuna dair hiçbir şey söylemez.
- **sonuç:** `kaynak` sütunu 29 satırda `grup1` yapıldı. Çıkarıma **dayanan
  iki iddia da düzeltildi:**
  - `LEDGER.md` AJ-12: "farklı makinelerde" ibaresi kaldırıldı; determinizmin
    yalnızca *aynı kurulumda tekrarlanabilirlik* olduğu, taşınabilirliğin
    kanıtlanmadığı eklendi.
  - `SPEC.md` 3.6: "Determinizm farklı makinelerde de korunur" senaryosu
    yanlıştı, kaldırıldı; yerine BELİRSİZ notu ve TODO yazıldı.
  - `EKSIK_VAKALAR.md`'ye yeni eksik vaka eklendi (T-01: ikinci kurulumdan
    tekrar görseli).
  - CSV'deki kopya satır notlarındaki "farklı kaynak" ifadesi düzeltildi.
- **ders:** Ajan, bir çıkarımı "önerilen" diye sunduğunda bile bu bir
  çıkarımdır. Buradaki asıl hata çıkarımı yapmak değil, çıkarıma **dayanan
  başka iddialar yazmaktı** (AJ-12, SPEC 3.6). Doğrulanmamış bir temelin
  üstüne iddia inşa edilmemeliydi.

### H1-02 — "Ondalık alanlar daima 7 basamakla gösterilir" (AŞIRI GENELLEME)

- **ne dedi:** `LEDGER.md` AJ-09 ve `SPEC.md` bölüm 3.7'de şöyle yazmıştım:
  *"λ, kritik F ve actual power alanları **7 ondalık basamakla** gösterilir —
  **29/29**"*, ve SPEC'te senaryoyu `Given herhangi bir başarılı analiz`
  diye **koşulsuz** yazmıştım.
- **neden yanlış:** Sayım doğruydu — o 29 satırda gerçekten tutuyordu. Hata
  **sayımda değil, kapsamdadır**: 29 satırın tamamı a priori ve hepsinde λ
  küçüktü. Ben bunu evrensel bir kural gibi yazdım.
- **nasıl fark edildi:** ikinci veri partisinde üç karşı örnek çıktı —
  id 43'te λ `0`, id 44'te λ `120`, id 39/40'ta kritik F `199.5`.
  Hiçbiri 7 ondalıkla gösterilmiyordu.
- **hangi kontrol yakaladı:** **yeni oracle verisi.** Mevcut 29 satır üstünde
  yapılan hiçbir kontrol bunu yakalayamazdı; kural o veri kümesinde
  gerçekten tutuyordu. Karşı örnek ancak veri kümesi genişleyince geldi.
- **sonuç:**
  - `LEDGER.md`'de AJ-09 kaldırıldı, yerine **bölüm 2.4** yazıldı: üç karşı
    örnek, üç destekleyici örnek (a priori'de tam sayı λ'lar *yine de*
    7 ondalıklı: id 4, 13, 18) ve iki aday hipotez, ikisi de **doğrulanmamış**
    olarak işaretlendi.
  - `SPEC.md` bölüm 5'teki senaryo "çoğunlukla" diye gevşetildi ve karşı
    örnekler yorum olarak eklendi.
  - `EKSIK_VAKALAR.md` bölüm 3'e iki **ayırt edici** vektör eklendi (D-01, D-02).
- **ders:** Bir desenin "29/29 tuttuğu" ile "kural budur" aynı şey değil.
  Sayım, yalnızca **eldeki verinin kapsadığı aralıkta** geçerlidir. Desen
  yazarken kapsam da yazılmalıydı: *"29/29 a priori satırda, λ < 22 ve
  kritik F < 5 aralığında"*. O zaman genellemenin nerede sınandığı görünürdü.

### H1-03 — Çapraz kontrol aracının kendisi yanıldı (ajan hatası DEĞİL, kayda değer)

- **ne oldu:** id 43 (`f = 0`) için scipy `ncf.sf(...)` **−0.95** döndürdü,
  yani G*Power'ın `0.0500000` değeriyle 1.0 fark verdi. İlk bakışta bu bir
  "FARK" satırıydı.
- **nasıl çözüldü:** nonsantralite tam **0** iken `scipy.stats.ncf` sayısal
  olarak bozuluyor. `λ = 1e−9` verildiğinde `0.0500000001`, merkezî
  `scipy.stats.f.sf` ile `0.05` çıkıyor. Yani **doğru değer G*Power'ınki**.
- **neden burada:** Görev kuralı "uyuşmazlığı düzeltme, raporla; G*Power
  değeri her zaman geçerlidir" diyor. Eğer scipy'ye güvenip CSV'deki değeri
  "düzeltseydim" oracle'ı bozmuş olurdum. Kural tam da bu yüzden var.
- **sonuç:** CSV'ye dokunulmadı. `tests/uyum_raporu.md` bölüm 2'de bu durum
  açıkça belgelendi ve o satır için merkezî F kullanıldı.

### Sayısal okumalarda doğrulanmış yanlış iddia

**Yok.** CSV'ye yazılan 44 satırın tamamı bağımsız bir ikinci uygulamayla
(scipy) sınandı: a priori **30/30**, post hoc **12/12** tutarlı çıktı
(tek "FARK" scipy'nin kendi hatasıydı — H1-03). Üretim sırasında yapısal
`assert`'ler (df1 = k−1, df2 = N−k, λ = f²·N, a priori'de N grup katı)
42/42 geçti. Ek olarak 8 görselin `v{id}.png` eşlemesi yeniden okunarak
doğrulandı. Bu, ekran görüntülerini **yanlış okumadığımın** kanıtıdır.

> Dikkat: bu, yazdığım hiçbir şeyin yanlış olmadığı anlamına gelmez —
> H1-01 ve H1-02 tam da bunu gösterdi. **Sayısal okumalar** tutarlı;
> **yorumlar ve genellemeler** hâlâ insan incelemesi ve yeni veri bekliyor.
> İki hatamın da sayıları okumakla değil, sayıların **ne anlama geldiğini
> söylemekle** ilgili olması dikkate değer.

### Yakalanan riskler (hataya dönüşmeden önce durduruldu)

#### H1-R01 — Kılavuzdan hatırladığımı sanıp `[DOK]` yazma eğilimi
- **ne olacaktı:** `LEDGER.md`'nin `[DOK]` bölümüne "Faul vd. (2007) λ = f²·N
  olduğunu yazar" gibi satırlar yazmayı düşündüm.
- **nasıl fark edildi:** Görev dosyasının 5. kuralı ("emin olmadığın bir değeri
  uydurma") ve `[DOK]` etiketinin tanımı: *belgede yazan*. Oysa bu oturumda
  ne kılavuz ne de makale açıldı.
- **hangi kontrol yakaladı:** kural kontrolü (etiket tanımı).
- **sonuç:** `[DOK]` bölümü **boş bırakıldı**, yerine "kontrol edilecek aday"
  listesi (DOK-01 … DOK-05) yazıldı ve belgenin okunmadığı açıkça belirtildi.

#### H1-R02 — JPEG dosyasına `.png` adı verme
- **ne olacaktı:** Görev "`v{id}.png` olarak kopyala" diyor. 15 kaynak dosya
  JPEG; bunları olduğu gibi `.png` adıyla kopyalamak, içeriği JPEG olan ama
  adı PNG olan dosyalar üretirdi.
- **nasıl fark edildi:** kopyalama adımını yazarken fark edildi.
- **hangi kontrol yakaladı:** ajanın kendi kontrolü (dosya biçimi ↔ uzantı).
- **sonuç:** JPEG kaynaklar Pillow ile **gerçekten PNG'ye dönüştürüldü**.
  `oracle/RENAME_MAP.csv` içindeki `islem` sütunu her satır için `kopya` mı
  `jpeg->png donusturuldu` mu olduğunu kaydeder.

#### H1-R03 — `n_per_group`'u "okunmuş" gibi sunma
- **ne olacaktı:** CSV'de `n_per_group` sütunu var; bu alan G*Power'ın a priori
  tek yönlü ANOVA ekranında **gösterilmiyor**. Doldurulmuş hâliyle, ekrandan
  okunmuş gibi görünebilirdi.
- **hangi kontrol yakaladı:** görev dosyasının "ekranda görünen basamak
  sayısıyla yaz, okunamayan alanı boş bırak" kuralı.
- **sonuç:** Değer `total_n / groups` olarak **türetildi** ve bu durum
  `LEDGER.md` AJ-11'de ve son raporda açıkça belirtildi.

### Bilinçli olarak boş bırakılanlar (uydurulmadı)

- `oracle/anova_oneway.csv` → `kaynak` sütunu: önce 29 satırın hepsinde `?`
  bırakıldı, tahmin yazılmadı, kullanıcıya soruldu. Cevap alınınca `grup1`
  yapıldı. Soru sorulmasaydı yanlış değer yazılmış olacaktı (bkz. H1-01).
- `LEDGER.md` → `[REA]` tablosu: tamamen boş şablon.
- `README.md` → `GPower.exe` SHA-256 ve demo video linki.
- `oracle/anova_oneway.csv` → id 37 ve 38'de `f` sütunu **boş**. Bu iki
  ekran görüntüsünde `Effect size f` kutusu hata kutusunun arkasında kaldı.
  Değer, kullanıcının bana verdiği girdi listesinden **çıkarılabilirdi**
  (ikisi de 0.25 olacaktı) ama o liste ekran görüntüsü değil; kâhin yalnızca
  ekranda görünendir. `notlar` sütununa `okunamadi` yazıldı.
- `SPEC.md` → post hoc senaryoları artık **dolu** (ikinci veri partisiyle),
  ama bölüm 6'daki geçersiz girdi senaryoları hâlâ doğrulanmamış olarak
  işaretli; oraya beklenen değer yazılmadı.
- `LEDGER.md` bölüm 2.4 → gösterim biçimi kuralı. İki aday hipotez yazıldı,
  **hiçbiri "kural budur" diye sunulmadı.**

---

## Oturum 2 — (motor yazımı)

_(henüz başlamadı)_
