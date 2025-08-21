# Integrated Development Environments System

This document describes the ENVIRONMENTS.py script and the YAML configuration system for managing Integrated Development Environments.

## Overview

The ENVIRONMENTS.py script automates the creation and management of development environments by:

- **Processing ENVIRONMENTS.yaml**: Reads environment configurations and generates supporting files
- **Template-driven generation**: Uses Jinja2 templates to create environment-specific configurations
- **Environment switching**: Manages workspace renaming and environment context switching
- **Multi-tool integration**: Supports Spacemacs, Tmuxinator, Chromium, and AIChat configurations

## ENVIRONMENTS.py Usage

### Basic Commands

```bash
# Process all environments (generate all configurations)
./ENVIRONMENTS.py

# List all available environments
./ENVIRONMENTS.py list

# Switch to a specific environment (renames workspaces, etc.)
./ENVIRONMENTS.py switch <environment_name>

# Show help
./ENVIRONMENTS.py --help
```

### Example Output

```bash
$ ./ENVIRONMENTS.py
  ✓ Spacemacs: canopy-env
  ✓ Tmuxinator: canopy-env  
  ✓ Chromium: canopy-env
  ✓ AIChat: canopy-grpc-client
  ✓ Workspace 1: www
```

## Environment Actions

The script processes environments and performs these actions based on configuration properties:

### 1. Spacemacs Desktop Files
- **Trigger**: `spacemacs: true` (default: false)
- **Action**: Creates desktop launcher at `~/.local/share/applications/emacs-{name}.desktop`
- **Template**: Uses `bin/generate_emacs_desktop_file.sh`

### 2. Tmuxinator Sessions
- **Trigger**: `tmuxinator: true` (default: false)
- **Action**: Creates tmux session config at `~/.config/tmuxinator/{name}.yml`
- **Template**: `templates/tmuxinator.yml`
- **Features**: 
  - Language-specific windows (Go, Python, Rust, JavaScript)
  - Conditional AIChat window (only if `aichat` property exists)
  - Database, Docker, Git windows based on environment properties

### 3. Chromium Data Directories
- **Trigger**: `chromium-datadir: true` (default: false)
- **Action**: Creates isolated browser launcher at `~/.local/share/applications/chromium-{name}.desktop`
- **Template**: `templates/chromium-datadir.desktop`
- **Benefit**: Separate browser profiles per project

### 4. AIChat Sessions
- **Trigger**: `aichat.session: true` 
- **Action**: Creates AI session config at `~/.config/aichat/sessions/{name}.yaml`
- **Template**: `templates/aichat_session.yaml`
- **Features**: Language-based model selection, role-specific configurations

### 5. Workspace Management
- **Trigger**: `wm_workspace_names` property
- **Action**: Renames i3 workspaces using current workspace names
- **Usage**: `./ENVIRONMENTS.py switch <name>` applies workspace renaming

## Configuration File Structure

The system uses `ENVIRONMENTS.yaml` (note: uppercase filename):
### ENVIRONMENTS.yaml Schema

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

### Action Properties  
- `spacemacs`: Boolean to create spacemacs desktop file (default: false)
- `tmuxinator`: Boolean to create tmuxinator config (default: false)  
- `chromium-datadir`: Boolean to create chromium desktop file with separate data directory (default: false)
- `aichat`: Object with AIChat configuration
  - `aichat.session`: Boolean to create AIChat session file (default: false)
  - `aichat.model`: Model to use (e.g., "claude:claude-sonnet-4-20250514", "openai:gpt-4o")

### Development Properties
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

### Window Management
- `wm_workspace_names`: Map of integer workspace numbers to string names for i3 workspace renaming

### Tmuxinator Customization
- `tmuxinator_windows_start`: Array of windows to add at the beginning of tmux session
- `tmuxinator_windows`: Array of windows to add in the middle of tmux session  
- `tmuxinator_windows_end`: Array of windows to add at the end of tmux session

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

## Example Environment Configuration

```yaml
environments:
  - name: "my-python-api"
    display_name: "Python API Service"
    language: "python"
    framework: "fastapi"
    role: "server"
    git_repo: "https://github.com/user/my-service.git"
    project: "backend"
    description: "FastAPI microservice for payments"
    working_directory: "~/projects/my-service"
    port: 8080
    
    # Action triggers
    spacemacs: true
    tmuxinator: true
    chromium-datadir: true
    aichat:
      session: true
      model: "claude:claude-sonnet-4-20250514"
    
    # Workspace management
    wm_workspace_names:
      1: "editor"
      2: "browser" 
      3: "terminal"
      4: "monitoring"
    
    # Development configuration
    tools:
      - "python"
      - "pip"
      - "uvicorn"
      - "pytest"
    python_version: "3.11"
    database: "postgresql"
    environment_vars:
      DEBUG: "true"
      DATABASE_URL: "postgresql://localhost:5432/myservice_dev"
    
    # Custom tmux windows
    tmuxinator_windows_start:
      - monitoring:
          layout: even-horizontal
          panes:
            - htop
            - docker stats
```

## Template System

The system uses Jinja2 templates with full access to environment configuration:

### Available Templates
- `templates/tmuxinator.yml`: Tmux session configuration
- `templates/chromium-datadir.desktop`: Chromium browser launcher
- `templates/aichat_session.yaml`: AIChat session configuration

### Template Variables
All templates receive these context variables:
- `env`: Full environment dictionary
- `global`: Global configuration
- `name`: Environment name
- `display_name`: Human-readable name
- `working_dir`: Working directory path
- `language`, `framework`, `role`, `project`: Environment properties
- `aichat`, `aichat_model`: AIChat configuration and model
- `wm_workspace_names`: Workspace naming map
- `tmuxinator_windows_*`: Custom window configurations

## Workflow Integration

### Daily Usage
1. **Setup**: Run `./ENVIRONMENTS.py` to generate all configurations
2. **Switch**: Use `./ENVIRONMENTS.py switch <env>` to change workspace context
3. **Launch**: Use generated desktop files or tmuxinator sessions
4. **Develop**: Work with environment-specific tools and configurations

### Project Onboarding
1. Add new environment to `ENVIRONMENTS.yaml`
2. Run `./ENVIRONMENTS.py` to generate configurations
3. Switch to environment: `./ENVIRONMENTS.py switch new-project`
4. Launch tmux session: `tmuxinator start new-project`

## Technical Details

### Dependencies
- **Python 3.7+** with `jinja2`, `pyyaml`
- **i3 window manager** for workspace management
- **tmuxinator** for session management
- **aichat** for AI assistance
- **Desktop environment** supporting .desktop files

### File Locations
- **Configuration**: `~/.config/home-manager/ENVIRONMENTS.yaml`
- **Script**: `~/.config/home-manager/ENVIRONMENTS.py`
- **Templates**: `~/.config/home-manager/templates/`
- **Generated Files**:
  - Spacemacs: `~/.local/share/applications/emacs-{name}.desktop`
  - Tmuxinator: `~/.config/tmuxinator/{name}.yml`
  - Chromium: `~/.local/share/applications/chromium-{name}.desktop`
  - AIChat: `~/.config/aichat/sessions/{name}.yaml`

## Best Practices

### Environment Design
1. **Naming**: Use descriptive, kebab-case names (`my-python-api`, not `MyPythonAPI`)
2. **Grouping**: Use consistent `project` values to group related environments
3. **Documentation**: Include clear `description` fields for each environment
4. **Tools**: List all required tools in the `tools` array for reproducibility

### Configuration Management
1. **Action Triggers**: Only enable actions you actually need (`spacemacs: true` only if using Spacemacs)
2. **Workspace Naming**: Use short, clear workspace names (`editor`, `browser`, not `development-environment`)
3. **Working Directories**: Use absolute paths or `~` for home directory references
4. **Model Selection**: Choose appropriate AI models for your language and complexity

### Template Customization
1. **Custom Windows**: Use `tmuxinator_windows_*` for project-specific tmux layouts
2. **Environment Variables**: Keep development vs production configs separate
3. **Port Management**: Ensure development ports don't conflict between environments

### Workflow Optimization
1. **Regular Updates**: Run `./ENVIRONMENTS.py` after configuration changes
2. **Environment Switching**: Use `switch` command for context changes, not just tmux session switching
3. **Tool Integration**: Leverage generated desktop files for consistent application launching
