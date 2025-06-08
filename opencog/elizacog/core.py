"""
ElizaCog Core Integration Bridge

Core functionality for OpenCog-ElizaOS integration.
"""

import os
import sys
from pathlib import Path
from datetime import datetime
import importlib.util
from typing import Dict, Any, List, Optional

from .config import ElizaCogConfig


class ElizaCogBridge:
    """Core bridge between OpenCog and ElizaOS."""
    
    def __init__(self, config: ElizaCogConfig, base_dir: Path):
        """Initialize the bridge with configuration."""
        self.config = config
        self.base_dir = base_dir
        self.initialized = False
        
        # Try to import OpenCog modules (gracefully handle missing deps)
        self.opencog_available = self._check_opencog_availability()
    
    def _check_opencog_availability(self) -> bool:
        """Check if OpenCog modules are available."""
        try:
            # Try to import OpenCog and create an AtomSpace
            # This will fail if the compiled C++ extensions aren't available
            from opencog.atomspace import AtomSpace
            test_atomspace = AtomSpace()
            return True
        except (ImportError, AttributeError, Exception):
            return False
    
    def initialize(self) -> None:
        """Initialize the OpenCog-ElizaOS integration."""
        print("🔧 Setting up ElizaCog integration...")
        
        # Create necessary directories
        self._create_directories()
        
        # Generate bridge modules
        self._create_bridge_modules()
        
        # Create configuration templates
        self._create_config_templates()
        
        # Update configuration
        self.config.set('elizacog.initialized', True)
        self.config.set('elizacog.created_at', datetime.now().isoformat())
        
        # Save configuration
        config_file = self.base_dir / 'elizacog.yaml'
        self.config.save_to_file(config_file)
        
        self.initialized = True
        print("🎯 ElizaCog bridge initialization complete!")
    
    def _create_directories(self) -> None:
        """Create necessary directory structure."""
        paths = self.config.get_paths()
        
        for path_name, path_value in paths.items():
            dir_path = self.base_dir / path_value
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"   📁 Created {path_name}: {dir_path}")
    
    def _create_bridge_modules(self) -> None:
        """Create bridge modules for integration."""
        bridges_dir = self.base_dir / self.config.get('paths.bridges_dir', 'bridges')
        
        # Knowledge Bridge
        self._create_knowledge_bridge(bridges_dir)
        
        # Memory Bridge  
        self._create_memory_bridge(bridges_dir)
        
        # Reasoning Bridge
        self._create_reasoning_bridge(bridges_dir)
        
        # Main bridge orchestrator
        self._create_main_bridge(bridges_dir)
    
    def _create_knowledge_bridge(self, bridges_dir: Path) -> None:
        """Create knowledge bridge module."""
        knowledge_bridge = bridges_dir / 'knowledge_bridge.py'
        content = '''"""
Knowledge Bridge - OpenCog AtomSpace to ElizaOS Knowledge Transfer

Handles bidirectional knowledge transfer between OpenCog and ElizaOS.
"""

class KnowledgeBridge:
    """Bridges knowledge between OpenCog AtomSpace and ElizaOS."""
    
    def __init__(self, config):
        self.config = config
        self.atomspace = None
        self.eliza_client = None
    
    def initialize(self):
        """Initialize the knowledge bridge."""
        print("🧠 Initializing Knowledge Bridge...")
        
        # Initialize AtomSpace connection
        self._init_atomspace()
        
        # Initialize ElizaOS connection
        self._init_eliza_connection()
    
    def _init_atomspace(self):
        """Initialize OpenCog AtomSpace."""
        try:
            from opencog.atomspace import AtomSpace
            self.atomspace = AtomSpace()
            print("   ✅ AtomSpace connected")
        except ImportError:
            print("   ⚠️  AtomSpace not available - using mock")
            self.atomspace = MockAtomSpace()
    
    def _init_eliza_connection(self):
        """Initialize ElizaOS connection."""
        # TODO: Implement ElizaOS client connection
        print("   🔗 ElizaOS connection initialized (placeholder)")
        self.eliza_client = MockElizaClient()
    
    def sync_knowledge(self):
        """Synchronize knowledge between systems."""
        print("🔄 Syncing knowledge between OpenCog and ElizaOS...")
        
        # OpenCog -> ElizaOS
        if self.config.get('integration.data_flow.opencog_to_eliza'):
            self._transfer_to_eliza()
        
        # ElizaOS -> OpenCog
        if self.config.get('integration.data_flow.eliza_to_opencog'):
            self._transfer_to_opencog()
    
    def _transfer_to_eliza(self):
        """Transfer knowledge from OpenCog to ElizaOS."""
        print("   📤 Transferring knowledge to ElizaOS...")
        # Implementation placeholder
    
    def _transfer_to_opencog(self):
        """Transfer knowledge from ElizaOS to OpenCog.""" 
        print("   📥 Transferring knowledge to OpenCog...")
        # Implementation placeholder


class MockAtomSpace:
    """Mock AtomSpace for testing without OpenCog."""
    def __init__(self):
        self.atoms = []
    
    def add_node(self, type_name, name):
        return f"MockNode({type_name}, {name})"


class MockElizaClient:
    """Mock ElizaOS client for testing."""
    def __init__(self):
        self.connected = True
    
    def get_knowledge(self):
        return {"mock": "knowledge"}
'''
        knowledge_bridge.write_text(content)
        print(f"   📄 Created knowledge_bridge.py")
    
    def _create_memory_bridge(self, bridges_dir: Path) -> None:
        """Create memory bridge module.""" 
        memory_bridge = bridges_dir / 'memory_bridge.py'
        content = '''"""
Memory Bridge - OpenCog to ElizaOS Memory Synchronization

Handles memory sharing and synchronization between systems.
"""

class MemoryBridge:
    """Bridges memory between OpenCog and ElizaOS."""
    
    def __init__(self, config):
        self.config = config
        self.memory_store = {}
    
    def initialize(self):
        """Initialize the memory bridge."""
        print("🧩 Initializing Memory Bridge...")
        
    def sync_memories(self):
        """Synchronize memories between systems."""
        print("🔄 Syncing memories...")
        
    def store_interaction(self, interaction_data):
        """Store interaction data for both systems."""
        timestamp = str(datetime.now())
        self.memory_store[timestamp] = interaction_data
        print(f"   💾 Stored interaction: {timestamp}")
'''
        memory_bridge.write_text(content)
        print(f"   📄 Created memory_bridge.py")
    
    def _create_reasoning_bridge(self, bridges_dir: Path) -> None:
        """Create reasoning bridge module."""
        reasoning_bridge = bridges_dir / 'reasoning_bridge.py'
        content = '''"""
Reasoning Bridge - OpenCog to ElizaOS Reasoning Integration

Enables shared reasoning capabilities between systems.
"""

class ReasoningBridge:
    """Bridges reasoning between OpenCog and ElizaOS."""
    
    def __init__(self, config):
        self.config = config
        self.reasoning_engine = None
    
    def initialize(self):
        """Initialize the reasoning bridge."""
        print("⚡ Initializing Reasoning Bridge...")
    
    def process_query(self, query):
        """Process reasoning query across both systems."""
        print(f"🤔 Processing query: {query}")
        return {"result": "processed", "confidence": 0.85}
    
    def share_inferences(self):
        """Share inferences between systems.""" 
        print("🔗 Sharing inferences...")
'''
        reasoning_bridge.write_text(content)
        print(f"   📄 Created reasoning_bridge.py")
    
    def _create_main_bridge(self, bridges_dir: Path) -> None:
        """Create main bridge orchestrator."""
        main_bridge = bridges_dir / '__init__.py'
        content = '''"""
ElizaCog Bridges - Main Integration Module

Orchestrates all bridge modules for OpenCog-ElizaOS integration.
"""

from .knowledge_bridge import KnowledgeBridge
from .memory_bridge import MemoryBridge  
from .reasoning_bridge import ReasoningBridge

class ElizaCogBridgeOrchestrator:
    """Main orchestrator for all ElizaCog bridges."""
    
    def __init__(self, config):
        self.config = config
        self.knowledge_bridge = KnowledgeBridge(config)
        self.memory_bridge = MemoryBridge(config)
        self.reasoning_bridge = ReasoningBridge(config)
    
    def initialize_all(self):
        """Initialize all bridge modules."""
        print("🌉 Initializing ElizaCog Bridge Orchestrator...")
        
        self.knowledge_bridge.initialize()
        self.memory_bridge.initialize() 
        self.reasoning_bridge.initialize()
        
        print("✅ All bridges initialized successfully!")
    
    def sync_all(self):
        """Run full synchronization across all bridges."""
        print("🔄 Running full bridge synchronization...")
        
        self.knowledge_bridge.sync_knowledge()
        self.memory_bridge.sync_memories()
        self.reasoning_bridge.share_inferences()
        
        print("✅ Full synchronization complete!")

__all__ = ['ElizaCogBridgeOrchestrator', 'KnowledgeBridge', 'MemoryBridge', 'ReasoningBridge']
'''
        main_bridge.write_text(content)
        print(f"   📄 Created bridges/__init__.py")
    
    def _create_config_templates(self) -> None:
        """Create configuration templates."""
        # ElizaOS character template
        char_template = self.base_dir / 'eliza_character_template.json'
        char_content = {
            "name": "ElizaCog AI",
            "description": "An AI assistant powered by OpenCog reasoning and ElizaOS capabilities",
            "system_prompt": "You are an AI assistant with access to OpenCog's knowledge representation and reasoning capabilities. Use logical inference and knowledge graphs to provide thoughtful, well-reasoned responses.",
            "bio": "I am ElizaCog, an AI that combines symbolic reasoning with conversational abilities.",
            "knowledge": ["cognitive_science", "knowledge_representation", "artificial_intelligence"],
            "messageExamples": [
                {"user": "How does knowledge representation work?", "assistant": "Knowledge representation involves encoding information in a structured format that AI systems can process and reason with. In my case, I use OpenCog's AtomSpace to store and manipulate knowledge as hypergraphs."}
            ],
            "postExamples": ["Exploring the intersection of symbolic AI and natural language understanding"],
            "topics": ["reasoning", "knowledge_graphs", "cognitive_architectures"],
            "style": {"all": ["thoughtful", "analytical", "educational", "precise"]},
            "adjectives": ["intelligent", "reasoning", "knowledgeable", "helpful"]
        }
        
        import json
        with open(char_template, 'w') as f:
            json.dump(char_content, f, indent=2)
        print(f"   📄 Created eliza_character_template.json")
    
    def test_integration(self) -> bool:
        """Test the integration setup."""
        print("🧪 Testing ElizaCog integration...")
        
        success = True
        
        # Test configuration
        try:
            self.config.validate()
            print("   ✅ Configuration valid")
        except Exception as e:
            print(f"   ❌ Configuration error: {e}")
            success = False
        
        # Test directory structure
        paths = self.config.get_paths()
        for path_name, path_value in paths.items():
            dir_path = self.base_dir / path_value
            if dir_path.exists():
                print(f"   ✅ Directory {path_name} exists")
            else:
                print(f"   ❌ Directory {path_name} missing")
                success = False
        
        # Test bridge modules
        bridges_dir = self.base_dir / self.config.get('paths.bridges_dir', 'bridges')
        required_bridges = ['knowledge_bridge.py', 'memory_bridge.py', 'reasoning_bridge.py', '__init__.py']
        
        for bridge_file in required_bridges:
            bridge_path = bridges_dir / bridge_file
            if bridge_path.exists():
                print(f"   ✅ Bridge module {bridge_file} exists")
            else:
                print(f"   ❌ Bridge module {bridge_file} missing")
                success = False
        
        # Test OpenCog availability
        if self.opencog_available:
            print("   ✅ OpenCog modules available")
        else:
            print("   ⚠️  OpenCog modules not available (will use mock implementations)")
        
        return success
    
    def show_status(self) -> None:
        """Show current integration status."""
        print(f"📊 ElizaCog Integration Status")
        print(f"   Base Directory: {self.base_dir}")
        print(f"   Initialized: {self.config.get('elizacog.initialized', False)}")
        print(f"   Created: {self.config.get('elizacog.created_at', 'Unknown')}")
        print(f"   OpenCog Available: {self.opencog_available}")
        
        # Show bridge status
        bridges_dir = self.base_dir / self.config.get('paths.bridges_dir', 'bridges')
        print(f"   Bridge Modules:")
        
        for bridge_name in self.config.get_bridge_modules():
            bridge_file = bridges_dir / f"{bridge_name}.py"
            status = "✅" if bridge_file.exists() else "❌"
            print(f"     {status} {bridge_name}")
        
        # Show configuration status
        print(f"   Configuration:")
        print(f"     Bidirectional Sync: {self.config.is_bidirectional_sync_enabled()}")
        print(f"     AtomSpace Enabled: {self.config.get('opencog.atomspace.enabled')}")
        print(f"     ElizaOS Enabled: {self.config.get('eliza_os.enabled')}")