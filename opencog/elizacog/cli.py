"""
ElizaCog CLI Interface

Command-line interface for OpenCog-ElizaOS integration.
"""

import argparse
import sys
import os
from pathlib import Path

from .core import ElizaCogBridge
from .config import ElizaCogConfig


def init_command(args):
    """Initialize OpenCog-ElizaOS integration."""
    print("🧠 ElizaCog: Initializing OpenCog-ElizaOS Integration")
    print("=" * 50)
    
    # Create configuration
    config = ElizaCogConfig()
    
    # Set up base directory for integration
    base_dir = Path(args.directory).resolve()
    base_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"📂 Integration directory: {base_dir}")
    
    # Initialize the bridge
    bridge = ElizaCogBridge(config, base_dir)
    
    try:
        bridge.initialize()
        print("✅ ElizaCog integration initialized successfully!")
        print(f"🔧 Configuration saved to: {base_dir / 'elizacog.yaml'}")
        print("🚀 Ready for cognitive excellence and seamless interoperability!")
        
        # Show next steps
        print("\n📋 Next Steps:")
        print(f"   1. Review configuration: {base_dir / 'elizacog.yaml'}")
        print(f"   2. Check bridge modules: {base_dir / 'bridges'}/")
        print(f"   3. Test the integration: elizacog test")
        
    except Exception as e:
        print(f"❌ Initialization failed: {e}")
        sys.exit(1)


def test_command(args):
    """Test OpenCog-ElizaOS integration."""
    print("🧪 ElizaCog: Testing Integration")
    print("=" * 30)
    
    base_dir = Path(args.directory).resolve()
    
    if not (base_dir / 'elizacog.yaml').exists():
        print("❌ ElizaCog not initialized. Run 'elizacog init' first.")
        sys.exit(1)
    
    config = ElizaCogConfig.load_from_file(base_dir / 'elizacog.yaml')
    bridge = ElizaCogBridge(config, base_dir)
    
    success = bridge.test_integration()
    
    if success:
        print("✅ Integration test passed!")
    else:
        print("❌ Integration test failed!")
        sys.exit(1)


def status_command(args):
    """Show ElizaCog integration status."""
    print("📊 ElizaCog: Integration Status")
    print("=" * 32)
    
    base_dir = Path(args.directory).resolve()
    
    if not (base_dir / 'elizacog.yaml').exists():
        print("❌ ElizaCog not initialized")
        return
    
    config = ElizaCogConfig.load_from_file(base_dir / 'elizacog.yaml')
    bridge = ElizaCogBridge(config, base_dir)
    
    bridge.show_status()


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="ElizaCog: OpenCog-ElizaOS Integration Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  elizacog init                    # Initialize in current directory
  elizacog init --directory ./ai  # Initialize in specific directory
  elizacog test                    # Test the integration
  elizacog status                  # Show integration status

For more information, visit: https://github.com/opencog/atomspace
        """
    )
    
    parser.add_argument(
        '--version', 
        action='version', 
        version='ElizaCog 1.0.0'
    )
    
    parser.add_argument(
        '--directory', 
        default='.', 
        help='Base directory for integration (default: current directory)'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Init command
    init_parser = subparsers.add_parser(
        'init', 
        help='Initialize OpenCog-ElizaOS integration'
    )
    init_parser.set_defaults(func=init_command)
    
    # Test command
    test_parser = subparsers.add_parser(
        'test', 
        help='Test the integration'
    )
    test_parser.set_defaults(func=test_command)
    
    # Status command
    status_parser = subparsers.add_parser(
        'status', 
        help='Show integration status'
    )
    status_parser.set_defaults(func=status_command)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    args.func(args)


if __name__ == '__main__':
    main()