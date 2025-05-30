[English](READMEEN.md) | [中文](README.md)

### 使用方法
打开中文版本“KNZ_Convert_zh_cn_ver_1.2.5.exe”，点击单文件处理，选择原始文件路径。点击转换右侧按钮
选择原始格式和目标格式。如果未指定输出文件路径，转换后的文件将生成在原始文件的同一目录下。点击批文件
处理，与单文件转换相同操作下，需要注意要保证输入文件的主要版本相同。否则会转换失败。转换后的文件命名
格式为：COV-{原文件名}.{原文件后缀名}

### 软件简介
本软件是基于Python开发，主要实现转换不同版本格式的RINEX观测值文件。目前已经实现RINEX 2.xx格式与
RINEX 3.xx格式基本的相互转换。

文件格式转换支持列表：

| FILE TYPE | MAJOR VERSION |2.10|2.11|2.12|3.00|3.01|3.02|3.03|3.04|3.20|3.30|4.00|4.01|
|-----------|---------------|----|----|----|----|----|----|----|----|----|----|----|----|
| RINEX OBS | 2.xx          | √  | √  | √  | √  | √  | √  | √  | √  | —— | —— | x  | x  |
|           | 3.xx          | √  | √  | √  | √  | √  | √  | √  | √  | —— | —— | x  | x  |
|           | 4.xx          | x  | x  | x  | x  | x  | x  | x  | x  | —— | —— | x  | x  |
| RINEX NAV | 2.xx          | x  | x  | x  | x  | x  | x  | x  | x  | —— | —— | x  | x  |
|           | 3.xx          | x  | x  | x  | x  | x  | x  | x  | x  | —— | —— | x  | x  |
|           | 4.xx          | x  | x  | x  | x  | x  | x  | x  | x  | —— | —— | x  | x  |
| RTCM      | 2.xx          | —— | —— | —— | —— | —— | —— | —— | —— | x  | x  | —— | —— |
|           | 3.xx          | —— | —— | —— | —— | —— | —— | —— | —— | x  | x  | —— | —— |


对于RINEX 2.xx版本的两字符观测值类型将按照如下表格进行匹配：

|SYSTEM  |FREQ.BAND  |FREQUENCY  |2.xx CODE        |  >  |3.xx CODE          |
|--------|-----------|-----------|-----------------|-----|-------------------|
|GPS     |L1         |1575.42    |[C, L, D, S] 1,P1|  >  |[C, L, D, S] 1C,C1W|
|        |L2         |1227.60    |[C, L, D, S] 2,P2|  >  |[C, L, D, S] 2C,C2W|
|        |L5         |1176.45    |[C, L, D, S] 5   |  >  |[C, L, D, S] 5I    |
|GLONASS |G1         |1602+K*9/16|[C, L, D, S] 1,P1|  >  |[C, L, D, S] 1C,C1P|
|        |G2         |1246+K*7/16|[C, L, D, S] 2,P2|  >  |[C, L, D, S] 2C,C2P|
|Galileo |E2-L1-E1   |1575.42    |[C, L, D, S] 1   |  >  |[C, L, D, S] 1C    |
|        |E5a        |1176.45    |[C, L, D, S] 5   |  >  |[C, L, D, S] 5I    |
|        |E5b        |1207.140   |[C, L, D, S] 7   |  >  |[C, L, D, S] 7I    |
|        |E5a+b      |1191.795   |[C, L, D, S] 8   |  >  |[C, L, D, S] 8I    |
|        |E6         |1278.75    |[C, L, D, S] 6   |  >  |[C, L, D, S] 6C    |
|SBAS    |L1         |1575.42    |[C, L, D, S] 1   |  >  |[C, L, D, S] 1C    |
|        |L2         |1176.45    |[C, L, D, S] 5   |  >  |[C, L, D, S] 5I    |


由于RINEX 3.xx版本的观测值类型无法完全兼容RINEX 2.xx版本，所以对于RINEX 3.xx同一频段的同类型观测值
转换时会进行缺省处理。一般按照原观测值文件头文件中观测值 “先列出先转换，后列出先省略”的方式进行兼容。
同时由于该转换是不可逆的处理方式，因此进行该转换时转换后的观测值文件数据只能作为参考使用，无法替代原生
的版本格式。

注：如需使用严格的RINEX格式文件，请勿使用本软件。

### 更新简记
2024/11/14: 目前已经对RINEX 2.xx格式转换进行了全面支持，修改了上一版本的格式输出错误，目前支持RINEX 2.xx转换为RINEX 3.xx。

2024/11/15: 更正了输出格式，忽略RINEX 2.xx空余信号并更改匹配规则

2024/11/17: 支持RINEX2.xx格式和RINEX3.xx格式的相互转换，同时支持同一主要版本之间的转换。

2024/11/18: 修复了在转换数据中标有注释的RINEX文件时崩溃的错误；提高了文件转换速度。

### 更新计划
1. ~~近期目标：支持转换RINEX2.xx版本与RINEX3.xx版本观测值文件。~~ √
2. 中期目标：支持转换RINEX2.xx版本与RINEX3.xx版本广播星历文件。
3. 中期目标：逐步引入对RTCM格式文件的转换支持。
4. 远期目标：接收机原始数据转换。
