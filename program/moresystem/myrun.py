'''
Requires the following files:
    - 01_input.txt / general input data 
    - 02_RunSystem.bat / batch file to run the program on a Windows system
    - results are shown in the HTML page 03_results.html (which is generated)
    - template.html (template page for results)
    
    - *.csv file from PVGIS website for PV production and wind at the given location
    - fuel-week.txt / fueling schedule for hydrogen cars (kg H2 per day)
    
    PYTHON program files:
    consum.py costs.py H2system.py myrun.py plotResults.py readInput.py solar.py wind.py writeHTML.py

    
    Uwe Reimer, January 2026
    University of Applied Sciences Emden/ Germany
'''
import math
import readInput, H2system, plotResults, writeHTML
import costs, consum, wind

### directories and files
indir = 'moresystem/'     # sub directory for python files
tempfile = indir + 'template.html'
htmlfile = '03_results.html'

### read input data
myIn = readInput.readIn('01_input.txt')
infile = indir + myIn['system'][0]
dataAll = readInput.readInPVGIS(infile)    # PV data is for 1 kW system, power is in W
wspeed = dataAll[1]
dataTemp = dataAll[2]

# PVGIS data is for 1 kW system -> recalculate for real PV size
sizePV = myIn['system'][2]  # size of PV system in kW
dataPV = []
for a in dataAll[0]:
    dataPV.append(sizePV * a / 1000.0)

### read wind data and calculate wind power
if myIn['wind'][1] > 0.0:
    height = myIn['wind'][0]
    nompower = myIn['wind'][1]
    nomspeed = myIn['wind'][2]
    von = myIn['wind'][3]
    voff = myIn['wind'][4]
    dataWind = wind.calc_wpowerFlex(wspeed, height, nompower, nomspeed, von, voff)

### prepare fueling of car
infile = indir + myIn['system'][1]
w = readInput.readInFuel(infile) # returns one week
offset = myIn['system'][7] # starting day for the year / year 2010 starts with a Friday 
offset = int(offset) # needs to be integer
y = len(dataPV)/ (365 * 24) # this is how many years we have
years = int(y) # just for safety
dataCar = consum.calcYear(w, offset, years) # fueling of car 

### heat demand of building
infile = indir + myIn['system'][0]
dataHeat = consum.heatDemand(dataTemp, myIn, years)      # heat demand of building

### Calculate power distribution: H2 / battery / grid
if myIn['wind'][1] > 0.0:       # if there is PV + wind available
    dataPVW = []
    x = 0
    while x < len(dataPV):
        a = dataPV[x] + dataWind[x]     # sum energy production
        dataPVW.append(a)
        x = x + 1
    myres = H2system.energyHeating(dataPVW, dataHeat, myIn)
    
else:              # only PV available
    myres = H2system.energyHeating(dataPV, dataHeat, myIn)

"""
[0] power for H2 generation / kWh
[1] electricity to grid / kWh
[2] charge in battery / kWh
[3] heating demand from hydro / kWh (this is full demand minus available PV+wind)
"""
a = H2system.hydrogenMass(myres[0], myIn)
myres.append(a)
a = H2system.hydrogenMassConsum(myres[3], myIn)
myres.append(a)
"""
[4] produced H2 / kg
[5] demand H2 / kg (heating)  -> this is the same as [3] just in kg
"""

## distribute H2 to car and tank
consum.hydrogenTank(dataCar, myIn, myres)
"""
[6] tank H2 stationary / kg
[7] H2 filled in car / kg
[8] H2 overproduction (cannot be stored) / kg
[9] additional heat demand (storage empty) / kWh
"""

## correction for limited storage / if tank full then no electrolysis
H2system.recalcEnergy(myres, myIn)

## calculate driving range (how much is car available?)
consum.calcRange(myres, dataCar)
"""
[10] Driving range of car / percent
"""

### Calculate separate contributions to heating
ownhy = []    # heat from hydrogen combustion
ownel = []    # heat electric PV + wind
    
a = 0
while a < len( myres[3] ):
    b = myres[3][a] - myres[9][a]      # heat demand from hydro - external demand
    ownhy.append(b)
    
    b = dataHeat[a] - myres[3][a]      # full heat demand - heat demand from hydro (this is what is provided directly by PV + wind)
    ownel.append(b)
    
    a = a + 1
    
myres.append(ownhy)
myres.append(ownel)
"""
[11] Heating by stored hydrogen / kW
[12] Heating by PV + wind / kW
"""

### Plotting of results

# if no wind generation, we need empty data structure
if int( myIn['wind'][1] ) == 0:
    dataWind = []
    for a in dataPV:
        dataWind.append(0.0)
        
# first check, if we should exclude the first year (e.g. for heating, H2 is generated in summer)
a = int(myIn['data'][1])    # just for safety
if a > 0:
    a = a * 365 * 24
    del dataPV[:a]
    del dataWind[:a]
    del dataTemp[:a]
    del dataHeat[:a]
    
    i = 0
    while i < 13:
        del myres[i][:a]
        i = i + 1
        
# calculate max limit for plotting
ymax = 0.0
for a in dataWind:
    if a > ymax: ymax = a
for a in dataPV:
    if a > ymax: ymax = a
ymax = math.ceil( ymax / 10.0 ) * 10.0

plotResults.plotMain(dataPV, dataWind, myres, ymax)
plotResults.plotStat(myres, myIn)
plotResults.plotHeat(dataHeat, dataTemp, myres, myIn)

### calculate yearly sums for HTML page
grid = 0.0
hyprod = 0.0
hycon = 0.0
pv = 0.0
wi = 0.0
ext = 0.0
pvheat = 0.0
hyheat = 0.0
for a in dataPV:  # power from photovoltaics / kWh
    pv = pv + a
for a in dataWind:  # power from wind / kWh
    wi = wi + a
    
for a in myres[1]:  # electricity to grid / kWh
    grid = grid + a
    
for a in myres[4]:  # produced H2 / kg
    hyprod = hyprod + a
   
for a in myres[11]:  # Heating by stored hydrogen / kW
    hycon = hycon + ( a / myIn['operation'][3] )
    hyheat = hyheat + a

for a in myres[7]:   # consumed H2 car / kg
    hycon = hycon + a
    
for a in myres[9]:  # heating external 
    ext = ext + a
   
for a in myres[12]:  # Heating by PV + wind / kW
    pvheat = pvheat + a

## calc per year
years = years - int(myIn['data'][1]) 
grid = grid / years   # electricity to grid / kWh
hyprod = hyprod / years  # produced H2 / kg
hycon = hycon /years
pv = pv / years
wi = wi / years
ext = ext / years
pvheat = pvheat / years
hyheat = hyheat / years

a = costs.calcCost(myIn, hyprod,pv,wi)
writeHTML.writeHT(myIn, tempfile, htmlfile, a,grid,hyprod, hycon,pv,wi, ext, pvheat, hyheat)

### Data Export (numbers in *.csv file for plotting, additional analysis, ...)
if myIn['data'][0] > 0.0:
    plotResults.writeCSV(dataHeat, dataTemp, dataPV, dataWind, myres)
    