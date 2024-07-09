import unittest
from unittest.mock import patch
import os
import shutil
import asyncio
import logging
import aiofiles
from pathlib import Path
from extension_aggregator import read_folder, parse_args, main

class TestFileSorter(unittest.TestCase):

    def setUp(self):
        # Setup source and output directories
        self.source_dir = Path('test_source')
        self.output_dir = Path('test_output')
        self.source_dir.mkdir(exist_ok=True)
        self.output_dir.mkdir(exist_ok=True)
        
        # Create test files
        (self.source_dir / 'file1.txt').write_text('This is a text file.')
        (self.source_dir / 'file2.jpg').write_text('This is an image file.')
        (self.source_dir / 'file3.pdf').write_text('This is a PDF file.')
        (self.source_dir / 'subfolder').mkdir(exist_ok=True)
        (self.source_dir / 'subfolder' / 'file4.txt').write_text('This is another text file.')

    # def tearDown(self):
        # Remove test directories after test
        # shutil.rmtree(self.source_dir)
        # shutil.rmtree(self.output_dir)

    def test_file_sorting(self):
        # Run the main function with test arguments
        args = ['script_name', str(self.source_dir), str(self.output_dir)]
        with unittest.mock.patch('sys.argv', args):
            asyncio.run(main())
        
        # Verify files are sorted correctly
        self.assertTrue((self.output_dir / 'txt' / 'file1.txt').exists())
        self.assertTrue((self.output_dir / 'txt' / 'file4.txt').exists())
        self.assertTrue((self.output_dir / 'jpg' / 'file2.jpg').exists())
        self.assertTrue((self.output_dir / 'pdf' / 'file3.pdf').exists())

    def test_logging(self):
        # Check if error log is created
        self.assertTrue(Path('error.log').exists())

if __name__ == '__main__':
    unittest.main()
