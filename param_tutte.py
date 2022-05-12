def boundary_edges( faces ):
    """Récupère les arêtes du bord"""
    bdry_e= set()
    darts = {}
    for f in faces:
        for i in range( len(f) ):
            if ( f[i] in darts ):
                darts[ f[ i ] ].append( f[ (i+1)%len(f) ] )
            else:
                darts[ f[ i ] ] = [ f[ (i+1)%len(f) ] ]
    for i, i_list in darts.items():
        for j in i_list:
            j_list = darts[ j ]
            if ( not i in j_list ):
                bdry_e.add( (j,i) )
    return bdry_e