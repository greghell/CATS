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
import sys
sys.stdout = open('FullLog.txt', 'w')
print 'creating log directory ' + os.getcwd()

# list dibas directories
print 'processing compute node #' + CompNodeNum[0]
dibaspaths = glob('/mnt_blc' + CompNodeNum[0] + '/datax*/dibas*')
NumDibasDir = np.size(dibaspaths)
print 'found ' + str(NumDibasDir) + ' dibas directories'
EmptyDibasDirLog = 'EmptyDibasBLC' + CompNodeNum[0] + '.txt'
emptydibaslist = open(EmptyDibasDirLog, 'w')
nEmptyDibas = 0
for direc in dibaspaths:
    if np.size(os.listdir(direc)) == 0:
        nEmptyDibas = nEmptyDibas + 1
        emptydibaslist.write(direc + '\n')
print 'found ' + str(nEmptyDibas) + ' EMPTY dibas directories'


# search RAW files in dibas directories
RAWFilList = []
for dir,_,_ in os.walk('/mnt_blc' + CompNodeNum[0] + '/'):
    RAWFilList.extend(glob(os.path.join(dir,'*.raw')))
NumRawFiles = np.size(RAWFilList)   # number of raw files
RawListLog = 'RawFilesBLC' + CompNodeNum[0] + '.txt'
DiagRawListLog = 'DiagRawFilesBLC' + CompNodeNum[0] + '.txt'
BLCnonDiagLog = 'BLC_non_diag_RawFilesBLC' + CompNodeNum[0] + '.txt'
GUPPInonDiagLog = 'GUPPI_non_diag_RawFilesBLC' + CompNodeNum[0] + '.txt'
NonStdnonDiagLog = 'non_standard_non_diag_RawFilesBLC' + CompNodeNum[0] + '.txt'
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
print str(NumRawFiles) + ' RAW files found on BLC' + CompNodeNum[0] + ' - listed in ' + RawListLog
print str(DiagRAW) + ' DIAG RAW files found on BLC' + CompNodeNum[0] + ' - listed in ' + DiagRawListLog
print str(BLCnonDiag) + ' non DIAG RAW files found on BLC' + CompNodeNum[0] + ' - listed in ' + BLCnonDiagLog + ' => TO GPUSPEC'
print str(GUPPInonDiag) + ' non DIAG GUPPI RAW files found on BLC' + CompNodeNum[0] + ' - listed in ' + GUPPInonDiagLog + ' => TO RE-GPUSPEC'
print str(NonStdNonDiag) + ' non standard RAW files found on BLC' + CompNodeNum[0] + ' - listed in ' + NonStdnonDiagLog


