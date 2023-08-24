import numpy as np
import pickle
import treecorr
import time
import h5py
import gc


def slicer(array, num_slices=15, ell_dict=None, ell=False):
    '''Slices positions of particles in a box perpendicular to the axes x, y and z.
    array has shape (N,3)
    (If ell=True we also slice the 2D ellipticity of the particle with index corresponding to index in position array)
    Returns a dictionary (or two) with each section containing positions of that slice (and the correlsponding 
    ellipticities for that axis)'''
    box_length = 25.0  # Length of the 3D box
    pos_index = 0
    slice_size = box_length / num_slices  # Size of each slice along the z-axis
    # Initialize an empty dictionary to store the particle positions for each slice
    sliced_positions = {}
    sliced_ell = {}
    
    # Initialize the dictionary with empty arrays for each slice along each axis
    for axis in ['x', 'y', 'z']:
        sliced_positions[axis] = {i: [] for i in range(num_slices)}
        if ell == True:
            sliced_ell[axis] = {i: [] for i in range(num_slices)}   
    
    # Iterate over each particle position
    for position in array:
        # Calculate the index of the slice based on the x, y, and z coordinates
        x_slice_index = int(position[0] // slice_size)
        y_slice_index = int(position[1] // slice_size)
        z_slice_index = int(position[2] // slice_size)

        # Append the position to the corresponding slice's array for each axis
        sliced_positions['x'][x_slice_index].append(position)
        sliced_positions['y'][y_slice_index].append(position)
        sliced_positions['z'][z_slice_index].append(position)    
        
        if ell==True:
            sliced_ell['x'][x_slice_index].append(ell_dict['x'][pos_index])
            sliced_ell['y'][y_slice_index].append(ell_dict['y'][pos_index])
            sliced_ell['z'][z_slice_index].append(ell_dict['z'][pos_index])
            pos_index+=1
        

    # Convert the lists to numpy arrays
    for axis in ['x', 'y', 'z']:
        for slice_index in sliced_positions[axis]:
            sliced_positions[axis][slice_index] = np.array(sliced_positions[axis][slice_index])
            if ell==True: 
                sliced_ell[axis][slice_index] = np.array(sliced_ell[axis][slice_index])


    # Print the positions for each slice along each axis
#     for axis in ['x', 'y', 'z']:
#         print(f"Slices along {axis}-axis:")
#         for slice_index in sliced_positions[axis]:
#             print(f"Slice {slice_index}:", sliced_positions[axis][slice_index].shape)

    if ell==True:
        return sliced_positions, sliced_ell
    else:
        return sliced_positions

####################
#filenum = 12
for filenum in range(100,150):
    # Load dictionaries from the pickled file
    try:
        with open(f'../CAMELS/ellipticity_measurements/LH{filenum}_ellipticities.pkl', 'rb') as f:
            data = pickle.load(f)
            pos_g = data['posg']
            e_glxys = data['ellipticities']
            pos_dm = data['dm_den']

        ####################
        # SLICING

        sliced_g, sliced_ell = slicer(pos_g, num_slices=15, ell_dict=e_glxys, ell=True) # slicing galaxies

        sliced_dm = slicer(pos_dm, num_slices=15) # slicing dark matter



        ##################

        xyz = [['x',1,2,0],['y',2,0,1],['z',0,1,2]]
        nbins = 8
        aggregate_corr_ng = []
        aggregate_corr_ngvar = []
        i=0
        for axis in range(3):
            _ax_ = xyz[axis][0] # which axis is perpendicular to the slice
            h = xyz[axis][1] # horizontal axis
            v = xyz[axis][2] # vertical axis
            for _slice_ in range(15):
                t1 = time.time()

                cat1 = treecorr.Catalog(x=sliced_dm[_ax_][_slice_][:,h], y=sliced_dm[_ax_][_slice_][:,v])
                cat2 = treecorr.Catalog(x=sliced_g[_ax_][_slice_][:,h], y=sliced_g[_ax_][_slice_][:,v],
                                                g1=sliced_ell[_ax_][_slice_].real, g2=sliced_ell[_ax_][_slice_].imag)# two shear values (g1, g2)
                ng = treecorr.NGCorrelation(min_sep=0.1, max_sep=25,bin_type='Log', nbins=nbins, var_method='jackknife',metric='Periodic',xperiod=25,yperiod=25)
                t2 = time.time()
                ng.process_cross(cat1,cat2)
                varg = treecorr.calculateVarG(cat2)
                ng.finalize(varg)
                aggregate_corr_ng.append(ng.xi)
                aggregate_corr_ngvar.append(varg)
                t3 = time.time()
                #print(f'axis {_ax_} slice {_slice_} Time:',t3-t2,"+",t2-t1)
                r=ng.rnom
                del cat1,cat2,ng
                gc.collect()


        ############################

        # Create an HDF5 file (or open if it exists)
        with h5py.File('../CAMELS/correlation_funcs/IllustrisLH100-150_corfuncs.h5', 'a') as hf:
            # Create datasets for simulation 1 arrays
            hf.create_dataset(f'simulation{filenum}/corrfunc', data=aggregate_corr_ng)
            hf.create_dataset(f'simulation{filenum}/corrvar', data=aggregate_corr_ngvar)

            if filenum ==0:
                hf.create_dataset(f'simulation{filenum}/bins', data=r)

        print("done number:", filenum)
    except:
        print("missed:", filenum)



