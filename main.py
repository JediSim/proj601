import numpy as np
import polyscope as ps
import pywavefront

scene = pywavefront.Wavefront('monkey.obj', collect_faces=True)

ps.init()

vertices = np.array(scene.vertices) # (V,3) vertex position array

faces = np.array(scene.mesh_list[0].faces) # (F,3) array of indices     
                                                # for triangular faces

print(f"{faces[0]=}")
print([vertices[faces[0][i]] for i in range(3)])
exit()

# Pour chaque face
#   pour chaque autre face
#       on compte le nombre de face ayant 2 vertex en commun avec le triangle actuel
#       si le nombre de face est < 3, on chercher quelle vertex ne sont utiliser qu'une seul fois

ps_mesh = ps.register_surface_mesh("my mesh", vertices, faces)

ps_mesh.set_enabled(False) # disable
ps_mesh.set_enabled() # default is true

ps_mesh.set_color((0.3, 0.6, 0.8)) # rgb triple on [0,1]
ps_mesh.set_edge_color((0.8, 0.8, 0.8)) 
ps_mesh.set_edge_width(1.0)
ps_mesh.set_smooth_shade(True)
ps_mesh.set_material("candy")
ps_mesh.set_transparency(0.5)

param_corner = np.random.rand(ps_mesh.n_corners(),2)
cA = (0.1, 0.2, 0.3)
cB = (0.4, 0.5, 0.6)
ps_mesh.add_parameterization_quantity("rand param corner3", param_corner, defined_on='corners',
                                       coords_type='unit', viz_style='grid', grid_colors=(cA, cB))

# alternately:
ps.register_surface_mesh("my mesh2", vertices, faces, enabled=False, 
                         color=(1., 0., 0.), edge_color=((0.8, 0.8, 0.8)),
                         edge_width=1.0, smooth_shade=True,
                         material='candy', transparency=0.5)

ps.show()

# Pour tutte il faut trouver les sommets qui sont au bord.
# polyscope permte peut etre de le faire
# sinon il faut regarder dans les faces. Les bords qui apparaisse une seul fois sont des bords.

