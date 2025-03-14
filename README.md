# PDFtoTXTdir
Using PYPDF2 to Convert all PDFs in input directory while preserving the input directory tree structure in the output directory.



### Usage

```plaintext
PDFtoTXT.exe [OPTIONS] [INPUT_DIRECTORY] [OUTPUT_DIRECTORY]
```

### Options

- `-i, --input INPUT_DIRECTORY`
  - Specify the input directory containing PDF files.
  - If not provided, the first positional argument will be used as the input directory.

- `-o, --output OUTPUT_DIRECTORY`
  - Specify the output directory for TXT files.
  - If not provided, the second positional argument will be used as the output directory.

- `-g, --gui`
  - Use GUI mode for directory selection.
  - If no directories are provided, the script will default to GUI mode.

### Examples

1. **Using named arguments:**
   ```plaintext
   PDFtoTXT.exe -i "C:\Input PDFs" -o "D:\Output"
   PDFtoTXT.exe --input "C:\Input PDFs" --output "D:\Output"
   ```

2. **Using positional arguments:**
   ```plaintext
   PDFtoTXT.exe "C:\Input PDFs" "D:\Output"
   ```

3. **Mixed style:**
   ```plaintext
   PDFtoTXT.exe "C:\Input PDFs" -o "D:\Output"
   ```

4. **Using GUI mode:**
   ```plaintext
   PDFtoTXT.exe
   PDFtoTXT.exe --gui
   ```

### Detailed Description

- **Positional Arguments:**
  - `INPUT_DIRECTORY`: The directory containing PDF files to be converted. If not provided as a named argument (`-i` or `--input`), it should be the first positional argument.
  - `OUTPUT_DIRECTORY`: The directory where the converted TXT files will be saved. If not provided as a named argument (`-o` or `--output`), it should be the second positional argument.

- **Named Arguments:**
  - `-i, --input`: Use this option to specify the input directory explicitly.
  - `-o, --output`: Use this option to specify the output directory explicitly.
  - `-g, --gui`: Use this option to enable GUI mode for directory selection.

### Notes

- If both positional and named arguments are provided, the named arguments will take precedence.
- If no arguments are provided, the script will default to GUI mode for directory selection.
- If all arguments are provided, -g, path selecter form will launch and -i and -o inputs will be ignored.
