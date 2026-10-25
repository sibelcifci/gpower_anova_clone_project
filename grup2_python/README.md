# Grup 2 — Tek yönlü ANOVA güç analizi

Bu program, sağlanan SPEC.md'deki davranışlara göre hazırlanmıştır.
G*Power kurulmadı ve ekranı açılmadı. SPEC.md kaynak belgenin değiştirilmemiş
kopyasıdır. Kaynakta anılan CSV, ekran görüntüleri ve uyum raporu verilmedi;
bağımsız G*Power uyumu iddiası yoktur.

## VS Code ile çalıştırma (Windows / PowerShell)

Bu klasörü VS Code'da açın. Terminalde:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
'{"mode":"a_priori","f":0.25,"alpha":0.05,"power":0.8,"groups":3}' | .\.venv\Scripts\python.exe anova_power.py
'{"mode":"post_hoc","f":0.25,"alpha":0.05,"total_n":100,"groups":3}' | .\.venv\Scripts\python.exe anova_power.py
.\.venv\Scripts\python.exe -m unittest discover -s . -p test_anova_power.py -v
```

İlk örnek N=159 ve actual_power=0.8048873 üretir. İkinci örnek
actual_power=0.5885389 ve warning alanı üretir. Program standart girdiden
tek JSON nesnesi okur, standart çıktıya tek satır JSON yazar. Girdi sonu
gerektiği için terminalde doğrudan etkileşimli giriş yerine yukarıdaki boruyu
veya dosyayı kullanın. Dosya örneği:

```powershell
Get-Content -Raw input.json | .\.venv\Scripts\python.exe anova_power.py
```

Başarı çıkış kodu 0, girdi/hesap hatası 1'dir. Hata JSON'unda sadece error
bulunur. Bağımlılıkların önceden kurulmuş olması gerekir.

## Hesap ve belirsizlik kararları

- df1=k−1, df2=N−k, lambda=f²N. Kritik F merkezi F dağılımının üst kuyruk
  alfa sınırıdır. Güç, bu sınırın üzerindeki nonsantral F olasılığıdır.
- A priori: grup başına tam sayı kişi üzerinden arama yapılır. Hedef gücü
  sağlayan en küçük grup sayısı katı seçilir. Karşılaştırmalar çıktı
  yuvarlanmadan önce yapılır; hedefe tam eşitlik kabul edilir.
- SPEC'in doğrulamadığı iki karar: grup başına minimum 2 kişi; tam eşitlikte
  aynı N'de kalma. Bunlar G*Power'dan gözlemlenmiş kurallar değildir.
- A priori power <= alpha desteklenmez ve açıklayıcı hata döner.
  f=0 ve power>alpha durumunda sonlu çözüm olmadığı için hata döner.
  Post hoc f=0 kabul edilir ve güç alpha olur.
- Kaynak sınırı toplam N=100.000.000'dur; G*Power davranışından türetilmedi.
  Çok uç parametrelerde güvenilir sonuç alınamazsa hata üretilir.
- Ondalık sonuçlar JSON sayısı olarak 7 ondalığa yuvarlanır; sondaki sıfırlar
  korunmaz. Python round kullanılır (tam yarımda çifte yuvarlama; ikili kayan
  nokta temsilinin etkileri vardır). SPEC ekran biçiminin kesin kuralını
  vermediği için G*Power'ın metinsel gösterimi taklit edilmez. Grafik yoktur.
- Tam sayı değerli JSON sayıları (örneğin 3.0) kabul edilir; bool, metin,
  NaN, sonsuz ve moda ait olmayan alanlar reddedilir.
- Post hoc çıktısında total_n alanı bulunmaz; SPEC çıktı tablosu izlenir.

## Test kapsamı

Testler SPEC içindeki 6 a priori ve 9 post hoc vektörünü, 6 kritik F
değerini; minimal N koşulunu, uyarıları, girdi hatalarını ve gerçek alt süreç
üzerinden JSON/çıkış kodu sözleşmesini kontrol eder. Eşitlik ve minimum N
testleri seçilen uygulama politikasını sınar. Ondalık referanslar için mutlak
tolerans 1e-7, N ve serbestlik dereceleri için tam eşitlik aranır.

44 satırın tümü sağlanmadığı için tam oracle regresyonu yapılmamıştır.
G*Power'ın küsürat gösterimindeki tüm sınırları bu testlerden çıkarılamaz.

CLI JSON streams use UTF-8 independently of the Windows locale. UTF-8 BOM input is accepted.
