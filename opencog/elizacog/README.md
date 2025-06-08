# ElizaCog: OpenCog-ElizaOS Integration

ElizaCog is a bridge module that enables seamless integration between the OpenCog AtomSpace and ElizaOS, creating a synergy of cognitive excellence and interoperability.

## Overview

ElizaCog provides:
- **Knowledge Bridge**: Bidirectional knowledge transfer between OpenCog's AtomSpace and ElizaOS
- **Memory Bridge**: Shared memory and learning capabilities across both systems  
- **Reasoning Bridge**: Unified reasoning engine leveraging both cognitive architectures
- **Configuration Management**: Centralized configuration for the integrated system
- **CLI Interface**: Easy-to-use command-line tools for initialization and management

## Installation

1. Install the OpenCog AtomSpace package:
```bash
pip install atomspace
```

2. The `elizacog` command will be available after installation.

## Quick Start

### Initialize Integration

```bash
# Initialize in current directory
elizacog init

# Initialize in specific directory
elizacog init --directory ./my-ai-project
```

This creates:
- `elizacog.yaml` - Main configuration file
- `bridges/` - Integration bridge modules
- `data/` - Data storage directory
- `logs/` - Logging directory
- `eliza_character_template.json` - ElizaOS character template

### Test Integration

```bash
elizacog test
```

### Check Status

```bash
elizacog status
```

## Configuration

The `elizacog.yaml` file contains comprehensive configuration options:

```yaml
elizacog:
  version: "1.0.0"
  initialized: true

opencog:
  atomspace:
    enabled: true
    default_space: "elizacog_main"
    persistence:
      backend: "file"
      location: "./atomspace_data"

eliza_os:
  enabled: true
  api_endpoint: "http://localhost:3000"
  authentication:
    method: "token"
    token_file: "./.eliza_token"

integration:
  bridge_modules:
    - knowledge_bridge
    - memory_bridge  
    - reasoning_bridge
  data_flow:
    opencog_to_eliza: true
    eliza_to_opencog: true
    bidirectional_sync: true
```

## Bridge Modules

### Knowledge Bridge (`bridges/knowledge_bridge.py`)

Handles knowledge transfer between systems:
- Converts OpenCog Atoms to ElizaOS knowledge format
- Imports ElizaOS memories into AtomSpace
- Maintains knowledge consistency across systems

### Memory Bridge (`bridges/memory_bridge.py`)

Manages shared memory and learning:
- Synchronizes conversation histories
- Shares learned patterns and associations
- Coordinates memory consolidation

### Reasoning Bridge (`bridges/reasoning_bridge.py`)

Enables unified reasoning:
- Routes reasoning queries to appropriate system
- Combines inference results from both architectures
- Provides confidence scoring across systems

## Usage in Code

```python
from opencog.elizacog import ElizaCogBridge, ElizaCogConfig

# Initialize configuration
config = ElizaCogConfig()
bridge = ElizaCogBridge(config, Path("./my-project"))

# Initialize integration
bridge.initialize()

# Test the setup
success = bridge.test_integration()

# Use the bridge modules
from bridges import ElizaCogBridgeOrchestrator
orchestrator = ElizaCogBridgeOrchestrator(config)
orchestrator.initialize_all()
orchestrator.sync_all()
```

## Integration with ElizaOS

To use with ElizaOS:

1. Copy `eliza_character_template.json` to your ElizaOS characters directory
2. Customize the character configuration as needed
3. Start ElizaOS with the ElizaCog character
4. The bridge will automatically sync knowledge and reasoning

## Integration with OpenCog

ElizaCog works with or without full OpenCog installation:
- **With OpenCog**: Full AtomSpace integration and reasoning capabilities
- **Without OpenCog**: Mock implementations allow development and testing

## Architecture

```
┌─────────────────┐    ┌─────────────────┐
│    ElizaOS      │    │   OpenCog       │
│   ┌─────────┐   │    │  ┌──────────┐   │
│   │  Agent  │   │◄──►│  │AtomSpace │   │
│   │ System  │   │    │  │          │   │
│   └─────────┘   │    │  └──────────┘   │
└─────────────────┘    └─────────────────┘
         ▲                       ▲
         │                       │
         ▼                       ▼
┌─────────────────────────────────────────┐
│           ElizaCog Bridge               │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐   │
│  │Knowledge│ │ Memory  │ │Reasoning│   │
│  │ Bridge  │ │ Bridge  │ │ Bridge  │   │
│  └─────────┘ └─────────┘ └─────────┘   │
└─────────────────────────────────────────┘
```

## Development

To run tests:
```bash
python3 -m unittest tests.elizacog.test_elizacog -v
```

To extend the integration:
1. Add new bridge modules in the `bridges/` directory
2. Update configuration in `elizacog.yaml`
3. Register new modules in the bridge orchestrator

## Examples

See the generated bridge modules for implementation examples:
- `bridges/knowledge_bridge.py` - Knowledge transfer patterns
- `bridges/memory_bridge.py` - Memory synchronization
- `bridges/reasoning_bridge.py` - Reasoning coordination

## Contributing

ElizaCog is part of the OpenCog project. Contributions are welcome!

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## License

ElizaCog is licensed under the AGPL-3.0-or-later license, same as OpenCog AtomSpace.

## Links

- [OpenCog AtomSpace](https://github.com/opencog/atomspace)
- [OpenCog Wiki](https://wiki.opencog.org/w/AtomSpace)
- [ElizaOS](https://github.com/ai16z/eliza) (Integration target)

---

*"Bridging symbolic AI with conversational intelligence for cognitive excellence."*