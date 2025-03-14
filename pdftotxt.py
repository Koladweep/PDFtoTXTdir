from tkinter import Tk, filedialog
import os
import logging
import argparse
from pypdf import PdfReader
from typing import Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class PDFConverter:
    @staticmethod
    def convert_pdf_to_txt(pdf_path: str, txt_path: str) -> bool:
        """
        Convert a single PDF file to TXT.

        Args:
            pdf_path: Path to source PDF file
            txt_path: Path where TXT file should be saved

        Returns:
            bool: True if conversion successful, False otherwise
        """
        try:
            with open(txt_path, 'w', encoding='utf-8') as txt_file:
                reader = PdfReader(pdf_path)
                for page in reader.pages:
                    txt_file.write(page.extract_text())
            return True
        except Exception as e:
            logger.error(f"Error converting {pdf_path}: {str(e)}")
            return False

    @staticmethod
    def process_directory(input_dir: str, output_dir: str) -> tuple[int, int]:
        """
        Process all PDF files in a directory and its subdirectories.

        Args:
            input_dir: Source directory containing PDF files
            output_dir: Target directory for TXT files

        Returns:
            tuple: (successful_conversions, failed_conversions)
        """
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        successful = 0
        failed = 0

        for root, _, files in os.walk(input_dir):
            relative_path = os.path.relpath(root, input_dir)
            output_root = os.path.join(output_dir, relative_path)

            if not os.path.exists(output_root):
                os.makedirs(output_root)

            for file in files:
                if file.lower().endswith('.pdf'):
                    pdf_path = os.path.join(root, file)
                    txt_path = os.path.join(output_root, os.path.splitext(file)[0] + '.txt')
                    logger.info(f"Converting: {pdf_path} -> {txt_path}")

                    if PDFConverter.convert_pdf_to_txt(pdf_path, txt_path):
                        successful += 1
                    else:
                        failed += 1

        return successful, failed

def validate_directory(path: str, is_input: bool = True) -> bool:
    """
    Validate if directory exists and has proper permissions.

    Args:
        path: Directory path to validate
        is_input: Whether this is an input directory (requires different checks)

    Returns:
        bool: True if valid, False otherwise
    """
    if not path:
        logger.error(f"{'Input' if is_input else 'Output'} directory not specified")
        return False

    if is_input:
        if not os.path.exists(path):
            logger.error(f"Input directory does not exist: {path}")
            return False

        if not any(f.lower().endswith('.pdf') for _, _, files in os.walk(path) for f in files):
            logger.error(f"No PDF files found in input directory: {path}")
            return False

    return True

def browse_directory(title: str = "Select a Directory") -> Optional[str]:
    """
    Open a GUI dialog to browse for a directory.

    Args:
        title: Dialog window title

    Returns:
        Optional[str]: Selected directory path or None if cancelled
    """
    root = Tk()
    root.withdraw()
    directory_path = filedialog.askdirectory(title=title)
    root.destroy()
    return directory_path

def main():
    parser = argparse.ArgumentParser(
        description='Convert PDF files to TXT files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
    python pdftotxt.py -i "C:/input_pdfs" -o "C:/output_texts"
    python pdftotxt.py --gui
    python pdftotxt.py  # launches GUI mode by default
        '''
    )
    parser.add_argument(
        '--input', '-i',
        help='Input directory containing PDF files',
        type=str,
        metavar='INPUT_DIR'
    )
    parser.add_argument(
        '--output', '-o',
        help='Output directory for TXT files',
        type=str,
        metavar='OUTPUT_DIR'
    )
    parser.add_argument(
        '--gui', '-g',
        action='store_true',
        help='Use GUI mode for directory selection'
    )
    args = parser.parse_args()

    # Handle directory selection
    if args.gui or (not args.input and not args.output):
        input_directory = browse_directory(title="Select input directory")
        if not validate_directory(input_directory):
            return

        output_directory = browse_directory("Select output directory")
        if not validate_directory(output_directory, is_input=False):
            return
    else:
        if not validate_directory(args.input):
            parser.error("Invalid input directory")
        if not validate_directory(args.output, is_input=False):
            parser.error("Invalid output directory")
        input_directory = args.input
        output_directory = args.output

    # Process files
    logger.info(f'Input directory: {input_directory}')
    logger.info(f'Output directory: {output_directory}')

    successful, failed = PDFConverter.process_directory(input_directory, output_directory)
    logger.info(f'Conversion complete. Successful: {successful}, Failed: {failed}')

if __name__ == "__main__":
    main()
