import MFI_Getter
import pandas as pd
import timeit
#under construction

start = timeit.default_timer()

symbolfile = open("symbols.txt")
symbolslistR = symbolfile.read()
symbolslist = symbolslistR.split('\n')

dfF = MFI_Getter.getMFI('KING')

for s in symbolslist:
    try:
        df = MFI_Getter.getMFI(s)
        dfF = dfF.append(df)
    except Exception as ex:
        template = "An exception of type {0} occured. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print message, s

dfF.to_csv('MFI'+'.csv')

stop = timeit.default_timer()
print "start= ",start,"stop= ",stop