# Integrated Development Environments Configuration

This document describes the YAML configuration format for defining Integrated Development Environments (IDEs) in `environments.yaml`.

An IDE consists of:

- Emacs (Spacemancs) configuration
- Tmux & tmuxinator configuration

# Tmuxinator Window Configuration

Window 1: claude
Window 2: aichat
Window 2: run

Use templates/tmuxinator.yaml
## Schema Overview

The configuration file consists of three main sections:

1. **environments**: Array of environment definitions
2. **global**: Global settings and defaults
3. **templates**: Reusable environment templates

## Environment Properties

Each environment in the `environments` array supports the following properties:

### Core Properties (Required)
- `name`: Unique identifier for the environment (kebab-case recommended)
- `display_name`: Human-readable name shown in UIs
- `language`: Primary programming language (e.g., "javascript", "python", "go", "rust")
- `role`: Environment type ("client", "server", "data", "infrastructure", "database", "research")
- `project`: Project grouping identifier
- `description`: Brief description of the environment's purpose
- `working_directory`: Absolute path to the project directory

### Optional Properties
- `spacemacs`: whether to create a spacemacs desktop file (default: true)
- `tmuxinator`: whether to create a tmuxinator config (default: true)
- `aichat`: whether to create an aichat config (default: true)
- `chromium-datadir`: whether to create a chromium desktop file with separate data directory (default: false)
- `framework`: Primary framework or library (e.g., "react", "express", "fastapi")
- `git_repo`: Git repository URL for cloning
- `port`: Default port for development server
- `database`: Database system used ("postgresql", "mysql", "mongodb", etc.)
- `tools`: Array of required tools and CLIs
- `python_version`: Specific Python version (for Python projects)
- `virtual_env`: Path to Python virtual environment
- `target_platforms`: Array of target platforms (for mobile/cross-platform)
- `cloud_provider`: Cloud provider ("aws", "gcp", "azure")
- `gpu_support`: Boolean indicating if GPU is required
- `wm_workspace_names`: Map of integer workspace numbers to string names for window manager workspace renaming

### Configuration Objects
- `environment_vars`: Key-value pairs of environment variables
- `editor_config`: Editor-specific configuration
  - `extensions`: Array of recommended extensions
  - `settings`: Editor settings object

## Roles

The following roles are supported:

- **client**: Frontend applications, mobile apps, desktop applications
- **server**: Backend services, APIs, web servers
- **data**: Data processing, ETL pipelines, analytics
- **infrastructure**: DevOps, IaC, deployment configurations
- **database**: Database schemas, migrations, queries
- **research**: ML experiments, research projects, prototypes

## Languages

Common languages and their typical frameworks:

- **javascript**: react, vue, express, nest
- **typescript**: angular, nest, next
- **python**: django, fastapi, flask, pytorch, tensorflow
- **go**: gin, echo, fiber
- **rust**: axum, warp, actix-web
- **java**: spring, quarkus
- **kotlin**: spring, ktor
- **dart**: flutter
- **sql**: postgresql, mysql
- **hcl**: terraform
- **yaml**: kubernetes, ansible

## Templates

Templates provide default configurations for common environment types. When creating a new environment, you can extend a template and override specific properties.

Available templates:
- `node_api`: Node.js/Express API server
- `react_client`: React frontend application
- `python_service`: Python/FastAPI service

## Usage Examples

### Creating a New Environment

To add a new environment, append to the `environments` array:

```yaml
environments:
  - name: "my-new-service"
    display_name: "My New Service"
    language: "python"
    framework: "fastapi"
    role: "server"
    git_repo: "https://github.com/user/my-service.git"
    project: "backend"
    description: "New microservice for handling payments"
    working_directory: "~/projects/my-service"
    port: 8080
    tools:
      - "python"
      - "pip"
      - "uvicorn"
    python_version: "3.11"
    wm_workspace_names:
      1: "editor"
      2: "browser"
      3: "terminal"
      4: "monitoring"
    environment_vars:
      DEBUG: "true"
      DATABASE_URL: "postgresql://localhost:5432/myservice_dev"
```

### Using Templates

Templates can be referenced when creating tooling that generates environments:

```yaml
# Reference the python_service template and override specific properties
name: "payment-processor"
template: "python_service"
display_name: "Payment Processor"
project: "payments"
git_repo: "https://github.com/company/payment-processor.git"
port: 8080
```

## Global Configuration

The `global` section contains system-wide defaults:

```yaml
global:
  default_shell: "zsh"          # Default shell for environments
  default_editor: "emacs"       # Default editor/IDE
  tmux_session_prefix: "dev"    # Prefix for tmux session names
  git_user: "Your Name"         # Git user name
  git_email: "you@example.com"  # Git email address
```

## Integration Points

This configuration format is designed to integrate with:

1. **Desktop File Generation**: Create environment-specific application launchers
2. **Tmuxinator**: Generate tmux session templates
3. **Editor Configuration**: Configure editor settings and extensions
4. **Shell Environment**: Set up environment variables and paths
5. **Development Tools**: Configure language servers, linters, formatters

## Validation

When creating environments, ensure:

- Environment names are unique
- Working directories exist or can be created
- Required tools are available in the system PATH
- Git repositories are accessible (if specified)
- Port numbers don't conflict between environments
- Environment variables are properly formatted

## Best Practices

1. Use descriptive, kebab-case names for environment identifiers
2. Group related environments using the same `project` value
3. Include comprehensive tool lists for reproducible environments
4. Set appropriate environment variables for development vs. production
5. Document the purpose of each environment in the `description` field
6. Use templates to maintain consistency across similar environments
