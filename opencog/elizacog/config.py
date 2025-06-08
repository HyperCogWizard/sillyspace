"""
ElizaCog Configuration Management

Handles configuration for OpenCog-ElizaOS integration.
"""

import yaml
from pathlib import Path
from typing import Dict, Any, Optional
import os


class ElizaCogConfig:
    """Configuration manager for ElizaCog integration."""
    
    def __init__(self, config_data: Optional[Dict[str, Any]] = None):
        """Initialize configuration with default values."""
        self.config = config_data or self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration values."""
        return {
            'elizacog': {
                'version': '1.0.0',
                'initialized': False,
                'created_at': None
            },
            'opencog': {
                'atomspace': {
                    'enabled': True,
                    'default_space': 'elizacog_main',
                    'persistence': {
                        'backend': 'file',
                        'location': './atomspace_data'
                    }
                },
                'scheme_modules': [
                    'opencog/base/core_types.scm',
                    'opencog/base/utilities.scm'
                ],
                'python_modules': [
                    'opencog.atomspace',
                    'opencog.utilities'
                ]
            },
            'eliza_os': {
                'enabled': True,
                'api_endpoint': 'http://localhost:3000',
                'authentication': {
                    'method': 'token',
                    'token_file': './.eliza_token'
                },
                'agent_config': {
                    'default_character': 'helpful_ai',
                    'memory_enabled': True,
                    'learning_enabled': True
                }
            },
            'integration': {
                'bridge_modules': [
                    'knowledge_bridge',
                    'memory_bridge',
                    'reasoning_bridge'
                ],
                'data_flow': {
                    'opencog_to_eliza': True,
                    'eliza_to_opencog': True,
                    'bidirectional_sync': True
                },
                'monitoring': {
                    'enabled': True,
                    'metrics_interval': 60,
                    'log_level': 'INFO'
                }
            },
            'paths': {
                'bridges_dir': './bridges',
                'data_dir': './data',
                'logs_dir': './logs',
                'temp_dir': './tmp'
            }
        }
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value using dot notation."""
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any) -> None:
        """Set configuration value using dot notation."""
        keys = key.split('.')
        config = self.config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
    
    def save_to_file(self, file_path: Path) -> None:
        """Save configuration to YAML file."""
        with open(file_path, 'w') as f:
            yaml.dump(self.config, f, default_flow_style=False, indent=2)
    
    @classmethod
    def load_from_file(cls, file_path: Path) -> 'ElizaCogConfig':
        """Load configuration from YAML file."""
        with open(file_path, 'r') as f:
            config_data = yaml.safe_load(f)
        return cls(config_data)
    
    def validate(self) -> bool:
        """Validate configuration values."""
        required_sections = ['elizacog', 'opencog', 'eliza_os', 'integration', 'paths']
        
        for section in required_sections:
            if section not in self.config:
                raise ValueError(f"Missing required configuration section: {section}")
        
        # Validate specific required fields
        if not self.get('elizacog.version'):
            raise ValueError("Missing elizacog.version")
        
        if not self.get('opencog.atomspace.enabled'):
            if self.get('opencog.atomspace.enabled') is None:
                raise ValueError("Missing opencog.atomspace.enabled")
        
        return True
    
    def get_bridge_modules(self) -> list:
        """Get list of enabled bridge modules."""
        return self.get('integration.bridge_modules', [])
    
    def get_paths(self) -> Dict[str, str]:
        """Get all configured paths."""
        return self.get('paths', {})
    
    def is_bidirectional_sync_enabled(self) -> bool:
        """Check if bidirectional synchronization is enabled."""
        return self.get('integration.data_flow.bidirectional_sync', False)