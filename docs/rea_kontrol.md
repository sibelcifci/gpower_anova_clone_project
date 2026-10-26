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
| `Power must be greater than or equal to alpha` | ascii | `1856032` | `Power must be greater than or equal to alpha.|Sample size must` |
