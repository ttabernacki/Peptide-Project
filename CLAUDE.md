# CLAUDE.md - AI Assistant Guide for Peptide-Project

## Project Overview

**Peptide-Project** is a Python-based web automation tool for immunoinformatics research. It uses Selenium WebDriver to automate peptide sequence analysis across multiple online bioinformatics services that predict peptide-HLA class I binding affinity.

### Purpose
The project automates the submission of peptide sequences to various prediction servers and collects results for comparative analysis of epitope predictions. This is valuable for vaccine design, immunotherapy research, and understanding T-cell recognition.

## Repository Structure

```
Peptide-Project/
├── Peptide.py          # Main automation script
└── CLAUDE.md           # This file
```

### Key Files

- **Peptide.py** (Peptide.py:1): Single monolithic script containing all functionality
  - Web automation functions for 4 different services
  - Data scraping and processing functions
  - CSV export functionality
  - Main execution logic at the bottom

## Technology Stack

### Core Dependencies
- **Python 3.x**: Primary language
- **Selenium WebDriver**: Browser automation (with Firefox/geckodriver)
- **Standard Library**: csv, sys modules

### External Services Integrated
1. **NetMHCpan** - Pan-specific MHC class I binding predictor
2. **NetMHC** - MHC class I binding predictor
3. **SYFPEITHI** - MHC ligand and peptide motif database
4. **RANKPEP** - MHC-peptide binding prediction

## Code Structure & Architecture

### Function Organization

**Job Submission Functions** (Peptide.py:12-97)
- `submit_job_NetMHCpan(peptide_sequence, peptide_length, HLA_Class)` - Submits to NetMHCpan
- `submit_job_NetMHC(peptide_sequence, peptide_length, HLA_Class)` - Submits to NetMHC
- `submit_job_SYFPEITHI(peptide_sequence, peptide_length, HLA_Class)` - Submits to SYFPEITHI
- `submit_job_RANKPEP(peptide_sequence, HLA_class_and_length)` - Submits to RANKPEP

**Data Processing Functions** (Peptide.py:99-135)
- `inputdata_from_textfile(input_filename)` - Reads peptides from text file
- `scrape_data_NetMHCpan()` - Extracts results from NetMHCpan page
- `text_to_list_NetMHCpan(string)` - Parses scraped text into list
- `write_csv_NetMHCpan(input_list)` - Writes results to CSV

**Main Execution** (Peptide.py:138-153)
- Initializes Firefox WebDriver
- Navigates to NetMHCpan
- Submits job and waits for results
- Exports data to CSV

## Development Workflows

### Setting Up Development Environment

```bash
# Install Python dependencies
pip install selenium

# Install Firefox and geckodriver
# Ubuntu/Debian:
sudo apt-get install firefox
sudo apt-get install firefox-geckodriver

# macOS:
brew install firefox
brew install geckodriver
```

### Running the Script

```bash
# Ensure input file exists
echo "PEPTIDESEQUENCE" > hervk.txt

# Run the automation
python Peptide.py
```

### Expected Input Format
- Text file with peptide sequences (one per line)
- Currently hardcoded to read from "hervk.txt" (Peptide.py:145)

### Expected Output
- CSV file named "writeData.csv" with parsed results (Peptide.py:130)

## Key Conventions & Best Practices

### Code Style
- Snake_case for function names
- PascalCase for HLA class parameters
- Inline comments explaining each step
- No external configuration files

### Web Automation Patterns
- Uses implicit waits (Peptide.py:35, 146)
- XPath for button location
- Element selection by name, index, or visible text
- Waits after submission for results to load

### Error Handling
- Minimal error handling currently implemented
- Try-except block only for removing optional list elements (Peptide.py:118-123)
- Assertion to validate page load (Peptide.py:142)

## Critical Issues & Technical Debt

### ⚠️ Deprecated Selenium Methods
The code uses deprecated Selenium methods that will fail with Selenium 4.x:

**Deprecated:**
- `find_element_by_name()` (Peptide.py:19, 25, 30, etc.)
- `find_element_by_xpath()` (Peptide.py:38, 59, etc.)

**Should be:**
```python
# Old style
driver.find_element_by_name("SEQPASTE")

# New style (Selenium 4.x)
driver.find_element(By.NAME, "SEQPASTE")
```

### Other Issues
1. **Hardcoded values**: Input filename (hervk.txt), output filename (writeData.csv), peptide length (9)
2. **No configuration management**: All parameters hardcoded in main execution
3. **Limited error handling**: No timeout handling, no retry logic
4. **Single-threaded**: Processes one peptide at a time
5. **No logging**: Print statements only for debugging
6. **Global driver instance**: WebDriver initialized at module level (Peptide.py:138)

## Working with This Codebase

### Adding New Services
To add a new peptide prediction service:

1. Create new function following naming pattern: `submit_job_ServiceName()`
2. Implement form filling logic using Selenium
3. Add corresponding scraping function if needed
4. Add parsing logic for service-specific output format
5. Update main execution block to use new service

### Modifying Existing Functions
- Functions are service-specific; changes to one don't affect others
- Each submission function is independent
- Data processing functions are NetMHCpan-specific currently

### Testing Strategy
- Manual testing required (no unit tests present)
- Verify web page structure hasn't changed
- Test with various peptide sequences and lengths
- Validate CSV output format

## Modernization Recommendations

### High Priority
1. **Update Selenium syntax** to 4.x compatible methods
2. **Add requirements.txt** with pinned dependencies
3. **Extract configuration** (filenames, HLA classes, URLs) to config file
4. **Add command-line argument parsing** for flexibility

### Medium Priority
5. **Implement proper error handling** and retries
6. **Add logging** instead of print statements
7. **Create separate functions** for driver initialization/cleanup
8. **Add docstrings** to all functions

### Low Priority
9. **Add unit tests** for data processing functions
10. **Consider async/parallel processing** for multiple peptides
11. **Create CLI interface** with argparse
12. **Add README.md** with usage documentation

## Git Workflow

### Branch Strategy
- Development occurs on feature branches prefixed with `claude/`
- Branch format: `claude/claude-md-{session-id}`
- Never push directly to main without explicit permission

### Commit Practices
- Clear, descriptive commit messages
- Focus on "why" rather than "what"
- Group related changes together

### Important Git Operations
```bash
# Always push with -u flag to track remote branch
git push -u origin <branch-name>

# Fetch specific branches
git fetch origin <branch-name>

# Network failures: retry up to 4 times with exponential backoff
```

## AI Assistant Guidelines

### When Working with This Project

**DO:**
- Read Peptide.py before making any changes
- Test Selenium element selectors may need updates if websites change
- Maintain the functional programming style
- Keep functions service-specific and independent
- Check if web services are still accessible before major refactoring

**DON'T:**
- Don't add unnecessary abstractions for this simple project
- Don't over-engineer solutions
- Don't add features unless explicitly requested
- Don't create separate modules unless codebase grows significantly
- Don't add comments to code you didn't change

### Common Tasks

**Updating Selenium to 4.x:**
- Replace all `find_element_by_*` methods with `find_element(By.*, value)`
- Import `By` from `selenium.webdriver.common.by`
- Test all functions after changes

**Adding New Peptides:**
- Modify or replace hervk.txt with new sequences
- Adjust peptide_length parameter if needed (Peptide.py:145)
- Change HLA class if analyzing different alleles

**Changing Output Format:**
- Modify `write_csv_NetMHCpan()` function (Peptide.py:126)
- Adjust parsing logic in `text_to_list_NetMHCpan()` if needed (Peptide.py:111)

## External Dependencies & Services

### Web Services
All services are external and may change their interfaces:
- http://www.cbs.dtu.dk/services/NetMHCpan/ (currently used)
- Note: URLs and form elements may change without notice
- Regular maintenance required to keep automation working

### Browser Dependencies
- Requires Firefox browser installed
- Requires geckodriver in PATH
- May need to update geckodriver version periodically

## Security Considerations

- No sensitive data in repository
- No authentication required for services
- Web scraping should respect robots.txt and terms of service
- Rate limiting may be enforced by external services

## Future Directions

Potential enhancements for this project:
1. Support for batch processing multiple peptides
2. Integration with additional prediction services
3. Statistical analysis of results across services
4. Visualization of binding predictions
5. RESTful API wrapper for programmatic access
6. Docker containerization for reproducibility

## Contact & Resources

### Related Documentation
- Selenium Documentation: https://selenium-python.readthedocs.io/
- NetMHCpan: https://services.healthtech.dtu.dk/services/NetMHCpan-4.1/
- MHC Binding Prediction Overview: https://www.iedb.org/

### Getting Help
- Check if web service structure has changed
- Verify geckodriver and Firefox versions are compatible
- Review Selenium version compatibility

---

**Last Updated:** 2026-01-16
**Project Status:** Active development
**Primary Use Case:** Automated peptide-HLA binding prediction
