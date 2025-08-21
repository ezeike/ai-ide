# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

⚠️ **IMPORTANT: Nix usage is deprecated in this project.**

This repository contains Linux development environment configuration files and dotfiles for a keyboard-driven interface optimized for productivity. While historical Nix Home Manager configuration exists, **all Nix-related functionality should be ignored unless specifically instructed otherwise.**

## Architecture Overview

⚠️ **DEPRECATED: The Nix-based architecture described below is no longer used.** 

This configuration was previously managed through a Nix-based architecture where `home.nix` served as the central configuration entry point. **This approach has been deprecated and should not be referenced or used.**

### Core Configuration Files
- ~~`home.nix` - **DEPRECATED** Main Home Manager configuration~~
- `zshrc` - ZSH shell configuration with oh-my-zsh, starship prompt, and modern CLI tools
- `tmux.conf` - Terminal multiplexer configuration with custom keybindings and status bar
- `i3.config` - Window manager configuration for keyboard-driven desktop interface
- `starship.toml` - Prompt configuration with visual indicators for git, directories, and development tools

### Application Management
- Desktop files in `applications/` directory provide project-specific Emacs launchers
- Each desktop file launches Emacs with environment-specific socket names and configurations

### Sub-configurations
- `emacs/` - Comprehensive Emacs/Spacemacs configuration with AI/LLM integration (see emacs/CLAUDE.md)
- `applications/` - Desktop entry files for application launchers (see applications/CLAUDE.md)
- `ssh/` - SSH configuration and key management
- `tmuxinator/` - Session management templates for different projects

## Common Commands and Workflows

### ~~Home Manager Operations~~ **DEPRECATED**
⚠️ **The following commands are deprecated and should not be used:**
```bash
# DEPRECATED - Do not use these commands
# home-manager switch
# home-manager build
```

### Configuration Management
```bash
# Navigate to config directory
cd ~/.config/home-manager

# Edit configuration files directly
# No special deployment commands needed - use standard file operations
```

### Development Environment Setup
```bash
# Manual configuration available for:
# - ZSH with oh-my-zsh, starship prompt, and modern CLI tools
# - tmux with custom keybindings and session management
# - i3 window manager with productivity-focused keybindings
# - Emacs with extensive AI/LLM integration capabilities

# Common aliases available through zsh configuration:
# - Modern alternatives: bat, exa, fd, rg, zoxide
# - Git shortcuts and enhanced completion
# - Custom development workflow shortcuts
```

### Email Configuration
The system includes dual email account setup:
- Fastmail account (primary): `ericnielson@fastmail.mx`
- Grove account: `eric@grove.city`
- Both configured with mbsync, msmtp, and mu for offline email management

## Configuration Patterns

### ~~Nix Package Management~~ **DEPRECATED**
⚠️ **The following Nix-based approaches are deprecated:**
- ~~Uses `nixpkgs.config.allowUnfree = true` for proprietary software~~
- ~~Packages defined in `home.packages` array~~
- ~~Custom desktop items created using `pkgs.makeDesktopItem`~~

### File Management Strategy
- Direct configuration file editing (no special deployment needed)
- SSH configuration and keys managed manually
- ~~Config files linked from repository to appropriate system locations~~ **DEPRECATED**
- ~~WezTerm terminal configuration embedded directly in `home.nix`~~ **DEPRECATED**
- Configuration files should be copied manually or via standard file operations

### Environment Isolation
- Multiple Brave browser profiles with separate user directories
- Project-specific Emacs environments using socket-based sessions
- tmuxinator templates for different development contexts
- Environment variables set for development tool configurations

## Development Workflow

### Configuration Management
- Edit files directly in `~/.config/home-manager/`
- ~~Apply changes with `home-manager switch`~~ **DEPRECATED**
- Manual copying/linking of configuration files to appropriate system locations
- Desktop files regenerated using the provided shell script

### Terminal and Shell Environment
- Starship prompt provides git status, directory context, and language versions
- ZSH configured with modern CLI tool replacements (bat, exa, fd, rg, zoxide)
- tmux configured with vim-like keybindings and custom status bar
- Custom keybindings throughout for efficient keyboard-driven workflow

### Window Management
- i3 window manager for tiling and keyboard control
- Custom keybindings for application launching and window management
- Integration with rofi for application launching and system control
- Flameshot for screenshot capabilities

## Important Configuration Details

### Security Considerations
- ~~SSH keys managed through home.nix file deployment~~ **DEPRECATED**
- SSH keys managed manually
- Email passwords stored in separate files (not in version control)
- Personal information properly separated from configuration logic

### Development Tools Integration
- newsboat RSS reader with vim-like keybindings
- htop system monitoring enabled
- Email stack (mbsync, msmtp, mu) for offline mail management
- Multiple browser profiles for project separation

### Customization Points
- Starship prompt easily customizable through starship.toml
- tmux configuration includes commented session templates
- i3 configuration includes autostart applications and custom keybindings
- Desktop file generation script easily extensible for new environments

## Directory Structure
```
├── home.nix              # DEPRECATED - Historical Nix configuration (ignore)
├── zshrc                 # ZSH shell configuration
├── tmux.conf            # Terminal multiplexer config
├── i3.config            # Window manager configuration
├── starship.toml        # Shell prompt configuration
├── applications/        # Desktop entry files and generation script
├── emacs/              # Emacs configuration (see emacs/CLAUDE.md)
├── ssh/                # SSH configuration and keys
├── tmuxinator/         # tmux session templates
└── bin/                # Custom scripts and utilities
```
