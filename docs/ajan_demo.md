# AI Ajanı Katmanı (+10) — MCP üzerinden doğal dil

Ajan katmanı **kendi hesabını yapmaz**. Doğal dildeki soruyu MCP araç
çağrısına çevirir, aracı çağırır, dönen JSON'u cümleye döker. Hesap
`src/anova_power/core.py`'de, tek yerde kalır (ödev kuralı 3).

```
kullanıcı (doğal dil)
   │
   ▼
AI ajanı (Claude Code / Claude Desktop)
   │  MCP: tools/call
   ▼
src/anova_power/mcp_server.py      ← ince katman, hesap yok
   │  analyze(...)
   ▼
src/anova_power/core.py            ← TEK MOTOR
```

## Kurulum

Repo kökünde `.mcp.json` hazırdır:

```json
{
  "mcpServers": {
    "anova-power": {
      "command": "python",
      "args": ["-m", "anova_power.mcp_server"],
      "env": { "PYTHONPATH": "src", "PYTHONUTF8": "1" }
    }
  }
}
```

Claude Code'u **repo kökünde** açmak yeterlidir; sunucu `anova-power` adıyla
yüklenir (`/mcp` ile doğrulanabilir). Üçüncü parti bağımlılık gerekmez.

## Doğrulanmış araç alışverişi

Aşağıdaki alışveriş `tests/mcp_test.py` ile otomatik doğrulanır ve elle de
yeniden üretilebilir:

```bash
PYTHONPATH=src PYTHONUTF8=1 python -m anova_power.mcp_server
```

### Araç listesi

İstek:

```json
{"jsonrpc":"2.0","id":2,"method":"tools/list"}
```

Sunucu iki araç bildirir: `anova_a_priori`, `anova_post_hoc`.

### Örnek 1 — "Kaç denek gerekir?"

> **Kullanıcı:** Üç gruplu bir çalışma planlıyorum, orta büyüklükte bir etki
> bekliyorum ve %80 güç istiyorum. Kaç denek gerekir?

Ajanın yapması gereken eşleme: *orta büyüklükte etki* → `f = 0.25`
(Cohen'in orta etki eşiği), *%80 güç* → `power = 0.80`, *üç grup* →
`groups = 3`, belirtilmeyen `alpha` → `0.05` (alan standardı).

Araç çağrısı:

```json
{"jsonrpc":"2.0","id":3,"method":"tools/call",
 "params":{"name":"anova_a_priori",
           "arguments":{"f":0.25,"alpha":0.05,"power":0.80,"groups":3}}}
```

Sunucu yanıtı (`isError: false`):

```json
{"lambda":9.9375,"critical_f":3.0540042,"df1":2,"df2":156,
 "actual_power":0.8048873,"total_n":159}
```

Ajanın cevabı: **toplam 159 denek**, grup başına 53. Gerçekleşen güç 0.8049,
yani istenen %80'in hemen üstünde. Bu değer oracle id 15/30 ile birebir aynıdır.

### Örnek 2 — "Elimdeki örneklemle gücüm ne?"

> **Kullanıcı:** 100 kişiyi üç gruba bölebiliyorum. Gücüm ne olur?

```json
{"jsonrpc":"2.0","id":4,"method":"tools/call",
 "params":{"name":"anova_post_hoc",
           "arguments":{"f":0.25,"alpha":0.05,"total_n":100,"groups":3}}}
```

Yanıt:

```json
{"lambda":6.25,"critical_f":3.0901867,"df1":2,"df2":97,
 "actual_power":0.5885389,
 "warning":"Toplam N grup sayısının katı değildir; analiz ortalama grup büyüklüğüne dayanır."}
```

Ajanın cevabı: güç yalnızca **%58.9** — yetersiz. Ayrıca `warning` alanı
100'ün 3'e tam bölünmediğini bildirir; ajan bunu kullanıcıya iletmelidir,
çünkü G*Power da aynı durumda bir `Please note` kutusu gösterir (SPEC 4.2,
oracle id 32/33).

### Örnek 3 — hata yolu

> **Kullanıcı:** 3 kişiyi 3 gruba bölsem?

```json
{"jsonrpc":"2.0","id":5,"method":"tools/call",
 "params":{"name":"anova_post_hoc",
           "arguments":{"f":0.25,"alpha":0.05,"total_n":3,"groups":3}}}
```

Yanıt (`isError: true`):

```json
{"error":"total_n grup sayısından büyük olmalı"}
```

Bu, G*Power'ın `Input error` kutusunun CLI/MCP karşılığıdır (oracle id 37/38,
`LEDGER.md` AJ-16, ikili kanıtı REA-07).

## Doğrulama

```bash
python -m unittest discover -s tests -p "mcp_test.py" -v
```

`test_sonuclar_motorla_ayni`, MCP çıktısının `core.analyze` çıktısıyla
**birebir aynı** olduğunu dört vakada sınar. Bu, MCP katmanının kendi hesabını
yapmadığının testle kanıtıdır.

## Eksik

- [ ] Claude Code oturumundan doğal dil dökümü / ekran görüntüsü
      (`docs/ajan_demo_ekran.png`) — araç çağrısı ve cevabı birlikte görünmeli.
- [ ] 60 saniyelik demo videosu (README'deki "Demo Video" bölümü).

> Yukarıdaki araç alışverişleri **gerçekten koşturuldu** ve `tests/mcp_test.py`
> ile otomatik doğrulanıyor. Doğal dil adımının ekran görüntüsü henüz
> eklenmedi; eklenene kadar bu dosya alışverişin kendisini kanıt olarak sunar.

---

# Gerçek ajan oturumu — 2026-10-26

> Bu bölümdeki alışveriş **elle yazılmadı.** Claude Code (Claude Opus 5)
> oturumunda, `.mcp.json` üzerinden yüklenen `anova-power` sunucusunun
> araçları gerçekten çağrıldı; aşağıdakiler o çağrıların birebir çıktısıdır.
> Yukarıdaki bölümler protokol düzeyinde örnektir, bu bölüm ajan düzeyinde
> kanıttır.

Ajanın elindeki araçlar: `mcp__anova-power__anova_a_priori`,
`mcp__anova-power__anova_post_hoc`. Ajan hiçbir hesabı kendisi yapmadı;
doğal dili araç çağrısına çevirdi ve dönen JSON'u cümleye döktü.

## 1. "Kaç denek gerekir?"

> **Kullanıcı:** Üç gruplu bir çalışma planlıyorum, orta büyüklükte bir etki
> bekliyorum ve %80 güç istiyorum. Kaç denek gerekir?

Ajanın yaptığı eşleme: *orta büyüklükte etki* → `f = 0.25` (Cohen'in orta
etki eşiği), *%80 güç* → `power = 0.80`, *üç grup* → `groups = 3`,
belirtilmeyen `alpha` → `0.05` (alan standardı).

Araç çağrısı `anova_a_priori(f=0.25, alpha=0.05, power=0.8, groups=3)`,
dönen değer:

```json
{"lambda":9.9375,"critical_f":3.0540042,"df1":2,"df2":156,
 "actual_power":0.8048873,"total_n":159}
```

> **Ajan:** Toplam **159 denek** gerekiyor, yani grup başına 53 kişi.
> Bu örneklemle gerçekleşen güç 0.8049 — istediğiniz %80'in biraz üstünde,
> çünkü N grup sayısının tam katı olmak zorunda.

Doğrulama: bu satır oracle'da **id 15 ve id 30** olarak iki kez var.

## 2. "Elimdeki örneklemle gücüm ne olur?"

> **Kullanıcı:** Elimde 100 kişi var, 3 grup, etki büyüklüğü 0.25.
> Gücüm ne olur?

Araç çağrısı `anova_post_hoc(f=0.25, alpha=0.05, total_n=100, groups=3)`,
dönen değer:

```json
{"lambda":6.25,"critical_f":3.0901867,"df1":2,"df2":97,
 "actual_power":0.5885389,
 "warning":"Toplam N grup sayısının katı değildir; analiz ortalama grup büyüklüğüne dayanır."}
```

> **Ajan:** Gücünüz **0.5885**, yani yaklaşık %59 — hedeflenen %80'in
> epey altında. Ayrıca 100, 3'e tam bölünmüyor; hesap ortalama grup
> büyüklüğüne dayanıyor. %80 güç için 159 kişiye çıkmanız gerekir.

Doğrulama: oracle **id 32 / id 33** (`0.5885389`), uyarı metni **AJ-14**.

## 3. Üçüncü çağrı bir KUSUR ortaya çıkardı

Bugün motora eklenen kuralı (`power < alpha` reddedilir, SPEC 6.8) ajan
katmanından sınadık:

Araç çağrısı `anova_a_priori(f=0.25, alpha=0.05, power=0.01, groups=3)`,
dönen değer:

```json
{"lambda":0.375,"critical_f":9.5520945,"df1":2,"df2":3,
 "actual_power":0.0622405,"total_n":6}
```

**Bu yanlıştır.** Aynı girdiyle CLI şunu döndürüyor:

```json
{"error":"power: alfadan küçük olamaz"}
```

### Sebep: sunucu süreci bayat

MCP sunucusu oturum başında, `core.py`'ye kural eklenmeden **önce**
başlatılmıştı; belleğindeki modül eski sürümdü. Kod iki yerde değil, tek
yerdedir — `mcp_server.py` içinde hesap yoktur:

```python
from .core import analyze
...
return analyze(dict(argumanlar, mode=MOD[ad]))
```

Yani bu, ödev kuralı 3'ün ihlali **değil**; tam tersine ince katman
olmanın doğrudan sonucu: sunucu, yüklendiği andaki motoru yansıtır.

### Ders

**Motor değiştiğinde MCP sunucusu yeniden başlatılmalıdır.** Claude Code'da
bu, oturumu yeniden açmak (ya da MCP bağlantısını yenilemek) demektir.
Tek motor mimarisi kodu tek yerde tutar ama **çalışan süreci kendiliğinden
tazelemez**.

**Aynı oturumda tekrar denendi (2026-10-26):** çağrı birebir yinelendi,
sonuç değişmedi — yine `total_n: 6`. Bu, tanıyı **güçlendiriyor**: sorun
geçici bir aksaklık değil, sürecin belleğindeki modülün eskiliği. Kod
diskte doğru (CLI aynı anda hata döndürüyor), süreç ise oturum boyunca
aynı kalıyor.

> **TODO (kapatılmadı):** Sunucu yeniden başlatıldıktan sonra 3. çağrı
> tekrarlanmalı ve `{"error":"power: alfadan küçük olamaz"}` döndüğü
> doğrulanmalıdır. Claude Code'da bu, oturumu kapatıp yeniden açmak demek;
> bu belgeyi yazan oturumun kendisi sonlanacağı için yapılmadı.
> **Bu belgede doğrulanmış gibi gösterilmiyor, çünkü doğrulanmadı.**

