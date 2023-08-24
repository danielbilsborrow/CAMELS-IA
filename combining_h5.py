import h5py

# List of input HDF5 files to be combined
begin = 100
end=150
input_files = ['../CAMELS/correlation_funcs/IllustrisLH_corfuncs.h5']
for i in range(18):
    input_files.append(f'../CAMELS/correlation_funcs/IllustrisLH{begin}-{end}_corfuncs.h5')
    begin+=50
    end+=50

# Output HDF5 file (the combined file)
output_file = '../CAMELS/correlation_funcs/all_IllustrisLH_corfuncs.h5'

# Create the output HDF5 file
with h5py.File(output_file, 'w') as out_f:
    for input_file in input_files:
        with h5py.File(input_file, 'r') as in_f:
            for dataset_name in in_f:
                in_dataset = in_f[dataset_name]
                # Copy the dataset from the input file to the output file
                out_dataset = out_f.create_dataset(dataset_name, data=in_dataset)

print(f"Combined HDF5 files into '{output_file}'.")







