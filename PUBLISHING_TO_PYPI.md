# Publishing QuantStratForge to PyPI

This guide walks you through the complete process of publishing your package to the official Python Package Index (PyPI).

## Prerequisites

✅ **COMPLETED:**
- [x] Package structure created
- [x] Poetry configuration (`pyproject.toml`) set up
- [x] All source files implemented
- [x] License file created
- [x] README.md written
- [x] Package built successfully (`.whl` and `.tar.gz` files created)

## Step-by-Step Publishing Process

### 1. Create a PyPI Account

If you don't already have a PyPI account:

1. Go to [https://pypi.org/account/register/](https://pypi.org/account/register/)
2. Fill in your details:
   - Username
   - Email address
   - Password
3. Verify your email address by clicking the link sent to your inbox

### 2. Enable Two-Factor Authentication (2FA)

PyPI requires 2FA for security:

1. Go to [https://pypi.org/manage/account/](https://pypi.org/manage/account/)
2. Navigate to "Account settings"
3. Under "Two factor authentication", click "Add 2FA with authentication application"
4. Use an authenticator app (Google Authenticator, Authy, etc.) to scan the QR code
5. Enter the verification code to enable 2FA

### 3. Generate an API Token

1. Go to [https://pypi.org/manage/account/token/](https://pypi.org/manage/account/token/)
2. Click "Add API token"
3. Enter a token name (e.g., "quantstratforge-upload")
4. Set the scope:
   - For first upload: Select "Entire account" (you can restrict it later)
   - After first upload: Select specific project "quantstratforge"
5. Click "Add token"
6. **IMPORTANT**: Copy the token immediately (it starts with `pypi-`)
   - You'll only see this token ONCE
   - Store it securely (password manager recommended)

### 4. Configure Poetry with Your PyPI Token

Run this command in your terminal (replace `YOUR_TOKEN_HERE` with your actual token):

```bash
poetry config pypi-token.pypi pypi-AgEIcGFnaS5vcmcC...YOUR_FULL_TOKEN...
```

Verify it's configured:

```bash
poetry config --list | grep pypi-token
```

### 5. Publish to PyPI

Now you're ready to publish! Run:

```bash
poetry publish
```

This will:
- Upload `quantstratforge-0.1.0.tar.gz` 
- Upload `quantstratforge-0.1.0-py3-none-any.whl`

You should see output like:
```
Publishing quantstratforge (0.1.0) to PyPI
 - Uploading quantstratforge-0.1.0.tar.gz 100%
 - Uploading quantstratforge-0.1.0-py3-none-any.whl 100%
```

### 6. Verify Your Package on PyPI

1. Visit [https://pypi.org/project/quantstratforge/](https://pypi.org/project/quantstratforge/)
2. Check that:
   - Version 0.1.0 is listed
   - README displays correctly
   - All metadata is correct
   - Both distribution files are available

### 7. Test Installation

Try installing your package:

```bash
# In a new virtual environment
pip install quantstratforge

# Test the import
python -c "from quantstratforge import DataFetcher, StrategyGenerator; print('Success!')"

# Test the CLI
quantstratforge --help
```

## Alternative: Publish Using Build + Twine

If you prefer not to use Poetry for publishing:

```bash
# Build the package
poetry build

# Install twine if not already installed
pip install twine

# Upload to PyPI
twine upload dist/quantstratforge-0.1.0*

# You'll be prompted for:
# - Username: __token__
# - Password: pypi-AgEIcGFnaS5vcmcC...YOUR_FULL_TOKEN...
```

## Troubleshooting

### Error: "The user 'username' isn't allowed to upload to project 'quantstratforge'"

This means the package name is already taken. Options:
1. Choose a different name (e.g., `quant-strat-forge`, `quantstratforge-ai`)
2. Contact PyPI support if you believe you own the name

### Error: "File already exists"

You're trying to upload a version that already exists. You need to:
1. Bump the version in `pyproject.toml`
2. Rebuild: `poetry build`
3. Publish again: `poetry publish`

### Error: "Invalid or non-existent authentication information"

Your API token is incorrect or expired:
1. Generate a new token on PyPI
2. Reconfigure Poetry: `poetry config pypi-token.pypi YOUR_NEW_TOKEN`

### Package Not Found After Upload

Wait 2-5 minutes for PyPI to index your package, then try again.

## Updating Your Package

When you make changes and want to release a new version:

```bash
# 1. Update version in pyproject.toml
# Change: version = "0.1.0"
# To:     version = "0.1.1"  (or 0.2.0, 1.0.0, etc.)

# 2. Update CHANGELOG or README if needed

# 3. Rebuild
poetry build

# 4. Publish
poetry publish

# 5. Commit and tag
git add pyproject.toml
git commit -m "Bump version to 0.1.1"
git tag v0.1.1
git push origin main --tags
```

## Semantic Versioning Guide

Follow [Semantic Versioning](https://semver.org/):

- **MAJOR** version (1.0.0 → 2.0.0): Breaking changes
- **MINOR** version (0.1.0 → 0.2.0): New features, backward compatible
- **PATCH** version (0.1.0 → 0.1.1): Bug fixes, backward compatible

## GitHub Actions for Automated Publishing

You can automate PyPI publishing with GitHub Actions. Create `.github/workflows/publish.yml`:

```yaml
name: Publish to PyPI

on:
  release:
    types: [published]

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.12'
      
      - name: Install Poetry
        run: |
          curl -sSL https://install.python-poetry.org | python3 -
          echo "$HOME/.local/bin" >> $GITHUB_PATH
      
      - name: Build package
        run: poetry build
      
      - name: Publish to PyPI
        env:
          POETRY_PYPI_TOKEN_PYPI: ${{ secrets.PYPI_TOKEN }}
        run: poetry publish
```

Then:
1. Add your PyPI token to GitHub Secrets (Settings → Secrets → New secret)
   - Name: `PYPI_TOKEN`
   - Value: Your PyPI token
2. Create a GitHub release to trigger automatic publishing

## Security Best Practices

1. **Never commit your PyPI token** to version control
2. **Use project-scoped tokens** when possible (after first upload)
3. **Rotate tokens periodically** (every 6-12 months)
4. **Enable 2FA** on your PyPI account
5. **Store tokens securely** in a password manager

## Post-Publication Checklist

- [ ] Package installs correctly: `pip install quantstratforge`
- [ ] README displays properly on PyPI
- [ ] CLI command works: `quantstratforge --help`
- [ ] All imports work correctly
- [ ] Badge links updated in README (if applicable)
- [ ] Announcement made (Twitter, LinkedIn, Reddit, etc.)
- [ ] Documentation site updated (if applicable)

## Current Build Information

**Package Name**: quantstratforge  
**Version**: 0.1.0  
**Built Files**:
- `dist/quantstratforge-0.1.0.tar.gz`
- `dist/quantstratforge-0.1.0-py3-none-any.whl`

**Status**: ✅ Ready to publish!

## Next Steps

1. Create PyPI account if you haven't already
2. Generate API token
3. Configure Poetry with the token
4. Run `poetry publish`
5. Celebrate! 🎉

## Support

If you encounter any issues:
- PyPI Documentation: [https://pypi.org/help/](https://pypi.org/help/)
- Poetry Publishing Docs: [https://python-poetry.org/docs/cli/#publish](https://python-poetry.org/docs/cli/#publish)
- Contact PyPI support: [https://pypi.org/help/#support](https://pypi.org/help/#support)

---

**Ready to publish?** Follow the steps above and your package will be live on PyPI in minutes!

