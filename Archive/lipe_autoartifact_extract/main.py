# Importing the modules needed
from fastapi import FastAPI, Response
import os
import shutil
import time  # Just for debugging usage
import subprocess
import re
import asyncio

# Create a basic FatsAPI endpoint that takes in the name
# of a forensics image file and then process that file.

# Create a basic FastAPI application
app = FastAPI()

# Create a single endpoint called ingest-image


@app.get('/ingest-image')
# The codes below are based on the test code in the Jupyter notebook.
async def ingestImage():
    # Some global variables
    fs_offsets = []

    # Set some paths as const so we can reuse them
    folder_image = 'image/'
    folder_cache = 'cache/'
    folder_output = 'output/'
    mmlsoutputpath = os.path.join(folder_cache, 'mmls_output.txt')
    image_path = os.path.join(folder_image, "Slade-B1-hda.img")

    # Get the partion information of the raw disk
    # os.chdir(folder_image)
    with open(mmlsoutputpath, 'w') as f:
        subprocess.run(["mmls", image_path], stdout=f, text=True)
        f.close()

    # Find the offset of the partition containing NTFS filesystem
    # os.chdir(folder_extracted)

    with open(mmlsoutputpath, 'r') as f:
        # Create a subset of the data of interest
        lines = f.readlines()[6:]
        # CLose the file as the working data is now residing in memory.
        f.close()

        for line in lines:
            # Do regex to find partitions containing NTFS file system
            if(re.search(r'\bNTFS\b', line)):
                offset = re.search(r'\d{10}', line.strip()).group()
                # Add the offset to a list that we can reference in the next step
                fs_offsets.append(offset)

    fls_outputs = []

    for offset in fs_offsets:
        # Create an output file for each partition
        fls_output = 'fls_output_'+offset+'.txt'
        fls_outputs.append(fls_output)
        with open(os.path.join(folder_cache, fls_output), 'w') as f:
            # Get a list of items in the root of the partition.
            f.write(offset)
            subprocess.run(["fls", "-l", "-p", "-o", offset,
                           "-r", image_path], stdout=f, text=True)
            f.close()

    # Using the partition's root listing, find location(inode) of files of interest
    # Array of dictionary to hold name : inode of file(s) of interests
    partition_file_inodes = []

    # Crete custom regex objects for each files we wish to search for
    regex_mft = re.compile(r'\s(\$MFT)\b')
    regex_sam = re.compile(r'\b(Windows/System32/config/SAM\s)\b')
    regex_system = re.compile(r'\b(Windows/System32/config/SYSTEM\s)\b')
    regex_security_evtx = re.compile(r'\b(Security\.evtx)\b')
    regex_system_evtx = re.compile(r'\b(System\.evtx)\b')
    regex_application_evtx = re.compile(r'\b(Application\.evtx)\b')
    regex_usnjrnl_j = re.compile(r'\$UsnJrnl\:\$J\b')
    regex_secure_sds = re.compile(r'\$Secure\:\$SDS\b')
    regex_inode = re.compile(r'(\d+-\d+-\d+)')
    regex_amcache = re.compile(r'(\d+-\d+-\d+)')

    for fls_output in fls_outputs:
        # Dictionary containing the name : inode pair(s)
        file_inodes = {}

        with open(os.path.join(folder_cache, fls_output), 'r') as f:
            lines = f.readlines()
            partition_offset = (lines[len(lines)-1])
            for line in lines:
                if(regex_mft.search(line)):
                    inode = regex_inode.search(line)[0]
                    file_inodes = {
                        "PartitionOffset": partition_offset, "File": "MFT", "Inode": inode}
                    partition_file_inodes.append(file_inodes)
                elif(regex_security_evtx.search(line)):
                    inode = regex_inode.search(line)[0]
                    file_inodes = {"PartitionOffset": partition_offset,
                                   "File": "Security.evtx", "Inode": inode}
                    partition_file_inodes.append(file_inodes)
                elif(regex_system_evtx.search(line)):
                    inode = regex_inode.search(line)[0]
                    file_inodes = {"PartitionOffset": partition_offset,
                                   "File": "System.evtx", "Inode": inode}
                    partition_file_inodes.append(file_inodes)
                elif(regex_application_evtx.search(line)):
                    inode = regex_inode.search(line)[0]
                    file_inodes = {"PartitionOffset": partition_offset,
                                   "File": "Application.evtx", "Inode": inode}
                    partition_file_inodes.append(file_inodes)
                elif(regex_secure_sds.search(line)):
                    inode = regex_inode.search(line)[0]
                    file_inodes = {
                        "PartitionOffset": partition_offset, "File": "SDS", "Inode": inode}
                    partition_file_inodes.append(file_inodes)
                elif(regex_usnjrnl_j.search(line)):
                    inode = regex_inode.search(line)[0]
                    file_inodes = {
                        "PartitionOffset": partition_offset, "File": "J", "Inode": inode}
                    partition_file_inodes.append(file_inodes)
                elif(regex_sam.search(line)):
                    inode = regex_inode.search(line)[0]
                    file_inodes = {
                        "PartitionOffset": partition_offset, "File": "SAM", "Inode": inode}
                    partition_file_inodes.append(file_inodes)
                elif(regex_system.search(line)):
                    inode = regex_inode.search(line)[0]
                    file_inodes = {
                        "PartitionOffset": partition_offset, "File": "SYSTEM", "Inode": inode}
                    partition_file_inodes.append(file_inodes)
            f.close()

    print(partition_file_inodes)

    # Extract the files using the list partition_file_inodes
    # Since there might be more than 1 partition, find the unique offsets and create folders for them.

    # Getting unique offsets
    offset_set = set()
    for index in range(len(partition_file_inodes)):
        offset_set.add(partition_file_inodes[index]["PartitionOffset"])

    # Creating folders
    for offset in offset_set:
        if not os.path.isdir(os.path.join(folder_cache, offset)):
            os.mkdir(os.path.join(folder_cache, offset))

    # Extract the files based on their inode
    for offset in offset_set:
        # Change to the offset folder
        # os.chdir(offset)
        with open("icat_log", 'a') as l:
            # Iterate the list where Offset value equals to the folder name
            for index in range(len(partition_file_inodes)):
                if(partition_file_inodes[index]["PartitionOffset"] == offset):
                    with open(os.path.join(folder_output, partition_file_inodes[index]["File"]), 'w') as f:
                        # Get a list of items in the root of the partition.
                        print(partition_file_inodes[index]["File"])
                        subprocess.run(["icat", "-v", "-i", "raw", "-o", offset, image_path,
                                       partition_file_inodes[index]["Inode"]], stdout=f, stderr=l, text=True)
                        f.close()

    new_files = []
    for offset in offset_set:
        # os.chdir(offset)
        new_files.append("Partition: "+offset)
        files = os.listdir()
        new_files.append(files)

    return new_files


# =================================================================================== #
# async def ingestImage(image: str):
# Mount the image and extract the files we can get data from.
# To Develope: Sanitize the string received.
# mount_and_extract(image)


# This function will extract the neccesary files from the image for processing


# def mount_and_extract(image: str):
# The assumption is that the image exist in a particular folder that was created
# by the case creator. We will create sub folders for each forensic image we process.

# We will create a folder using the image name. The end user will be able
# to provide a string with a custom name in the future.

# Change the working directory to the case folder. This should be provided by
# the user via a chosen mechanism.
# folder = '/home/aelindgard/Documents/Source/FARM/large-file-upload/file-upload-backend/case01/extracted/'
# os.chdir(folder)

# Delete any folder that was created previous during testing.
# shutil.rmtree(os.path.join(folder, image))

# Create the new folder.
# os.mkdir(image)

# Mount the image using SIFT fls
# data_extraction(image)


# This function extracts the data contained within the various
# files that have been extracted by the function mount_and_extract.


# def data_extraction(worfking_folder: str):
# Iterate through the folder and extract data that can be used to generate events.
# a = 1
