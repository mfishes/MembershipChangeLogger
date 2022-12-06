import os
import pandas as pd

lsPeople = {}
lsfilestats = {}

def parseRow(row, filestats):
    fZip = 'Billing_Zip'
    fStatus = 'membership_status'
    
    currentID = int(row['AK_ID'])
    if currentID in lsPeople:
        data = lsPeople[currentID]
        if data[fStatus] != isactivemember(row[fStatus]):
            #update the member
            lsPeople[currentID][fStatus] = isactivemember(row[fStatus])
            #log it
            if data[fStatus]: filestats['renewed'] += 1
            else: filestats['lapsed or cancelled'] += 1               
        #todo: track actual zip changes
        if row[fZip] != data[fZip]: filestats['moved'] += 1   
            
    else:
        lsPeople.update({currentID : {
            fStatus : isactivemember(row[fStatus]),
            fZip : row[fZip]
        }})
        
def isactivemember(value):
    member = ['member', 'member in good standing']
    return True if value in member else False

def parseFileStats(lsFileStats):
    output = ""
    lastvalues = {}
    for  filestat in sorted(filestats):
        if len(lastvalues) == 0:
            output = 'starting with '
        directory = 'InputFiles\CSV'  
        
    

directory = 'InputFiles\CSV'  
for filename in sorted(os.listdir(directory)):
    pdFile = pd.read_csv(os.path.join(directory,filename))
    filestats = {'new' : 0, 'renewed' : 0, 'lapsed or cancelled' : 0, 'moved' : 0, 'active' : 0, 'inactive' : 0}
    for index, row in pdFile.iterrows():
        parseRow(row, filestats)
    lsfilestats.update({filename : filestats})
            