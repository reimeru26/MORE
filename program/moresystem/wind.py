"""
This file contains functions for the program 'wind-year.py'.
    * read(): reads data from a *.cvs file (PVGIS website)
    * calc_wpower(): calculates power output based on a wind profile 
        - Logarithmic wind profile
        - power curve equation
    * calc_wpower2(): calculates power output based on a wind profile 
        - Power Law for wind profile (Hellman Equation)
        - power curve equation
        
Uwe Reimer, HS Emden/Leer, April 2025
"""
import math

###########################################################################################
def calc_wpowerEmden(wspeed):
    """
    This is a fitted model for ENERCON E-18 which is operated presently at the university of applied science Emden-Leer at Emden, Germany.
    *power Law*
    Calcultate wind power based on speed and power curve
    
    Input = wind speed at 10 meters
    height = target height
    r = surface roughness
    
    Part1: calculate wind speed at target height
    see https://wind-data.ch/tools/profile.php?lng=en
        
    Part2: Calculate power from power curve
    function needs to be fitted or provided for each type
    see https://www.wind-turbine-models.com/turbines/353-enercon-e-18
    """
    height = 36.0  # wind power target height in m
    r = 0.13   # surface roughness length (wrough)
    #znull = 0.016   # surface roughness exponent
    
    newspeed = []
    for s in wspeed:
        a = height / 10.0
        ns = s * math.pow( a, r )
        newspeed.append(ns)
        
    wpower = []
    for s in newspeed:
        p = 0.09 * math.pow( s, 2.82 )  # wind power curve
        if p > 80.0: p = 80.0       # correction for high wind speed, the equation is only good until 10 m/s (sets max. power)
        if s > 20.0: p = 0.0        # this is max speed, the turbine is shut down
        wpower.append(p)
        
    return wpower
    
###########################################################################################
###########################################################################################
def calc_wpowerFlex(wspeed, height, nompower, nomspeed, von, voff):
    """
    Generic wind model:
    1) calculates wind speed from PVGIS data (at 10 m) to target height with power law
    2) Calculates power generation based on generic power curve
    
    !!! Attention !!!
    This is a rough estimation. The power curve tends to overestimate power at low wind speed.
    In reality the power output depends not only on wind speed, but also direction - especially
    for small devices at hub height < 100 m.
    
    Well, better than nothing ;-)
    Gives a reasonable estimation for the overall production at the resolution of one hour.
  
    """
    r = 0.13   # surface roughness length for urban area (more or less)

    # calculate wind speed at hub height
    newspeed = [] 
    for s in wspeed:
        a = height / 10.0
        ns = s * math.pow( a, r )
        newspeed.append(ns)
        
    wpower = []
    for s in newspeed:
        p = 0.1 * math.pow( s, 3.0 )  # wind power curve (actually for ENERCON E-18, replace by other curve if possible)
        p = nompower * p / 80.0     # recalc power
        if p > nompower: p = nompower       # set max. power
        if s >= voff: p = 0.0       # this is max speed, the turbine is shut down
        if s < von: p = 0.0         # this is min speed
        wpower.append(p)
        
    return wpower