'''

This gives the specs for a brilliant pebbles cluster required to knock out land based solid icbms
It can also be used to model solid Sub-based missiles by multiplying by the ssbn factor
'''

# Python standard libraries
# AWP libraries
import brilliant_pebbles
import numpy as np

from brilliant_pebbles.python_tools.Spacecraft import Spacecraft as SC
import brilliant_pebbles.python_tools.orbit_calculations as oc
from brilliant_pebbles.python_tools.planetary_data import earth
import brilliant_pebbles.python_tools.plotting_tools as pt
import brilliant_pebbles.python_tools.bp_tools as bpt

PEBBLES_ALTITUDE=400 #km
INTERCEPT_ALTITUDE = 180 #km 300 for ss-18 180 for topol
INTERCEPT_TIME = 180# seconds time from first firing to intercept. 300for SS-18. 180 for topol
SOLID_BURN_TIME = 10#seconds
LIQUID_BURN_TIME = 45#seconds
SOLID_ISP = 250
LIQUID_ISP = 250

MASS0 = 300 #all up
MASS1 = 100 #solid exhausted
MASS2 = 50 #post sep
MASS3 = 3.5 # liquid exhausted

THRUST_DIRECTION_GRID = np.linspace(-1,1,10) #increments to apply thrust vector over
INCLINATION = 70 #inclination of the cluster

S1_MASS_BURN_RATE = (MASS1-MASS0)/SOLID_BURN_TIME #kg/s 2.1 for 45s burn at 250s isp
S2_MASS_BURN_RATE = (MASS3-MASS2)/LIQUID_BURN_TIME

SSBM_INTERVAL = 14 #interval between missile launches for an SSBM. from op Behemoth
S1_THRUST = abs(S1_MASS_BURN_RATE * 9.81 *SOLID_ISP)
S2_THRUST = abs(S2_MASS_BURN_RATE * 9.81 *SOLID_ISP)

THRUST_VECTOR = [-1,0,0]

final_bp_states = np.empty(shape=(1,3))

if __name__ == '__main__':
    
	
	start_coes = [ earth[ 'radius' ] + PEBBLES_ALTITUDE, 0.00, 0.0, 0.0, 0.0, 0.0 ] #TLE
	thrust_direction1 = np.array(THRUST_VECTOR)
	thrust_direction1 = thrust_direction1/sum(abs(thrust_direction1)) #normalise direction
	thrust_direction1 = thrust_direction1 * S1_THRUST
	
	#stage 1 burn
	sc   = SC(
			{
			'coes'       : start_coes,
			'tspan'      : SOLID_BURN_TIME, 
			'dt'         : 1,
			'orbit_perts': { 'J2': True },
			'thrust': S1_THRUST,
			'thrust_duration': SOLID_BURN_TIME,
			'thrust_direction': thrust_direction1,
			'mass_burn_rate': S1_MASS_BURN_RATE,
			'mass0': MASS0,
			'disable_deorbit': True
			} )
	sc.plot_3d()


	post_burn_state1 = sc.states[-1][0:6].tolist() #dont care about mass anymore
	
	thrust_direction2 = np.array(THRUST_VECTOR)
	thrust_direction2 = thrust_direction2/sum(abs(thrust_direction2)) #normalise direction
	thrust_direction2 = thrust_direction2 * S2_THRUST

	#stage 2 burn
	sc2   = SC(
			{
			'orbit_state': post_burn_state1,
			'tspan'      : LIQUID_BURN_TIME, 
			'dt'         : 1,
			'orbit_perts': { 'J2': True },
			'thrust': S2_THRUST,
			'thrust_duration': LIQUID_BURN_TIME,
			'thrust_direction': thrust_direction2,
			'mass_burn_rate': S2_MASS_BURN_RATE,
			'mass0': MASS2,
			'disable_deorbit': True
			} )
	sc2.plot_3d()

	post_burn_state2 = sc2.states[-1][0:6].tolist()

	sc3 = SC(
			{
			'orbit_state': post_burn_state2,
			'tspan'      : INTERCEPT_TIME - SOLID_BURN_TIME - LIQUID_BURN_TIME, 
			'dt'         : 1,
			'orbit_perts': { 'J2': True },
			'disable_deorbit': True
			} )
	sc3.plot_3d()
	final_bp_states = np.append(final_bp_states,[sc3.states[-1][0:3]], axis=0)