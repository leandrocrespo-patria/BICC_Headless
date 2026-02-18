# BICC Oracle ERP Jobs Reset Automation

![Python](https://img.shields.io/badge/python-v3.7+-blue.svg)
![Selenium](https://img.shields.io/badge/selenium-4.0+-green.svg)
![Chrome](https://img.shields.io/badge/chrome-webdriver-orange.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

Automation tool for bulk resetting of jobs in Oracle ERP Cloud through the BICC (Business Intelligence Cloud Connector) web interface.

## 📋 Description

This script automates the job reset process in Oracle ERP Cloud, specifically in the BICC "Manage Jobs" module. It uses Selenium WebDriver to simulate user interactions and process multiple job rows in batch mode, optimized for headless execution in server environments or scheduled tasks.

### 🎯 Key Features

- ✅ **Complete Web Automation**: Automatic navigation, authentication and processing
- ✅ **Headless Mode**: Execution without graphical interface for servers and CI/CD
- ✅ **Batch Processing**: Handling multiple jobs (33 rows by default)
- ✅ **Detailed Logging**: Complete operation logs with timestamps
- ✅ **Robust Error Handling**: Automatic recovery and processing continuity
- ✅ **Smart Scrolling**: Automatic navigation in Oracle dynamic tables
- ✅ **Safe Cleanup**: Controlled browser and resource closure

## 🛠️ System Requirements

### Required Software
- **Python 3.7+**
- **Google Chrome** (updated version)
- **ChromeDriver** (compatible with installed Chrome version)

### Python Dependencies
```
selenium>=4.0.0
```

## 📦 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/leandrocrespo-patria/BICC_Headless.git
cd BICC_Headless
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure ChromeDriver
**Option A: Automatic Installation (Recommended)**
```bash
pip install webdriver-manager
```

**Option B: Manual Installation**
1. Download ChromeDriver from [https://chromedriver.chromium.org/](https://chromedriver.chromium.org/)
2. Add ChromeDriver to system PATH
3. Verify installation: `chromedriver --version`

## ⚙️ Configuration

### Configuration Variables
Edit the constants in `oracle_bicc_reset_headless.py`:

```python
# Oracle Cloud Credentials
ORACLE_USER = "your_username"        # Oracle service user
ORACLE_PASS = "your_password"        # Service password
ORACLE_URL = "https://your-instance.oraclecloud.com/biacm"  # Your instance URL

# Processing Configuration
TOTAL_ROWS = 33                      # Number of rows to process
PAGE_LOAD_TIMEOUT = 20               # Page load timeout
OPERATION_DELAY = 2                  # Delay between operations
```

### Logging Configuration
```python
SKIP_LOGOUT = False                  # True to skip logout
LOGOUT_TIMEOUT = 5                   # Timeout for logout operations
```

## 🚀 Usage

### Basic Execution
```bash
python oracle_bicc_reset_headless.py
```

### Execution with Console Logging
```bash
python oracle_bicc_reset_headless.py 2>&1 | tee execution.log
```

### Scheduled Execution (Cron/Task Scheduler)
```bash
# Linux/Mac - Crontab entry for daily execution at 2:00 AM
0 2 * * * cd /path/to/project && python oracle_bicc_reset_headless.py
```

```batch
# Windows - Task Scheduler
schtasks /create /tn "Oracle BICC Reset" /tr "C:\path\to\project\oracle_bicc_reset_headless.py" /sc daily /st 02:00
```

## 📁 Project Structure

```
BICC_Headless/
├── 📄 oracle_bicc_reset_headless.py    # Main script
├── 📄 requirements.txt                 # Python dependencies
├── 📄 README.md                       # Documentation (this file)
├── 📄 INSTRUCCIONES_PROGRAMACION.md   # Technical documentation
├── 📄 oracle_bicc_reset.log          # Execution logs
└── 📁 Uploads/                       # Auxiliary files
    └── user_message_*.txt
```

## 📊 Execution Process

### Workflow
1. **Initialization**: Chrome browser configuration in headless mode
2. **Authentication**: Automatic login to Oracle Cloud
3. **Navigation**: Access to "Manage Jobs" module 
4. **Processing**: Iteration over job rows (0 to TOTAL_ROWS-1)
   - Action element location
   - Smart scrolling if necessary
   - Click on action icon
   - "Reset" selection
   - Dialog confirmation
5. **Cleanup**: Logout and safe browser closure

### Output Example
```
1. Navigating to Oracle Cloud login page...
2. Performing user authentication...
3. Waiting for dashboard to load...
4. Accessing 'Manage Jobs' module...
5. Starting batch processing of 33 job rows...

--- Processing Row 1/33 (Index: 0) ---
   > Successfully clicked row action icon
   > Successfully clicked 'Reset' option
   > Confirmed reset operation with 'Y' key
   > Row 1 reset operation completed successfully

--- Processing Row 2/33 (Index: 1) ---
   ...

BATCH PROCESSING COMPLETED
6. Performing clean logout...
SCRIPT EXECUTION COMPLETED SUCCESSFULLY
```

## 📝 Logging

### Log File
- **Location**: `oracle_bicc_reset.log` (same directory as script)
- **Format**: `YYYY-MM-DD HH:MM:SS - LEVEL - MESSAGE`
- **Encoding**: UTF-8

### Log Example
```log
2026-02-18 14:30:15 - INFO - ============================================================
2026-02-18 14:30:15 - INFO - EXECUTION START - 2026-02-18 14:30:15
2026-02-18 14:30:15 - INFO - ============================================================
2026-02-18 14:30:16 - INFO - Initializing Chrome browser in headless mode...
2026-02-18 14:30:17 - INFO - Browser initialized successfully  
2026-02-18 14:30:18 - INFO - Navigating to Oracle Cloud...
2026-02-18 14:30:22 - INFO - Performing authentication...
2026-02-18 14:30:35 - INFO - Starting processing of 33 rows...
```

## 🔧 Troubleshooting

### Common Issues

#### 1. ChromeDriver not found
```bash
selenium.common.exceptions.WebDriverException: 'chromedriver' executable needs to be in PATH
```
**Solution**: Install ChromeDriver or add it to system PATH.

#### 2. Element timeout
```bash
selenium.common.exceptions.TimeoutException: Message: 
```
**Solution**: Increase `PAGE_LOAD_TIMEOUT` or verify XPath selectors.

#### 3. Authentication issues
```bash
selenium.common.exceptions.NoSuchElementException: Message: no such element: Unable to locate element
```
**Solution**: Verify credentials and Oracle Cloud URL.

#### 4. Scrolling errors
**Solution**: The script includes multiple scrolling strategies. Check logs for details.

### Debug Mode
To enable debug mode (with graphical interface):
```python
# Comment this line in the code:
# options.add_argument('--headless=new')
```

## 🔒 Security

### Best Practices
- **Never hardcode credentials** in source code
- Use environment variables for sensitive information:
  ```python
  import os
  ORACLE_USER = os.getenv('ORACLE_USER', 'default_user')
  ORACLE_PASS = os.getenv('ORACLE_PASS', 'default_pass')
  ```
- Keep logs secure with restrictive permissions
- Rotate credentials regularly

## 📈 Performance

### Typical Metrics
- **Time per row**: ~3-5 seconds
- **33 complete rows**: ~2-3 minutes
- **Memory usage**: ~100-150 MB (headless mode)

### Optimizations
- Headless mode reduces resource usage by ~40%
- Configurable timeouts for different network environments
- Smart scrolling minimizes DOM operations

## 🤝 Contributions

### Contribution Process
1. Fork the repository
2. Create branch for new feature (`git checkout -b feature/new-feature`)
3. Commit changes (`git commit -am 'Add new feature'`)
4. Push to branch (`git push origin feature/new-feature`)
5. Create Pull Request

### Report Issues
- Use GitHub issue template
- Include relevant logs
- Specify Python, Chrome and ChromeDriver versions

## 📄 License

This project is under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

### Contact
- **Author**: Leandro Crespo - Enterprise Architecture Team
- **Email**: [leandro.crespo@patria.com]
- **Issues**: [GitHub Issues](https://github.com/leandrocrespo-patria/BICC_Headless/issues)

### Additional Documentation
- [Selenium Documentation](https://selenium-python.readthedocs.io/)
- [ChromeDriver Documentation](https://chromedriver.chromium.org/getting-started)
- [Oracle Cloud Documentation](https://docs.oracle.com/en/cloud/)

---

**Version**: 3.6-headless (improved logout handling)  
**Last Update**: February 2026  
**Maintained by**: leandrocrespo-patria
