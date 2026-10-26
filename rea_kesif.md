# REA dize araması — çıktı

- ikili: `GPowerNT.exe`
- boyut: 2287616 bayt
- SHA-256: `c63e6a133eb6372932f810c08cc33dc35a06d1ddb658f897bd6c34a754efc812`

### Mesaj parçaları (REA-07 / REA-08)

Tam mesaj tek parça halinde bulunmaz; parçalar bitişik bir dize tablosunda durur ve çalışma anında birleştirilir.

| aranan | kodlama | bayt offseti | alıntı |
|---|---|---|---|
| `The total sample size (` | ascii | `1856584` | `The total sample size (|where the lower bound corresponds to 1/(` |
| `) is not a multiple of` | ascii | `1856560` | `) is not a multiple of|The total sample size (|where the lower ` |
| `the number of groups (` | ascii | `1856161` | `the number of groups (|Sample size must be greater than| the num` |
| `the number of groups (` | ascii | `1856536` | `the number of groups (|) is not a multiple of|The total sample` |
| `). The analysis was ` | ascii | `1856512` | `). The analysis was |the number of groups (|) is not a multi` |
| `based on the average group size.` | ascii | `1856476` | `based on the average group size.|). The analysis was |the ` |
| `Total sample size must be greater than` | ascii | `1856400` | `Total sample size must be greater than| the number of response v` |
| `The total sample size must be greater than the number of groups` | utf16 | `1907320` | `The total sample size must be greater than the number of groups|` |
| `The size of each group must be greater or equal 1` | utf16 | `1896904` | `The size of each group must be greater or equal 1|The number o` |

### Diyalog başlıkları (B-10)

| aranan | kodlama | bayt offseti | alıntı |
|---|---|---|---|
| `Input error` | ascii | `1846036` | `Input error (illegal character?)|Input error|<{|G` |
| `Input error` | ascii | `1846072` | `Input error|<{|G|z|?|Y@|t|^|C| |C|C|Bino` |
| `Input error` | utf16 | `1951204` | `Input error|Please note|Interruption|` |
| `Please note` | utf16 | `1951228` | `Please note|Interruption|` |
| `Interruption` | utf16 | `1951280` | `Interruption|` |
| `Internal math error` | utf16 | `1951488` | `Internal math error|` |

### Sayı biçimleme format dizeleri (B-09 / REA-10)

| aranan | kodlama | bayt offseti | alıntı |
|---|---|---|---|
| `%.16g` | ascii | `1846004` | `%.16g|%.f|%.5g|f|%.|g|Input error (illegal character?)` |
| `%.15g` | utf16 | `1886544` | `%.15g|Error in expr: |_|P|p|\models\|txt|*.txt|all|*.*|Choo` |
| `%.7g` | ascii | `1925748` | `%.7g|1|xt]|x|S|^P| |_|S|p|S|x@|w@|x@|` |
| `%.7g` | utf16 | `1891840` | `%.7g|All expected probabilities p(H0)|must be greater than 1e` |
| `%.6g` | ascii | `1872531` | `%.6g| - | = |?|?333333|?ffffff|?|Y@|@|` |
| `%.6g` | utf16 | `1892664` | `%.6g|The sum of the expected probabilitie` |
| `%.5g` | ascii | `1846016` | `%.5g|f|%.|g|Input error (illegal character?)|Input er` |
| `%g` | ascii | `876295` | `%g|V|]|j:V|d|V|g|V|>|j|E|P|` |
| `%g` | utf16 | `1892636` | `%g|sum > 1.0|%.6g|The sum of the expecte` |
| `%.7f` | utf16 | `1943636` | `%.7f|]|T|P|_|T|T|@|@|@|Z|Z|Z|Z|Z|Z|Z|T|Z|Z|Z|Z|Z|Z|Z|Z` |
| `%.6f` | — | **YOK** | — |
| `%.5f` | — | **YOK** | — |
| `%.3f` | — | **YOK** | — |
| `%.0f` | — | **YOK** | — |
| `%.f` | ascii | `1846012` | `%.f|%.5g|f|%.|g|Input error (illegal character?)|Inpu` |
| `%ld` | ascii | `1846000` | `%ld|%.16g|%.f|%.5g|f|%.|g|Input error (illegal charact` |
| `%ld` | utf16 | `1897116` | `%ld) is different from that given in|the main window (%ld)!|Do ` |
| `%ld` | utf16 | `1897224` | `%ld)!|Do you want to adjust the value in the main window?|The ` |

### Sayısal yordam ipuçları (REA-04 / REA-05)

| aranan | kodlama | bayt offseti | alıntı |
|---|---|---|---|
| `BinomialDist-Quantile: input parameter out of range` | ascii | `1846132` | `BinomialDist-Quantile: input parameter out of range|BinomialDist` |
| `BinomialDist-Quantile: answer below lower search bound` | ascii | `1846184` | `BinomialDist-Quantile: answer below lower search bound|Binomial` |
| `BinomialDist-Quantile: answer above upper search bound` | ascii | `1846240` | `BinomialDist-Quantile: answer above upper search bound|Binomial` |

### Ek arama

| aranan | kodlama | bayt offseti | alıntı |
|---|---|---|---|
| `is outside the admissible range` | ascii | `1855710` | `is outside the admissible range (|Alpha is outside the admissibl` |
| `is outside the admissible range` | ascii | `1855750` | `is outside the admissible range (| must be non-negative.|Noncen` |
| `is outside the admissible range` | ascii | `1855961` | `is outside the admissible range (| is inside the prohibited ran` |
| `There must be at least 2 groups` | ascii | `1856916` | `There must be at least 2 groups.| groups.|There must be at` |
| `Effect size f` | ascii | `1852872` | `Effect size f$^2$|Effect size f|Effect size r|Noncentralit` |
| `Effect size f` | ascii | `1852892` | `Effect size f|Effect size r|Noncentrality parameter $\lambda` |
| `Effect size f` | ascii | `1854140` | `Effect size f$^2$(U)|Effect size f$^2$(T1)|Effect size f$^2` |
| `admissible` | ascii | `1855725` | `admissible range (|Alpha is outside the admissible range (| must` |
| `admissible` | ascii | `1855765` | `admissible range (| must be non-negative.|Noncentrality paramet` |
| `admissible` | ascii | `1855976` | `admissible range (| is inside the prohibited range (|Power mu` |

## Keşif taraması

Taranan dize: 4138

### Sayısal yordam adları ve arama sınırları (REA-03 / REA-04 / REA-05)

Toplam 84 benzersiz dize; ilk 40 tanesi:

| kodlama | bayt offseti | dize |
|---|---|---|
| ascii | `1846132` | `BinomialDist-Quantile: input parameter out of range` |
| ascii | `1846184` | `BinomialDist-Quantile: answer below lower search bound` |
| ascii | `1846240` | `BinomialDist-Quantile: answer above upper search bound` |
| ascii | `1846296` | `BinomialDist-Quantile: p + q != 1.0` |
| ascii | `1846332` | `BinomialDist-Quantile: unknown error` |
| ascii | `1846680` | `ChiDist-Cdf: input parameter out of range` |
| ascii | `1846724` | `ChiDist-Cdf: answer below lower search bound` |
| ascii | `1846772` | `ChiDist-Cdf: answer above upper search bound` |
| ascii | `1846820` | `ChiDist-Cdf: p + q != 1.0` |
| ascii | `1846848` | `ChiDist-Cdf: unknown error` |
| ascii | `1846876` | `ChiDist-Quantile: input parameter out of range` |
| ascii | `1846924` | `ChiDist-Quantile: answer below lower search bound` |
| ascii | `1846976` | `ChiDist-Quantile: answer above upper search bound` |
| ascii | `1847028` | `ChiDist-Quantile: p + q != 1.0` |
| ascii | `1847060` | `ChiDist-Quantile: unknown error` |
| ascii | `1847156` | `CorrDist-Cdf: input parameter out of range` |
| ascii | `1847200` | `CorrDist-Cdf: answer below lower search bound` |
| ascii | `1847248` | `CorrDist-Cdf: answer above upper search bound` |
| ascii | `1847296` | `CorrDist-Cdf: p + q != 1.0` |
| ascii | `1847324` | `CorrDist-Cdf: unknown error` |
| ascii | `1847352` | `CorrDist-Quantile: input parameter out of range` |
| ascii | `1847400` | `CorrDist-Quantile: answer below lower search bound` |
| ascii | `1847452` | `Corrist-Quantile: answer above upper search bound` |
| ascii | `1847504` | `CorrDist-Quantile: p + q != 1.0` |
| ascii | `1847536` | `CorrDist-Quantile: unknown error` |
| ascii | `1848860` | `Exponential-Quantile: illegal parameter lambda` |
| ascii | `1848908` | `Exponential-Quantile: parameter out of bounds` |
| ascii | `1849032` | `FDist-Pdf: failed to converge` |
| ascii | `1849104` | `FDist-Cdf: answer below lower search bound` |
| ascii | `1849148` | `FDist-Cdf: answer above upper search bound` |
| ascii | `1849244` | `FDist-Quantile: input parameter out of range` |
| ascii | `1849292` | `FDist-Quantile: answer below lower search bound` |
| ascii | `1849340` | `FDist-Quantile: answer above upper search bound` |
| ascii | `1849388` | `FDist-Quantile: p + q != 1.0` |
| ascii | `1849420` | `FDist-Quantile: unknown error` |
| ascii | `1850132` | `HypergeometricDist-Quantile: input parameter out of range` |
| ascii | `1850244` | `LaplaceDist-Pdf: input parameter out of range` |
| ascii | `1850292` | `LaplaceDist-Cdf: input parameter out of range` |
| ascii | `1850340` | `LaplaceDist-Quantile: input parameter out of range` |
| ascii | `1850392` | `LogNormalDist-Pdf: input parameter out of range` |

### Kısıt ve doğrulama mesajları (REA-02 / REA-06)

Toplam 72 benzersiz dize; ilk 40 tanesi:

| kodlama | bayt offseti | dize |
|---|---|---|
| ascii | `1852812` | `Number of groups` |
| ascii | `1855784` | ` must be non-negative.` |
| ascii | `1855836` | `Degrees of Freedom must be greater or equal one.` |
| ascii | `1855888` | `Degrees of Freedom must be greater ` |
| ascii | `1855940` | ` must be greater ` |
| ascii | `1856032` | `Power must be greater than or equal to alpha.` |
| ascii | `1856080` | `Sample size must be greater than or equal to ` |
| ascii | `1856128` | `Sample size must be greater than` |
| ascii | `1856161` | `the number of groups (` |
| ascii | `1856400` | `Total sample size must be greater than` |
| ascii | `1856476` | `based on the average group size.` |
| ascii | `1856560` | `) is not a multiple of` |
| ascii | `1856916` | `There must be at least 2 groups.` |
| ascii | `1856964` | `There must be at least ` |
| ascii | `1857036` | `There must be at least 2 measurements.` |
| ascii | `1857076` | `There must be at least 1 predictor.` |
| ascii | `1857112` | `There must be at least one response variable.` |
| ascii | `1857160` | `Standard error $\sigma$ must be greater or equal ` |
| ascii | `1857364` | `Effect size (ratio) must be > ` |
| ascii | `1870320` | `Cannot compute result! The most probable reasons is that the number of` |
| ascii | `1871096` | `At least one predictor must be tested.` |
| ascii | `1871800` | `must be greater than the start value` |
| ascii | `1871882` | `must be a positive value` |
| ascii | `1871964` | `) must be greater than or equal to` |
| ascii | `1872164` | `must be an integer value greater 1.` |
| ascii | `1872237` | `must be a positive value.` |
| ascii | `1872428` | `The power must be greater than or equal to` |
| ascii | `1872472` | `The power must be greater than or equal to $\alpha$!` |
| ascii | `1876512` | `effect size must be greater than 0.00001.` |
| ascii | `1876612` | `The base rate exp(b0) must be > 0.` |
| ascii | `1876648` | `The mean exposure time must be > 0.` |
| ascii | `1876964` | `) must be smaller than |sy/sx| (= ` |
| ascii | `1877544` | `from p = 1/2 must be greater than 0.00001.` |
| ascii | `1877716` | `The relative standard deviation must be greater than 1e-6` |
| ascii | `1881432` | `The odds ratio must be positive` |
| ascii | `1881712` | `The standard deviation must be > 0.` |
| ascii | `1881800` | `The parameter lambda must be > 0.` |
| ascii | `1881836` | `The left interval border must be lower than the right border.` |
| ascii | `1881900` | `The variance under H0 must be greater than zero.` |
| ascii | `1881952` | `The variance under H1 must be greater than zero.` |

### Nonsantralite ve etki büyüklüğü sözlüğü (REA-01 / REA-09)

Toplam 96 benzersiz dize; ilk 40 tanesi:

| kodlama | bayt offseti | dize |
|---|---|---|
| ascii | `1846592` | `lambda` |
| ascii | `1846600` | `noncentrality lambda` |
| ascii | `1848772` | `Exponential-Pdf: illegal parameter lambda` |
| ascii | `1848816` | `Exponential-Cdf: illegal parameter lambda` |
| ascii | `1848860` | `Exponential-Quantile: illegal parameter lambda` |
| ascii | `1851815` | `?A priori: Compute required sample size - given $\alpha$, power, and e` |
| ascii | `1851896` | `Post hoc: Compute achieved power - given $\alpha$, sample size, and ef` |
| ascii | `1851976` | `Compromise: Compute implied $\alpha$ & power - given $\beta$/$\alpha$ ` |
| ascii | `1852088` | `Sensitivity: Compute required effect size - given $\alpha$, power, and` |
| ascii | `1852176` | `Criterion: Compute required $\alpha$ - given power, effect size, and s` |
| ascii | `1852264` | `Post hoc: Compute power - given $\alpha$, and noncentrality parameter` |
| ascii | `1852336` | `Criterion: Compute alpha - given $\beta$, and noncentrality parameter` |
| ascii | `1852408` | `Sensitivity: Compute noncentrality parameter - given $\alpha$, and pow` |
| ascii | `1852488` | `Compromise: Compute $\alpha$ and $\beta$ - given $\beta$/$\alpha$ rati` |
| ascii | `1852700` | `Effect size` |
| ascii | `1852736` | `Noncentrality parameter` |
| ascii | `1852840` | `Effect size w` |
| ascii | `1852856` | `Effect size d` |
| ascii | `1852872` | `Effect size f$^2$` |
| ascii | `1852892` | `Effect size f` |
| ascii | `1852908` | `Effect size r` |
| ascii | `1852924` | `Noncentrality parameter $\lambda$` |
| ascii | `1853052` | `Noncentrality parameter $\delta$` |
| ascii | `1853120` | `Noncentrality parameter $\mu$` |
| ascii | `1853260` | `Effect size g` |
| ascii | `1853604` | `Effect size h` |
| ascii | `1853660` | `Effect size q` |
| ascii | `1853780` | `Effect size $\Delta$` |
| ascii | `1853916` | `Effect size |$\rho$|` |
| ascii | `1853940` | `Noncentral dist. SD $\sigma$` |
| ascii | `1854140` | `Effect size f$^2$(U)` |
| ascii | `1854164` | `Effect size f$^2$(T1)` |
| ascii | `1854188` | `Effect size f$^2$(T2)` |
| ascii | `1854212` | `Effect size f$^2$(V)` |
| ascii | `1854236` | `Effect size f(U)` |
| ascii | `1854256` | `Effect size f(T1)` |
| ascii | `1854276` | `Effect size f(T2)` |
| ascii | `1854296` | `Effect size f(V)` |
| ascii | `1854368` | `Effect size dz` |
| ascii | `1855008` | `X parm $\lambda$` |

### Kayan nokta tipi ipuçları (REA-11)

Toplam 7 benzersiz dize; ilk 7 tanesi:

| kodlama | bayt offseti | dize |
|---|---|---|
| ascii | `1863684` | `Underflow` |
| ascii | `1885224` | `Math overflow` |
| ascii | `1981220` | `overflow` |
| ascii | `1981232` | `underflow` |
| ascii | `2123044` | `_isnan` |
| ascii | `2123378` | `_finite` |
| utf16 | `1913288` | `outside the admissible range [0..1]. To avoid overflow` |
