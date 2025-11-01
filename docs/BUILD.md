# Build and Distribution Guide
ISO 42001 AI Management System

## Build Process Overview

The ISO 42001 system provides multiple distribution options:

1. **Standalone Executable** - Single .exe file using PyInstaller
2. **Windows Installer** - Professional installer using NSIS
3. **Portable Distribution** - ZIP package for portable use

## Prerequisites

### For Executable Building
- Python 3.13+ with virtual environment
- PyInstaller (automatically installed by build script)

### For Windows Installer
- NSIS (Nullsoft Scriptable Install System)
- Download from: https://nsis.sourceforge.io/

## Build Scripts

### 1. Build Standalone Executable

```batch
scripts\build.bat
```

**What it does:**
- Activates virtual environment
- Installs PyInstaller if needed
- Creates single executable file
- Output: `dist\ISO42001-AIManagementSystem.exe`

**Features:**
- All dependencies bundled
- No installation required
- Database created in same directory as executable
- Version information embedded

### 2. Build Windows Installer

```batch
scripts\build-installer.bat
```

**Prerequisites:** Install NSIS first
```batch
scripts\install-nsis.bat
```

**What it does:**
- Checks for NSIS installation
- Builds professional Windows installer
- Creates Start Menu shortcuts
- Includes uninstaller
- Output: `installer\ISO42001-AIManagementSystem-Setup-v1.0.0.exe`

**Installer Features:**
- EULA acceptance dialog
- Professional Windows integration
- Start Menu and Desktop shortcuts
- Proper uninstall support
- Registry entries for Windows compatibility

### 3. Build Portable Distribution

```batch
scripts\build-portable.bat
```

**What it does:**
- Creates portable directory structure
- Includes all documentation
- Creates launcher script
- Packages as ZIP file
- Output: `portable\ISO42001-AIManagementSystem-Portable-v1.0.0.zip`

**Portable Features:**
- No installation required
- Self-contained package
- Easy distribution
- Database created in package directory

## File Structure

### After Building Executable
```
dist/
└── ISO42001-AIManagementSystem.exe    # Standalone executable
```

### After Building Installer
```
installer/
└── ISO42001-AIManagementSystem-Setup-v1.0.0.exe    # Windows installer
```

### After Building Portable
```
portable/
├── ISO42001-AIManagementSystem-Portable-v1.0.0/    # Portable directory
│   ├── ISO42001-AIManagementSystem.exe              # Executable
│   ├── Start-ISO42001.bat                           # Launcher script
│   ├── PORTABLE-README.txt                          # Instructions
│   ├── README.md                                    # Documentation
│   ├── LICENSE                                      # License file
│   ├── EULA.txt                                     # End User License Agreement
│   └── docs/                                        # Documentation folder
└── ISO42001-AIManagementSystem-Portable-v1.0.0.zip # ZIP package
```

## Distribution Options

### For End Users
1. **Windows Installer** (Recommended)
   - Professional installation experience
   - Automatic shortcuts and integration
   - Easy uninstallation

2. **Portable Version**
   - No installation required
   - Good for testing or temporary use
   - Can run from USB drive

### For Developers
1. **Source Code Distribution**
   - Clone from GitHub
   - Use `scripts\run.bat` for development
   - Full source code access

## Troubleshooting

### Build Issues

**PyInstaller Errors:**
- Ensure virtual environment is activated
- Check Python version compatibility
- Run `scripts\build.bat` as Administrator if needed

**NSIS Not Found:**
- Run `scripts\install-nsis.bat` to get installation help
- Verify NSIS is installed in standard location
- Check both Program Files and Program Files (x86)

**Database Path Issues:**
- Fixed in current version with PyInstaller-aware path detection
- Database creates automatically in executable directory

### Runtime Issues

**Executable Won't Start:**
- Check Windows Defender/Antivirus settings
- Run as Administrator if needed
- Ensure all Visual C++ redistributables are installed

**Database Errors:**
- Ensure write permissions in executable directory
- Check disk space availability
- Database will be created automatically on first run

## Version Management

Update version using the version management script:

```batch
# Show current version
scripts\bump.bat show

# Increment version
scripts\bump.bat patch    # 1.0.0 -> 1.0.1
scripts\bump.bat minor    # 1.0.0 -> 1.1.0
scripts\bump.bat major    # 1.0.0 -> 2.0.0

# Set specific version
scripts\bump.bat set 1.2.3
```

After version changes, rebuild all distributions:
1. `scripts\build.bat`
2. `scripts\build-installer.bat`
3. `scripts\build-portable.bat`

## License and Legal

All distributions include:
- **EULA.txt** - End User License Agreement
- **LICENSE** - Creative Commons License (CC BY-NC-SA 4.0)
- Copyright information for Gressling Consulting GmbH

The EULA includes:
- Usage terms and restrictions
- No warranty disclaimer
- Compliance with German law
- Creative Commons licensing terms