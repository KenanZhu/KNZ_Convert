# @ File : rnx_convert.py
#
# Copyright (c) 2024 - 2024 KenanZhu. All Right Reserved.
#
# @ Author         : KenanZhu
# @ Time           : 2024/11/13
# @ Brief          :
#                  :
# @ IDE            : PyCharm
#
# ----------------------------------------------------------------------------------------
import re
import time
import math
import threading

bnk=' '
def conv_time():
  # Get the locate time and transform to RINEX format
  y=time.localtime().tm_year
  m=time.localtime().tm_mon
  d=time.localtime().tm_mday
  h=time.localtime().tm_hour
  min=time.localtime().tm_min
  sec=time.localtime().tm_sec
  localtime=str(y)+str(m)+str(d)+bnk+"%02d"%h+"%02d"%min+"%02d"%sec+bnk+"LLC"+bnk
  outline=('KNZ_Convert ver1.2.1'+20*bnk+
           '%s'%localtime+
           'COV-PGM / DATE\n')
  return outline
# =======================================================================================
# Convert observ type of RINEX 2.xx to others
# =======================================================================================
def obsfmt_conv(obstype):
  match obstype[1:2]:
    case '1':
      if obstype[0:1]=='P':
        obstype='C1P'
      else:
        obstype+='C'
    case '2':
      if obstype[0:1]=='P':
        obstype='C2P'
      else:
        obstype+='C'
    case '3': pass
    case '4': pass
    case '5': obstype+='I'
    case '6': obstype+='C'
    case '7': obstype+='I'
    case '8': obstype+='I'
  return obstype
# =======================================================================================
# Convert Format
# =======================================================================================
def datefmt_conv(inline):
  hou = inline[49:51]
  min = inline[52:54]
  sec = inline[55:57]
  return (inline[0:49] +
          hou +
          min +
          sec +
          bnk + "UTC" +
          bnk + "PGM / RUN BY / DATE\n")
# =======================================================================================
# Convert observ msg of RINEX 2.xx to others
# =======================================================================================
def obstype_conv(inline, in_f):
  outlines=[]
  obstypes=[]
  system=['G', 'R', 'E', 'S']

  obsnum=int(inline[0:6])

  for i in range(math.ceil(obsnum/9)):
    obstypes.extend(inline[6:60].split())
    if i+1==math.ceil(obsnum/9): break
    inline = in_f.readline()

  for i in range(len(obstypes)):
    obstypes[i]=obsfmt_conv(obstypes[i])

  for sys in system:
    outline=sys+3*bnk+'%2d'%len(obstypes) + bnk
    for i in range(len(obstypes)):
      outline+=obstypes[i] + bnk
      if (i+1)%13==0:
        outlines.append(
        outline+bnk+'SYS / # / OBS TYPES\n')
        outline = 7*bnk
      elif (i+1)==obsnum:
        outlines.append(
        outline + ( (13-len(obstypes))%13*4 + 1)*bnk + 'SYS / # / OBS TYPES\n')

  return outlines
# =======================================================================================
# Convert obs of RINEX 2.xx to others
# =======================================================================================
def rnx2uni_head_bxx(in_path, out_path, oriver, desver):
  try:
    with open(in_path, 'r'): pass
  except FileNotFoundError:
    return -12

  outlines=[]
  in_f=open(in_path, 'r')
  while True:
    inline=in_f.readline()
    if not inline: return 0
    if inline.find('COMMENT')>=0:
      outlines.append(inline)
    elif inline.find('RINEX VERSION / TYPE')>=0:
      if not inline.find('OBSERVATION DATA')>=0:
        return -10
      if not float(inline[5: 9])<3: return -10
      outlines.append(
        5*bnk+'%s->%s'%(str(oriver),str(desver))+
        1*bnk+'COV-OBSERVATION DATA'+
        24*bnk+'COV-RINEX VER / TYPE\n')
      outlines.append(conv_time())
      outlines.append(inline.replace(
        '%s'%re.search(r'[1-9]\d*.\d*|0\.\d*[1-9]\d*', inline).group(),
        desver))
    elif inline.find('PGM / RUN BY / DATE')>=0:
      outlines.append(datefmt_conv(inline))
    elif inline.find('# / TYPES OF OBSERV')>=0:
      outlines.extend(obstype_conv(inline, in_f))
    elif inline.find("WAVELENGTH FACT L1/2")>=0: pass
    elif inline.find("END OF HEADER")>=0:
      outlines.append(inline)
      break
    else: outlines.append(inline)

  try:
    with open(out_path, 'w'): pass
  except PermissionError:
    return -11

  out_f=open(out_path, 'a')
  out_f.writelines(outlines)
  out_f.close()

  return 1
# =======================================================================================
# Convert head_data of RINEX 3.xx to Uni-format
# =======================================================================================
def data2uni_bxx(inline, obsnum, in_f):
  sPRN=[]
  outlines=[]
  count_er=0

  year  =  int(inline[0               :3])
  month =  int(inline[0+3             :3+3])
  day   =  int(inline[0+3+3           :3+3+3])
  hour  =  int(inline[0+3+3+3         :3+3+3+3])
  minute=  int(inline[0+3+3+3+3       :3+3+3+3+3])
  second=float(inline[0+3+3+3+3+3     :3+3+3+3+3+11])
  e_flag=  int(inline[0+3+3+3+3+3+11  :3+3+3+3+3+11+3])
  satnum=  int(inline[0+3+3+3+3+3+11+3:3+3+3+3+3+11+3+3])

  outlines.append(
    "> %4d %02d %02d %02d %02d %10.7f %2d %2d\n" \
    % (year + 2000, month, day, hour, minute, second, e_flag, satnum))

  for i in range(math.ceil(satnum/12)):
    if not i==0: inline = in_f.readline()
    if i+1<math.ceil(satnum/12): count_er=12
    if i+1==math.ceil(satnum/12): count_er=satnum-i*12
    for j in range(count_er):
      sPRN.append(inline[32+3*j : 32+3*(j+1)].replace(bnk, "0"))

  for i in range(satnum):
    outline=''
    if obsnum <= 5:
      inline=in_f.readline()
      outline+=inline.replace("\n","").replace("\r","")
    elif obsnum > 5:
      for j in range(math.ceil(obsnum/5)):
        inline=in_f.readline()
        outline+=inline.replace("\n","").replace("\r","")
        if len(outline)%16==15: outline+=bnk
        if len(outline)%16==14: outline+=2*bnk
        outline+=(5 - int(len(outline)/16))*16*bnk
    outlines.append(sPRN[i] + outline + "\n")

  return outlines
# =======================================================================================
# Convert Uni-format to RINEX 3.xx
# =======================================================================================
def uni2data_cxx(outlines, out_path):
  out_f = open(out_path, 'a')
  out_f.writelines(outlines)
  out_f.close()
# =======================================================================================
# Convert data of RINEX 3.xx to Uni-format
# =======================================================================================
def rnx2uni_data_bxx(in_path, out_path, desver):
  obsnum=0
  obsget=False

  in_f=open(in_path, 'r')
  while True:
    inline = in_f.readline()
    if not inline: break
    elif inline.find('# / TYPES OF OBSERV')>=0:
      if not obsget:
        obsget=True
        obsnum=int(inline[0:6])
      else: continue
    elif inline.find("END OF HEADER")>=0: break

  while True:
    inline = in_f.readline()
    if not inline: break
    elif inline[0:5]==5*bnk: continue
    elif inline.find("COMMENT")>=0: continue
    else:
      outlines=data2uni_bxx(inline, obsnum, in_f)
      uni2data_cxx(outlines, out_path)
  return 1
# =======================================================================================
#
#
#
#
# =======================================================================================
def Convert_Un(in_path, out_path, oriver, desver, resqueue):
  origin=0
  match oriver:
    case '2.10': origin=2
    case '2.11': origin=2
    case '3.03': origin=3
    case '3.04': origin=3
    case '3.05': origin=3

  if origin==2:
    match rnx2uni_head_bxx(in_path, out_path, oriver, desver):
      case  1: rnx2uni_data_bxx(in_path, out_path, desver)
      case  0: return resqueue.put(0)
      case-10: return resqueue.put(0)
      case-11: return resqueue.put(0)
      case-12: return resqueue.put(0)
  elif origin==3: resqueue.put(0)

  resqueue.put(1)
# =======================================================================================
def _Convert_Un(in_path, out_path, oriver, desver, resqueue):
  T=threading.Thread(
    target=lambda :Convert_Un(in_path, out_path, oriver, desver, resqueue)
  )
  T.start()

  T.join()
  return resqueue.get()