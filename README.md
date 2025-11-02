# ISO 42001 AI Management System

Enterprise-grade web application for ISO 42001 AI Management System compliance and bookkeeping. Built with Python Dash framework and SQLite database for comprehensive AI lifecycle management and regulatory compliance tracking.

<img width="768" height="441" alt="image" src="https://github.com/user-attachments/assets/2fbb1bc4-4c96-447f-8796-37387d916b45" />

## Features

- **Asset Management**: Comprehensive tracking of AI assets, systems, and their operational properties
- **Risk Assessment**: Systematic recording and evaluation of AI-related risks and mitigation strategies
- **Control Framework**: Management of implemented controls, safeguards, and governance measures
- **Incident Management**: Detailed logging and tracking of AI-related incidents and responses
- **Compliance Monitoring**: Audit trail maintenance and compliance status reporting
- **Data Administration**: Database export/import functionality for backup and migration operations

<img width="768" height="434" alt="image" src="https://github.com/user-attachments/assets/c4ca969d-9ede-4e56-a2cc-11baa14ac0af" />

## Installation

### Option 1: Windows Executable (Standalone)
Download the pre-built Windows installer for immediate deployment without Python installation:

**Download**: [ISO 42001 Management Tool - Windows Installer](https://gressling.com/42001-management-tool/)

The Windows executable provides:
- Zero-configuration deployment - no Python or dependencies required
- Professional installer with sample database included
- Single-click installation and launch
- Automatic browser opening and port detection
- Complete offline functionality

### Option 2: Developer / Python Deployment
The deployment script automatically provisions and manages the Python virtual environment:

```bash
# Navigate to the project directory
cd /path/to/42001

# Run the application (creates .venv automatically)
scripts\run.bat
```

The automated deployment process:
- Provisions Python virtual environment (.venv) if not present
- Installs all required dependencies within isolated environment
- Launches application with proper environment activation

### Option 3: Manual Environment Configuration
1. Virtual environment creation and activation:
```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment (Windows)
.venv\Scripts\activate.bat

# Activate virtual environment (PowerShell)  
.venv\Scripts\Activate.ps1
```

2. Dependency installation:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

3. Application startup:
```bash
python main.py
```

4. Access web interface at `http://127.0.0.1:8050`

### Option 4: Development Environment Setup
```bash
# Install package in development mode with editable installation
pip install -e .

# Command-line interface usage
iso42001 --help
iso42001 --host 0.0.0.0 --port 8080 --debug
```

## Project Architecture

```
42001/
├── src/iso42001/          # Core application package  
│   ├── __init__.py        # Package initialization and metadata
│   ├── app.py            # Dash web application and user interface
│   ├── database.py       # SQLite database operations and schema
│   ├── callbacks.py      # Interactive callback functions
│   └── cli.py            # Command-line interface implementation
├── tests/                # Test suite and sample data
│   ├── test_app.py       # Unit and integration tests
│   └── create_sample_data.py  # Sample data generation utility
├── scripts/              # Automation and utility scripts
│   ├── run.bat          # Application launcher with environment setup
│   └── bump.bat         # Semantic version management
├── data/                 # Persistent data storage
│   └── iso42001.db      # SQLite database (created automatically)
├── docs/                 # Technical documentation
├── main.py              # Application entry point
├── setup.py             # Python package configuration
├── requirements.txt     # Python dependency specifications
└── README.md           # Project documentation
```

## Database Architecture

The application utilizes SQLite for data persistence and transaction management. The database file (`iso42001.db`) is automatically created in the `data/` directory upon initial application startup with complete schema initialization.

### Sample Data
The application includes comprehensive sample data for **ChemTech Industries**, a fictional SME chemical company, featuring:

- **R&D AI Systems**: Synthesis prediction algorithms, molecular discovery platforms, predictive maintenance systems
- **Business AI Systems**: Supply chain optimization, demand forecasting models, automated document processing  
- **15 AI Assets** distributed across research and business operations
- **9 Active Risks** with industry-specific safety and regulatory compliance considerations
- **12 Control Measures** including safety protocols and regulatory compliance frameworks
- **7 Documented Incidents** demonstrating real-world AI challenges in chemical manufacturing environments
- **8 Audit Records** covering safety assessments, regulatory compliance, and intellectual property protection

Database population with sample data:
```bash
# Activate virtual environment and execute sample data generation
.venv\Scripts\activate
python tests\create_sample_data.py
```

Comprehensive sample data documentation available in [`docs/ChemTech_Industries_Sample_Data.md`](docs/ChemTech_Industries_Sample_Data.md).

## License

This project is licensed under Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0). See LICENSE file for complete terms and conditions.

## Automation Scripts

### Semantic Version Management
Automated version control using semantic versioning principles:

```bash
# Display current version information
scripts\bump.bat show

# Increment patch version (1.0.0 → 1.0.1)  
scripts\bump.bat patch

# Increment minor version (1.0.0 → 1.1.0)
scripts\bump.bat minor

# Increment major version (1.0.0 → 2.0.0)
scripts\bump.bat major

# Set explicit version number
scripts\bump.bat set 1.2.3
```

### Application Deployment
```bash
# Launch application with automated environment validation
scripts\run.bat
```

## Development Operations

### Testing Framework
```bash
# Execute application test suite
python tests\test_app.py

# Generate sample data for development and testing
python tests\create_sample_data.py
```

### Package Management
```bash
# Install in development mode with editable installation
pip install -e .

# Build distribution packages for deployment
python setup.py sdist bdist_wheel
```

## Copyright

Copyright (c) 2025 Gressling Consulting GmbH, Germany E.U.

