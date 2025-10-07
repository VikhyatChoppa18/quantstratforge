# 🚀 PyPI Publishing Guide for QuantStratForge

## Prerequisites

### 1. Create PyPI Accounts
- **Test PyPI**: https://test.pypi.org/account/register/
- **Real PyPI**: https://pypi.org/account/register/

### 2. Install Required Tools
```bash
pip install twine
```

## Step-by-Step Publishing Process

### Step 1: Test Locally
```bash
# Check package integrity
twine check dist/*

# Test installation from local files
pip install dist/quantstratforge-0.1.0-py3-none-any.whl
```

### Step 2: Publish to Test PyPI
```bash
# Upload to Test PyPI (you'll be prompted for credentials)
twine upload --repository testpypi dist/*
```

**Credentials needed:**
- Username: Your Test PyPI username
- Password: Your Test PyPI password (or API token)

### Step 3: Test Installation from Test PyPI
```bash
# Install from Test PyPI
pip install --index-url https://test.pypi.org/simple/ quantstratforge

# Test the package
python -c "import quantstratforge; print('✅ Package installed successfully!')"
```

### Step 4: Publish to Real PyPI
```bash
# Upload to real PyPI
twine upload dist/*
```

**Credentials needed:**
- Username: Your PyPI username
- Password: Your PyPI password (or API token)

### Step 5: Verify Publication
```bash
# Install from PyPI
pip install quantstratforge

# Test the package
quantstratforge --help
```

## API Token Setup (Recommended)

### For Test PyPI:
1. Go to https://test.pypi.org/manage/account/token/
2. Create a new API token
3. Use `__token__` as username and the token as password

### For Real PyPI:
1. Go to https://pypi.org/manage/account/token/
2. Create a new API token
3. Use `__token__` as username and the token as password

## Publishing Commands Summary

```bash
# 1. Build package
python setup.py sdist bdist_wheel

# 2. Check package
twine check dist/*

# 3. Upload to Test PyPI
twine upload --repository testpypi dist/*

# 4. Test installation
pip install --index-url https://test.pypi.org/simple/ quantstratforge

# 5. Upload to real PyPI
twine upload dist/*

# 6. Final verification
pip install quantstratforge
```

## Troubleshooting

### Common Issues:

1. **Package name already exists**: Choose a different name or add version suffix
2. **Authentication failed**: Check username/password or use API tokens
3. **Metadata errors**: Ensure all required fields are in setup.py
4. **Dependency conflicts**: Check version constraints in requirements

### Version Management:
```bash
# Update version in setup.py before publishing
# Change version = "0.1.0" to version = "0.1.1"
```

## Post-Publication Checklist

- [ ] Package installs successfully from PyPI
- [ ] CLI command works: `quantstratforge --help`
- [ ] Import works: `import quantstratforge`
- [ ] All dependencies install correctly
- [ ] Documentation is accessible
- [ ] GitHub repository is linked
- [ ] License file is included

## Next Steps After Publishing

1. **Create GitHub Release**: Tag the version and create a release
2. **Update Documentation**: Ensure README reflects the published version
3. **Monitor Downloads**: Check PyPI stats for download metrics
4. **Gather Feedback**: Monitor GitHub issues and PyPI comments
5. **Plan Next Version**: Based on user feedback

## Security Best Practices

- Use API tokens instead of passwords
- Never commit credentials to version control
- Use `.pypirc` file for configuration (optional)
- Keep tokens secure and rotate regularly

## Package Information

- **Package Name**: quantstratforge
- **Current Version**: 0.1.0
- **Python Requirements**: >=3.12
- **License**: Proprietary
- **Keywords**: quantitative, trading, ai, machine-learning, finance, privacy, federated-learning

---

**Ready to publish? Run the commands above step by step!** 🚀
