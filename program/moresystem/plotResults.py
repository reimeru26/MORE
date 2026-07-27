"""
    Plot results of the system simulation.  
    
    * plotYear(dataPV, myres)
    - Energy to electrolyser -> EnergyToH2.png
    - Enery to grid -> EnergyToGrid.png
    - Hydrogen production (cumulated, this would refer to unlimited tank and no consumption) -> H2Prod.png
    
    * plotStat(myres)
    - State of stationary storage (in kg) -> Tank.png
    - State of car fueling (driving range in %), this indicates if there is enough hydrogen to drive -> Car.png
    - Hydrogen overproduction (this is internal data, electrolyser needs to shut down because storage is full) - OverProd.png

Uwe Reimer, Emden, January 2026

"""
import matplotlib.pyplot as plt

def plotStat(myres, myIn):
    tank = myres[6]
    car = myres[10]
    hy = myres[4]
    con = myres[3] # consumed H2 in kWh
    
    fwidth = 15                 # figure width in cm
    fwidth = fwidth / 2.54      # conversion inches to cm
    fheight = fwidth * 3/4		# using a ratio of 3/4 for height
    
    mx = len(tank) + 1
    x = range(1, mx, 1) # number of hours
    
    ###
    pngfile = 'Tank' + '.png'		# file name for output
    plt.subplots( figsize=( fwidth,fheight ) )

    y = tank
    plt.plot(x, y, color='grey')	# line plot 

    plt.xlabel('Hours')           # label x-axis
    plt.ylabel('Hydrogen / kg')    # label y-axis
    
    #plt.ylim(0,myIn['system'][6])
    plt.tight_layout()          # optimize placement
    plt.savefig(pngfile)        # create file for output
    plt.close()
    
    ###
    pngfile = 'Car' + '.png'		# file name for output
    plt.subplots( figsize=( fwidth,fheight ) )

    y = car
    plt.plot(x, y, color='forestgreen')	# line plot 

    plt.xlabel('Hours')           # label x-axis
    plt.ylabel('Driving range / %')    # label y-axis
    
    plt.ylim(0,101)
    plt.tight_layout()          # optimize placement
    plt.savefig(pngfile)        # create file for output
    plt.close()
    
    ###
    pngfile = 'H2Heating' + '.png'		# file name for output
    plt.subplots( figsize=( fwidth,fheight ) )

    y = con
    plt.plot(x, y, color='red')	# line plot 

    plt.xlabel('Hours')           # label x-axis
    plt.ylabel('Heating in kW')    # label y-axis
    
    #plt.ylim(0,101)
    plt.tight_layout()          # optimize placement
    plt.savefig(pngfile)        # create file for output
    plt.close()

    ###
    pngfile = 'OverProd' + '.png'		# file name for output
    plt.subplots( figsize=( fwidth,fheight ) )

    y = []
    for a in myres[8]:
        b = a * myIn['operation'][2]
        y.append(b)
        
    plt.plot(x, y, color='red', label='H2 overproduction')	# line plot 

    plt.xlabel('Hours')           # label x-axis
    plt.ylabel('Power / kW')    # label y-axis

    plt.legend(loc='upper left')
    plt.tight_layout()          # optimize placement
    plt.savefig(pngfile)        # create file for output
    plt.close()
    
    ###
    b = 0.0     # sum up H2 production
    h = []
    for a in hy:
        b = b + a
        h.append(b)
    
    pngfile = 'H2Prod' + '.png'		# file name for output
    plt.subplots( figsize=( fwidth,fheight ) )

    y = h
    plt.plot(x, y, color='royalblue')	# line plot 

    plt.xlabel('Hours')           # label x-axis
    plt.ylabel('Hydrogen / kg')    # label y-axis

    plt.tight_layout()          # optimize placement
    plt.savefig(pngfile)        # create file for output
    plt.close()
    
##############################
def plotMain(dataPV,dataWind, myres, ymax):
    
    hydro = myres[0]
    grid = myres[1]
    bat = myres[2]
    
    fwidth = 15                 # figure width in cm
    fwidth = fwidth / 2.54      # conversion inches to cm
    fheight = fwidth * 3/4		# using a ratio of 3/4 for height
    
    mx = len(dataPV) + 1
    x = range(1, mx, 1) # number of hours
    
    ###
    pngfile = 'ProdPV' + '.png'		# file name for output
    plt.subplots( figsize=( fwidth,fheight ) )

    y = dataPV
    plt.plot(x, y, label='PV prod.', color='orange')	# line plot 

    plt.xlabel('Hours')           # label x-axis
    plt.ylabel('Power / kW')    # label y-axis
    
    plt.ylim(0,ymax)
    plt.legend(loc='upper right')
    plt.tight_layout()          # optimize placement
    plt.savefig(pngfile)        # create file for output
    plt.close()
    
    ###
    ###
    pngfile = 'ProdWind' + '.png'		# file name for output
    plt.subplots( figsize=( fwidth,fheight ) )

    y = dataWind
    plt.plot(x, y, label='Wind prod.', color='peru')	# line plot 
    

    plt.xlabel('Hours')           # label x-axis
    plt.ylabel('Power / kW')    # label y-axis
    
    plt.ylim(0,ymax)
    plt.legend(loc='upper right')
    plt.tight_layout()          # optimize placement
    plt.savefig(pngfile)        # create file for output
    plt.close()
    
    
    ###
    pngfile = 'EnergyToH2' + '.png'		# file name for output
    plt.subplots( figsize=( fwidth,fheight ) )

    y = hydro
    plt.plot(x, y, label='H2', color='royalblue')	# line plot 

    plt.xlabel('Hours')           # label x-axis
    plt.ylabel('Power / kW')    # label y-axis
    
    plt.ylim(0,ymax)
    #plt.legend(loc='upper right')
    plt.tight_layout()          # optimize placement
    plt.savefig(pngfile)        # create file for output
    plt.close()
    
    ###
    pngfile = 'EnergyToGrid' + '.png'		# file name for output
    plt.subplots( figsize=( fwidth,fheight ) )

    y = grid
    plt.plot(x, y, label='to grid', color='gray')	# line plot 

    plt.xlabel('Hours')           # label x-axis
    plt.ylabel('Power / kW')    # label y-axis

    #plt.legend(loc='upper right')
    plt.ylim(0,ymax)
    plt.tight_layout()          # optimize placement
    plt.savefig(pngfile)        # create file for output
    plt.close()
    
    ###
    pngfile = 'Battery' + '.png'		# file name for output
    plt.subplots( figsize=( fwidth,fheight ) )

    y = bat
    plt.plot(x, y, color='grey')	# line plot 
    #plt.ylim(0,100)

    plt.xlabel('Hours')           # label x-axis
    plt.ylabel('Power / kW')    # label y-axis

    plt.tight_layout()          # optimize placement
    plt.savefig(pngfile)        # create file for output
    plt.close()
    
##############################
def plotWind(dataWind, ymax):
       
    fwidth = 15                 # figure width in cm
    fwidth = fwidth / 2.54      # conversion inches to cm
    fheight = fwidth * 3/4		# using a ratio of 3/4 for height
    
    mx = len(dataWind) + 1
    x = range(1, mx, 1) # number of hours
    
    ###
    pngfile = 'ProdWind' + '.png'		# file name for output
    plt.subplots( figsize=( fwidth,fheight ) )

    y = dataWind
    plt.plot(x, y, label='Wind prod.', color='peru')	# line plot 
    

    plt.xlabel('Hours')           # label x-axis
    plt.ylabel('Power / kW')    # label y-axis
    
    plt.ylim(0,ymax)
    plt.legend(loc='upper right')
    plt.tight_layout()          # optimize placement
    plt.savefig(pngfile)        # create file for output
    plt.close()
    
##############################################
def writeCSV(dataHeat, dataTemp, dataPV, dataWind, myres):
    # write data (shown in plots) to separate *.csv file
    
    """ myres    
    [0] power for H2 generation / kWh
    [1] electricity to grid / kWh
    [2] charge in battery / kWh
    [3] heating demand from hydro / kWh (this is full demand minus available PV+wind)
    [4] produced H2 / kg
    [5] demand H2 / kg (heating)  -> this is the same as [3] just in kg
    [6] tank H2 stationary / kg
    [7] H2 filled in car / kg
    [8] H2 overproduction (cannot be stored) / kg
    [9] additional heat demand (storage empty) / kWh
    [10] Driving range of car / percent
    [11] Heating by stored hydrogen / kW
    [12] Heating by PV + wind / kW
    """
    
    mx = len(dataPV) + 1
    x = range(1, mx, 1) # number of hours
    
    myfile = 'PVpower' + '.csv'		# file name for output
    y = dataPV
    myout = open(myfile, 'w') 
    i = 0
    mytext = '# hours / PV power in kW \n'
    while i < len(x):
        mytext = mytext + '%.2f , %.2f \n' %(x[i], y[i])
        i = i + 1
    
    myout.write(mytext)
    myout.close()
    
    myfile = 'WindPower' + '.csv'		# file name for output
    y = dataWind
    myout = open(myfile, 'w') 
    i = 0
    mytext = '# hours / wind power in kW \n'
    while i < len(x):
        mytext = mytext + '%.2f , %.2f \n' %(x[i], y[i])
        i = i + 1
    
    myout.write(mytext)
    myout.close()
    
    myfile = 'EnergyToH2' + '.csv'		# file name for output
    y = myres[0]
    myout = open(myfile, 'w') 
    i = 0
    mytext = '# hours / energy to hydrogen in kWh \n'
    while i < len(x):
        mytext = mytext + '%.2f , %.2f \n' %(x[i], y[i])
        i = i + 1
    
    myout.write(mytext)
    myout.close()
    
    myfile = 'EnergyToGrid' + '.csv'		# file name for output
    y = myres[1]
    myout = open(myfile, 'w') 
    i = 0
    mytext = '# hours / energy to grid in kWh \n'
    while i < len(x):
        mytext = mytext + '%.2f , %.2f \n' %(x[i], y[i])
        i = i + 1
    
    myout.write(mytext)
    myout.close()
    
    myfile = 'Battery' + '.csv'		# file name for output
    y = myres[2]
    myout = open(myfile, 'w') 
    i = 0
    mytext = '# hours / Charge in battery in kWh \n'
    while i < len(x):
        mytext = mytext + '%.2f , %.2f \n' %(x[i], y[i])
        i = i + 1
    
    myout.write(mytext)
    myout.close()
    
    myfile = 'Tank' + '.csv'		# file name for output
    y = myres[6]
    myout = open(myfile, 'w') 
    i = 0
    mytext = '# hours / Hydrogen in stationary storage in kg \n'
    while i < len(x):
        mytext = mytext + '%.2f , %.2f \n' %(x[i], y[i])
        i = i + 1
    
    myout.write(mytext)
    myout.close()
    
    myfile = 'Car' + '.csv'		# file name for output
    y = myres[10]
    myout = open(myfile, 'w') 
    i = 0
    mytext = '# hours / Driving range of car in % \n'
    while i < len(x):
        mytext = mytext + '%.2f , %.2f \n' %(x[i], y[i])
        i = i + 1
    
    myout.write(mytext)
    myout.close()
    
    myfile = 'OwnHeat' + '.csv'
    myout = open(myfile, 'w') 
    
    i = 0
    mytext = '# hours / Temperature in °C / Heat demand in kWh / Heat from PV and wind in kWh / Heat from H2 combustion in kWh / Demand from external in kWh \n'
    a = dataTemp
    b = dataHeat
    c = myres[12]
    d = myres[11]
    e = myres[9]
    while i < len(x):
        mytext = mytext + '%.2f , %.2f , %.2f , %.2f , %.2f , %.2f \n' %(x[i], a[i], b[i], c[i], d[i], e[i])
        i = i + 1
    
    myout.write(mytext)
    myout.close()
    
#####################################################
##############################
def plotYear(dataPV, myres):
    
    hydro = myres[0]
    grid = myres[1]
    bat = myres[2]
    
    fwidth = 15                 # figure width in cm
    fwidth = fwidth / 2.54      # conversion inches to cm
    fheight = fwidth * 3/4		# using a ratio of 3/4 for height
    
    mx = len(dataPV) + 1
    x = range(1, mx, 1) # number of hours
    
    ###
    pngfile = 'EnergyToH2' + '.png'		# file name for output
    plt.subplots( figsize=( fwidth,fheight ) )

    y = dataPV
    plt.plot(x, y, label='PV prod.', color='orange')	# line plot 
    
    y = hydro
    plt.plot(x, y, label='H2', color='royalblue')	# line plot 

    plt.xlabel('Hours')           # label x-axis
    plt.ylabel('Power / kW')    # label y-axis
    
    #plt.ylim(0,z)

    plt.legend(loc='upper right')
    plt.tight_layout()          # optimize placement
    plt.savefig(pngfile)        # create file for output
    plt.close()
    
    ###
    pngfile = 'EnergyToGrid' + '.png'		# file name for output
    plt.subplots( figsize=( fwidth,fheight ) )

    y = dataPV
    plt.plot(x, y, label='PV prod.', color='orange')	# line plot 
        
    y = grid
    plt.plot(x, y, label='to grid', color='gray')	# line plot 

    plt.xlabel('Hours')           # label x-axis
    plt.ylabel('Power / kW')    # label y-axis

    plt.legend(loc='upper right')
    plt.tight_layout()          # optimize placement
    plt.savefig(pngfile)        # create file for output
    plt.close()
    
    ###
    pngfile = 'Battery' + '.png'		# file name for output
    plt.subplots( figsize=( fwidth,fheight ) )

    y = bat
    plt.plot(x, y, color='grey')	# line plot 
    #plt.ylim(0,100)

    plt.xlabel('Hours')           # label x-axis
    plt.ylabel('Power / kW')    # label y-axis

    plt.tight_layout()          # optimize placement
    plt.savefig(pngfile)        # create file for output
    plt.close()


#################################
##############################
def plotHeat(dataHeat, dataTemp, myres, myIn):
    """
    [9] additional heat demand (storage empty) / kWh
    [11] Heating by stored hydrogen / kW
    [12] Heating by PV + wind / kW
    """
    fwidth = 15                 # figure width in cm
    fwidth = fwidth / 2.54      # conversion inches to cm
    fheight = fwidth * 3/4		# using a ratio of 3/4 for height
    
    mx = len( myres[9] ) + 1
    x = range(1, mx, 1) # number of hours
    
    ###
    pngfile = 'ExHeat' + '.png'		# file name for output
    plt.subplots( figsize=( fwidth,fheight ) )

    y = myres[9]
    plt.plot(x, y, label='External heat demand', color='red')	# line plot 

    plt.xlabel('Hours')           # label x-axis
    plt.ylabel('Power / kW')    # label y-axis
    
    #plt.legend(loc='upper right')
    plt.tight_layout()          # optimize placement
    plt.savefig(pngfile)        # create file for output
    plt.close()
    
    ###
    pngfile = 'OwnHeat' + '.png'		# file name for output
    plt.subplots( figsize=( fwidth,fheight ) )
    
    #y = dataHeat
    #plt.plot(x, y, label='Overall heat demand', color='gray', alpha=0.5)

    y = myres[9]
    plt.plot(x, y, label='External heat demand', color='red')
    
    y = myres[12]
    plt.plot(x, y, label='PV + wind', color='orange') 
    
    y = myres[11]
    plt.plot(x, y, label='Hydrogen combustion', color='blue', alpha=0.5 )

    plt.xlabel('Hours')           # label x-axis
    plt.ylabel('Power / kW')    # label y-axis
    
    #plt.ylim(0,ymax)
    plt.legend(loc='upper right')
    plt.tight_layout()          # optimize placement
    plt.savefig(pngfile)        # create file for output
    plt.close()
    
    ###
    pngfile = 'OutTemp' + '.png'		# file name for output
    plt.subplots( figsize=( fwidth,fheight ) )

    y = dataTemp
    plt.plot(x, y, label='Temperature (outside)', color='peru')
    
    y = [ myIn['heating'][2] ] * len(x)         # temperature limit for heating
    plt.plot(x, y, color='gray', linestyle='--')
    
    #y = dataHeat
    #plt.plot(x, y, label='Overall heat demand', color='gray')

    plt.xlabel('Hours')           # label x-axis
    plt.ylabel('Temperature / °C')    # label y-axis
    
    #plt.ylim(0,ymax)
    #plt.legend(loc='upper right')
    plt.tight_layout()          # optimize placement
    plt.savefig(pngfile)        # create file for output
    plt.close()