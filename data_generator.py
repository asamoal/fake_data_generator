import hashlib
import argparse
import os
import shutil
import base64
import sys
import time
import datetime
from faker import Faker


class CustomArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)


def parse_size(size_str):
    # default to bytes if no unit is provided
    units = {'KB': 1024, 'MB': 1024 * 1024, 'GB': 1024 * 1024 * 1024}
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


def human_time_span(time_span):
    parts = datetime.timedelta(milliseconds=time_span)
    if parts < datetime.timedelta(seconds=1):
        return str(parts.total_seconds() * 1000) + " milliseconds"
    elif parts < datetime.timedelta(minutes=5):
        return str(parts.total_seconds()) + " seconds"
    elif parts < datetime.timedelta(hours=1):
        return str(parts.total_seconds() // 60) + " minutes"
    elif parts < datetime.timedelta(days=1):
        return str(parts.total_seconds() // 3600) + " hours"
    else:
        return str(parts.total_seconds() // 86400) + " days"


def convert_bytes(num):
    """
    this function will convert bytes to MB.... GB... etc
    """
    step_unit = 1000.0  # 1024 bad the size

    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < step_unit:
            return "%3.1f %s" % (num, x)
        num /= step_unit


def generate_files(num_files, file_size, name_pattern):
    print("""
     __  __    __    ___             __  __             
     \ \/ /__ / /_  / _ | ___  ___  / /_/ /  ___ ____   
      \  / -_) __/ / __ |/ _ \/ _ \/ __/ _ \/ -_) __/   
      /_/\__/\__/_/_/ |_/_//_/\___/\__/_//_/\__/_/      
      / __/__ _/ /_____                                 
     / _// _ `/  '_/ -_)                                
    /_/__\_,_/_/\_\\__/                                 
      / _ \___ _/ /____ _                               
     / // / _ `/ __/ _ `/                               
    /____/\_,_/\__/\_,_/         __                     
     / ___/__ ___  ___ _______ _/ /____  ____           
    / (_ / -_) _ \/ -_) __/ _ `/ __/ _ \/ __/           
    \___/\__/_//_/\__/_/  \_,_/\__/\___/_/              
    """)

    fake = Faker()

    manifest_file = ""
    checksum_file = ""
    manifest = []
    checksums = {}

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
        os.makedirs(name_pattern, exist_ok=True)

    total_start_time = time.time() * 1000
    total_size = 0

    print(f"Generating for pattern: {pattern}")
    for i in range(1, num_files + 1):
        single_start_time = time.time() * 1000

        file_name = os.path.join(name_pattern, f"{name_pattern}-{i:03}.txt")
        manifest_file = os.path.join(name_pattern, f"{name_pattern}_manifest.txt")
        checksum_file = os.path.join(name_pattern, f"{name_pattern}_checksums.txt")

        data = fake.text(file_size)[:file_size]

        with open(file_name, 'w') as f:
            f.write(data)
            manifest.append(file_name)

        total_size += os.path.getsize(file_name)

        with open(file_name, 'rb'):
            checksums[file_name] = {
                'md5': compute_checksum(file_name, 'md5'),
                'sha256': compute_checksum(file_name, 'sha256')
            }

        single_end_time = time.time() * 1000
        print(f"Time taken to create file-{i}: {human_time_span(single_end_time - single_start_time)}")

    with open(manifest_file, 'w') as f:
        for file_name in manifest:
            size = convert_bytes(os.path.getsize(file_name))  # use convert_bytes here
            creation_date = datetime.datetime.utcfromtimestamp(os.path.getctime(file_name)).isoformat() + 'Z'
            f.write(f'{os.path.basename(file_name)},{size},{creation_date}\n')

    with open(checksum_file, 'w') as f:
        for filename, checksum_values in checksums.items():
            f.write(
                f'{os.path.basename(filename)},{checksum_values["md5"][0]},{checksum_values["md5"][1]},'
                f'{checksum_values["sha256"][0]},{checksum_values["sha256"][1]}\n')

    total_end_time = time.time() * 1000
    print(f"Generated {num_files} files of {convert_bytes(file_size)} each, "  # use convert_bytes here
          f"with names following the pattern {name_pattern}.")
    print(f"Total size: {convert_bytes(total_size)}")
    print(f"Total time taken: {human_time_span(total_end_time - total_start_time)}\n")


# Set up argument parser
parser = CustomArgumentParser()
parser.add_argument("-n", "--num_files", type=int, help="number of files to generate")
parser.add_argument("-s", "--size", type=str, help="size of each file in KB, MB or GB")
parser.add_argument("-p", "--pattern", type=str, nargs='+', help="name pattern for the files")

# Parse arguments
args = parser.parse_args()

# it also makes sense to check if the expected arguments are actually provided
expected_args = [args.num_files, args.size, args.pattern]
if not all(expected_args):
    parser.error("Unexpected set of arguments, please provide --num_files, --size, and --pattern.")

# Call function
size_in_bytes = parse_size(args.size)
for pattern in args.pattern:
    generate_files(args.num_files, size_in_bytes, pattern)