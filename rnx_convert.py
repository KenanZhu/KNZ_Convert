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

emp=''
bnk=' '

# Get local time of converting ----------------------- #
def conv_time():
  # generate convert timestamp
  covpro='KNZ_Convert ver1.2.5'
  covtmp='COV-PGM / DATE'

  # Get the locate time and transform to RINEX format
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
           covtmp   +
           '\n')
  
  return outline



# Convert Format ------------------------------ #
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



# Convert Format ------------------------------ #
def datefmt3_conv(inline):
  hou=inline[49:51]
  min=inline[51:53]
  sec=inline[53:55]
  return (inline[0:49] +
          hou + ':' +
          min + ':' +
          sec + ':' +
         'UTCPGM / RUN BY / DATE\n')



# Convert observ type of RINEX 2.xx to Uni-Format --------------- #
def obsfmt2_conv(obstypes, sys):

  counter =0
  obstypex=[]
  obsbomit=''

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



# Convert observ msg of RINEX 2.xx to Uni-Format ---------------- #
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
        outlines.append(outline+bnx+obsobs+'\n')
        outline=0*bnk
      elif (i+1)%13==0:
        outlines.append(outline+bnk+obsobs+'\n')
        outline=7*bnk
  return outlines



# Convert obstpe msg of RINEX 2.xx to Uni-Format --------------- #
def obstpe2_conv(inline, outlines, desver):
  oriver=inline[ 5: 9]
  # generate convert stamp
  obscov='COV-OBSERVATION DATA'
  covpro='COV-RINEX VER / TYPE'

  outlines.append( 5*bnk+
                  oriver+
                  '->'  +
                  desver+
                   1*bnk+
                  obscov+
                  24*bnk+
                  covpro+
                  '\n')
  outlines.append(conv_time())
  outlines.append(
    inline.replace('%s'%re.search(r'[1-9]\d*.\d*|0\.\d*[1-9]\d*', inline).group(), desver))
  return



# Convert head_data of RINEX 2.xx to Uni-format -------------- #
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
    if   not inline: pass
    if   inline.find(obscom)>=0: outlines.append(inline)
    elif inline.find(obspro)>=0: outlines.append(datefmt2_conv(inline))
    elif inline.find(obsobs)>=0: outlines.extend(obstype2_conv(inline, in_f, omilist))
    elif inline.find(obstpe)>=0: obstpe2_conv(inline, outlines, desver)
    elif inline.find(obsl12)>=0: continue
    elif inline.find(obsend)>=0: break
    else                       : outlines.append(inline)

  # get the end message after break
  outlines.append(60*bnk+obsend+'\n')

  return 1



# Convert obs of RINEX 2.xx to Uni-Format ------------------- #
def rnx2_data2uni(in_f, outlines, omilist, obsnum):
  sPRN=[]
  scounter=0
  outline=emp

  # return false when file end
  inline=in_f.readline()
  if not inline  : return False

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
def uni2rnx3_data(outlines, out_path):
  out_f = open(out_path, 'a')
  out_f.writelines(outlines)
  out_f.close()
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



# Convert data of RINEX 2.xx to Des-format ----------------- #
def rnx2des(in_path, out_path, oriver, desver):
  headread=False
  outlines=[]
  omilist=[]
  # convert rinex 2.xx(header) to Uni-format
  in_f=open(in_path, 'r')
  match rnx2_head2uni(in_f, desver, outlines, omilist):
    case 1: headread=True
    case 0: headread=False
  
  uni2rnx3_data(outlines, out_path)
  outlines=[]

  if headread:
    # get each observ type and omit the empty
    obsnum=omilist[0]
    omilist.pop(0)
    getomit(omilist)

    while rnx2_data2uni(in_f, outlines, omilist, obsnum):
      match desver[0:1]:
        case '2': return 0
        case '3': uni2rnx3_data(outlines, out_path)
      outlines=[]
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
      case '3': resqueue.put(0)
  else        : resqueue.put(0)

  resqueue.put(1)
  return

# Multi-threading task --------------------------- #
def _Convert_Un(in_path, out_path, oriver, desver, resqueue):
  T=threading.Thread(
    target=lambda :Convert_Un(in_path, out_path, oriver, desver, resqueue)
  )
  T.start()
  T.join()
  return resqueue.get()







# --------------------------------------------------------------- #
# The functions below are not be useable. on progress............ #
#
#
# --------------------------------------------------------------- #

# Convert observ type of RINEX 3.xx to Uni-Format --------------- #
def obsfmt_conv_cxx(obstypes):
  outlines=[]
  outline='%6d'%len(obstypes)

  for i in range(len(obstypes)):
    outline+='%6s'%obstypes[i]
    if   (i+1)==len(obstypes):
      outlines.append(outline + (9 - (i+1)%9)*6*bnk + '# / TYPES OF OBSERV\n')
      outline=''
    elif (i+1)%9==0:
      outlines.append(outline + '# / TYPES OF OBSERV\n')
      outline=6*bnk
  return outlines
# Convert observ msg of RINEX 3.xx to Uni-Format ---------------- #
def obstype_conv_cxx(obstypes, inline, in_f):
  while True:
    if   inline[0:1]=='G': flag=True
    elif inline[0:1]=='E': flag=True
    elif inline[0:1]=='R': flag=True
    elif inline[0:1]=='S': flag=True
    else: flag=False

    if flag:
      obsnum=int(inline[2:6])
      for i in range(math.ceil(obsnum/13)):
        for obs in inline[6:60].split():
          if obs[1:2]=='3': continue
          if obs[1:2]=='4': continue
          if obs[2:3]=='P': obs='P'+obs[1:2]
          else: obs=obs[0:2]
          if obs and obs not in obstypes:
            obstypes.append(obs)

        if i+1==math.ceil(obsnum/13):
          break
        inline=in_f.readline()
    return
# Convert head_data of RINEX 3.xx to Uni-format -------------- #
def rnx3_head2uni(in_path, out_path, desver):
  try:
    with open(in_path, 'r'): pass
  except FileNotFoundError:
    return -12

  obstypes=[]
  outlines=[]
  in_put=False
  output=False
  in_f=open(in_path, 'r')
  while True:
    inline=in_f.readline()
    if   not inline:
      return 0
    
    if   in_put and not output:
      if not inline.find('SYS / # / OBS TYPES')>=0:
        output=True

    if   in_put and output:
      outlines.extend(obsfmt_conv_cxx(obstypes))
      in_put=False
      output=False

    if   inline.find('COMMENT')>=0:
      outlines.append(inline)

    elif inline.find('RINEX VERSION / TYPE')>=0:
      if not inline.find('OBSERVATION DATA')>=0:
        return -10
      if not float(inline[5: 9])>=3:
        return -10
      # Output convert message
      outlines.append(
         5*bnk+'%s->%s'%(str(inline[5: 9]),str(desver))+
         1*bnk+'COV-OBSERVATION DATA'+
        24*bnk+'COV-RINEX VER / TYPE\n')
      outlines.append(conv_time())
      outlines.append(inline.replace(
        '%s'%re.search(r'[1-9]\d*.\d*|0\.\d*[1-9]\d*', inline).group(),
        desver))
      
    elif inline.find('PGM / RUN BY / DATE')>=0:
      outlines.append(datefmt3_conv(inline))

    elif inline.find('SYS / # / OBS TYPES')>=0:
      in_put=True
      obstype_conv_cxx(obstypes, inline, in_f)

    elif inline.find('SYS / PHASE SHIFT')>=0:
      continue

    elif inline.find('GLONASS COD/PHS/BIS')>=0:
      continue

    elif inline.find('GLONASS SLOT / FRQ #')>=0:
      continue

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