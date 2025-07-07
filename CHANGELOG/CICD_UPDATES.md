# CI/CD Pipeline Updates 🚀

## Overview
All GitHub Actions workflows have been updated to reflect the new repository structure with configuration files moved to the `config/` directory.

## Updated Workflows

### Core CI/CD Workflows
- ✅ `ci.yml` - Main CI pipeline
- ✅ `python.yml` - Python-specific CI
- ✅ `dependency-testing.yml` - Dependency validation
- ✅ `deploy-staging.yml` - Staging deployment
- ✅ `performance-monitoring.yml` - Performance tracking
- ✅ `performance-regression.yml` - Performance regression detection

### Changes Made
All workflows updated to use:
- `config/requirements.txt` instead of `requirements.txt`
- `config/requirements-dev.txt` instead of `requirements-dev.txt`

### Automated Update Process
Used PowerShell batch replacement to update all workflow files:
```powershell
Get-ChildItem -Name '*.yml' | ForEach-Object { 
    (Get-Content $_) -replace 'pip install -r requirements\.txt', 'pip install -r config/requirements.txt' -replace 'pip install -r requirements-dev\.txt', 'pip install -r config/requirements-dev.txt' | Set-Content $_ 
}
```

## Verification
All workflows now correctly reference the new configuration directory structure and should work seamlessly with the reorganized repository.

## Next Steps
1. **Test CI/CD**: Create a test PR to verify all workflows function correctly
2. **Update Documentation**: Ensure all documentation references use the new paths
3. **Team Communication**: Notify team members of the new structure

## Status: ✅ Complete
All CI/CD workflows have been successfully updated for the new repository structure.
