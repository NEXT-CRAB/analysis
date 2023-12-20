# This module is meant to simplify and collect some common steps used for visualization
import numpy


def slice_and_pack_data(tpx_data, drift_scale=1.0, min_time=None, max_time=None,  
                        shift_to_min=False, normalize_xy = True):
    
    if min_time is None:
        min_time = tpx_data['TOA'].min()

    if max_time is None:
        max_time = tpx_data['TOA'].max()

    # Slice the data:
    this_slice = tpx_data.time_slice(min_time, max_time)

    # Render the slice into x/y/z:
    if normalize_xy:
        x = this_slice['x'] / 256. - 0.5
        y = this_slice['y'] / 256. - 0.5
    else:
        x = this_slice['x']
        y = this_slice['y']

    t = this_slice['TOA'] - min_time
    if shift_to_min:
        t = t - numpy.min(t)
    t = t*drift_scale

    xyz = numpy.stack([x,y,t], axis=-1)
    z = this_slice['TOT']

    return xyz, z


box_template = numpy.array([[ 0 , 0, 0],
                            [ 1 , 0, 0],
                            [ 1 , 1, 0],
                            [ 0 , 1, 0],
                            [ 0 , 0, 1],
                            [ 1 , 0, 1],
                            [ 1 , 1, 1],
                            [ 0 , 1, 1]],
                            dtype=float)
box_template = box_template - 0.5





faces_template = numpy.array([[0, 1, 2],
                            [0, 2, 3],
                            [0, 1, 4],
                            [1, 5, 4],
                            [1, 2, 5],
                            [2, 5, 6],
                            [2, 3, 6],
                            [3, 6, 7],
                            [0, 3, 7],
                            [0, 4, 7],
                            [4, 5, 7],
                            [5, 6, 7]])

def convert_xyz_to_cubes(xyz, z, cmap):

    n_voxels = len(xyz)

    verts = numpy.zeros((n_voxels*8,3))
    faces = numpy.zeros((n_voxels*12,3), dtype=numpy.int32)
    colors = numpy.zeros((n_voxels*12,4))


    for i, point in enumerate(xyz):
        verts[8*i:8*(i+1),:] = makeBox(point, size=1./256)
        faces[12*i:12*(i+1)] = faces_template + 8*i

        color = cmap(z[i])

        colors[12*i:12*(i+1),:] = color

    return verts, faces, colors

def makeBox(centroid, size):
    verts_box = numpy.copy(box_template)

    #Scale all the points of the box to the right voxel size:
    verts_box *= size

    #Move the points to the right coordinate in this space
    verts_box += centroid

    return verts_box