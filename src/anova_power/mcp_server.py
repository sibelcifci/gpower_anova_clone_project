"""MCP sunucusu — motoru çağıran ince katman (ödev bonus +15).

Hesap yapmaz: her araç `core.analyze`'ı çağırır. CLI ile **aynı** motoru
paylaşır, bu yüzden iki arayüzün sonucu tanım gereği aynıdır.

Protokol: Model Context Protocol, stdio taşıması üzerinde satır sınırlı
JSON-RPC 2.0. Üçüncü parti bağımlılık **yoktur**; yalnızca standart kütüphane.
Bu tercih bilinçli: `pip install mcp` gerektirmediği için teslim edilen repo
her makinede olduğu gibi çalışır.

Çalıştırma (elle deneme):

    echo '{"jsonrpc":"2.0","id":1,"method":"tools/list"}' | python -m anova_power.mcp_server

Claude Code / Claude Desktop yapılandırması için repo kökündeki `.mcp.json`.
"""
import json
import sys

from .core import analyze

PROTOKOL = "2024-11-05"
SUNUCU = {"name": "anova-power", "version": "1.0.0"}

_ORTAK = {
    "f": {"type": "number", "minimum": 0,
          "description": "Etki büyüklüğü f (Cohen). Post hoc'ta 0 geçerlidir."},
    "alpha": {"type": "number", "exclusiveMinimum": 0, "exclusiveMaximum": 1,
              "description": "Alfa hata olasılığı."},
    "groups": {"type": "integer", "minimum": 2,
               "description": "Grup sayısı k."},
}

ARACLAR = [
    {
        "name": "anova_a_priori",
        "description": ("Tek yönlü ANOVA (F testi, sabit etkiler, omnibus) için "
                        "gereken toplam örneklem büyüklüğünü (N) hesaplar. "
                        "'Kaç denek gerekir?' sorusunun cevabı budur. "
                        "Bulunan N daima grup sayısının tam katıdır."),
        "inputSchema": {
            "type": "object",
            "properties": dict(_ORTAK, power={
                "type": "number", "exclusiveMinimum": 0, "exclusiveMaximum": 1,
                "description": "İstenen güç (1 - beta)."}),
            "required": ["f", "alpha", "power", "groups"],
        },
    },
    {
        "name": "anova_post_hoc",
        "description": ("Verilen toplam örneklem için gerçekleşen gücü hesaplar. "
                        "Toplam N'in grup sayısının katı olması gerekmez; katı "
                        "değilse sonuçta ayrıca bir 'warning' alanı döner."),
        "inputSchema": {
            "type": "object",
            "properties": dict(_ORTAK, total_n={
                "type": "integer",
                "description": "Toplam örneklem N. Grup sayısından büyük olmalı."}),
            "required": ["f", "alpha", "total_n", "groups"],
        },
    },
]

MOD = {"anova_a_priori": "a_priori", "anova_post_hoc": "post_hoc"}


def _araci_calistir(ad, argumanlar):
    """Aracı motora bağlar. Motorun hatası MCP araç hatasına çevrilir."""
    if ad not in MOD:
        raise ValueError(f"Bilinmeyen araç: {ad}")
    if not isinstance(argumanlar, dict):
        raise ValueError("arguments bir nesne olmalı")
    return analyze(dict(argumanlar, mode=MOD[ad]))


def _yanit(istek_id, sonuc):
    return {"jsonrpc": "2.0", "id": istek_id, "result": sonuc}


def _hata(istek_id, kod, mesaj):
    return {"jsonrpc": "2.0", "id": istek_id, "error": {"code": kod, "message": mesaj}}


def istegi_isle(istek):
    """Tek bir JSON-RPC isteğini işler. Bildirimler için None döndürür."""
    yontem = istek.get("method")
    istek_id = istek.get("id")

    if yontem == "initialize":
        istenen = (istek.get("params") or {}).get("protocolVersion") or PROTOKOL
        return _yanit(istek_id, {
            "protocolVersion": istenen,
            "capabilities": {"tools": {}},
            "serverInfo": SUNUCU,
        })
    if yontem in ("notifications/initialized", "initialized"):
        return None
    if yontem == "ping":
        return _yanit(istek_id, {})
    if yontem == "tools/list":
        return _yanit(istek_id, {"tools": ARACLAR})
    if yontem == "tools/call":
        parametre = istek.get("params") or {}
        try:
            sonuc = _araci_calistir(parametre.get("name"),
                                    parametre.get("arguments") or {})
        except (ValueError, TypeError, OverflowError, ArithmeticError) as hata:
            # Araç düzeyi hata: protokol hatası değil, isError ile döner.
            return _yanit(istek_id, {
                "content": [{"type": "text",
                             "text": json.dumps({"error": str(hata)}, ensure_ascii=False)}],
                "isError": True,
            })
        return _yanit(istek_id, {
            "content": [{"type": "text",
                         "text": json.dumps(sonuc, ensure_ascii=False)}],
            "structuredContent": sonuc,
            "isError": False,
        })
    if istek_id is None:
        return None  # tanınmayan bildirim sessizce yutulur
    return _hata(istek_id, -32601, f"Desteklenmeyen yöntem: {yontem}")


def main():
    for akis, kodlama in ((sys.stdin, "utf-8"), (sys.stdout, "utf-8")):
        try:
            akis.reconfigure(encoding=kodlama)
        except (AttributeError, OSError):
            pass
    for satir in sys.stdin:
        satir = satir.strip()
        if not satir:
            continue
        try:
            istek = json.loads(satir)
        except json.JSONDecodeError as hata:
            cevap = _hata(None, -32700, f"Ayrıştırma hatası: {hata}")
        else:
            cevap = istegi_isle(istek) if isinstance(istek, dict) else _hata(
                None, -32600, "İstek bir nesne olmalı")
        if cevap is not None:
            sys.stdout.write(json.dumps(cevap, ensure_ascii=False) + "\n")
            sys.stdout.flush()
    return 0


if __name__ == "__main__":
    sys.exit(main())
