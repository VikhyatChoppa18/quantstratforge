# 🔐 GitHub Authentication Fix Guide

## Problem
GitHub password authentication is deprecated. You need a Personal Access Token (PAT).

## Solution: Create and Use Personal Access Token

### Step 1: Create Personal Access Token

1. Go to https://github.com/settings/tokens
2. Click **"Generate new token"** → **"Generate new token (classic)"**
3. Give it a name: `QuantStratForge Publishing`
4. Set expiration: **No expiration** (or custom)
5. Select scopes:
   - ✅ `repo` (Full control of private repositories)
   - ✅ `workflow` (Update GitHub Action workflows)
   - ✅ `write:packages` (Upload packages to GitHub Package Registry)
6. Click **"Generate token"**
7. **COPY THE TOKEN** (you won't see it again!)

### Step 2: Remove Old Remote and Add with Token

```bash
# Remove existing remote
git remote remove origin

# Add remote with token (replace TOKEN and USERNAME)
git remote add origin https://TOKEN@github.com/VikhyatChoppa18/quantstratforge.git
```

### Step 3: Push to GitHub

```bash
# Push to main branch
git branch -M main
git push -u origin main
```

## Alternative: Use SSH (More Secure)

### Step 1: Generate SSH Key

```bash
# Generate SSH key
ssh-keygen -t ed25519 -C "vikkychoppa@gmail.com"

# Start SSH agent
eval "$(ssh-agent -s)"

# Add SSH key
ssh-add ~/.ssh/id_ed25519

# Copy SSH public key
cat ~/.ssh/id_ed25519.pub
```

### Step 2: Add SSH Key to GitHub

1. Go to https://github.com/settings/keys
2. Click **"New SSH key"**
3. Title: `QuantStratForge Ubuntu`
4. Paste the public key
5. Click **"Add SSH key"**

### Step 3: Use SSH Remote

```bash
# Remove HTTPS remote
git remote remove origin

# Add SSH remote
git remote add origin git@github.com:VikhyatChoppa18/quantstratforge.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## Quick Fix (For Now)

Use this command to push with username and token:

```bash
git push https://VikhyatChoppa18:YOUR_TOKEN_HERE@github.com/VikhyatChoppa18/quantstratforge.git main
```

Replace `YOUR_TOKEN_HERE` with your actual Personal Access Token.

---

**Choose your preferred method and follow the steps above!** 🚀
