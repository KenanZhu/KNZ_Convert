- [中文](ReadmeCN.md)

### Using method ###

Click to open KNZ_Convert_en_us_ver_1.2.1.exe of english version.

Click "Single file convert" or "Batch files convert", input the RINEX file of version of 2.10 or 2.11.

If not click the output diectory, the converted file will generate at the same directory of original file, 
the file name of converted file is "COV-{originalfilename}"

The converted file will note the version of convert at the heder of file.

The converted file own some traits as below:

1. Conversion does not require additional parameter information,
the file is lossless conversion, only convert the foemat,
do not modify the information. 
2. The double character observation types of RINEX2.xx version will be automatically matched according to the following table:

### Update brief ###
2024/11/14: At present, the RINEX2.xx format conversion has been fully supported,
the format output error of the previous version has been modified,
and the conversion from 2.xx to 3.xx is currently supported.

2024/11/15: Correct the output format, omit the empty observation and change the
rule of match.

2024/11/17: Fully support the conversion of RINEX 2.xx & RINEX 3.xx, also support
the conversion of same major version.

### Update plan ###
1. 2.xx and 3.xx versions are fully supported, and support mutual conversion.
2. Gradually introduce the conversion support for RTCM files.
3. Long-term goal: receiver raw data conversion
