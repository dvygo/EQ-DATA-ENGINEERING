# Contributing to NSE Corporate Filings Data Pipeline

Thank you for your interest in contributing to the NSE Corporate Filings Data Pipeline! We welcome contributions from the community.

## Getting Started

### Prerequisites

- Python 3.7 or higher
- Git
- Basic understanding of financial data and XBRL format

### Development Setup

1. **Fork and clone the repository**
   ```bash
   git clone https://github.com/your-username/nse-corporate-filings.git
   cd nse-corporate-filings
   ```

2. **Install dependencies**
   ```bash
   pip install requests openpyxl
   ```

3. **Test the setup**
   ```bash
   python fetcher.py --help
   ```

## How to Contribute

### Reporting Issues

Before creating an issue, please check if it already exists. When creating a new issue:

1. **Use a clear and descriptive title**
2. **Provide detailed steps to reproduce** the problem
3. **Include error messages** and stack traces
4. **Specify your environment** (OS, Python version, etc.)

### Suggesting Features

We welcome feature suggestions! Please:

1. **Check existing issues** to avoid duplicates
2. **Describe the use case** clearly
3. **Explain why this feature would be useful**
4. **Consider implementation complexity**

### Code Contributions

#### Pull Request Process

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Follow the existing code style
   - Add comments for complex logic
   - Update documentation if needed

3. **Test your changes**
   ```bash
   # Test with a small symbol set
   echo "RELIANCE" > test_symbols.txt
   python fetcher.py
   python downloader.py
   python converter.py
   python extractor.py
   ```

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: add new feature description"
   ```

5. **Push and create pull request**
   ```bash
   git push origin feature/your-feature-name
   ```

#### Code Style Guidelines

- **Use descriptive variable names**
- **Add docstrings to functions**
- **Handle exceptions gracefully**
- **Include progress logging**
- **Follow PEP 8 style guide**

Example:
```python
def download_xbrl_file(url, filepath):
    """
    Download XBRL file from URL to specified filepath.
    
    Args:
        url (str): XBRL file URL
        filepath (str): Local file path to save
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        with open(filepath, 'wb') as f:
            f.write(response.content)
            
        print(f"[OK] Downloaded: {os.path.basename(filepath)}")
        return True
        
    except Exception as e:
        print(f"[FAIL] Download failed: {e}")
        return False
```

### Documentation

- **Update README.md** for new features
- **Add inline comments** for complex logic
- **Include usage examples**
- **Document edge cases**

### Testing

#### Manual Testing

Test with different scenarios:

1. **Small symbol set** (1-3 symbols)
2. **Large symbol set** (50+ symbols)
3. **Symbols with no XBRL data**
4. **Network interruption scenarios**
5. **Existing file scenarios**

#### Test Cases

```bash
# Test 1: Normal flow
echo -e "RELIANCE\nTCS" > symbols.txt
python fetcher.py && python downloader.py

# Test 2: Resume capability
# Run downloader.py again - should skip existing files

# Test 3: Invalid symbol
echo "INVALID_SYMBOL" > symbols.txt
python fetcher.py  # Should handle gracefully
```

## Development Areas

### Priority Areas for Contribution

1. **Error Handling**
   - Better network error recovery
   - Graceful handling of malformed data
   - Retry mechanisms with exponential backoff

2. **Performance Optimization**
   - Parallel downloads
   - Memory usage optimization
   - Faster XBRL parsing

3. **Data Quality**
   - Additional financial field extraction
   - Data validation and cleaning
   - Support for different XBRL schemas

4. **User Experience**
   - Progress bars and better logging
   - Configuration file support
   - Command-line argument parsing

5. **Platform Support**
   - Docker containerization
   - Linux/macOS compatibility testing
   - Cloud deployment guides

### Code Areas

- **fetcher.py**: NSE API interaction and JSON processing
- **downloader.py**: XBRL file downloading and organization
- **converter.py**: EC2 service integration and Excel conversion
- **extractor.py**: Financial data extraction and CSV generation

## Commit Message Format

Use conventional commit format:

```
type(scope): description

[optional body]

[optional footer]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance tasks

Examples:
```
feat(downloader): add parallel download support
fix(converter): handle EC2 timeout errors
docs(readme): update installation instructions
```

## Review Process

1. **Automated checks** (if available)
2. **Code review** by maintainers
3. **Testing** on different environments
4. **Documentation review**
5. **Merge** after approval

## Community

- **Be respectful** and inclusive
- **Help others** learn and contribute
- **Share knowledge** about financial data processing
- **Follow our [Code of Conduct](CODE_OF_CONDUCT.md)**

## Questions?

- **Create an issue** for technical questions
- **Check existing documentation** first
- **Provide context** when asking for help

## License

By contributing, you agree that your contributions will be licensed under the Apache License 2.0.

---

Thank you for contributing to the NSE Corporate Filings Data Pipeline! 🚀
