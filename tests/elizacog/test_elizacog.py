"""
Tests for ElizaCog Integration Module
"""

import unittest
import tempfile
import shutil
from pathlib import Path
import sys
import os

# Add the source directory to the path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from opencog.elizacog.config import ElizaCogConfig
from opencog.elizacog.core import ElizaCogBridge


class TestElizaCogConfig(unittest.TestCase):
    """Test ElizaCog configuration management."""
    
    def test_default_config(self):
        """Test default configuration creation."""
        config = ElizaCogConfig()
        
        # Test basic structure
        self.assertIn('elizacog', config.config)
        self.assertIn('opencog', config.config)
        self.assertIn('eliza_os', config.config)
        self.assertIn('integration', config.config)
        self.assertIn('paths', config.config)
        
        # Test specific values
        self.assertEqual(config.get('elizacog.version'), '1.0.0')
        self.assertTrue(config.get('opencog.atomspace.enabled'))
        self.assertTrue(config.get('eliza_os.enabled'))
    
    def test_config_get_set(self):
        """Test configuration get/set operations."""
        config = ElizaCogConfig()
        
        # Test getting existing value
        self.assertEqual(config.get('elizacog.version'), '1.0.0')
        
        # Test getting non-existent value with default
        self.assertEqual(config.get('nonexistent.key', 'default'), 'default')
        
        # Test setting value
        config.set('test.key', 'test_value')
        self.assertEqual(config.get('test.key'), 'test_value')
    
    def test_config_validation(self):
        """Test configuration validation."""
        config = ElizaCogConfig()
        
        # Valid config should pass
        self.assertTrue(config.validate())
        
        # Invalid config should fail
        config.config = {}  # Empty config
        with self.assertRaises(ValueError):
            config.validate()
    
    def test_bridge_modules(self):
        """Test bridge module configuration."""
        config = ElizaCogConfig()
        
        modules = config.get_bridge_modules()
        expected_modules = ['knowledge_bridge', 'memory_bridge', 'reasoning_bridge']
        self.assertEqual(modules, expected_modules)
    
    def test_bidirectional_sync(self):
        """Test bidirectional sync configuration."""
        config = ElizaCogConfig()
        self.assertTrue(config.is_bidirectional_sync_enabled())


class TestElizaCogBridge(unittest.TestCase):
    """Test ElizaCog bridge functionality."""
    
    def setUp(self):
        """Set up test environment."""
        self.test_dir = Path(tempfile.mkdtemp())
        self.config = ElizaCogConfig()
        self.bridge = ElizaCogBridge(self.config, self.test_dir)
    
    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.test_dir)
    
    def test_bridge_initialization(self):
        """Test bridge initialization."""
        # Before initialization
        self.assertFalse(self.bridge.initialized)
        
        # Initialize
        self.bridge.initialize()
        
        # After initialization
        self.assertTrue(self.bridge.initialized)
        self.assertTrue(self.config.get('elizacog.initialized'))
        self.assertIsNotNone(self.config.get('elizacog.created_at'))
    
    def test_directory_creation(self):
        """Test directory structure creation."""
        self.bridge.initialize()
        
        # Check that all required directories exist
        paths = self.config.get_paths()
        for path_name, path_value in paths.items():
            dir_path = self.test_dir / path_value
            self.assertTrue(dir_path.exists(), f"Directory {path_name} should exist")
            self.assertTrue(dir_path.is_dir(), f"{path_name} should be a directory")
    
    def test_bridge_modules_creation(self):
        """Test bridge module file creation."""
        self.bridge.initialize()
        
        bridges_dir = self.test_dir / 'bridges'
        required_files = ['knowledge_bridge.py', 'memory_bridge.py', 'reasoning_bridge.py', '__init__.py']
        
        for file_name in required_files:
            file_path = bridges_dir / file_name
            self.assertTrue(file_path.exists(), f"Bridge file {file_name} should exist")
            self.assertTrue(file_path.is_file(), f"{file_name} should be a file")
            
            # Check that files have content
            content = file_path.read_text()
            self.assertGreater(len(content), 0, f"{file_name} should have content")
    
    def test_config_file_creation(self):
        """Test configuration file creation."""
        self.bridge.initialize()
        
        config_file = self.test_dir / 'elizacog.yaml'
        self.assertTrue(config_file.exists(), "Configuration file should exist")
        
        # Test loading the saved configuration
        loaded_config = ElizaCogConfig.load_from_file(config_file)
        self.assertTrue(loaded_config.get('elizacog.initialized'))
    
    def test_character_template_creation(self):
        """Test ElizaOS character template creation."""
        self.bridge.initialize()
        
        template_file = self.test_dir / 'eliza_character_template.json'
        self.assertTrue(template_file.exists(), "Character template should exist")
        
        # Test that it's valid JSON
        import json
        with open(template_file, 'r') as f:
            template_data = json.load(f)
        
        self.assertIn('name', template_data)
        self.assertIn('description', template_data)
        self.assertIn('system_prompt', template_data)
    
    def test_integration_test(self):
        """Test the integration testing functionality."""
        # Before initialization - should fail
        self.assertFalse(self.bridge.test_integration())
        
        # After initialization - should pass
        self.bridge.initialize()
        self.assertTrue(self.bridge.test_integration())
    
    def test_opencog_availability_check(self):
        """Test OpenCog availability checking."""
        # This will depend on whether OpenCog is actually installed
        availability = self.bridge._check_opencog_availability()
        self.assertIsInstance(availability, bool)


class TestElizaCogIntegration(unittest.TestCase):
    """Integration tests for complete ElizaCog workflow."""
    
    def setUp(self):
        """Set up integration test environment."""
        self.test_dir = Path(tempfile.mkdtemp())
    
    def tearDown(self):
        """Clean up integration test environment."""
        shutil.rmtree(self.test_dir)
    
    def test_full_workflow(self):
        """Test complete initialization and testing workflow."""
        # Step 1: Initialize
        config = ElizaCogConfig()
        bridge = ElizaCogBridge(config, self.test_dir)
        bridge.initialize()
        
        # Step 2: Verify initialization
        self.assertTrue(bridge.initialized)
        self.assertTrue((self.test_dir / 'elizacog.yaml').exists())
        
        # Step 3: Test integration
        self.assertTrue(bridge.test_integration())
        
        # Step 4: Verify bridge modules are importable
        bridges_dir = self.test_dir
        sys.path.insert(0, str(bridges_dir))
        
        try:
            from bridges import ElizaCogBridgeOrchestrator
            orchestrator = ElizaCogBridgeOrchestrator(config)
            self.assertIsNotNone(orchestrator)
        except ImportError:
            self.fail("Bridge modules should be importable")
        finally:
            sys.path.remove(str(bridges_dir))


if __name__ == '__main__':
    unittest.main()