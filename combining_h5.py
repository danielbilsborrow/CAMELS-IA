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
# Open the output file in write mode
with h5py.File(output_file, 'w') as out_file:
    for input_file in input_files:
        # Open each input file in read mode
        with h5py.File(input_file, 'r') as in_file:
            # Iterate through datasets in the input file
            for dataset_name in in_file:
                try:
                    # Copy dataset from the input file to the output file
                    in_file.copy(dataset_name, out_file)
                except:
                    print("skipped",dataset_name)

print(f"Combined HDF5 files into '{output_file}'.")







