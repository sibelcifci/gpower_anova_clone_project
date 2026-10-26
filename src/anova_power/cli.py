"""CLI — motoru çağıran ince katman. Hesap yapmaz, yalnızca girdi/çıktı çevirir.

İki giriş yolu vardır; ikisi de aynı motoru (`core.analyze`) çağırır:

1. Bayraklı (ödev sözleşmesi):
     python -m anova_power --mode a_priori --f 0.25 --alpha 0.05 --power 0.80 --groups 3
     python -m anova_power --mode post_hoc  --f 0.25 --alpha 0.05 --total-n 100 --groups 3
2. stdin'den tek JSON nesnesi (SPEC.md bölüm 2 sözleşmesi):
     echo '{"mode":"a_priori","f":0.25,"alpha":0.05,"power":0.8,"groups":3}' | python -m anova_power

Her iki yolda da çıktı **tek satır JSON**'dur. Başarıda çıkış kodu 0;
geçersiz girdide çıktı yalnızca `{"error":"..."}` ve çıkış kodu 1 olur.
"""
import argparse
import json
import sys

from .core import analyze

# Bazı koşucular test ailesini --test ile geçiyor; tek aile desteklendiği için
# kabul edilir ama yalnızca doğrulanır.
AILE = {"anova", "anova_oneway", "f", "anova-oneway", "anova_fixed_omnibus_oneway"}


def _ayristirici():
    p = argparse.ArgumentParser(
        prog="anova_power", add_help=True,
        description="Tek yönlü ANOVA (F testi, sabit etkiler, omnibus) güç analizi")
    p.add_argument("--test", default=None, help="test ailesi (yalnızca anova destekli)")
    p.add_argument("--mode", "--type", dest="mode", default=None,
                   choices=["a_priori", "post_hoc"], help="analiz türü")
    p.add_argument("--f", "--effect-size", dest="f", type=float, default=None,
                   help="etki büyüklüğü f (Cohen)")
    p.add_argument("--alpha", type=float, default=None, help="alfa hata olasılığı")
    p.add_argument("--power", type=float, default=None, help="hedef güç (a_priori)")
    p.add_argument("--groups", "-k", type=int, default=None, help="grup sayısı k")
    p.add_argument("--total-n", "--total_n", "-n", dest="total_n", type=int,
                   default=None, help="toplam örneklem N (post_hoc)")
    p.add_argument("--json", default=None,
                   help="girdiyi JSON metni olarak ver (stdin yerine)")
    return p


def _bayraktan_veri(arg):
    """Bayrakları motorun beklediği sözlüğe çevirir. Verilmeyen alan eklenmez;
    eksik alanın hatasını motor üretir, böylece tek doğrulama yeri kalır."""
    if arg.test is not None and arg.test.strip().lower() not in AILE:
        raise ValueError(f"--test: desteklenmeyen test ailesi: {arg.test}")
    veri = {"mode": arg.mode}
    for ad, deger in (("f", arg.f), ("alpha", arg.alpha), ("groups", arg.groups)):
        if deger is not None:
            veri[ad] = deger
    if arg.mode == "a_priori" and arg.power is not None:
        veri["power"] = arg.power
    if arg.mode == "post_hoc" and arg.total_n is not None:
        veri["total_n"] = arg.total_n
    # Moda ait olmayan bayrak sessizce yutulmaz; motor bunu reddetmeli.
    if arg.mode == "a_priori" and arg.total_n is not None:
        veri["total_n"] = arg.total_n
    if arg.mode == "post_hoc" and arg.power is not None:
        veri["power"] = arg.power
    return veri


def main(argv=None):
    # JSON akışı Windows yerel kod sayfasına bağlı olmamalı.
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, OSError):
        pass
    arg = _ayristirici().parse_args(argv)
    try:
        if arg.json is not None:
            veri = json.loads(arg.json)
        elif arg.mode is None:
            try:
                sys.stdin.reconfigure(encoding="utf-8-sig")
            except (AttributeError, OSError):
                pass
            veri = json.loads(sys.stdin.read(), parse_constant=_sabit_reddet)
        else:
            veri = _bayraktan_veri(arg)
        sonuc, kod = analyze(veri), 0
    except (ValueError, TypeError, OverflowError, ArithmeticError) as hata:
        sonuc, kod = {"error": str(hata)}, 1
    print(json.dumps(sonuc, ensure_ascii=False, allow_nan=False, separators=(",", ":")))
    return kod


def _sabit_reddet(metin):
    raise ValueError(f"Geçersiz JSON sabiti: {metin}")


if __name__ == "__main__":
    sys.exit(main())
