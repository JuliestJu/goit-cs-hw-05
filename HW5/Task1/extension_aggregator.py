import argparse
import asyncio
import os
import shutil
import logging
from pathlib import Path
import aiofiles

# Configure logging
logging.basicConfig(level=logging.ERROR, filename='error.log', filemode='w', 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Function to parse command-line arguments
def parse_args():
    parser = argparse.ArgumentParser(description='Asynchronous file sorter based on file extensions.')
    parser.add_argument('source', type=str, help='Source folder to read files from')
    parser.add_argument('output', type=str, help='Output folder to copy files to')
    return parser.parse_args()

# Asynchronous function to read all files in the source directory
async def read_folder(source_path, output_path):
    for root, _, files in os.walk(source_path):
        for file in files:
            file_path = Path(root) / file
            await copy_file(file_path, output_path)

# Asynchronous function to copy a file to the appropriate subfolder based on its extension
async def copy_file(file_path, output_path):
    extension = file_path.suffix.lstrip('.').lower()
    target_folder = Path(output_path) / extension
    
    try:
        os.makedirs(target_folder, exist_ok=True)
        async with aiofiles.open(file_path, 'rb') as src_file:
            async with aiofiles.open(target_folder / file_path.name, 'wb') as dest_file:
                while True:
                    chunk = await src_file.read(1024)  # Read file in chunks
                    if not chunk:
                        break
                    await dest_file.write(chunk)
    except Exception as e:
        logging.error(f"Failed to copy {file_path} to {target_folder}: {e}")

# Main function
async def main():
    args = parse_args()
    source_path = Path(args.source)
    output_path = Path(args.output)

    if not source_path.is_dir():
        logging.error(f"Source path {source_path} is not a directory")
        return
    
    if not output_path.is_dir():
        try:
            os.makedirs(output_path)
        except Exception as e:
            logging.error(f"Failed to create output directory {output_path}: {e}")
            return
    
    await read_folder(source_path, output_path)

# Run the main function
if __name__ == '__main__':
    asyncio.run(main())
