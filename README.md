# VEP 2026 System

A comprehensive voter file processing and validation system built as a monorepo workspace using UV package management. The system provides AI-powered validation, automated file loading, and robust data processing capabilities for voter registration data.

## 🏗️ System Architecture

```mermaid
graph TB
    subgraph "VEP 2026 System"
        subgraph "Core Packages"
            VFL[vep-file-loading<br/>📁 File Processing & Database Operations]
            VAV[vep-ai-validation-tools<br/>🤖 AI-Powered Validation & Parsing]
            VVT[vep-validation-tools<br/>🔍 Traditional Validation Rules]
            EU[election-utils<br/>🗳️ Election Data Utilities]
            SVF[state-voterfiles<br/>🗺️ State-Specific Voter File Handling]
            VRM[vep-record-matcher<br/>🔗 Record Matching & Deduplication]
        end
        
        subgraph "Data Flow"
            CSV[CSV Voter Files] --> VFL
            VFL --> DB[(Database<br/>PostgreSQL/SQLite)]
            VFL --> VAV
            VFL --> VRM
            VAV --> AI[AI Models<br/>LLM Processing]
            VAV --> VVT
            VVT --> EU
            EU --> SVF
            VRM --> VVT
            VRM --> DB
        end
        
        subgraph "External Dependencies"
            LLM[Ollama LLM<br/>Local AI Processing]
            WEB[Selenium<br/>Web Scraping]
            POST[Postal<br/>Address Validation]
        end
        
        AI -.-> LLM
        VFL -.-> WEB
        VAV -.-> POST
    end
    
    subgraph "Development Tools"
        UV[UV Package Manager<br/>🚀 Fast Python Package Management]
        GIT[Git Submodules<br/>📦 Modular Development]
        TEST[Pytest & Testing<br/>🧪 Quality Assurance]
    end
    
    VFL --> UV
    VAV --> UV
    VVT --> UV
    EU --> UV
    SVF --> UV
    VRM --> UV
    
    style VFL fill:#e1f5fe
    style VAV fill:#f3e5f5
    style VVT fill:#e8f5e8
    style EU fill:#fff3e0
    style SVF fill:#fce4ec
    style VRM fill:#e8f5e8
    style DB fill:#f5f5f5
    style AI fill:#ffebee
```

## 📦 Package Overview

### Core Packages

| Package | Purpose | Key Features |
|---------|---------|--------------|
| **vep-file-loading** | File processing and database operations | Smart upsert logic, batch processing, database optimization |
| **vep-ai-validation-tools** | AI-powered validation and parsing | LLM integration, intelligent field parsing, workflow graphs |
| **vep-validation-tools** | Traditional validation rules | Address validation, phone validation, data integrity checks |
| **election-utils** | Election data utilities | State-specific election handling, district codes |
| **state-voterfiles** | State-specific voter file handling | Multi-state support, TOML configuration, file readers |
| **vep-record-matcher** | Record matching and deduplication | Fuzzy matching, absolute matching, voter record comparison |

### Key Features

- **🔄 Smart Deduplication**: Automatic record deduplication using hashing
- **⚡ Performance Optimized**: Hybrid caching and batch processing
- **🤖 AI-Powered**: LLM integration for intelligent data parsing
- **🗄️ Database Agnostic**: Works with PostgreSQL, SQLite, and more
- **📊 Multi-File Support**: Track records across multiple source files
- **🔍 Data Integrity**: Comprehensive validation and error recovery
- **📈 Scalable**: Handles large voter files efficiently
- **🛡️ Error Handling**: Robust validation and recovery mechanisms

## 🚀 Quick Start

### Prerequisites

- **Python 3.12.8+**
- **UV package manager** (recommended)
- **PostgreSQL** (recommended) or SQLite
- **Git** with SSH access configured

### Installation

1. **Clone the repository with submodules:**
   ```bash
   git clone --recurse-submodules git@github.com:your-org/vep-2026-system.git
   cd vep-2026-system
   ```

2. **Initialize and update submodules:**
   ```bash
   git submodule update --init --recursive
   ```

3. **Install dependencies:**
   ```bash
   uv sync
   ```

4. **Activate the environment:**
   ```bash
   uv shell
   ```

### Basic Usage

#### 1. File Loading Example

```python
from vep_file_loading.database import CreatePublicModels, CreateRawFileModel
from sqlmodel import create_engine

# Setup database connection
engine = create_engine("postgresql://user:password@localhost:5432/voterfiles")

# Initialize models
public_models = CreatePublicModels()
public_models.setup(engine)

raw_file_model = CreateRawFileModel()
raw_file_model.public_models = public_models
raw_file_model.setup(engine)

# Load voter file with automatic deduplication
raw_file_model.read_file(
    engine=engine,
    file_path="path/to/voterfile.csv",
    state_abbreviation="TX",
    vendor_name="Voter Registration Office",
    county_name="Harris",
    batch_size=1000
)
```

#### 2. AI-Powered Validation Example

```python
from vep_ai_validation_tools import process_individual_voter_record
import asyncio

# Process a single voter record with AI validation
async def validate_voter():
    record = {
        "first_name": "John",
        "last_name": "Doe",
        "address": "123 Main St",
        "city": "Houston",
        "state": "TX"
    }
    
    result = await process_individual_voter_record(record, "record_001")
    print(f"Processed record: {result}")
    
asyncio.run(validate_voter())
```

#### 3. Traditional Validation Example

```python
from vep_validation_tools.funcs.address_validation import validate_address
from vep_validation_tools.funcs.phone_validation import validate_phone

# Validate address and phone number
address_result = validate_address("123 Main St, Houston, TX 77001")
phone_result = validate_phone("(555) 123-4567")

print(f"Address valid: {address_result}")
print(f"Phone valid: {phone_result}")
```

#### 4. Record Matching Example

```python
from vep_record_matcher.existing_match import SetupNewMatch, MatchedKey
from datetime import date

# Setup record matching between voter file and target records
matcher = SetupNewMatch(
    state="TX",
    voterfile=voter_file_data,  # Your voter file data
    targets=target_records,     # Target records to match against
    start_date=date(2020, 1, 1)  # Filter records from this date forward
)

# Run the matching process
results = matcher.start()

# Access matching results
print(f"Found {len(results.all_matches)} total matches")
print(f"Absolute matches: {len(results.absolute_matches)}")
print(f"Fuzzy matches: {len(results.all_matches) - len(results.absolute_matches)}")

# Export results for further processing
export_data = results.for_export
```

## 🛠️ Development Setup

### Workspace Structure

```
vep-2026-system/
├── packages/
│   ├── election-utils/           # Election data utilities (submodule)
│   ├── state-voterfiles/         # State-specific voter file handling (submodule)
│   ├── vep-ai-validation-tools/  # AI-powered validation (submodule)
│   ├── vep-file-loading/         # File processing and database operations (submodule)
│   ├── vep-record-matcher/       # Record matching and deduplication (submodule)
│   └── vep-validation-tools/     # Traditional validation rules (submodule)
├── pyproject.toml               # Workspace configuration
└── README.md                    # This file
```

### Development Commands

```bash
# Run tests for all packages
uv run pytest packages/

# Run linting
uv run ruff check .

# Run type checking
uv run mypy packages/

# Install development dependencies
uv sync --group dev

# Run tests for specific package
uv run pytest packages/vep-file-loading/

# Format code
uv run ruff format .
```

### Working with Submodules

```bash
# Update all submodules to latest
git submodule update --remote

# Update specific submodule
git submodule update --remote packages/state-voterfiles

# Commit submodule changes
cd packages/state-voterfiles
git add .
git commit -m "Update state-voterfiles"
git push

# Commit submodule pointer in main repo
cd ../..
git add packages/state-voterfiles
git commit -m "Update state-voterfiles submodule"
```

## 🔧 Configuration

### Database Setup

1. **PostgreSQL (Recommended):**
   ```bash
   # Install PostgreSQL
   brew install postgresql  # macOS
   sudo apt-get install postgresql  # Ubuntu
   
   # Create database
   createdb voterfiles
   ```

2. **Environment Variables:**
   ```bash
   export DATABASE_URL="postgresql://user:password@localhost:5432/voterfiles"
   export OLLAMA_BASE_URL="http://localhost:11434/v1"
   export OLLAMA_MODEL="llama3.2"
   ```

### AI Model Configuration

The system uses Ollama for local AI processing. Configure your model:

```python
# In your application
from vep_ai_validation_tools.agents.base import OpenAIProvider, OpenAIModel, ModelSettings

provider = OpenAIProvider(base_url="http://localhost:11434/v1")
model = OpenAIModel(
    model_name="llama3.2",
    provider=provider,
    settings=ModelSettings(temperature=0.1, max_retries=3)
)
```

## 📊 Performance & ROI

The VEP system provides significant time and cost savings:

### Local Government Scenario (50K-500K residents)
- **Manual Processing**: 48 hours/month
- **Automated Processing**: 6 hours/month
- **Time Savings**: 42 hours/month (87.5% reduction)
- **Cost Savings**: $2,100/month (at $50/hour)

### State-Level Scenario
- **Manual Processing**: 200+ hours/month
- **Automated Processing**: 25 hours/month
- **Time Savings**: 175+ hours/month
- **Cost Savings**: $8,750+/month

## 🧪 Testing

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=packages/

# Run specific test categories
uv run pytest -m "not slow"  # Skip slow tests
uv run pytest packages/vep-file-loading/tests/  # Package-specific tests

# Run integration tests
uv run pytest tests/integration/
```

## 📚 Documentation

- [vep-file-loading README](packages/vep-file-loading/README.md)
- [vep-ai-validation-tools README](packages/vep-ai-validation-tools/README.md)
- [vep-validation-tools README](packages/vep-validation-tools/README.md)
- [ROI Analysis](packages/vep-file-loading/ROI_ANALYSIS.md)

## 🤝 Contributing

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes** and add tests
4. **Run the test suite**: `uv run pytest`
5. **Commit your changes**: `git commit -m 'Add amazing feature'`
6. **Push to the branch**: `git push origin feature/amazing-feature`
7. **Open a Pull Request**

### Development Guidelines

- Follow PEP 8 style guidelines
- Add type hints to all functions
- Write comprehensive tests
- Update documentation as needed
- Use conventional commit messages

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/your-org/vep-2026-system/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-org/vep-2026-system/discussions)
- **Email**: dev@abstractdata.io

## 🔮 Roadmap

- [ ] Enhanced AI model integration
- [ ] Real-time processing capabilities
- [ ] Advanced analytics dashboard
- [ ] Multi-language support
- [ ] Cloud deployment options
- [ ] API endpoints for external integration

---

**Built with ❤️ by [Abstract Data](https://github.com/Abstract-Data)**