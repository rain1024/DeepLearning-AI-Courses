Compile LaTeX files to PDF using pdflatex.

## Instructions

1. If the user provides a specific .tex file path, use that file
2. If no file is specified, search for .tex files in the current working directory or recent context
3. Navigate to the directory containing the .tex file
4. Run pdflatex to compile the document:
   ```bash
   pdflatex -interaction=nonstopmode <filename>.tex
   ```
5. Report the compilation result and the output PDF location
6. If there are errors, show relevant error messages and suggest fixes

## Notes

- Use `-interaction=nonstopmode` to avoid interactive prompts
- The PDF will be generated in the same directory as the .tex file
- LaTeX auxiliary files (.aux, .log, etc.) are automatically created but should be in .gitignore
- If compilation fails, check for missing packages or syntax errors in the LaTeX source
