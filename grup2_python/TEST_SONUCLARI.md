# Test sonuçları

Tarih: 25 Ekim 2026

Ortam: Windows, Python 3.14, SciPy 1.18.1, NumPy 2.5.4.
Bağımlılıklar çalışma klasörüne kuruldu; testler terminalden çalıştırıldı.
VS Code arayüzünde çalıştırma yapılmadı.

`python -m unittest discover -s outputs -p test_anova_power.py -v`

Sonuç: **6 test yöntemi başarılı**, süre 13,119 saniye.
Bu yöntemler parametreli alt örnekler içerir:

- SPEC bölüm 3.4'teki 6 a priori örneği: N ve gerçekleşen güç uyumlu.
- SPEC bölüm 4'teki 9 post hoc örneği: güç, df ve lambda uyumlu.
- 6 kritik F referansı tolerans içinde.
- Geçersiz girdiler, uyarı, en küçük yeterli N ve CLI sözleşmesi başarılı.
- Belirsiz eşitlik/minimum N için seçilen uygulama davranışı başarılı.

Ek komut satırı kontrolü:

Girdi: `{"mode":"a_priori","f":0.25,"alpha":0.05,"power":0.8,"groups":3}`

Çıktı:

```json
{"lambda":9.9375,"critical_f":3.0540042,"df1":2,"df2":156,"actual_power":0.8048873,"total_n":159}
```

Referans yalnızca kullanıcı tarafından verilen SPEC.md'dir. G*Power açılmadı.
Belgenin atıf yaptığı 44 satırlık CSV ve ekran görüntüleri sağlanmadığından
tam G*Power doğrulaması yapılmadı. Uygulama kararları README.md'dedir.
