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
