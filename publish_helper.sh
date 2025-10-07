#!/bin/bash

# QuantStratForge PyPI Publishing Helper Script
# Copyright (c) 2025 Venkata Vikhyat Choppa

set -e

echo "======================================"
echo "QuantStratForge PyPI Publishing Helper"
echo "======================================"
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if Poetry is installed
if ! command -v poetry &> /dev/null; then
    echo -e "${RED}❌ Poetry is not installed!${NC}"
    echo "Install it with: curl -sSL https://install.python-poetry.org | python3 -"
    exit 1
fi

echo -e "${GREEN}✅ Poetry is installed: $(poetry --version)${NC}"
echo ""

# Check if package is built
if [ ! -d "dist" ]; then
    echo -e "${YELLOW}⚠️  No dist directory found. Building package...${NC}"
    poetry build
    echo -e "${GREEN}✅ Package built successfully!${NC}"
    echo ""
else
    echo -e "${GREEN}✅ Package already built${NC}"
    echo ""
fi

# Display built files
echo "📦 Built packages:"
ls -lh dist/
echo ""

# Check for PyPI token
echo -e "${YELLOW}Checking for PyPI authentication...${NC}"
if poetry config pypi-token.pypi &> /dev/null; then
    echo -e "${GREEN}✅ PyPI token is configured${NC}"
    echo ""
    
    # Offer to publish
    echo -e "${YELLOW}Ready to publish to PyPI!${NC}"
    echo ""
    echo "This will publish:"
    echo "  - Package: quantstratforge"
    echo "  - Version: 0.1.0"
    echo "  - To: https://pypi.org/"
    echo ""
    read -p "Do you want to proceed with publishing? (yes/no): " -r
    echo ""
    
    if [[ $REPLY =~ ^[Yy](es)?$ ]]; then
        echo "Publishing to PyPI..."
        poetry publish
        
        if [ $? -eq 0 ]; then
            echo ""
            echo -e "${GREEN}🎉 SUCCESS! Package published to PyPI!${NC}"
            echo ""
            echo "Your package is now available at:"
            echo "  https://pypi.org/project/quantstratforge/"
            echo ""
            echo "Install it with:"
            echo "  pip install quantstratforge"
            echo ""
            echo "Next steps:"
            echo "  1. Verify the package: pip install quantstratforge"
            echo "  2. Test the CLI: quantstratforge --help"
            echo "  3. Update README badges if needed"
            echo "  4. Announce your package! 🚀"
        else
            echo ""
            echo -e "${RED}❌ Publishing failed!${NC}"
            echo "Check the error message above for details."
            exit 1
        fi
    else
        echo "Publishing cancelled."
    fi
else
    echo -e "${RED}❌ No PyPI token configured!${NC}"
    echo ""
    echo "To publish to PyPI, you need to:"
    echo ""
    echo "1. Create a PyPI account at https://pypi.org/account/register/"
    echo "2. Enable 2FA at https://pypi.org/manage/account/"
    echo "3. Generate an API token at https://pypi.org/manage/account/token/"
    echo "4. Configure Poetry with your token:"
    echo ""
    echo -e "   ${GREEN}poetry config pypi-token.pypi pypi-YOUR_TOKEN_HERE${NC}"
    echo ""
    echo "5. Run this script again"
    echo ""
    echo "For detailed instructions, see: PUBLISHING_TO_PYPI.md"
    echo ""
    
    read -p "Do you have a PyPI token ready? (yes/no): " -r
    echo ""
    
    if [[ $REPLY =~ ^[Yy](es)?$ ]]; then
        echo "Please paste your PyPI token (it will not be displayed):"
        read -s PYPI_TOKEN
        echo ""
        
        if [[ $PYPI_TOKEN == pypi-* ]]; then
            echo "Configuring Poetry with your token..."
            poetry config pypi-token.pypi "$PYPI_TOKEN"
            echo -e "${GREEN}✅ Token configured successfully!${NC}"
            echo ""
            echo "Now publishing to PyPI..."
            poetry publish
            
            if [ $? -eq 0 ]; then
                echo ""
                echo -e "${GREEN}🎉 SUCCESS! Package published to PyPI!${NC}"
                echo ""
                echo "Your package is now available at:"
                echo "  https://pypi.org/project/quantstratforge/"
            else
                echo ""
                echo -e "${RED}❌ Publishing failed!${NC}"
                exit 1
            fi
        else
            echo -e "${RED}❌ Invalid token format. Token should start with 'pypi-'${NC}"
            exit 1
        fi
    else
        echo "No problem! Follow the steps above to get your PyPI token."
        echo "Then run this script again: ./publish_helper.sh"
    fi
fi

echo ""
echo "======================================"
echo "Publishing Helper Complete"
echo "======================================"

