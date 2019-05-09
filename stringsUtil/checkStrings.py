# -*- coding: utf-8 -*- 
import xlrd
import re
import  os

data = xlrd.open_workbook(os.path.abspath('thr.xls'))
table = data.sheets()[0]
nrows = table.nrows
xlKeys = []
reKeyCount = 0
reKey = ''
for rownum in range(1,nrows):
    row = table.row_values(rownum)
    if row:
        tempkey = row[1].strip()
        if len(tempkey) <= 0:
            nrows = nrows - 1
            continue
        result = re.match('^#?\w+$',tempkey)
        if result:
            if tempkey.startswith('#'):
                if reKey != tempkey[1:]:
                    reKey = tempkey[1:]
                    reKeyCount = 0
                reKeyCount += 1
                reKeyStr = reKey+'_%d' %reKeyCount
                xlKeys.append(reKeyStr)
            else:
                xlKeys.append(tempkey)
        else:
            nrows = nrows - 1
    else:
        nrows = nrows - 1

strFile = open(os.path.abspath('Localizable.strings'))
line = strFile.readline()
strKeys = []
while line:
    if line.startswith('\"'):
        strs = line.split('\"')
        strKeys.append(strs[1])
    line = strFile.readline()
strFile.close()

diffKeys = []
for key in xlKeys:
    if key in strKeys:
        strKeys.remove(key)
    else:
        diffKeys.append(key)
        print(key)

print(len(diffKeys))
for key in strKeys:
    print(key)
print(len(strKeys))
