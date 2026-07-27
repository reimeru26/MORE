'''
    Reads template for HTML file.
    Adds text for results and writes results file.
    (File names are hard coded here.)
    
    Uwe Reimer, January 2025 / Campus Emden
'''

def writeHT(myIn, infile, outfile, a, grid,hyprod,hycon,pv,wi,ext, pvheat, hyheat):
    #global infile, outfile
    
    myin = open(infile, 'r')  # open a text file in read modus
    mf = myin.read()    # here, we read the entire file into one string 
    myin.close()
    # calculate heat demand -> decide if we need heating
    heatdem = myIn['heating'][0] * myIn['heating'][1]
    
    ### data from input

    mystat = '<b> Input data from <em>01_input.txt</em>: </b><br />' + '<br />'
    mystat = mystat + 'Size of PV system / kW: &emsp; %.2f <br />' %(myIn['system'][2])
    mystat = mystat + 'Size of wind turbine / kW: &nbsp; %.2f <br />' %(myIn['wind'][1])
    mystat = mystat + ' <br />'
    mystat = mystat + 'Size of electrolyser / kW: &emsp; %.2f <br />' %(myIn['system'][3])
    mystat = mystat + 'Size of battery / kWh: &emsp; &emsp; %.2f <br />' %(myIn['system'][4])
    mystat = mystat + 'Size of compressor / kW: &emsp; %.2f <br />' %(myIn['system'][5])
    mystat = mystat + 'Size of H<sub>2</sub> storage / kg: &emsp; %.2f <br />' %(myIn['system'][6])
    mystat = mystat + ' <br />'
    
    if heatdem > 0.0 :
        mystat = mystat + 'Heat demand of building / kWh / m2: &emsp; %.2f <br />' %(myIn['heating'][1])
        mystat = mystat + 'Area for heating / m2: &emsp; %.2f <br />' %(myIn['heating'][0])
        mystat = mystat + ' <br />'
    
    mystat = mystat + 'Data for PV production from file: &emsp; %s <br />' %(myIn['system'][0])
    mystat = mystat + 'H<sub>2</sub> car fueling per week from file: &emsp; %s <br />' %(myIn['system'][1])
    
    ### Sums per year
    mytext = '<b> Sums per year: </b><br />'
    
    sumenergy = pv + wi
    mytext = mytext + 'Electricity from PV / kWh: &emsp; %.2f &emsp; ( %.0f %% ) <br />' %(pv, (100.0 * pv/sumenergy) )
    mytext = mytext + 'Electricity from wind / kWh: &nbsp; %.2f &emsp; ( %.0f %% ) <br />' %(wi, (100.0 * wi/sumenergy) )
    mytext = mytext + 'Electricity to grid / kWh: &emsp; &emsp; %.2f &emsp; ( %.0f %% ) <br />' %(grid, (100.0 * grid/sumenergy) )
    mytext = mytext + 'Produced H<sub>2</sub> / kg: &emsp; &emsp; &emsp; %.2f <br />' %(hyprod)
    mytext = mytext + 'Consumed H<sub>2</sub> / kg: &emsp; &emsp; &emsp; %.2f <br />' %(hycon)
    
    ### Summary heating 
    
    if heatdem > 0.0 :
        mytext = mytext + '<br /><b> Summary heating per year: </b><br />'
        mytext = mytext + 'Heating from H<sub>2</sub> / kWh: &emsp; &emsp; &emsp; &emsp; &emsp; &emsp; %.2f &emsp; ( %.0f %% ) <br />' %(hyheat, 100.0*hyheat/heatdem)
        mytext = mytext + 'Heating from PV + wind / kWh: &emsp; &emsp; &emsp; &emsp; %.2f &emsp; ( %.0f %% ) <br />' %(pvheat, 100.0*pvheat/heatdem)
        mytext = mytext + 'External electricity demand heating / kWh:  &emsp; %.2f &emsp; ( %.0f %% ) <br />' %(ext, 100.0*ext/heatdem)

    ### Costs per year 
    
    mytext = mytext + '<br /><b> Costs per year: </b><br />'
    mytext = mytext + 'Electricity from PV / EUR/kWh: &emsp; %.2f <br />' %(a[0])
    mytext = mytext + 'Electricity from wind / EUR/kWh: &nbsp; %.2f <br />' %(a[3])
    mytext = mytext + 'Hydrogen prod. / EUR/kWh: &emsp; &emsp; %.2f &emsp; ( %.2f EUR/kg ) <br />' %( a[1] / myIn['operation'][3], a[1] )   # HHV for hydrogen
    mytext = mytext + 'Hydrogen storage / EUR/kWh: &emsp; %.2f &emsp; ( %.2f EUR/kg ) <br />' %( a[2] / myIn['operation'][3] , a[2] )
    mytext = mytext + 'Hydrogen total / EUR/kWh : &emsp; &emsp; %.2f &emsp; ( %.2f EUR/kg ) <br />' %(  ( ( a[1] + a[2] ) / myIn['operation'][3] ) , ( a[1] + a[2] ) )
    
    ### Environmental impact
    
    mytext = mytext + '<br /><b> Environmental impact per year: </b><br />'
    mytext = mytext + 'Water consumption for electrolysis / m3: &emsp; %.2f <br />' %( myIn['environment'][2] * hyprod )
    mytext = mytext + 'CO<sub>2</sub> avoided (based on crude oil) / tons: &emsp; %.2f <br />' %( myIn['environment'][1] * (pv + wi) / 1000.0 )
    mytext = mytext + 'CO<sub>2</sub> avoided (based on natural gas) / tons: &emsp; %.2f <br />' %( myIn['environment'][0] * (pv + wi) / 1000.0 )

    a = mf.split('####')
    nt = a[0] + mystat + a[1] + mytext + a[2]
    
    myout = open(outfile, 'w')
    myout.write(nt)
    myout.close
    
    return 0