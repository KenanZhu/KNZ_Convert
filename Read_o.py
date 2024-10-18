import time
import math

def ConvertObsVersion(ofile_path, out_directory, version, system):
    blank = " "
    global outf
    if version == 2.10 or version == 2.11:
        with open(ofile_path, 'r') as f:
            with open(out_directory, 'w') as outf:
                outf.close()

            # Get the locate time and transform to RINEX format
            y = time.localtime().tm_year
            m = time.localtime().tm_mon
            d = time.localtime().tm_mday
            h = time.localtime().tm_hour
            min = time.localtime().tm_min
            sec = time.localtime().tm_sec

            localtime = str(y)+str(m)+str(d)+blank+"%02d"%h+"%02d"%min+"%02d"%sec+blank+"LOC"+blank

            # Output the convert message
            outf = open(out_directory, 'a')
            print("     %4.2f->3.04 COV-OBSERVATION DATA    %s                   CONVERT VERSION / TYPE\n"
                    "KNZ_Convert ver 1.0.6                   %sCONVERT BY / TIME\n"
                    %(version, system, localtime)
                    , end="", file=outf)

            #Refactoring header file format to 3.04
            while 1:
                line = f.readline()
                if line.find("COMMENT") >= 0:

                    print(line,end="",file=outf)


                elif line.find("RINEX VERSION / TYPE") >= 0:
                    line = "%9s"%("3.04") + line[ 9:80] + "\r"

                    print(line,end="",file=outf)


                elif line.find("PGM / RUN BY / DATE") >= 0:
                    hour = line[49:51]
                    min  = line[52:54]
                    sec  = line[55:57]
                    line = line[ 0:49] + hour + min + sec + blank + "UTC" + blank + "PGM / RUN BY / DATE\n"

                    print(line,end="",file=outf)


                elif line.find("WAVELENGTH FACT L1/2") >= 0:
                    pass

                elif line.find("# / TYPES OF OBSERV") >= 0:

                    global obsnum
                    obsnum = int(line[ 0: 6])

                    count0 = 0 # The line counters
                    count1 = 0 # The total counters
                    obstypes= []
                    while 1:
                        obstypes.append( str.strip(line[ 0 + 6 * (count0 + 1): 6 + 6 * (count0 + 1)]) )
                        count0 += 1
                        count1 += 1
                        if count1 == obsnum:
                            break
                        if count0 % 9 == 0:
                            line = f.readline()
                            count0 = 0
                    #                                               #
                    #                                               #
                    #                                               #
                    #Covert the observation types from 2.xx to 3.04
                    count = 0
                    for obstype in obstypes:
                        if obstype.find("5") >= 0 or obstype.find("7") >= 0 or obstype.find("8") >= 0:
                            obstype = obstype + "I"
                        elif obstype.find("6") >= 0:
                            obstype = obstype + "C"
                        elif obstype.find("1") >= 0 or obstype.find("2") >= 0:
                            if obstype.find("P") >= 0:
                                obstype = "C" + obstype[1:2] + "P"
                            else:
                                obstype = obstype + "C"

                        obstypes[count] = obstype
                        count += 1

                    #Refactoring observation type format to 3.04
                    syss = ['G', 'R', 'E', 'S']
                    for sys in syss:
                        line = sys + 3*blank + "%2d"%obsnum + blank
                        count0 = 0
                        count1 = 0
                        for obstype in obstypes:
                            line += obstype + blank
                            count0 += 1
                            count1 += 1
                            # Output the final line
                            if count1 == obsnum:
                                line += (13 - count0) * 4 * blank + blank + "SYS / # / OBS TYPES\n"
                                print(line, end="", file=outf)
                                break
                            # Output the first line
                            if count0 % 13 == 0:
                                line +=  blank + "SYS / # / OBS TYPES\n"
                                print(line, end="", file=outf)
                                line = 7*blank
                                count0 = 0


                elif line.find("END OF HEADER") >= 0:
                    print(line,end="",file=outf)

                    break

                else:
                    print(line,end="",file=outf)


            # Refactoring data file format to 3.04
            while 1:
                line = f.readline()
                if line == "":
                    break
                elif line[0:5] == 5*blank:
                    print(line, end="", file=outf)
                elif line.find("COMMENT") >= 0:
                    print(line, end="", file=outf)
                else:
                    # Refactoring epoch format to 3.04
                    year   =   int(line[ 0               : 3])
                    month  =   int(line[ 0+3             : 3+3])
                    day    =   int(line[ 0+3+3           : 3+3+3])
                    hour   =   int(line[ 0+3+3+3         : 3+3+3+3])
                    minute =   int(line[ 0+3+3+3+3       : 3+3+3+3+3])
                    second = float(line[ 0+3+3+3+3+3     : 3+3+3+3+3+11])
                    e_flag =   int(line[ 0+3+3+3+3+3+11  : 3+3+3+3+3+11+3])
                    satnum =   int(line[ 0+3+3+3+3+3+11+3: 3+3+3+3+3+11+3+3])

                    sPRN = []

                    lineo = ">" + blank + "%4d %02d %02d %02d %02d %10.7f %2d %2d\n"\
                                         %(year+2000, month, day, hour, minute, second, e_flag, satnum)

                    print(lineo, end="", file=outf)



                    count0 = 0 # The line counters
                    count1 = 0 # The total counters
                    while 1:
                        sPRN.append(line[32+3*count0:32+3*(count0+1)].replace(blank,"0"))
                        count0 += 1
                        count1 += 1
                        if count1 == satnum:
                            break
                        if count0 % 12 == 0:
                            count0 = 0
                            line = f.readline()
                    #                                #
                    #                                #
                    #                                #
                    #Refactoring data format to 3.04
                    count = 0
                    while 1:
                        if obsnum <= 5:
                            line = f.readline()
                            line = sPRN[count] + line
                        elif obsnum > 5:
                            count1 = 0
                            lineo =""
                            while 1:
                                line = f.readline()
                                lineo += line.replace("\n", "").replace("\r", "")
                                if len(lineo) % 16 == 15:
                                    lineo += blank
                                if len(lineo) % 16 == 14:
                                    lineo += 2*blank
                                if len(line) < 80:
                                    lineo += (5 - int(len(lineo)/16))*16*blank

                                count1 += 1
                                if count1 == math.ceil(obsnum/5):
                                    line = sPRN[count] + lineo +"\n"
                                    break
                        print(line, end="", file=outf)
                        count += 1
                        if count == satnum:
                            break
            outf.close()
            f.close()
        return 1

def ReadObsVersion(ofile_path, out_directory):
    obsfile = None
    # Get the obs file name---------------------------#
    obspath = len(ofile_path)
    while obspath > 0:
        flag = ofile_path[obspath - 1:obspath]
        if flag == "/":
            obsfile =  ofile_path[obspath:]
            break
        obspath -= 1
    if out_directory == '':
        # Get the file's father folder-------------------#
        pathlon = len(ofile_path)
        while pathlon - 3 > 0:
            flag = ofile_path[pathlon - 3 - 1:pathlon - 3]
            if flag == "/":
                out_directory = ofile_path[:pathlon - 3] + "COV-" + obsfile
                break
            pathlon -= 1
        # -----------------------------------------------#
    else:
        out_directory += "COV-" + obsfile
    with open(ofile_path, 'r') as f:
        while 1:
            line = f.readline()
            if line.find("RINEX VERSION / TYPE") >= 0:
                version = float(line[ 5: 9])
                system = line[40:41]
                f.close()
                if version > 2.11:
                    return 0

                return ConvertObsVersion(ofile_path, out_directory, version, system)
            else:
                return 0




