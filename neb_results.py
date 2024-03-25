from ase.io import read
from dlePy.vasp.getdata import get_energy
import os
import numpy as np
import sys

def get_neb_data( outcar ):
    with open( outcar, 'r' ) as f:
        lines = f.readlines()
    d1    = None
    d2    = None
    angle = None
    force = None
    count = 0
    data = {}
    for i in range( len( lines ) ):
        if 'FORCES: max atom, RMS' in lines[ i ]:
            count += 1
            force = float( lines[ i ].split()[ 4 ] )
            for j in range( 10000 ):
                if 'NEB: distance' in lines[ i - j ]:
                    [d1, d2, angle] = [ float(x ) for x in lines[ i - j ].split()[ 8:11 ] ]
                if 'energy  without entropy' in lines[ i - j ]:
                    energy = float( lines[ i -j ].split()[ 6 ] )
                    break
            data[ count ] = { 'energy': energy, 'd1': d1, 'd2':d2, 'angle':angle, 'maxforce': force }
    if count == 0:
        energy = get_energy( outcar )
        data[ count ] = { 'energy': energy, 'd1': d1, 'd2':d2, 'angle':angle, 'maxforce': force }

    return data

def print_data( Iter ):
    is_data = get_neb_data(  '00/OUTCAR' )
    data_01 = get_neb_data( '01/OUTCAR' )
    Niter = np.max( np.array( [ x for x in data_01.keys() ] ) )
    if Iter != None and Iter > Niter:
        print( 'ERROR: Max iteration # is ' + str( Niter ) )
        exit()
    if Iter == None:
        Iter = Niter

    images = sorted( [ x for x in os.listdir( './' ) if os.path.isfile( x + '/POSCAR' ) ] )

    print( '' )
    print ( 'TOTAL NUMBER OF ITERATIONS: ', Niter ) 
    print ( 'NEB DATA FOR ITERATION    : ', Iter ) 
    print ( "==========================================================================" )
    print ( "%5s %12s %12s %12s %12s %12s" %('IMAGE', 'ENERGY', 'D PRV', 'D NEXT', 'ANGLE', 'MAXFORCE' ) )
    print ( "==========================================================================" )
    for image in images:
        data_ = get_neb_data( image + '/OUTCAR' )
        try:
            data = data_[ Iter ]
        except:
            data = data_[ 0 ]
        try:
            print( "%5s %12s %12s %12s %12s %12s" %( 
            image, str( round( data[ 'energy' ] - is_data[ 0 ][ 'energy' ], 4 ) ), 
            str( round( data[ 'd1' ],4) ), str( round( data[ 'd2' ], 4 )) , 
            str( round( data[ 'angle' ], 4 ) ), str( round( data[ 'maxforce' ],4 ) ) ) )
        except:
            print( "%5s %12s %12s %12s %12s %12s" %(
            image, str( round( data[ 'energy' ] - is_data[ 0 ][ 'energy' ], 3 ) ),
            str( data[ 'd1' ] ), str( data[ 'd2' ] ) ,
            str( data[ 'angle' ] ), str( data[ 'maxforce' ] ) ) )
    print ( "==========================================================================" )




if __name__ == "__main__":
    print( 'ANALIZING NEB CALCULATION' )
    if len( sys.argv ) > 1:
        Iter = int ( sys.argv[ 1 ] )
    else:
        print( 'Syntax: python ' + sys.argv[ 0 ] + ' [Iter] ' )
        Iter = None
    print_data( Iter )
