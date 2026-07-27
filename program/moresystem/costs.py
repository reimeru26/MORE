"""
    Calculate the costs per year.

    Uwe Reimer, January 2025 / Campus Emden
    
    [0] power for H2 generation / kWh
    [1] electricity to grid / kWh
    [2] charge in battery / kWh
    [3] produced H2 / kg
"""
def calcCost(myIn, hyprod, pv,wi):        
    # cost of electricity from PV  
    
    size = myIn['system'][2]
    if size > 0.0:
        #                PV invest                             PV operation
        coe = size * ( myIn['CAPEX'][0] +  myIn['CAPEX'][0] * myIn['OPEX'][0] )
        coe = coe / pv
    else:
        coe = 0.0
    
    size = myIn['wind'][1]
    if size > 0.0:
        #                wind invest                             wind operation
        cow = size * ( myIn['CAPEX'][6] +  myIn['CAPEX'][6] * myIn['OPEX'][6] )
        cow = cow / wi
    else:
        cow = 0.0
    
    # cost of H2 production includes electrolyser, battery and compressor
    if hyprod > 0.0:
        sizeel = myIn['system'][3]
        sizebat = myIn['system'][4]
        sizeco = myIn['system'][5]
        #
        coh = sizeel * (myIn['CAPEX'][1] + myIn['CAPEX'][1] * myIn['OPEX'][1] ) 
        coh = coh + sizebat * ( myIn['CAPEX'][2] + myIn['CAPEX'][2] * myIn['OPEX'][2] )
        coh = coh + sizeco * ( myIn['CAPEX'][4] + myIn['CAPEX'][4] * myIn['OPEX'][4] )
        coh = coh / hyprod      # hyprod is in kg
        # you need to pay electricity for H2
        if cow > 0.0:
            mysum = pv + wi
            coh = coh + (pv / mysum) * coe + (wi / mysum) * cow # if there is windpower, costs are related to total electricity
        else:
            coh = coh + coe  # only pv power
        
        # cost for H2 storage includes only tank
        sizeta = myIn['system'][6]
        cos = sizeta * ( myIn['CAPEX'][5] + myIn['CAPEX'][5] * myIn['OPEX'][5] )
        cos = cos / hyprod         # hyprod is in kg
        
    else :
        coh = 0.0
        cos = 0.0
    
    mycosts = []
    mycosts.append(coe) # cost of electr PV in EUR/kWh
    mycosts.append(coh) # cost of hydrogen in EUR/kg
    mycosts.append(cos) # cost of H2 storage in EUR/kg
    mycosts.append(cow) # cost of electr wind in EUR/kWh
    
    return mycosts