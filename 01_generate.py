from ase import *
from ase.io import *
import os
import numpy as np
from ase.visualize import view
from ase.constraints import *
from dlePy.strucmod import rotate_group

loc = '/home/theodoros/PROJ_ElectroCat/theodoros/energy_paths/potential_dependence/NoCation/'

init= loc + 'CONF519/chg_-1.4/target_potential/CONTCAR'
final= loc + 'CONF520/chg_-1.4/target_potential/CONTCAR'


def move_cell( system, dir = 0, limit = 0.85 ):
    scale=system.get_scaled_positions()
    for i in range(len(init_sys)-1,-1,-1):
        if scale[i,dir] > limit:
            scale[i,dir] = 1-scale[i,dir]

    system.set_scaled_positions(scale)
    return system

def move_atom( system, at, dir, d ):
    scale=system.get_scaled_positions()

    for i in range( len( at ) ):
        scale[ at[ i ], dir[ i ]] = scale[at[ i ],dir[ i ]] + d[ i ]

    system.set_scaled_positions(scale)
    return system

init_sys=read(init,format='vasp')
final_sys=read(final,format='vasp')

'''
# This part may be used if the images are not well generated
#init_sys =  move_cell( init_sys, 1, 0.99 )
#init_sys =  move_cell( init_sys, 0, 0.99 )

init_sys =  move_atom( init_sys, [ 0, 2, 36, 38, 39, 3, 36, 0 ], 
                                 [ 0, 0, 0,  0,  1,  1,  1, 1 ],
                                 [-1,-1,-1, -1, -1, -1, -1,-1 ] )

final_sys =  move_atom( final_sys, [ 0, 1, 2, 36, 37, 38, 36, 39, 42, 0, 6, 3 ], 
                                   [ 0, 0, 0,  0,  0,  0, 1,  1,   1, 1, 1, 1 ],  
                                   [-1, -1,-1,-1, -1, -1, -1, -1, -1, -1, -1, -1 ] )
'''

NPTS=7

sysref=read(init,format='vasp')


image=[init_sys]
for i in range(0,NPTS):
    system=read(init,format='vasp')
    for iat in range(len(system)):
        dx=(final_sys.positions[iat,:]-init_sys.positions[iat,:])/float(NPTS-1)
        system.positions[iat,:]=init_sys.positions[iat,:]+dx[:]*i
    #Fix C-O bondlength if they are not the same as typical value
    if i>0 and i < NPTS-1:
        if  system.get_distance( 96, 97 ) < 0.978:
            system.set_distance( 96, 97, 0.978, fix = 0 )
    if i> 0:
        image.append(system)
    write('POSCAR.'+str(i),system,format='vasp',direct=True)
view(image)
write('POSCAR.traj',image,format='traj')
