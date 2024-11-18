# @ File           : rnx_convert.py
#
# @ Brief          : RINEX Convert functions.
#
# Copyright (c) 2024 - 2024 KenanZhu. All Right Reserved.
#
# @ Author         : KenanZhu
# @ Time stamp     : [2024/11/13] First release.
#                  : [2024/11/14] Correct: convert of observation type of 
#                                 'P1/P2' of GPS is correct into 'C1W/C2W'.
#                  : [2024/11/15] Fix bug: remove the empty observation of 
#                                 RINEX 2.xx format.
#                  : [2024/11/17] Add new: complish the funtions of convert
#                                 form RINEX 3.xx to RINEX 2.xx and also support 
#                                 convert in major version of RINEX.
#                  : [2024/11/18] Fix bug: correct the bug when Convert RINEX file
#                                 with comment in the middle of data will cause 
#                                 crash.
#                                 Correct: correct the mistake in the functions
#                                 below:
#                                       1. Correct function: getsys_rnx3()
#                                       2. Correct function: obstype3_conv()
#                                       3. Correct function: rnx2uni3_data()
#                                       4. Correct function: rnx2_data2uni()
#                                       5. Correct function: rnx3rnx2_data()
#                                 Optimze: enhance the speed of converting.
#
# 
# @ IDE/Editor     : PyCharm / VisualStudio Code
#
# ----------------------------------------------------------------------------------------
# ---STDPORT--- #
import re
import time
import math
import threading
# ------------- #
emp=''
bnk=' '

# Get local time of converting ----------------------- #
def conv_time():
  # generate convert timestamp
  covpro='KNZ_Convert ver1.2.6'
  covcom='COMMENT'

  # Get the locate time and transform to Uni-format
  y=time.localtime().tm_year
  m=time.localtime().tm_mon
  d=time.localtime().tm_mday
  h=time.localtime().tm_hour
  min=time.localtime().tm_min
  sec=time.localtime().tm_sec
  localtime=('%04d'%y  +
             '%02d'%m  +
             '%02d'%d  +bnk+
             '%02d'%h  +
             '%02d'%min+
             '%02d'%sec+bnk+
             'LLC'     +bnk)
  
  outline=(covpro   +
           20*bnk   +
           localtime+
           covcom   +
           '\n')
  
  return outline

# Convert data format --------------------------- #
def datefmt2_conv(inline):
  hou=inline[49:51]
  min=inline[52:54]
  sec=inline[55:57]
  return (inline[0:49] +
          hou +
          min +
          sec +
          bnk + "UTC" +
          bnk + "PGM / RUN BY / DATE\n")

# Convert data format --------------------------- #
def datefmt3_conv(inline):
  hou=inline[49:51]
  min=inline[51:53]
  sec=inline[53:55]
  return (inline[0:49] +
          hou + ':' +
          min + ':' +
          sec +
         'UTCPGM / RUN BY / DATE\n')

# Convert observ type of RINEX 2.xx to Uni-format ------------- #
def obsfmt2_conv(obstypes, sys):

  counter =0
  obstypex=[]
  obsbomit=emp

  match sys:
    case 'G':
      for obs in obstypes:
        counter+=1
        if   obs[1:2]=='1':
          if obs[0:1]=='P': obs='C1W'
          else: obs+='C'
        elif obs[1:2]=='2':
          if obs[0:1]=='P': obs='C2W'
          else: obs+='C'
        elif obs[1:2]=='5': obs+='I'
        else:
          obsbomit+=('%02d'%counter)
          continue
        obstypex.append(obs)
    case 'E':
      for obs in obstypes:
        counter+=1
        if   obs[1:2]=='1':
          if obs[0:1]=='P': 
            obsbomit+=('%02d'%counter)
            continue
          else: obs+='C'
        elif obs[1:2]=='5': obs+='I'
        elif obs[1:2]=='6': obs+='C'
        elif obs[1:2]=='7': obs+='I'
        elif obs[1:2]=='8': obs+='I'
        else:
          obsbomit+=('%02d'%counter)
          continue
        obstypex.append(obs)
    case 'R':
      for obs in obstypes:
        counter+=1
        if   obs[1:2]=='1':
          if obs[0:1]=='P': obs='C1P'
          else: obs+='C'
        elif obs[1:2]=='2':
          if obs[0:1]=='P': obs='C2P'
          else: obs+='C'
        else:
          obsbomit+=('%02d'%counter)
          continue
        obstypex.append(obs)
    case 'S':
      for obs in obstypes:
        counter+=1
        if   obs[1:2]=='1':
          if obs[0:1]=='P': 
            obsbomit+=('%02d'%counter)
            continue
          else: obs+='C'
        elif obs[1:2]=='5': obs+='I'
        else:
          obsbomit+=('%02d'%counter)
          continue
        obstypex.append(obs)
  
  obstypex.append(obsbomit)
  
  return obstypex

# Convert observ msg of RINEX 2.xx to Uni-format ---------------- #
def obstype2_conv(inline, in_f, omilist):
  # uni-format message label
  obsobs='SYS / # / OBS TYPES'

  outlines=[]
  obstypes=[]
  obstypex=[]
  system=['G', 'E', 'R', 'S']

  obsnum=int(inline[0:6])
  omilist.append(obsnum)
  for i in range(math.ceil(obsnum/9)):
    obstypes.extend(inline[6:60].split())
    if i+1==math.ceil(obsnum/9): break
    inline = in_f.readline()

  for sys in system:
    obstypex=obsfmt2_conv(obstypes, sys)
    omilist.append(obstypex[-1])

    # S___2D_
    num    =len(obstypex)-1
    outline=sys+3*bnk+'%2d'%num+bnk

    for i in range(num):
      outline+=obstypex[i]+bnk
      if   (i+1)==num:
        bnx=((13-num%13)*4+1)*bnk
        if num%13==0: bnx=bnk
        outlines.append(outline+bnx+obsobs+'\n')
        outline=0*bnk
      elif (i+1)%13==0:
        outlines.append(outline+bnk+obsobs+'\n')
        outline=7*bnk
  return outlines

# Generate the convert stamp ------------------------ #
def conv_stamp(inline, outlines, desver):
  oriver=inline[ 5: 9]
  # generate convert stamp
  obscov='COV-OBSERVATION DATA'
  obscom='COMMENT'  

  outlines.append( 5*bnk+
                  oriver+
                  '->'  +
                  desver+
                   1*bnk+
                  obscov+
                  24*bnk+
                  obscom+
                  '\n')
  outlines.append(conv_time())
  outlines.append(
    inline.replace('%s'%re.search(r'[1-9]\d*.\d*|0\.\d*[1-9]\d*', inline).group(), desver))
  return

# Convert RINEX 2.xx(header) to Uni-format -------------- #
def rnx2_head2uni(in_f, desver, outlines, omilist):
  # rinex message label
  obscom='COMMENT'
  obstpe='RINEX VERSION / TYPE'
  obsl12='WAVELENGTH FACT L1/2'
  obspro='PGM / RUN BY / DATE'
  obsobs='# / TYPES OF OBSERV'
  obsend='END OF HEADER'

  # get input head file & convert
  while True:
    inline=in_f.readline()
    # file is aleady checked so no need to judge again
    if   not inline: break
    if   inline.find(obscom)>=0: outlines.append(inline)
    elif inline.find(obspro)>=0: outlines.append(datefmt2_conv(inline))
    elif inline.find(obsobs)>=0: outlines.extend(obstype2_conv(inline, in_f, omilist))
    elif inline.find(obstpe)>=0: conv_stamp(inline, outlines, desver)
    elif inline.find(obsl12)>=0: continue
    elif inline.find(obsend)>=0: break
    else                       : outlines.append(inline)

  # get the end message after break
  outlines.append(60*bnk+obsend+'\n')

  return 1

# Convert RINEX 2.xx(data) to Uni-Format ------------------- #
def rnx2_data2uni(in_f, outlines, omilist, obsnum):
  sPRN=[]
  scounter=0
  outline=emp

  # return false when file end
  inline=in_f.readline()
  if not inline: return False
  if not inline[28:29]=='0':
    outlines.append(inline)
    for i in range(int(inline[29:32])):
      outlines.append(in_f.readline())
    return True

  # get epoch message & flag state
  year  =  int(inline[0               :3])
  month =  int(inline[0+3             :3+3])
  day   =  int(inline[0+3+3           :3+3+3])
  hour  =  int(inline[0+3+3+3         :3+3+3+3])
  minute=  int(inline[0+3+3+3+3       :3+3+3+3+3])
  second=float(inline[0+3+3+3+3+3     :3+3+3+3+3+11])
  e_flag=  int(inline[0+3+3+3+3+3+11  :3+3+3+3+3+11+3])
  satnum=  int(inline[0+3+3+3+3+3+11+3:3+3+3+3+3+11+3+3])
  if not e_flag==0: return True

  # time to Uni-Format
  outlines.append(
    "> %4d %02d %02d %02d %02d %10.7f %2d %2d\n" \
    % (year + 2000, month, day, hour, minute, second, e_flag, satnum))

  # get list of sPRN
  for i in range(math.ceil(satnum/12)):
    if  not i==0                 : inline  =in_f.readline()
    if  i+1< math.ceil(satnum/12): scounter=12
    if  i+1==math.ceil(satnum/12): scounter=satnum-i*12
    for j in range(scounter):
      sPRN.append(inline[32+3*j:32+3*(j+1)].replace(bnk,'0'))

  # convert epoch data to Uni-Format
  for i in range(satnum):
    oulist=[]
    outline=emp

    # get omit list
    match sPRN[i][0:1]:
      case 'G': omitlis=omilist[0]
      case 'E': omitlis=omilist[1]
      case 'R': omitlis=omilist[2]
      case 'S': omitlis=omilist[3]
    
    # observ amount lower than 5. no need to enter
    if   obsnum <= 5:
      outline=in_f.readline()
      outline=inline.replace('\n',emp).replace('\r',emp)

    # elif, need to enter
    elif obsnum > 5:
      for j in range(math.ceil(obsnum/5)):
        inline=in_f.readline()
        outline+=inline.replace('\n',emp).replace('\r',emp)
        if len(outline)%16==15: outline+=bnk
        if len(outline)%16==14: outline+=2*bnk
        outline+=(5 - int(len(outline)/16))*16*bnk
    
    # omit the empty observ by ''
    # outline be divide into parts
    for j in range(obsnum):
      oulist.append(outline[16*j:16*j+16])
    for j in range(len(omitlis)):
      oulist[omitlis[j]-1]=emp
    
    # remerge into outline
    outline=emp.join(oulist)

    outlines.append(sPRN[i]+outline+"\n")
  return True

# Convert Uni-format to RINEX 3.xx --------------------- #
def uni2rnx3_data(outlines, out_f):
  out_f.writelines(outlines)
  return

# Get observ type need be omitted --------------------- #
def getomit(omilist):
  for i in range(len(omilist)):
      sysomit=[]
      omitlis=omilist[0]
      omitnum=len(omitlis)/2
      for j in range(int(omitnum)):
        sysomit.append(int(omitlis[j*2+0:j*2+2]))
      omilist.append(sysomit)
      omilist.pop(0)
  return

# Convert RINEX 2.xx to Des-format --------------------- #
def rnx2des(in_path, out_path, oriver, desver):
  headread=False
  outlines=[]
  omilist=[]
  in_f=open(in_path, 'r')
  out_f=open(out_path, 'a')
  # convert RINEX 2.xx(header) to Uni-format
  match rnx2_head2uni(in_f, desver, outlines, omilist):
    case 1: headread=True
    case 0: headread=False

  if       headread:
  # convert Uni-foramt(header) to Des-format
    match desver[0:1]:
          case '2': addemp=uni2rnx2_data(4, outlines, out_f, True, None)
          case '3': uni2rnx3_data(outlines, out_f)
    outlines=[]
    # get each observ type and omit the empty
    obsnum=omilist[0]
    omilist.pop(0)
    getomit(omilist)
    # convert RINEX 2.xx(data) to Uni-format
    while rnx2_data2uni(in_f, outlines, omilist, obsnum):
      # convert Uni-foramt(data) to Des-format
      match desver[0:1]:
        case '2': uni2rnx2_data(4, outlines, out_f, False, addemp)
        case '3': uni2rnx3_data(outlines, out_f)
      outlines=[]
  elif not headread: return 0
  in_f.close()
  out_f.close()
  return 1

# Get the position of new add observ type ----------------- #
def getaddemp(alltypes, sysstype):
  addemp=[[],[],[],[]]
  for i in range(len(sysstype)):
    for j in range(len(sysstype[i])):
      for k in range(len(alltypes)):
        if sysstype[i][j]==alltypes[k]:
          addemp[i].append(k)
  return addemp

# Filter the same obs fmt in RINEX 2.xx ----------------- #
def obsfmt_filter(alltypes):
  empemp=[]
  spos=npos=0
  empemp.append(len(alltypes))
  while True:
    npos+=1
    if spos==empemp[0]: break
    if npos==empemp[0]:
      spos+=1
      npos=spos
      continue
    if not alltypes[spos]: continue
    if not alltypes[npos]: continue
    if alltypes[spos]==alltypes[npos]:
      alltypes[npos]=emp
      empemp.append(npos)
  # restruct the data
  totnum=empemp[0]
  empemp=sorted(empemp[1:])
  empemp.insert(0,totnum)
  empemp.clear()
  # addemp.append(empemp)
  # clear the empty
  alltypes=[obs for obs in alltypes if obs!=emp]
  return alltypes

# Sort by observ type --------------------------- #
def sort_observ(alltypes):
  alltypex=[]
  temtypes=[]
  freindex=['1','2','3','4',
            '5','6','7','8']
  obsetype=['C','L','D','S']

  for type in alltypes:
    freidx=freindex.index(type[1:2])/ 1
    if type=='P1C' or type=='P2C':
      tyeidx=obsetype.index(type[2:3])/10
    else:
      tyeidx=obsetype.index(type[0:1])/10
    alltypex.append(freidx+tyeidx)

  sdx=ndx=0
  while True:
    if len(alltypex)==0:
      break
    if (ndx+1)==len(alltypex):
      temtypes.append(alltypes[sdx])
      alltypes.pop(sdx)
      alltypex.pop(sdx)
      sdx=ndx=0
      continue
    ndx+=1
    if alltypex[ndx]<=alltypex[sdx]:
      sdx=ndx
      continue
  return temtypes

# Convert observ type of RINEX 3.xx to Uni-Format --------------- #
def obsfmt3_conv(alltypes):
  alltypex=[]

  for type in alltypes:
    if   type[1:2]=='1':
      if type=='C1W': type='P1'
    elif type[1:2]=='2':
      if type=='C2W': type='P2'
    else: pass
    alltypex.append(type[0:2])

  return alltypex

# Convert observ msg of RINEX 3.xx to Uni-Format ---------------- #
def obstype3_conv(i, sysnum, outlines, outlinex):
  alltypes=[]
  obstypes=[]
  sysstype=[[],[],[],[]]
  # rinex message label
  obsobs='# / TYPES OF OBSERV'

  for j in range(sysnum):
    obstypes=[]
    # reject system not support in Uni-Format
    match outlines[i][0:1]:
      case 'G': obstypes.append(0)
      case 'E': obstypes.append(1)
      case 'R': obstypes.append(2)
      case 'S': obstypes.append(3)
      case 'C':
        i+=math.ceil(int(outlines[i][1:6])/13)
        continue
      case 'I':
        i+=math.ceil(int(outlines[i][1:6])/13)
        continue
      case 'J':
        i+=math.ceil(int(outlines[i][1:6])/13)
        continue
      case   _: 
        i+=1
        continue

    obsnum=int(outlines[i][1:6])
    for k in range(math.ceil(obsnum/13)):
      obstypes.extend(outlines[i][6:60].split())
      if k+1==math.ceil(obsnum/13): break
      i+=1
    
    # check the differ observ type in glonass
    if obstypes[0]==2:
      try:
        pos=obstypes.index('C1P')
        obstypes[pos]='P1C'
      except ValueError: pass
      try:
        pos=obstypes.index('C2P')
        obstypes[pos]='P2C'
      except ValueError: pass

    sysstype[obstypes[0]]=obsfmt3_conv(obstypes[1:])
    alltypes=list(set(obstypes[1:]+alltypes))
    i+=1

  # sort observ types
  alltypes=sort_observ(alltypes)
  # convert observ type into des-format
  alltypes=obsfmt3_conv(alltypes)
  # fliter the same observ type
  alltypes=obsfmt_filter(alltypes)
  # get new added pos
  addemp=getaddemp(alltypes, sysstype)

  num    =len(alltypes)
  outline=4*bnk+'%2d'%num

  for j in range(num):
    outline+=4*bnk+alltypes[j]
    if   (j+1)==num:
      bnx=((9-num%9)*6)*bnk
      if num%9==0: bnx=emp
      outlinex.append(outline+bnx+obsobs+'\n')
      outline=0*bnk
    elif (j+1)%9==0:
      bnx=0*bnk
      outlinex.append(outline+bnx+obsobs+'\n')
      outline=6*bnk
  # get amout of observ tyeps
  addemp.append(num)
  return addemp

# Get the total amount of sat system -------------------- #
def getsys_rnx3(in_f):
  # rinex message label
  obsobs='SYS / # / OBS TYPES'
  readst=False
  syslis=[]
  sysnum=0

  while True:
    inline=in_f.readline()
    if   not inline: break
    if   inline.find(obsobs)>=0:
      readst=True
      sys=inline[0:1]
      if sys==bnk: continue
      if sys not in syslis:
        syslis.append(sys)
        sysnum+=1
    elif readst and inline.find(obsobs)<0: break
  
  in_f.seek(0)
  return sysnum

# Convert head_data of RINEX 3.xx to Uni-format -------------- #
def rnx3_head2uni(in_f, desver, outlines):
  # rinex message label
  # obscom='COMMENT'
  obstpe='RINEX VERSION / TYPE'
  # obspro='PGM / RUN BY / DATE'
  # obsobs='SYS / # / OBS TYPES'
  obsshi='SYS / PHASE SHIFT'
  obsrsb='GLONASS COD/PHS/BIS'
  obsrsl='GLONASS SLOT / FRQ #'
  obsend='END OF HEADER'

  # get input head file & convert
  while True:
    inline=in_f.readline()
    # file is aleady checked so no need to judge again
    if   not inline: break
    #if   inline.find(obscom)>=0: outlines.append(inline)
    #elif inline.find(obspro)>=0: outlines.append(inline)
    #elif inline.find(obsobs)>=0: outlines.append(inline)
    elif inline.find(obstpe)>=0: conv_stamp(inline, outlines, desver)
    elif inline.find(obsshi)>=0: continue
    elif inline.find(obsrsb)>=0: continue
    elif inline.find(obsrsl)>=0: continue
    elif inline.find(obsend)>=0: break
    else                       : outlines.append(inline)

  # get the end message after break
  outlines.append(60*bnk+obsend+'\n')

  return 1

# Convert obs of RINEX 3.xx to Uni-format ------------------- #
def rnx2uni3_data(outlines, in_f):
  inline=in_f.readline()
  if not inline: return False
  if not inline[0:1]=='>': return True
  if not int(inline[30:32])==0: return True
  outlines.append(inline)
  satnum=int(inline[33:35])
  for i in range(satnum):
    outlines.append(in_f.readline())
  return True

# Convert RINEX 3.xx(epoch msg) to RINEX 2.xx --------------- #
def rnx3rnx2_epo(outline, sPRN):
  outlines=[]
  datedat=outline.split()
  # omit data when flag !=0 
  if not int(datedat[7])==0: return outlines
  outline=(
  '%3d%3d%3d%3d%3d%11.7f%3d%3d'
  %(int(datedat[1])-2000,int(datedat[2]),  int(datedat[3]),# |year |month  |day
    int(datedat[4])     ,int(datedat[5]),float(datedat[6]),# |hour |minute |second
    int(datedat[7])     ,len(sPRN)))                       # |flag |satnum |

  # convert to RINEX 2.xx
  satnum=len(sPRN)
  for i in range(satnum):
    outline+=sPRN[i]
    if   (i+1)==len(sPRN):
      outlines.append(outline+'\n')
    elif (i+1)%12==0:
      outlines.append(outline+'\n')
      outline=32*bnk
  return outlines

# Convert RINEX 3.xx(data of each sat) to RINEX 2.xx ------------ #
def rnx3rnx2_dat(addemp, obsnum, outline):
  outlines=[]
  num=range(len(addemp))

  empdat=16*bnk
  outlinx=[empdat for i in range(obsnum)]

  for i,j in zip(num,addemp):
    if    not outlinx[j]==empdat: continue
    if outline[i*16+3:i*16+16+3]:
      outlinx[j]=outline[i*16+3:i*16+16+3]\
        .replace('\n',2*bnk).replace('\r',2*bnk)
    else: continue

  outline=emp
  for i in range(len(outlinx)):
    outline+=outlinx[i]

  for i in range(math.ceil(len(outline)/80)):
    outlines.append(outline[i*80:i*80+80]+'\n')
  
  return outlines

# Convert RINEX 3.xx to RINEX 2.xx --------------------- #
def rnx3rnx2_data(outlines, addemp):
  sPRN=[]
  datline=[]
  outlinex=[]
  # filter the sat system ecxcept:#
  # ---GPS-Galileo-GLONASS-SBAS---#
  for i in range(len(outlines)):
    if   outlines[i][0:1]=='G': pass
    elif outlines[i][0:1]=='E': pass
    elif outlines[i][0:1]=='R': pass
    elif outlines[i][0:1]=='S': pass
    else: continue
    datline.append(i)
    sPRN.append(outlines[i][0:3])

  outlinex.extend(rnx3rnx2_epo(outlines[0], sPRN))

  for i in datline:
    if   outlines[i][0:1]=='G': idx=0
    elif outlines[i][0:1]=='E': idx=1
    elif outlines[i][0:1]=='R': idx=2
    elif outlines[i][0:1]=='S': idx=3
    else: continue
    outlinex.extend(rnx3rnx2_dat(addemp[idx], addemp[4], outlines[i]))
  return outlinex

# Convert Uni-format to RINEX 2.xx --------------------- #
def uni2rnx2_data(sysnum, outlines, out_f, headordata, add_emp):
  # rinex message label
  obspro='PGM / RUN BY / DATE'
  obsobs='SYS / # / OBS TYPES'
  obsend='END OF HEADER'

  outlinex=[]
  obsread=False

  # convert Uni-format to RINEX 2.xx(header)
  if       headordata:
    for i in range(len(outlines)):
      if   outlines[i].find(obspro)>=0: outlinex.append(datefmt3_conv(outlines[i]))
      elif outlines[i].find(obsobs)>=0:
        if not obsread:
          obsread=True
          addemp=obstype3_conv(i, sysnum, outlines, outlinex)
        else: continue
      elif outlines[i].find(obsend)>=0: outlinex.append(outlines[i])
      else:outlinex.append(outlines[i])

  # convert Uni-format to RINEX 2.xx(data)
  elif not headordata:
      if not outlines: return 0
      outlinex=rnx3rnx2_data(outlines, add_emp)

  # output to destination file
  out_f.writelines(outlinex)
  

  if       headordata: return addemp
  elif not headordata: return 0

# Convert data of RINEX 3.xx to Des-format ----------------- #
def rnx3des(in_path, out_path, oriver, desver):
  headread=False
  outlines=[]
  in_f=open(in_path, 'r')
  out_f=open(out_path, 'a')
  # get the amount of sat system
  sysnum=getsys_rnx3(in_f)
  # convert RINEX 3.xx(header) to Uni-format
  match rnx3_head2uni(in_f, desver, outlines):
    case 1: headread=True
    case 0: headread=False
  # convert Uni-foramt(header) to Des-format
  if       headread:
    match desver[0:1]:
      case '2': addemp=uni2rnx2_data(sysnum, outlines, out_f, True, None)
      case '3': uni2rnx3_data(outlines, out_f)
    outlines=[]
    # convert RINEX 3.xx(data) to Uni-format
    while rnx2uni3_data(outlines, in_f):
      # convert Uni-foramt(data) to Des-format
      match desver[0:1]:
        case '2': uni2rnx2_data(sysnum, outlines, out_f, False, addemp)
        case '3': uni2rnx3_data(outlines, out_f)
      outlines=[]
  elif not headread: return 0
  in_f.close()
  out_f.close()
  return 1

# Reject data of invaild input ----------------------- #
def rnx_reject(in_path, out_path, oriver):
  # rinex message label
  obstpe='RINEX VERSION / TYPE'
  obsmsg='OBSERVATION DATA'
  obsend='END OF HEADER'

  # reject cause cant input file
  try:
    with open(in_path, 'r'): pass
  except FileNotFoundError: return 0
  
  # reject wrong format or version
  in_f=open(in_path, 'r')
  while True:
    inline=in_f.readline()
    if not inline: return 0
    if inline.find(obstpe)>=0:
      if not inline.find(obsmsg)>=0: return 0
      if not inline[ 5: 6]==oriver : return 0
    elif inline.find(obsend)>=0: break

  # reject cause cant output file
  try:
    with open(out_path, 'w'): pass
  except PermissionError: return 0

  return 1

# ---------------------------------------------------------------------------------------
# CONVERT FUNCTION
#
# Brief  :Determine the file format and assign handlers
# Return :
#         queue msg==0: fail.
#         queue msg==1: ok.
# ---------------------------------------------------------------------------------------
def Convert_Un(in_path, out_path, oriver, desver, resqueue):
  file_state=False

  match rnx_reject(in_path, out_path, oriver):
    case  1: file_state=True
    case  0: file_state=False
  
  if file_state:
    match oriver:
      case '2': rnx2des(in_path, out_path, oriver, desver)
      case '3': rnx3des(in_path, out_path, oriver, desver)
  else        : return resqueue.put(0)

  return resqueue.put(1)
  
# Multi-threading task --------------------------- #
def _Convert_Un(in_path, out_path, oriver, desver, resqueue):
  T=threading.Thread(
    target=lambda :Convert_Un(in_path, out_path, oriver, desver, resqueue)
  )
  T.start()
  T.join()
  return resqueue.get()