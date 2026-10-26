"""MCP sunucusu testi — gerçek alt süreç üzerinden protokol sözleşmesi.

Sunucuyu `python -m anova_power.mcp_server` olarak ayrı bir süreçte başlatır,
stdio üzerinden JSON-RPC konuşur ve şunları doğrular:

- `initialize` el sıkışması ve sunucu kimliği
- `tools/list` iki aracı bildiriyor
- `tools/call` sonuçları **CLI ile birebir aynı** (tek motor kanıtı)
- geçersiz girdide `isError: true` ve yalnızca `error` alanı
- bildirimlere (`notifications/initialized`) yanıt üretilmiyor

Çalıştırma (repo kökünden):

    python -m unittest discover -s tests -p "mcp_test.py" -v
"""
import json
import os
import subprocess
import sys
import unittest

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(KOK, "src")
sys.path.insert(0, SRC)

from anova_power import analyze  # noqa: E402


def konus(istekler):
    """Sunucuyu çalıştırır, satır sınırlı istekleri gönderir, yanıtları döndürür."""
    ortam = dict(os.environ, PYTHONPATH=SRC, PYTHONUTF8="1")
    girdi = "".join(json.dumps(i, ensure_ascii=False) + "\n" for i in istekler)
    surec = subprocess.run(
        [sys.executable, "-m", "anova_power.mcp_server"],
        input=girdi, capture_output=True, text=True, encoding="utf-8",
        env=ortam, cwd=KOK, timeout=120)
    if surec.returncode != 0:
        raise AssertionError(f"sunucu {surec.returncode} ile cikti: {surec.stderr[:500]}")
    return [json.loads(s) for s in surec.stdout.splitlines() if s.strip()]


EL_SIKISMA = [
    {"jsonrpc": "2.0", "id": 1, "method": "initialize",
     "params": {"protocolVersion": "2024-11-05", "capabilities": {},
                "clientInfo": {"name": "test", "version": "1"}}},
    {"jsonrpc": "2.0", "method": "notifications/initialized"},
]


class McpTests(unittest.TestCase):
    def test_initialize_ve_bildirim(self):
        yanitlar = konus(EL_SIKISMA)
        # Bildirime yanit URETILMEMELI: tek yanit beklenir.
        self.assertEqual(len(yanitlar), 1)
        sonuc = yanitlar[0]["result"]
        self.assertEqual(sonuc["serverInfo"]["name"], "anova-power")
        self.assertIn("tools", sonuc["capabilities"])

    def test_tools_list(self):
        yanitlar = konus(EL_SIKISMA + [
            {"jsonrpc": "2.0", "id": 2, "method": "tools/list"}])
        araclar = yanitlar[-1]["result"]["tools"]
        self.assertEqual({a["name"] for a in araclar},
                         {"anova_a_priori", "anova_post_hoc"})
        for arac in araclar:
            self.assertTrue(arac["description"].strip())
            self.assertEqual(arac["inputSchema"]["type"], "object")
            self.assertIn("groups", arac["inputSchema"]["properties"])

    def test_sonuclar_motorla_ayni(self):
        """MCP katmani kendi hesabini yapmiyor: cikti motorla birebir ayni."""
        vakalar = [
            ("anova_a_priori", {"f": .25, "alpha": .05, "power": .80, "groups": 3}, "a_priori"),
            ("anova_a_priori", {"f": .25, "alpha": .05, "power": .95, "groups": 4}, "a_priori"),
            ("anova_post_hoc", {"f": .25, "alpha": .05, "total_n": 100, "groups": 3}, "post_hoc"),
            ("anova_post_hoc", {"f": 0, "alpha": .05, "total_n": 150, "groups": 3}, "post_hoc"),
        ]
        istekler = list(EL_SIKISMA)
        for sira, (ad, argumanlar, _) in enumerate(vakalar, start=10):
            istekler.append({"jsonrpc": "2.0", "id": sira, "method": "tools/call",
                             "params": {"name": ad, "arguments": argumanlar}})
        yanitlar = {y["id"]: y for y in konus(istekler) if "id" in y}
        for sira, (ad, argumanlar, mod) in enumerate(vakalar, start=10):
            with self.subTest(arac=ad, argumanlar=argumanlar):
                sonuc = yanitlar[sira]["result"]
                self.assertFalse(sonuc["isError"])
                mcp_cikti = json.loads(sonuc["content"][0]["text"])
                self.assertEqual(mcp_cikti, analyze(dict(argumanlar, mode=mod)))

    def test_gecersiz_girdi_isError(self):
        vakalar = [
            ("anova_post_hoc", {"f": .25, "alpha": .05, "total_n": 3, "groups": 3}),
            ("anova_a_priori", {"f": .25, "alpha": 0, "power": .8, "groups": 3}),
            ("anova_a_priori", {"f": .25, "alpha": .05, "power": .8, "groups": 1}),
            ("anova_bilinmeyen", {"f": .25}),
        ]
        istekler = list(EL_SIKISMA)
        for sira, (ad, argumanlar) in enumerate(vakalar, start=20):
            istekler.append({"jsonrpc": "2.0", "id": sira, "method": "tools/call",
                             "params": {"name": ad, "arguments": argumanlar}})
        yanitlar = {y["id"]: y for y in konus(istekler) if "id" in y}
        for sira, (ad, argumanlar) in enumerate(vakalar, start=20):
            with self.subTest(arac=ad):
                sonuc = yanitlar[sira]["result"]
                self.assertTrue(sonuc["isError"])
                self.assertEqual(set(json.loads(sonuc["content"][0]["text"])), {"error"})

    def test_bilinmeyen_yontem(self):
        yanitlar = konus(EL_SIKISMA + [
            {"jsonrpc": "2.0", "id": 3, "method": "kaynaklar/listele"}])
        self.assertEqual(yanitlar[-1]["error"]["code"], -32601)


if __name__ == "__main__":
    unittest.main(verbosity=2)
