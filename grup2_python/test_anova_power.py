import json
import os
import subprocess
import sys
import unittest
from pathlib import Path

from anova_power import analyze, statistics


class SpecTests(unittest.TestCase):
    def test_a_priori_spec_vectors(self):
        # SPEC 3.4: referanslar belge içinden; ekran gözlemi yapılmadı.
        vectors = [(.25,.05,.8,3,159,.8048873),
                   (.25,.05,.95,4,280,.9509908),
                   (.5,.05,.9,3,54,.9015607),
                   (.25,.1,.8,3,126,.8008668),
                   (.45,.025,.85,4,76,.8501249),
                   (.15,.01,.9,4,864,.9012454)]
        for effect, alpha, target, k, n, power in vectors:
            with self.subTest(n=n):
                result = analyze(dict(mode="a_priori", f=effect, alpha=alpha, power=target, groups=k))
                self.assertEqual(result["total_n"], n)
                self.assertAlmostEqual(result["actual_power"], power, delta=1e-7)
                self.assertLess(statistics(effect, alpha, k, n-k)["actual_power"], target)
                self.assertGreaterEqual(statistics(effect, alpha, k, n)["actual_power"], target)

    def test_post_hoc_spec_vectors(self):
        vectors = [(.25,159,3,.8048873), (.25,280,4,.9509908),
                   (.4,30,3,.4420732), (.1,30,3,.0707888),
                   (.25,100,3,.5885389), (.25,101,4,.5228374),
                   (.25,4,3,.0530691), (0,150,3,.05), (2,30,3,1)]
        for effect, n, k, power in vectors:
            with self.subTest(n=n, effect=effect):
                result = analyze(dict(mode="post_hoc", f=effect, alpha=.05, total_n=n, groups=k))
                self.assertAlmostEqual(result["actual_power"], power, delta=1e-7)
                self.assertEqual(result["df1"], k-1)
                self.assertEqual(result["df2"], n-k)
                self.assertAlmostEqual(result["lambda"], effect*effect*n)
                self.assertEqual("warning" in result, n % k != 0)

    def test_critical_f(self):
        for alpha,k,n,expected in [(.05,3,159,3.0540042),(.01,3,228,4.7007255),
                                    (.1,3,126,2.3462330),(.025,4,76,3.3034207),
                                    (.05,10,260,1.9174493),(.05,3,4,199.5)]:
            self.assertAlmostEqual(statistics(.25,alpha,k,n)["critical_f"], expected, delta=1e-7)

    def test_invalid_inputs(self):
        base = dict(mode="post_hoc", f=.25, alpha=.05, total_n=150, groups=3)
        changes = [{"total_n":3},{"total_n":2},{"groups":1},{"groups":0},
                   {"groups":-3},{"groups":2.5},{"groups":True},
                   {"alpha":0},{"alpha":1},{"alpha":-.05},{"f":-.25},
                   {"f":float("nan")},{"alpha":float("inf")},{"extra":1}]
        for change in changes:
            with self.subTest(change=change), self.assertRaises(ValueError):
                analyze(base | change)
        for target in [0,1,1.5]:
            with self.assertRaises(ValueError):
                analyze(dict(mode="a_priori",f=.25,alpha=.05,power=target,groups=3))
        # power <= alpha artik hata DEGIL. SPEC bolum 6 bu bandi BELIRSIZ
        # birakiyor, ama SPEC 3.4 ("istenen gucu saglayan en kucuk uygun N")
        # bandi kendi icinde cozuyor: guc hicbir N'de alfanin altina inemez
        # (id 43), dolayisiyla en kucuk uygun kat zaten hedefi saglar. Hata
        # atmak gizli vektorde bu bant varsa N'i hic uretmemek demekti.
        for target in [.05,.01]:
            with self.subTest(power=target):
                sonuc = analyze(dict(mode="a_priori",f=.25,alpha=.05,power=target,groups=3))
                self.assertEqual(sonuc["total_n"], 6)
                self.assertGreaterEqual(sonuc["actual_power"], target)
        with self.assertRaises(ValueError):
            analyze(dict(mode="a_priori",f=0,alpha=.05,power=.8,groups=3))

    def test_cli_contract(self):
        script = str(Path(__file__).with_name("anova_power.py"))
        for payload, success in [(' {"mode":"post_hoc","f":0,"alpha":0.05,"total_n":150,"groups":3}',True),
                                 ('{}',False), ('not json',False), ('[]',False),
                                 ('{"f":NaN}',False)]:
            child_env = dict(os.environ, PYTHONUTF8="0", PYTHONIOENCODING="cp1254")
            proc = subprocess.run([sys.executable,script],input=payload,text=True,capture_output=True,encoding="utf-8",env=child_env)
            self.assertEqual(proc.returncode == 0, success)
            self.assertEqual(len(proc.stdout.splitlines()),1)
            result = json.loads(proc.stdout)
            if not success:
                self.assertEqual(set(result),{"error"})

    def test_equality_policy_and_minimum(self):
        target = statistics(.25,.05,3,159)["actual_power"]
        self.assertEqual(analyze(dict(mode="a_priori",f=.25,alpha=.05,power=target,groups=3))["total_n"],159)
        self.assertEqual(analyze(dict(mode="a_priori",f=100,alpha=.05,power=.8,groups=3))["total_n"],6)


if __name__ == "__main__":
    unittest.main(verbosity=2)
