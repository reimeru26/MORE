'''
    Calculate power for H2 production / loop over hours
    Functions in this file:
    
    * energy(dataPV, myIn)
    - input is energy production by photovoltaics
    - calculates energy distribution to battery, electrolyser and grid
    
    * hydrogenMass(hypower, myIn)
    - converts kWh into kg hydrogen
    
    * recalcEnergy(myres, myIn)
    - Limited storage: not all hydrogen may be stored if tank is full
    - in that case the electrolyser is shut down and energy is delivered to the grid
    
    Uwe Reimer, January 2025 / Campus Emden
'''

########################################
def hydrogenMass(hypower, myIn):
    ''' Calculate H2 production in kg
    '''
    ed = myIn['operation'][2]   # kWh / kg H2
    h = [] # produced hydrogen in kg
    
    for a in hypower:
        b = a / ed
        h.append(b)
        
    return h
    
########################################
def hydrogenMassConsum(hypower, myIn):
    ''' Calculate H2 consumption in kg
    '''
    ed = myIn['operation'][3]   # kWh / kg H2 - higher heating value
    h = [] # produced hydrogen in kg
    
    for a in hypower:
        b = a / ed
        h.append(b)
        
    return h

########################################
def recalcEnergy(myres, myIn):
    """
    Correction for limited storage: if tank is full then no electrolysis
    (This has been calculated in the previous step.)
    Now, the follwoing data needs to be updated for shutdown of electrolyser.
    
    [0] power for H2 generation / kWh
    [1] electricity to grid / kWh
    [4] produced H2 / kg
    [8] H2 overproduction (cannot be stored)
    """
    ed = myIn['operation'][2]   # kWh / kg H2
    
    x = 0
    while x < len(myres[4]):
        m = myres[8][x]     # this is to much / should not be produced
        
        if m > 0.0:
            e = m * ed      # this is the equivalent in kWh
            
            myres[4][x] = myres[4][x] - m
            myres[0][x] = myres[0][x] - e
            myres[1][x] = myres[1][x] + e
            
        x = x + 1
    
########################################
def energyHeating(dataPV, dataHeat, myIn):
    ''' Calculate power for H2 production based on a fixed size of electrolyser
        and fixed size of battery
        
        Energy is distributed betwen HEATING, H2 Prod. and GRID.
        Energy for heating is either from PV + wind (preferred) or stored hydrogen.
        If Heating is ON, then no electrolysis.
    '''
    elyse = myIn['system'][3]   # size of electrolyser in kW
    bat = myIn['system'][4]     # battery size in kWh
    elim = elyse * myIn['operation'][0] # limit -> only operate elyse above this value    
    batlim = bat * myIn['operation'][1] # limit for discharge
    
    hydro = []      # H2 production in kWh
    rest = []       # remaining electricity going to base load or grid
    cbat = []       # charge in battery / kWh
    burnhydro = []  # heat demand for H2 consumption in kWh
    
    ebat = 0.0      # power in battery, start with empty battery
    
    hour = 0
    while hour < len(dataPV):
        strom = dataPV[hour]
        heat = dataHeat[hour]
        hour = hour + 1
    
        egrid = 0.0     # power to grid
        ehydro = 0.0    # power for H2 generation 
        hyheat = 0.0    # heat from H2 consumption
        
        if heat > 0.0:  ### no electrolysis if heat demand
            
            if strom < heat:   # heat with el. and H2 from storage
                hyheat = heat - strom   # remaining energy for heating comes from storage
                egrid = 0.0         
                                     
            else:               # heat only with el.
                strom = strom - heat
                
                b = bat - ebat      # check battery
                if b > 0:      # charge battery
                    ebat = ebat + b
                    egrid = strom - b
                else:
                    egrid = strom
        
        ######################################
        else:           ### no heating -> H2 production is an option
            egrid = 0.0     # power to grid
            ehydro = 0.0    # power for H2 generation

            if strom >= elim:   # H2 production
                
                if strom <= elyse:   # alles in H2
                    ehydro = strom
                    egrid = 0.0
                    
                    if ebat > batlim:   # use power of battery
                        a = ebat - batlim   # max power from bat 
                        b = elyse - ehydro  # remaining capacity of elyse
                        c = a - b
                        if c <= 0.0:        # all in elyse, bat will be empty
                            ehydro = ehydro + a
                            ebat = batlim
                        else:               # part of bat goes to elyse
                            ehydro = ehydro + b
                            ebat = ebat - b
                
                else:               # strom > elyse
                    ehydro = elyse    # full load elyse
                    b = strom - elyse   # remaining electricity
                    
                    if ebat == bat:     # battery is full
                        egrid = b
                    else:               # charge battery
                        a = bat - ebat      # this is how much bat can take
                        c = b - a
                        if c > 0.0:
                            egrid = c
                            ebat = bat
                        else:
                            ebat = ebat + b     # partial loading bat
                            egrid = 0.0
                                     
            else:               # low power from PV
                b = strom + ebat - batlim       # this is how much power is available
                
                if b >= elim:       # if above lim for elyse -> use also power from bat
                    c = elyse - b       # this is how much elyse can take
                    if c > 0.0:         # all in elyse
                        ehydro = b
                        ebat = batlim
                    else:           # too much power, battery only partial discharge 
                        ehydro = elyse
                        ebat = ebat + strom - elyse
                        
                else:           # only charge bat
                    ehydro = 0.0
                    if ebat < bat:
                        ebat = ebat + strom
                    else:
                        egrid = strom
            
        ### collect data for output
        hydro.append(ehydro)        # power for H2 generation
        rest.append(egrid)          # collect remaining electricity
        cbat.append(ebat)           # collect charge in battery 
        burnhydro.append(hyheat)    # collect H2 consumption

    myres = []   # list for results
    myres.append(hydro)
    myres.append(rest)
    myres.append(cbat)
    myres.append(burnhydro)
    
    return myres

########################################
