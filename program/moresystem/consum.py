'''
    Consumption of hydrogen (in a wide sense)
    Functions in this file:
    
    * calcYear(myIn, w, offset, years)
    - input is fueling data 8consumption) for one week (7 days)
    - creates a load profile for hydrogen consumption at the resultion of one hour for the entire simulation time
    
    * calcRange(w, myres)
    - Calculate 'driving range'; actually shows how much the tank of the car could be filled (in percent)
    
    * hydrogenTank(hmass, dataCar, myIn, myres)
    - input is produced hydrogen (per hour)
    - distributes H2 to stationary tank and car -> detect overproduction (no storage capacity)
    
    Uwe Reimer, January 2025 / Campus Emden
'''

def calcYear(w, offset, years):
    # this is for fueling of a hydrogen car
    # we have seven days - we need a full year, one year has 52-53 weeks
    w = w * 53 * years
    d = w[offset:] # this is days
    
    #now, create hours
    hours = []
    for day in d:
        
        x = 1
        while x < 8:    
            hours.append(0.0)
            x = x + 1
        
        hours.append(day)   # -> fueling (in kg) at 09:00
        
        while x < 24:    
            hours.append(0.0)
            x = x + 1
    
    #print(len(hours))
    return hours
############################
def calcRange(myres, dataCar):
    # calculate driving range as indication for tank status in car    
    # myres[7] -> contains only filling events (status THIS IS)
    # dataCar  -> contains filling plan (status SHOULD BE)
    myrange = []
    r = 0.0
    a = 0
    while a < len(myres[7]):
        
        if dataCar[a] > 0.0:
            r = 100.0 * myres[7][a] / dataCar[a]
            
        myrange.append(r)
        a = a + 1
        
    myres.append(myrange)
    return None

############################
def hydrogenTank(dataCar, myIn, myres):
    tank = []   # hydrogen tank stationary
    car = []    # car tank 
    diff = []   # H2 overproduction (cannot be stored)
    hdemand = []    # heat demand that cannot be delivered by H2 (empty storage)
    maxStore = myIn['system'][6]
    stor = 0.0  # tank stationary
    onefill = 0.0 # car tank 
    
    hmass = myres[4] # produced H2 by electrolysis / kg
    hcon = myres[5]  # demand H2 by heating / kg
    
    a = 0
    while a < len(hmass):
        
        if hcon[a] > 0.0:   # if heating, then no H2 production
                stor = stor - hcon[a]        # burning H2 from tank
        else:
            stor = stor + hmass[a]       # H2 production to tank
            
        
        if stor < 0.0:
            e = stor * (-1.0)               # mass H2 in kg (which would be needed additionally)
            e = e * myIn['operation'][3]    # equivalent heat from combustion H2
            hdemand.append(e)               # additional demand in kWh
            stor = 0.0
        else:
            hdemand.append(0.0)
            
        onefill = 0.0
        if dataCar[a] > 0.0:         # car fueling
            if stor == 0.0:             # is empty, no filling
                onefill = 0.0
            elif stor < dataCar[a]:
                onefill = stor
            else:
                onefill = dataCar[a]
            
            stor = stor - onefill
        
        #### 3) check capacity (overproduction)
        mydiff = 0.0
        if stor > maxStore:        
            mydiff = stor - maxStore
        stor = stor - mydiff
                
        car.append(onefill)
        tank.append(stor)
        diff.append(mydiff)
        
        a = a + 1
       
    myres.append(tank)
    myres.append(car)
    myres.append(diff)
    myres.append(hdemand)
    
    return None
    
###################################
############################
def hydrogenTankOld1(dataCar, myIn, myres):
    tank = []   # hydrogen tank stationary
    car = []    # car tank 
    diff = []   # H2 overproduction (cannot be stored)
    hdemand = []    # heat demand that cannot be delivered by H2 (empty storage)
    maxStore = myIn['system'][6]
    stor = 0.0  # tank stationary
    onefill = 0.0 # car tank 
    
    hmass = myres[4] # produced H2 by electrolysis
    hcon = myres[5]  # consumed H2 by heating
    
    a = 0
    while a < len(hmass):
        stor = stor + hmass[a]       # 1) H2 production
        stor = stor - hcon[a]        # heating
        if stor < 0.0:
            e = stor * (-1.0)               # mass H2 in kg
            e = e * myIn['operation'][3]    # equivalent heat from combustion H2
            hdemand.append(e)
            stor = 0.0
        else:
            hdemand.append(0.0)
            
        if dataCar[a] > 0.0:         # 2) fueling
            if stor == 0.0:             # is empty, no filling
                onefill = 0.0
            elif stor < dataCar[a]:
                onefill = stor
            else:
                onefill = dataCar[a]
            
            stor = stor - onefill
        
        mydiff = 0.0
        if stor > maxStore:        # 3) check capacity (overproduction)
            mydiff = stor - maxStore
        stor = stor - mydiff
                
        car.append(onefill)
        tank.append(stor)
        diff.append(mydiff)
        
        a = a + 1
       
    myres.append(tank)
    myres.append(car)
    myres.append(diff)
    myres.append(hdemand)
    
    return None
##################################
def heatDemand(dataTemp, myIn, years):
    # Calculate heat demand per hour
    m = myIn['heating'][0]       # m2 area for heating
    heatyear = myIn['heating'][1] # kWh / m2
    tlim = myIn['heating'][2]
    tnorm = myIn['heating'][3]    
    
    heat = []   # heat demand
    dt = []     # temp difference inside / outside
    sumt = 0.0
    for a in dataTemp:
        if a < tlim:
            b = tnorm - a
            dt.append(b)
            sumt = sumt + b
        else:
            dt.append(0.0)
        
    # heat coefficient 
    k = ( heatyear * years * m ) / sumt
    
    for a in dt:
        b = k * a
        heat.append(b)
    
    return heat   # heat demand in kW
##################################
def heatOld(dataTemp):
    ### Heizlast lineare Regression / kW
    reg_m = -1.0898
    reg_null = 15.258

    ## Heizbedarf bei Nachtabsenkung
    # Hier: 6:00 bis 18:00 Uhr normal / ab 19:00 bis 5:00 Uhr auf 80% abgesenkt
    #ab = 0.8
    #n = 1.0 
    #senk_profil = [ab, ab, ab, ab, ab, n, n, n, n, n, n, n, n, n, n, n, n, n, ab, ab, ab , ab, ab , ab ]
    #senk = senk_profil * 365 # Jahresprofil
    

    # Heizbedarf
    heat = []
    #h_senk = []

    hour = 0
    for t in dataTemp:
        
        h = 0.0
        if t < 13.9:
            h = t * reg_m + reg_null
            
        if hour > 3792 and hour < 6000:       # Heizperiode nicht Juni - August  /  3792 - 6000
            h = 0.0
        
        heat.append(h)
        #h_senk.append( h * senk[hour] )
        
        hour = hour + 1
        
    """
    m = 0.0
    for a in heat:
        m = m + a
    
    s = 0.0
    for a in h_senk:
        s = s + a
    
    print("Wärmebedarf   :       ", m)
    print("Wärmebedarf abges.  : ", s)
    """
    
    return heat   # heat demand in kW
    
############
def tankRealOld1(dataCar, hycar):
    # dataCar = plan of fueling (from file) / kg
    # hycar = hydrogen incar -> myres[7] H2 in car / kg (this is how much is actually filled in)
    
    car = []
    a = 0
    while a < len(hycar):
        c = 0.0
        if dataCar[a] > 0: # planned filling
            c = hycar[a]   # real filling
        car.append(c)
        a = a + 1
        
    return car