import os
import paramiko
import pickle

# Cluster SSH connection details
cluster_hostname = 'splinter-login.star.ucl.ac.uk'
cluster_username = 'zcapdjl'
cluster_password = 'game751722'  

# Remote directory containing pkl files on the cluster
remote_directory = '/share/data1/zcapdjl/CAMELS/ellipticity_measurements/'

# Local directory to save extracted data
local_extracted_directory = 'C:\CAMELS DATA\ellipticities_LHsim'

# Create SSH client
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# Connect to the cluster
ssh.connect(cluster_hostname, username=cluster_username, password=cluster_password)

# List files in the remote directory
stdin, stdout, stderr = ssh.exec_command(f'ls {remote_directory}')
remote_files = stdout.read().decode().split()

i=0# Extract and save data from each pkl file
for remote_file in remote_files:
    if remote_file.endswith('.pkl'):
        remote_path = os.path.join(remote_directory, remote_file)
        print(remote_path)
        # Download the pkl file
        sftp = ssh.open_sftp()
        local_path = os.path.join('C:\CAMELS DATA', remote_file)
        sftp.get(remote_path, local_path)
        sftp.close()
        
        # Load and extract data from the pkl file
        with open(local_path, 'rb') as f:
            data = pickle.load(f)
            ellipticities = data['ellipticities']
            posg = data['posg']
            
            # Save ellipticities and posg to local_extracted_directory
            extracted_filename = os.path.splitext(remote_file)[0] + '_extracted.pkl'
            extracted_path = os.path.join(local_extracted_directory, extracted_filename)
            
            with open(extracted_path, 'wb') as extracted_file:
                extracted_data = {'ellipticities': ellipticities, 'posg': posg}
                pickle.dump(extracted_data, extracted_file)
        
        # Remove the downloaded pkl file
        os.remove(local_path)
        print("LH:",i)
        i+=1

# Disconnect from the cluster
ssh.close()






