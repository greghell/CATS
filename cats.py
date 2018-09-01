# CATS
import os
import time
from glob import glob
import numpy as np

CompNodeNum = ['00','01','02','03','04','05','06','07',\
               '10','11','12','13','14','15','16','17',\
               '20','21','22','23','24','25','26','27',\
               '30','31','32','33','34','35','36','37']

# set up workspace
os.chdir('/home/ghellbou/CATS/catspy/') # MAKE IT USER VALUE
timestr = time.strftime("%Y%m%d-%H%M%S")
dirname = 'CATS_'+timestr
os.mkdir(dirname)
os.chdir(dirname)
print '\ncreating log directory ' + os.getcwd()

for CompNode in CompNodeNum:
    
    # list dibas directories
    print '\nprocessing compute node #' + CompNode
    dibaspaths = glob('/mnt_blc' + CompNode + '/datax*/dibas*')
    for pathtofile in dibaspaths:
        if not os.path.isdir(pathtofile):
            dibaspaths.remove(pathtofile)
    NumDibasDir = np.size(dibaspaths)
    print 'found ' + str(NumDibasDir) + ' dibas directories'
    EmptyDibasDirLog = 'EmptyDibasBLC' + CompNode + '.txt'
    emptydibaslist = open(EmptyDibasDirLog, 'w')
    nEmptyDibas = 0
    for direc in dibaspaths:
        if np.size(os.listdir(direc)) == 0:
            nEmptyDibas = nEmptyDibas + 1
            emptydibaslist.write(direc + '\n')
    print 'found ' + str(nEmptyDibas) + ' EMPTY dibas directories'
    
    
    # search RAW files in dibas directories
    RAWFilList = []
    FILFilList = []
    for dir,_,_ in os.walk('/mnt_blc' + CompNode + '/'):
        RAWFilList.extend(glob(os.path.join(dir,'*.raw')))
        FILFilList.extend(glob(os.path.join(dir,'*.fil')))
    NumRawFiles = np.size(RAWFilList)   # number of raw files
    RawListLog = 'RawFilesBLC' + CompNode + '.txt'
    DiagRawListLog = 'DiagRawFilesBLC' + CompNode + '.txt'
    BLCnonDiagLog = 'BLC_non_diag_RawFilesBLC' + CompNode + '.txt'
    GUPPInonDiagLog = 'GUPPI_non_diag_RawFilesBLC' + CompNode + '.txt'
    NonStdnonDiagLog = 'non_standard_non_diag_RawFilesBLC' + CompNode + '.txt'
    rawlist = open(RawListLog, 'w')
    DiagRawlist = open(DiagRawListLog, 'w')
    BLCNonDiagRawlist = open(BLCnonDiagLog, 'w')
    GUPPINonDiagRawlist = open(GUPPInonDiagLog, 'w')
    NonStdNonDiagRawlist = open(NonStdnonDiagLog, 'w')
    DiagRAW = 0
    BLCnonDiag = 0
    GUPPInonDiag = 0
    NonStdNonDiag = 0
    for fil in RAWFilList:
        rawlist.write(fil + '\n')   # write raw file name in log
        if fil.find('diag')!=-1 or fil.find('DIAG')!=-1 or fil.find('Diag')!=-1:    # if DIAG file : write to DIAG log
            DiagRAW = DiagRAW + 1
            DiagRawlist.write(fil + '\n')
        else:
            FileName = fil.split("/")[-1]
            if FileName[:3]=='blc' or FileName[:3]=='BLC':
                BLCnonDiag = BLCnonDiag+1
                BLCNonDiagRawlist.write(fil + '\n')
            elif FileName[:5]=='guppi':
                GUPPInonDiag = GUPPInonDiag+1
                GUPPINonDiagRawlist.write(fil + '\n')
            else:
                NonStdNonDiag = NonStdNonDiag+1
                NonStdNonDiagRawlist.write(fil + '\n')
    rawlist.close()
    DiagRawlist.close()
    BLCNonDiagRawlist.close()
    GUPPINonDiagRawlist.close()
    NonStdNonDiagRawlist.close()
    print str(NumRawFiles) + ' RAW files found on BLC' + CompNode + ' - listed in ' + RawListLog
    print str(DiagRAW) + ' DIAG RAW files found on BLC' + CompNode + ' - listed in ' + DiagRawListLog
    print str(BLCnonDiag) + ' non DIAG RAW files found on BLC' + CompNode + ' - listed in ' + BLCnonDiagLog + ' => TO GPUSPEC'
    print str(GUPPInonDiag) + ' non DIAG GUPPI RAW files found on BLC' + CompNode + ' - listed in ' + GUPPInonDiagLog + ' => TO RE-GPUSPEC'
    print str(NonStdNonDiag) + ' non standard RAW files found on BLC' + CompNode + ' - listed in ' + NonStdnonDiagLog
    
    # find FIL files associated with guppi raw files
    GUPPINonDiagRawlist = open(GUPPInonDiagLog, 'r')
    guppilist = GUPPINonDiagRawlist.readlines()
    GuppiFILnum = 0
    Guppi_NO_FILnum = 0
    guppiFILlog = 'guppi_fil_filesBLC' + CompNode + '.txt'
    guppi_without_FILlog = 'guppi_without_fil_filesBLC' + CompNode + '.txt'
    guppiFILlist = open(guppiFILlog, 'w')
    guppi_no_FILlist = open(guppi_without_FILlog, 'w')
    old_fname = ''
    for rawfile in guppilist:
        fname =  rawfile.split("/")[-1]
        if len(fname) > 11:
            corename = fname[:-10]
            pathtofile = os.path.dirname(rawfile)
            if old_fname != corename:
                filfiles = glob(pathtofile + '/*' + corename + '*.fil')
                if len(filfiles) > 0:
                    GuppiFILnum = GuppiFILnum+1
                    for filfilename in filfiles:
                        guppiFILlist.write(filfilename + '\n')
                else:
                    Guppi_NO_FILnum = Guppi_NO_FILnum + 1
                    guppi_no_FILlist.write(rawfile)
        old_fname = corename
    print 'found ' + str(GuppiFILnum) + ' FIL files datasets associated with GUPPI RAW files on BLC' + CompNode + ' - listed in ' + guppiFILlog + ' -> to delete and try to re-GPUSPEC'
    print 'found ' + str(Guppi_NO_FILnum) + ' GUPPI RAW files datasets without FIL files on BLC' + CompNode + ' - listed in ' + guppi_without_FILlog + ' -> try to re-GPUSPEC'
    guppiFILlist.close()
    guppi_no_FILlist.close()
    
    
    ## work on filterbank files
    
    NumFILFiles = np.size(FILFilList)   # number of raw files
    FILListLog = 'FILFilesBLC' + CompNode + '.txt'
    non_blc_FILListLog = 'non_blc_FILFilesBLC' + CompNode + '.txt'
    FILlist = open(FILListLog, 'w')
    non_blc_FILlist = open(non_blc_FILListLog, 'w')
    num_fil_no_blc = 0
    for fil in FILFilList:
        FILlist.write(fil + '\n')
        fname = fil.split("/")[-1]
        if fname[:5] != 'blc' + CompNode and fname[:5] != 'BLC' + CompNode:
            num_fil_no_blc = num_fil_no_blc+1
            non_blc_FILlist.write(fil + '\n')
    print str(NumFILFiles) + ' FIL files found on BLC' + CompNode + ' - listed in ' + FILListLog
    print str(num_fil_no_blc) + ' FIL files NOT starting with ~BLC' + CompNode + '~ found on BLC' + CompNodeNum[0] + ' - listed in ' + non_blc_FILListLog
    
    
    
