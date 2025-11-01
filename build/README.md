# Build Configuration

This directory contains build configuration files for the ISO 42001 AI Management System.

## Files

- **iso42001.spec** - PyInstaller specification for executable building
- **iso42001-installer.nsi** - NSIS script for Windows installer creation  
- **version_info.txt** - Windows version information for executable

## Usage

Use the master build script:

```bash
# Build executable only
scripts\build.bat exe

# Build installer (requires NSIS)
scripts\build.bat installer

# Build portable distribution
scripts\build.bat portable

# Build everything
scripts\build.bat all

# Clean build artifacts
scripts\build.bat clean
```

Build outputs:
- **Executable**: `dist\ISO42001-AIManagementSystem.exe`
- **Installer**: `installer\ISO42001-AIManagementSystem-Setup-v1.0.0.exe`  
- **Portable**: `portable\ISO42001-AIManagementSystem-Portable-v1.0.0.zip`