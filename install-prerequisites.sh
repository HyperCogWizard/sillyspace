#!/bin/bash
#
# AtomSpace Prerequisite Installation Script
#
# This script installs all the prerequisites needed to build the OpenCog AtomSpace
# Supports Ubuntu/Debian systems
#

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo ""
    echo "==============================================="
    echo "$1"
    echo "==============================================="
}

# Check if running on supported system
check_system() {
    if ! command -v apt-get &> /dev/null; then
        print_error "This script currently only supports Ubuntu/Debian systems with apt-get"
        exit 1
    fi
    
    print_info "Detected system: $(lsb_release -d 2>/dev/null | cut -f2 || echo "Ubuntu/Debian")"
}

# Update package lists
update_packages() {
    print_header "Updating Package Lists"
    print_info "Running apt update..."
    sudo apt-get update
    print_success "Package lists updated"
}

# Install basic prerequisites available via apt
install_apt_packages() {
    print_header "Installing Prerequisites via apt"
    
    local packages=(
        "cmake"
        "build-essential"
        "git"
        "guile-3.0-dev"
        "cxxtest"
        "libpython3-dev"
        "cython3"
        "pkg-config"
    )
    
    print_info "Installing packages: ${packages[*]}"
    
    for package in "${packages[@]}"; do
        if dpkg -l | grep -q "^ii  $package "; then
            print_info "$package is already installed"
        else
            print_info "Installing $package..."
            sudo apt-get install -y "$package"
        fi
    done
    
    print_success "All apt packages installed"
}

# Install optional packages
install_optional_packages() {
    print_header "Installing Optional Prerequisites"
    
    local optional_packages=(
        "ocaml"
        "ocaml-findlib"
        "valgrind"
    )
    
    for package in "${optional_packages[@]}"; do
        if dpkg -l | grep -q "^ii  $package "; then
            print_info "$package is already installed"
        else
            print_info "Installing optional package $package..."
            sudo apt-get install -y "$package" || print_warning "Failed to install $package (optional)"
        fi
    done
    
    print_success "Optional packages installation completed"
}

# Check if cogutil is already installed
check_cogutil() {
    if pkg-config --exists cogutil 2>/dev/null; then
        print_success "CogUtil is already installed"
        return 0
    elif [ -f "/usr/local/lib/cmake/CogUtil/CogUtilConfig.cmake" ]; then
        print_success "CogUtil is already installed"
        return 0
    else
        return 1
    fi
}

# Install CogUtil from source
install_cogutil() {
    print_header "Installing CogUtil from Source"
    
    if check_cogutil; then
        return 0
    fi
    
    local temp_dir="/tmp/cogutil-build"
    
    print_info "Cloning CogUtil repository..."
    rm -rf "$temp_dir"
    git clone https://github.com/opencog/cogutil.git "$temp_dir"
    
    cd "$temp_dir"
    
    print_info "Building CogUtil..."
    mkdir -p build
    cd build
    cmake ..
    make -j$(nproc)
    
    print_info "Installing CogUtil..."
    sudo make install
    
    # Update library cache
    sudo ldconfig
    
    print_success "CogUtil installed successfully"
    
    # Clean up
    cd /
    rm -rf "$temp_dir"
}

# Verify installation
verify_installation() {
    print_header "Verifying Installation"
    
    local checks=(
        "cmake --version"
        "guile --version"
        "cxxtestgen --version"
        "python3 --version"
    )
    
    for check in "${checks[@]}"; do
        if eval "$check" >/dev/null 2>&1; then
            print_success "$check ✓"
        else
            print_error "$check ✗"
        fi
    done
    
    # Check CogUtil
    if check_cogutil; then
        print_success "CogUtil installation ✓"
    else
        print_error "CogUtil installation ✗"
    fi
}

# Print completion message
print_completion() {
    print_header "Installation Complete"
    echo ""
    print_success "All prerequisites have been installed!"
    echo ""
    print_info "You can now build the AtomSpace by running:"
    echo "  mkdir build"
    echo "  cd build" 
    echo "  cmake .."
    echo "  make -j$(nproc)"
    echo "  sudo make install"
    echo ""
    print_info "To run tests:"
    echo "  make -j$(nproc) check"
    echo ""
}

# Main execution
main() {
    print_header "OpenCog AtomSpace Prerequisites Installer"
    
    check_system
    update_packages
    install_apt_packages
    install_optional_packages
    install_cogutil
    verify_installation
    print_completion
}

# Run main function
main "$@"