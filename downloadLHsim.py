import os
import requests

def download_file(url, save_path):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f"Download completed: {save_path}")
    else:
        print(f"Failed to download: {url}")

filenum = 686

if __name__ == "__main__":
    url = f"https://users.flatironinstitute.org/~camels/FOF_Subfind/IllustrisTNG/LH/LH_{filenum}/fof_subhalo_tab_033.hdf5"
    save_directory = "C:/CAMELS DATA"
    new_file_name = "LH686_fof_subhalo_tab_033.hdf5"  # Change this to the new desired name
    save_path = os.path.join(save_directory, new_file_name)

    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    download_file(url, save_path)

    url = f"https://users.flatironinstitute.org/~camels/Sims/IllustrisTNG/LH/LH_{filenum}/snap_033.hdf5"
    new_file_name = "LH686_snap_033IllustrisTNG.hdf5"  # Change this to the new desired name
    save_path = os.path.join(save_directory, new_file_name)

    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    download_file(url, save_path)

    print("done")





