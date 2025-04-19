[English](Readme.md) | [中文](ReadmeCN.md)

### USING METHOD
Open the English version"KNZ_Convert_en_us_ver_1.2.5.exe", Click the "Single Convert", and
select the path of origin file. Click the button on the right of "Convert" button to choose
the origin format and target format. The converted file will generate in the same diectory
of origin file, if not select the path of output file. Click the "Batch Convert", same 
as the operate of "Single Convert", it is to be noticed that the major version of files must
be same or the file of different version will fail to convert. The file name format of 
converted is like: COV-{$originfilename}.{$originfileextensions}

### BRIEF
This software is developed by Python, mainly to complish the convert of different format
of RINEX observation data. At present, the convert between RINEX 2.xx and RINEX 3.xx is 
already be basiclly supported.

Supported file format：

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


The double-character observation type of RINEX 2.xx will be matched by the list
below:

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

Because of the observation type of RINEX 3.xx is not completely compatible with the type of
RINEX 2.xx. So, it will be omitted for the observation of same type from the same frequency.
In general, based on the rule: "Convert the first, omit the next." to compatible with the
RINEX 2.xx. At the same time, since this conversion is an irreversible processing method, 
the converted observation file data can only be used as a reference when performing this
conversion, cannot replace the original version format.

Tip: if need to use RINEX file of strict format, you are supposed to be not use this software.

### UPDATE STAMP
2024/11/14: Currently, full support for RINEX 2.xx format conversion has been implemented, and
            the format output errors of the previous version have been corrected. Currently, 
            support for converting RINEX 2.xx to RINEX 3.xx is available.
            
2024/11/15: Corrected output format, ignored RINEX 2.xx free signals and changed matching rules.

2024/11/17: Supports conversion between RINEX2.xx format and RINEX3.xx format, and also supports
            conversion between the same major versions.

2024/11/18: Correct crash when input RINEX file with comment in the middle of data; Enhance the 
            speed of converting.

### UPDATE PLAN
1. ~~Short-term  goals：Supports conversion of RINEX2.xx and RINEX3.xx observation files.~~ √
2. Middle-term goals：Supports conversion of RINEX2.xx and RINEX3.xx broadcast ephemeris files.
3. Middle-term goals：Gradually introduce support for conversion of RTCM format files.
4. Long-term   goals：Receiver raw data conversion.
