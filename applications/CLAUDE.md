# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This directory contains desktop entry files for a Home Manager configuration, specifically for launching different Emacs environments. The repository manages application launchers for various project-specific Emacs sessions.

## Architecture

The desktop files follow a consistent pattern:
- Each file creates a launcher for a specific Emacs environment (canopy, config, pm, hugo, etc.)
- Files use `emacsclient` with socket-based sessions (`-s <socket-name>`)
- Environment variables are set via `EMACS_ENV=<environment>` to distinguish contexts
- Most files support both file opening and creating new frames
- The `emacs30-pokt.desktop` file uses a different Emacs version (30.0.50) with custom init directory

## Common Patterns

### Desktop Entry Structure
All desktop files follow the standard .desktop format with:
- Name, GenericName, Comment fields for display
- MimeType associations for file types
- Exec command with conditional logic for file arguments
- Actions for new-window and new-instance

### Emacs Client Commands
- Standard pattern: `emacsclient -s <socket> --alternate-editor= --create-frame`
- File opening: Uses `$DISPLAY` environment variable
- Some entries include `--eval` for setting environment-specific variables

## File Types

- `emacs-*.desktop`: Standard Emacs environment launchers
- `emacs30-*.desktop`: Emacs 30.0.50 specific launchers with custom init directories
- `yed.desktop`: Java-based diagram editor with custom scaling

## Environment Management

Each Emacs environment is isolated through:
- Unique socket names for emacsclient sessions
- Environment variables (EMACS_ENV) for context identification
- Some environments use eval statements to set internal variables

## Modification Guidelines

When adding new desktop entries:
1. Follow the existing naming pattern: `emacs-<environment>.desktop`
2. Use consistent socket naming: `-s <environment>`
3. Set appropriate EMACS_ENV variable
4. Include both conditional file opening and frame creation logic
5. Maintain standard Actions for new-window and new-instance