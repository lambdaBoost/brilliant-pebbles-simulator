'''

This gives the specs for a brilliant pebbles cluster required to knock out land based icbms
It also gives the margin needed to increase the cluster by for protection against SSBMs
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
INTERCEPT_ALTITUDE = 300 #km 300 for ss-18 180 for topol
INTERCEPT_TIME = 300# seconds time from first firing to intercept. 300for SS-18. 180 for topol
BURN_TIME = 45#seconds
ISP = 250

THRUST_DIRECTION_GRID = np.linspace(-1,1,10) #increments to apply thrust vector over
INCLINATION = 70 #inclination of the cluster
INITIAL_MASS = 50
FINAL_MASS = 3.5
MASS_BURN_RATE = (INITIAL_MASS-FINAL_MASS)/BURN_TIME #kg/s 2.1 for 45s burn at 250s isp

SSBM_INTERVAL = 14 #interval between missile launches for an SSBM. from op Behemoth
THRUST = MASS_BURN_RATE * 9.81 *ISP

final_bp_states = np.empty(shape=(1,3))

if __name__ == '__main__':
    
	for i in THRUST_DIRECTION_GRID:
		for j in THRUST_DIRECTION_GRID:
			for k in THRUST_DIRECTION_GRID:
				start_coes = [ earth[ 'radius' ] + PEBBLES_ALTITUDE, 0.00, 0.0, 0.0, 0.0, 0.0 ] #TLE
				thrust_direction = np.array([i,j,k])
				thrust_direction = thrust_direction/sum(abs(thrust_direction)) #normalise direction
				thrust_direction = thrust_direction * THRUST
				sc   = SC(
						{
						'coes'       : start_coes,
						'tspan'      : BURN_TIME, 
						'dt'         : 1,
						'orbit_perts': { 'J2': True },
						'thrust': THRUST,
						'thrust_duration': BURN_TIME,
						'thrust_direction': thrust_direction,
						'mass_burn_rate': MASS_BURN_RATE,
						'mass0': INITIAL_MASS
						} )
				#sc.plot_3d()
			

				post_burn_state = sc.states[-1][0:6].tolist() #dont care about mass anymore
				#post_burn_coes = oc.state2coes(post_burn_state)
				sc2 = SC(
						{
						'orbit_state': post_burn_state,
						'tspan'      : INTERCEPT_TIME - BURN_TIME, 
						'dt'         : 1,
						'orbit_perts': { 'J2': True }
						} )
				#sc2.plot_3d()
				final_bp_states = np.append(final_bp_states,[sc2.states[-1][0:3]], axis=0)
    
	final_bp_states = final_bp_states[1:]
	pt.plot_point_cloud(final_bp_states, args={'azimuth'    : 0, 'elevation':30})
 
	intercept_envelope = bpt.get_intercept_radius(final_bp_states, INTERCEPT_ALTITUDE)
	pt.plot_circle_3d(intercept_envelope['center'], 
                   intercept_envelope['normal'],
                   intercept_envelope['radius'],
                   num_points=36)
 
	cluster_requirements = bpt.get_cluster_requirements(intercept_envelope['radius'], INCLINATION, SSBM_INTERVAL)