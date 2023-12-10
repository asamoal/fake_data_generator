import hashlib
import argparse
import os
import shutil
import base64
import datetime
from faker import Faker

def parse_size(size_str):
    # default to bytes if no unit is provided
    units = {'KB': 1024, 'MB': 1024*1024, 'GB': 1024*1024*1024}
    size_str = size_str.upper()
    if size_str[-2:] in units:
        return int(size_str[:-2]) * units[size_str[-2:]]
    else:  # Default is bytes
        return int(size_str)

def compute_checksum(file_name, algorithm):
    with open(file_name, 'rb') as f:
        if algorithm == 'md5':
            checksum = hashlib.md5()
        elif algorithm == 'sha256':
            checksum = hashlib.sha256()
        for chunk in iter(lambda: f.read(4096), b''):
            checksum.update(chunk)
    return checksum.hexdigest(), base64.b64encode(checksum.digest()).decode()


def generate_files(num_files, file_size, name_pattern):
    fake = Faker()


    manifest_file = ""
    checksum_file = ""
    manifest = []
    checksums = {}

    # Check if directory exists
    if os.path.isdir(name_pattern):
        # Remove all files in directory
        for filename in os.listdir(name_pattern):
            file_path = os.path.join(name_pattern, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f'Failed to delete {file_path}. Reason: {e}')
    else:
        # If directory does not exist, create it
        os.makedirs(name_pattern, exist_ok=True)

    for i in range(1, num_files + 1):
        file_name = os.path.join(name_pattern, f"{name_pattern}-{i:03}.txt")
        manifest_file = os.path.join(name_pattern, f"{name_pattern}_manifest.txt")
        checksum_file = os.path.join(name_pattern, f"{name_pattern}_checksums.txt")

        # Generate fake data
        data = fake.text(file_size)[:file_size]

        with open(file_name, 'w') as f:
            f.write(data)
            manifest.append(file_name)

        with open(file_name, 'rb'):
            checksums[file_name] = {
                'md5': compute_checksum(file_name, 'md5'),
                'sha256': compute_checksum(file_name, 'sha256')
            }

    with open(manifest_file, 'w') as f:
        f.write('FileName,FileSize,CreationDate\n')
        for file_name in manifest:
            size = os.path.getsize(file_name)
            creation_date = datetime.datetime.utcfromtimestamp(os.path.getctime(file_name)).isoformat() + 'Z'
            f.write(f'{file_name},{size},{creation_date}\n')

    with open(checksum_file, 'w') as f:
        f.write('FileName,MD5,MD5_Base64,SHA256,SHA256_Base64\n')
        for filename, checksum_values in checksums.items():
            f.write(
                f'{filename},{checksum_values["md5"][0]},{checksum_values["md5"][1]},{checksum_values["sha256"][0]},{checksum_values["sha256"][1]}\n')

    print(f"Generated {num_files} files of {file_size} bytes each, "
          f"with names following the pattern {name_pattern}.")


# Set up argument parser
parser = argparse.ArgumentParser()
parser.add_argument("-n", "--num_files", type=int, help="number of files to generate")
parser.add_argument("-s", "--size", type=str, help="size of each file in KB, MB or GB")
parser.add_argument("-p", "--pattern", type=str, help="name pattern for the files")

# Parse arguments
args = parser.parse_args()

# Call function
size_in_bytes = parse_size(args.size)
generate_files(args.num_files, size_in_bytes, args.pattern)
