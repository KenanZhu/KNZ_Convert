ENGLISH:

Click to open KNZ_Convert_en_us_ver_1.0.6.exe of english version.

Using method

Click "Single file convert" or "Batch files convert", input the RINEX file of version of 2.10 or 2.11.

If not click the output diectory, the converted file will generate at the same directory of original file, 
the file name of converted file is "COV-{originalfilename}"

The converted file will note the version of convert at the heder of file.

The converted file own some traits as below:

1. Conversion does not require additional parameter information,
	the file is lossless conversion, only convert the foemat,
	do not modify the information. 
2. For the obsrved value types ofdifferent frequency hands in the original file,
	the software will automatically match and general default is the conversion table at the end of the readme


SYSTEM	  |	FREQ.BAND	FREQUENCY   | 2.11 || 2.10 CODE   ->	  3.04 CODE             |

GPS		  | L1          1575.42 	| [C, L, D, S] 1,P1   -> 	  [C, L, D, S]1C, C1P   |
		  | L2		    1227.60	    | [C, L, D, S] 2,P2   ->      [C, L, D, S]2C, C2P   |
		  | L5          1176.45	    | [C, L, D, S] 5      -> 	  [C, L, D, S]5I        |

GLONASS	  | G1		    1602+K*9/16 | [C, L, D, S] 1,P1   ->      [C, L, D, S]1C, C1P   |
		  | G2		    1246+K*7/16 | [C, L, D, S] 2,P2   -> 	  [C, L, D, S]2C, C2P   |

Galileo	  | E2-L1-E1    1575.42	    | [C, L, D, S] 1      ->      [C, L, D, S]1C        |
		  | E5a		    1176.45	    | [C, L, D, S] 5      ->      [C, L, D, S]5I        |
		  | E5b	        1207.140    | [C, L, D, S] 7      ->      [C, L, D, S]7I        |
		  | E5a+b	    1191.795    | [C, L, D, S] 8      ->      [C, L, D, S]8I        |
		  | E6		    1278.75	    | [C, L, D, S] 6      ->      [C, L, D, S]6C        |

SBAS	  | L1		    1575.42	    | [C, L, D, S] 1      ->      [C, L, D, S]1C        |
		  | L5		    1176.45	    | [C, L, D, S] 5      ->      [C, L, D, S]5I        |

