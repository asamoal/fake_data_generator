# Fake Dataset Generator

This Python script generates a package of fake dataset files, each of a specific size, along with a manifest file that details the file names, sizes and creation dates. A checksum file is also generated which provides both MD5 and SHA256 checksums (in Hex and Base64 formats) for each file. All the files are put together into a single directory, named as per the user specified pattern, forming a neat package.

## Usage

You can run the script from the command line, specifying the number of files to generate, the size of each file and a naming pattern for the files. 

Example:

```bash python3 generate_files.py --num_files 10 --size 10MB --pattern dataset```

This command will generate a directory named 'dataset' containing 10 files of 1MB each, named `dataset_001.txt`, `dataset_002.txt`, etc. The directory will also contain a `dataset_manifest.txt` file listing the details of all generated files and a `dataset_checksums.txt` file providing the MD5 and SHA256 checksums of each file.

Arguments:
- `--num_files` - The number of files to generate
- `--size` - The size of each file, which could be specified in bytes, or with units KB, MB, GB (e.g. 1KB, 1MB, 1GB)
- `--pattern` - The naming pattern for the files

## Files generated
1. Dataset files: Contain randomly generated fake text data.
2. Manifest file: A TXT file listing all the files in the dataset, their sizes, and creation dates. Named after the pattern provided.
3. Checksum file: A TXT file containing the MD5 and SHA256 checksums (in Hex and Base64) of each file in the dataset.

## Limitations

This script does not perform error checking, and assumes that the user has appropriate permissions to write all these files to the current directory. Additionally, it uses very simple methods of generating dummy file contents and computing checksums.