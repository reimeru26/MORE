"""
    Read input data for system simulation.
    Functions in this file:
    
    * readInPV(infile)
    - read data for photovoltaics production (from PVGIS website)
    
    * readInFuel(infile)
    - read data for car driving cycle (7 days)
    
    * readIn(infile)
    - read input parameter for system simulation
    - process data (conert to numbers or text) and store it in a dictionary


Uwe Reimer, Emden, January 2026
"""
##########################################################
def readInPVGIS(infile):
    # function to read file with PV power data for one year 

    myin = open(infile, 'r')  # open a text file in read modus
    mytext = myin.readlines()    # here, we read the entire file into a list of strings (each line is one item)
    myin.close()

    # remove header line from list / there are 11 lines
    del mytext[0:11]   

    # remove lines at the end / there are also 11 lines
    b = len(mytext)
    a = b - 11
    del mytext[a:b]

    # Step 2: convert text to numbers 
    dataAll = []
    pv = []
    wind = []
    temp = []

    for a in mytext:
        b = a.split(',')
        p = float( b[1] )
        pv.append(p)
        p = float( b[5] )
        wind.append(p)
        p = float( b[4] )
        temp.append(p)
        
    dataAll.append(pv)
    dataAll.append(wind)
    dataAll.append(temp)
    
    return dataAll
##########################################################

def readInFuel(infile):
    # function to read file with H2 fueling data for one week (7 days) 

    myin = open(infile, 'r')  # open a text file in read modus
    mytext = myin.readlines()    # here, we read the entire file into a list of strings (each line is one item)
    myin.close()

    # remove header line from list 
    del mytext[0]   

    # Step 2: convert text to numbers 
    d = []

    for a in mytext:
        b = a.split()
        p = float( b[1] )
        d.append(p)
    
    return d
##########################################################
def readIn(infile):
    # function to read file with input data for system simulation 
    myall = {}  # dictionary for all entries
    mykeys = []
    v = [] # list for parameters

    myin = open(infile, 'r')  # open a text file in read modus
    mytext = myin.readlines()    # here, we read the entire file into a list of strings (each line is one item)
    myin.close()
    
    # read sections
    for a in mytext:
        if a[0] == '#':
           b = a.split(' ')
           mykeys.append( b[1] )

    # read values
    x = -1
    for a in mytext:
        if a[0] == '#':
            if x > (-1):
                myall[ mykeys[x] ] = v
                v = []
            x = x + 1
        else:
            b = a.split('=')
            v.append(b[1])
            
    # last entry
    myall[ mykeys[x] ] = v
    
    # processing
    for a in myall.keys():

        if a == 'system':
            b = myall[a]
            x = 0
            v = []
            for c in b:
                if x > 1:
                    v.append( float(c) )
                else:
                    v.append( c.strip() ) # remove whitespace
                x = x + 1
            myall[a] = v
        elif a == 'CAPEX':
            b = myall[a]
            v = []
            for c in b:
                d = c.split('/')
                e = float(d[0]) / float(d[1])
                v.append(e)
            myall[a] = v
        else:
            b = myall[a]
            v = []
            for c in b:
                v.append( float(c) )
            myall[a] = v
                    
    """ check
    for a in myall.keys():
        print(a, myall[a])
    """
    return myall