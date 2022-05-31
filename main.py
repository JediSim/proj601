import numpy as np
import polyscope as ps
from wavefront import *
from param_tutte import *
from scipy.linalg import solve

#scene = load_obj('monkey.obj', 'monkey.mtl')
scene = load_obj('test.obj')
edges_border = scene.numpy_boundary_edges()

vertices_border = list(scene.boundary_vertices())

vertices = scene.only_coordinates()

faces = scene.only_faces()

# ========================================================================================== creation ps_mesh
L = make_laplacian(vertices, faces)
print(L)

b = np.zeros((L.shape[0],1))

print("edges_border : ",vertices_border)

L2, b2 = fix_bord(L, vertices_border,b)

print("L2 : ",L2)
print("b2 : ",b2)

x = solve(L2.toarray(), b2)
print("x : ",x)
# exit(0)

ps.init()

ps_mesh = ps.register_surface_mesh("my mesh", vertices, faces)

ps_mesh.set_enabled()  # default is true

ps_mesh.set_color((0.3, 0.6, 0.8))  # rgb triple on [0,1]
ps_mesh.set_edge_color((0.8, 0.8, 0.8))
ps_mesh.set_edge_width(1.0)
ps_mesh.set_smooth_shade(True)
# ps_mesh.set_material("wax")
# ps_mesh.set_transparency(0.5)


ps_mesh.add_parameterization_quantity("rand param corner", np.array(x), defined_on='corners')
# alternately:
ps.register_surface_mesh("my mesh2", vertices, faces, enabled=False,
                         color=(1., 0., 0.), edge_color=((0.8, 0.8, 0.8)),
                         edge_width=1.0, smooth_shade=True,
                         material='candy')

border = ps.register_curve_network(
    "boundary", scene.only_coordinates(), edges_border)
border.set_color((0.8, 0.8, 0.3))

ps.show()

# ========================================================================================== creation ps_mesh


# Pour tutte il faut trouver les sommets qui sont au bord.
# polyscope permte peut etre de le faire
# sinon il faut regarder dans les faces. Les bords qui apparaisse une seul fois sont des bords.

# on construit le laplacien
# les bords sont a fixer sur le bord d'une forme convexe (ex: un cercle).
# pour les fixer (les vertex du bord) on met un 1 dans la diag, des 0 dans le reste de la ligne,
# dans le vecteur b (L'u=b) on met la position dans le cercle (ex: un angle de rotation sur le bord du cercle)
# on fait la resolution du systeme pour obtenir les resultats.
