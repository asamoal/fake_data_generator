# Fake Dataset Generator

This Python script generates a package of fake dataset files, each of a specific size, along with a manifest file that details the file names, sizes and creation dates. A checksum file is also generated which provides both MD5 and SHA256 checksums (in Hex and Base64 formats) for each file. All the files are put together into one or more directories, named as per the user specified patterns, forming a group of neat packages.

## Usage

You can run the script from the command line, specifying the number of files to generate, the size of each file and one or more naming patterns for the files.

Example:

```bash python3 data_generator.py --num_files 10 --size 10MB --pattern dataset dataset2 dataset3```

This command will generate three directories named 'dataset', 'dataset2', and 'dataset3', each containing 10 files of size 10MB, named `dataset_001.txt`, `dataset_002.txt`, etc. Each directory will also contain a `dataset_manifest.txt` file listing the details of all generated files and a `dataset_checksums.txt` file providing the MD5 and SHA256 checksums of each file.

If your terminal supports brace expansion (like Bash, Zsh, and similar shells), you can leverage this to specify multiple patterns easily. 

For example:
```bash python3 data_generator.py --num_files 10 --size 10MB --pattern $(echo dataset{1,2,3})```

This command will use brace expansion to generate three patterns: 'dataset1', 'dataset2', and 'dataset3'.

Arguments:
- `--num_files` - The number of files to generate
- `--size` - The size of each file, which could be specified in bytes, or with units KB, MB, GB (e.g. 1KB, 1MB, 1GB)
- `--pattern` - One or more naming patterns for the files

Arguments are required. If the script is run without any arguments or with incorrect arguments, it will display an error message along with the help message.

## Files generated
1. Dataset files: Contain randomly generated fake text data. Sizes are specific to what user has passed in the `--size` argument.
2. Manifest file: A TXT file listing all the files in the dataset, their sizes in human readable format (bytes, KB, MB, GB etc.), and creation dates. Named after the pattern provided. Only contains the file name, not the full path.
3. Checksum file: A TXT file containing the MD5 and SHA256 checksums (in Hex and Base64) of each file in the dataset. Only contains the file name, not the full path.

## Timing the File Creation

As of recent updates, the script now includes timers that measure the time taken to generate each individual file and the total duration for the script to generate all requested files. This can help with performance monitoring and optimization. 

The timing for the creation of each file is displayed as the file is created. Upon completion of all files, the script will display the total size of the generated data and the total time taken. 

Times are displayed in a human readable format, as milliseconds, seconds, minutes, hours, or days, depending on the magnitude of the duration. 

## Limitations

This script assumes that the user has appropriate permissions to write all these files to the current directory.