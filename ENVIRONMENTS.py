#!/usr/bin/env python3
"""
ENVIRONMENTS.py

This script reads ENVIRONMENTS.yaml and executes actions based on each environment's configuration.
It's designed to be easily extendable for additional properties and actions.
"""

import json
import os
import subprocess
import sys
import yaml
from pathlib import Path
from typing import Dict, List, Any

try:
    from jinja2 import Environment, FileSystemLoader, Template
except ImportError:
    print("Error: jinja2 not found. Install with: pip install jinja2")
    sys.exit(1)


class EnvironmentProcessor:
    """Processes environment configurations and executes corresponding actions."""

    def __init__(self, config_file: str = "ENVIRONMENTS.yaml"):
        """Initialize with the path to the environments configuration file."""
        self.config_file = Path(config_file)
        self.script_dir = Path(__file__).parent
        self.environments = []
        self.global_config = {}
        self.templates = {}

    def load_config(self) -> None:
        """Load the environments configuration from YAML file."""
        try:
            with open(self.config_file, "r") as file:
                config = yaml.safe_load(file)

            self.environments = config.get("environments", [])
            self.global_config = config.get("global", {})
            self.templates = config.get("templates", {})

            print(
                f"Loaded {len(self.environments)} environments from {self.config_file}"
            )

        except FileNotFoundError:
            print(f"Error: Configuration file {self.config_file} not found")
            sys.exit(1)
        except yaml.YAMLError as e:
            print(f"Error parsing YAML file: {e}")
            sys.exit(1)

    def process_spacemacs_action(self, env: Dict[str, Any]) -> None:
        """Process the spacemacs property by calling generate_emacs_desktop_file.sh."""
        if not env.get("spacemacs", False):  # Default to True if not specified
            return

        env_name = env["name"]
        script_path = self.script_dir / "bin" / "generate_emacs_desktop_file.sh"

        if not script_path.exists():
            print(
                f"Warning: Script {script_path} not found, skipping spacemacs action for {env_name}"
            )
            return

        try:
            result = subprocess.run(
                [str(script_path), env_name],
                cwd=self.script_dir / "applications",
                capture_output=True,
                text=True,
                check=True,
            )
            print(f"  ✓ Spacemacs: {env_name}")

        except subprocess.CalledProcessError as e:
            print(f"  ✗ Spacemacs failed: {env_name} ({e})")
        except Exception as e:
            print(f"  ✗ Spacemacs error: {env_name} ({e})")

    def process_tmuxinator_action(self, env: Dict[str, Any]) -> None:
        """Process the tmuxinator property by generating tmuxinator config from template."""
        if not env.get("tmuxinator", False):  # Default to True if not specified
            return

        env_name = env["name"]
        template_path = self.script_dir / "templates" / "tmuxinator.yml"
        output_dir = Path.home() / ".config" / "tmuxinator"
        output_file = output_dir / f"{env_name}.yml"

        # Check if template exists
        if not template_path.exists():
            print(
                f"Warning: Template {template_path} not found, skipping tmuxinator action for {env_name}"
            )
            return

        # Ensure output directory exists
        output_dir.mkdir(exist_ok=True)

        try:
            # Load template
            with open(template_path, "r") as f:
                template_content = f.read()

            # Create Jinja2 environment with custom filters and whitespace control
            jinja_env = Environment(
                trim_blocks=True,  # Remove newlines after block tags
                lstrip_blocks=True,  # Remove leading whitespace before block tags
            )

            def yaml_filter(value):
                """Convert Python object to YAML string."""
                return yaml.dump(value, default_flow_style=False).rstrip()

            jinja_env.filters["toyaml"] = yaml_filter

            # Create Jinja2 template
            template = jinja_env.from_string(template_content)

            # Create template context with full environment access
            context = {
                "env": env,
                "global": self.global_config,
                "templates": self.templates,
                "name": env["name"],
                "display_name": env.get("display_name", env["name"]),
                "working_dir": env.get("working_directory", "~/"),
                "language": env.get("language", ""),
                "description": env.get("description", ""),
                "framework": env.get("framework", ""),
                "role": env.get("role", ""),
                "project": env.get("project", ""),
                "tmuxinator_windows_start": env.get("tmuxinator_windows_start", []),
                "tmuxinator_windows": env.get("tmuxinator_windows", []),
                "tmuxinator_windows_end": env.get("tmuxinator_windows_end", []),
                "wm_workspace_names": env.get("wm_workspace_names", {}),
            }

            # Render template
            rendered_content = template.render(**context)

            # Write output file
            with open(output_file, "w") as f:
                f.write(rendered_content)

            print(f"  ✓ Tmuxinator: {env_name}")

        except Exception as e:
            print(f"  ✗ Tmuxinator error: {env_name} ({e})")

    def process_chromium_datadir_action(self, env: Dict[str, Any]) -> None:
        """Process the chromium-datadir property by generating chromium desktop file from template."""
        if not env.get("chromium-datadir", False):  # Default to False if not specified
            return

        env_name = env["name"]
        template_path = self.script_dir / "templates" / "chromium-datadir.desktop"
        output_dir = Path.home() / ".local" / "share" / "applications"
        output_file = output_dir / f"chromium-{env_name}.desktop"

        # Check if template exists
        if not template_path.exists():
            print(
                f"Warning: Template {template_path} not found, skipping chromium-datadir action for {env_name}"
            )
            return

        # Ensure output directory exists
        output_dir.mkdir(parents=True, exist_ok=True)

        try:
            # Load template
            with open(template_path, "r") as f:
                template_content = f.read()

            # Create Jinja2 environment with custom filters and whitespace control
            jinja_env = Environment(
                trim_blocks=True,  # Remove newlines after block tags
                lstrip_blocks=True,  # Remove leading whitespace before block tags
            )

            def yaml_filter(value):
                """Convert Python object to YAML string."""
                return yaml.dump(value, default_flow_style=False).rstrip()

            jinja_env.filters["toyaml"] = yaml_filter

            # Create Jinja2 template
            template = jinja_env.from_string(template_content)

            # Create template context with full environment access
            context = {
                "env": env,
                "global": self.global_config,
                "templates": self.templates,
                "name": env["name"],
                "display_name": env.get("display_name", env["name"]),
                "working_dir": env.get("working_directory", "~/"),
                "description": env.get("description", ""),
                "language": env.get("language", ""),
                "framework": env.get("framework", ""),
                "role": env.get("role", ""),
                "project": env.get("project", ""),
                "wm_workspace_names": env.get("wm_workspace_names", {}),
            }

            # Render template
            rendered_content = template.render(**context)

            # Write output file
            with open(output_file, "w") as f:
                f.write(rendered_content)

            print(f"  ✓ Chromium: {env_name}")

        except Exception as e:
            print(f"  ✗ Chromium error: {env_name} ({e})")

    def switch_to_environment(self, env: Dict[str, Any]) -> None:
        """Switch to an environment by executing environment-specific tasks."""
        env_name = env.get("name", "unknown")

        if not env_name or env_name == "unknown":
            print("  ✗ Error: Environment missing required 'name' field")
            return

        # Rename workspaces if wm_workspace_names is defined
        self.rename_workspaces(env)

    def get_current_workspaces(self) -> List[Dict[str, Any]]:
        """Get current i3 workspace information using i3-msg and jq."""
        try:
            cmd = "i3-msg -t get_workspaces"
            result = subprocess.run(
                cmd, shell=True, capture_output=True, text=True, check=True
            )

            # Parse the JSON array directly
            workspaces_data = json.loads(result.stdout)

            # Extract only the fields we need: name, visible, focused
            workspaces = []
            for ws in workspaces_data:
                workspaces.append(
                    {
                        "name": ws["name"],
                        "visible": ws["visible"],
                        "focused": ws["focused"],
                    }
                )
            return workspaces

        except subprocess.CalledProcessError as e:
            return []
        except json.JSONDecodeError as e:
            return []
        except Exception as e:
            return []

    def rename_workspaces(self, env: Dict[str, Any]) -> None:
        """Rename i3 workspaces based on wm_workspace_names mapping."""
        workspace_names = env.get("wm_workspace_names", {})

        if not workspace_names:
            return

        env_name = env["name"]

        # Get current workspace state
        current_workspaces = self.get_current_workspaces()

        for workspace_num, workspace_name in workspace_names.items():
            try:
                # Find current workspace name that matches this number
                current_name = None
                for ws in current_workspaces:
                    ws_name = ws["name"]
                    # Check if workspace name starts with our target number or equals the number
                    if ws_name.startswith(f"{workspace_num}:") or ws_name == str(
                        workspace_num
                    ):
                        current_name = ws_name
                        break

                # Use current name if found, otherwise fallback to number
                source_name = current_name if current_name else str(workspace_num)
                target_name = f"{workspace_num}:{workspace_name}"

                # Skip if already correctly named
                if source_name == target_name:
                    continue

                # Execute rename command using current name
                cmd = f'i3-msg \'rename workspace "{source_name}" to "{target_name}"\''
                result = subprocess.run(
                    cmd, shell=True, capture_output=True, text=True, check=True
                )

                print(f"  ✓ Workspace {workspace_num}: {workspace_name}")

            except subprocess.CalledProcessError as e:
                print(f"  ✗ Workspace {workspace_num} failed: {e}")
            except Exception as e:
                print(f"  ✗ Workspace {workspace_num} error: {e}")

    def process_environment(self, env: Dict[str, Any]) -> None:
        """Process a single environment configuration."""
        env_name = env.get("name", "unknown")

        # Validate required fields
        if not env_name or env_name == "unknown":
            print("  ✗ Error: Environment missing required 'name' field")
            return

        # Process spacemacs action
        self.process_spacemacs_action(env)

        # Process tmuxinator action
        self.process_tmuxinator_action(env)

        # Process chromium-datadir action
        self.process_chromium_datadir_action(env)

        # Add more action processors here as needed
        # Example:
        # self.process_aichat_action(env)

    def process_all_environments(self) -> None:
        """Process all environments in the configuration."""
        if not self.environments:
            print("No environments found to process")
            return

        for env in self.environments:
            self.process_environment(env)

    def switch_environment(self, env_name: str) -> None:
        """Switch to a specific environment by name."""
        # Find the environment
        target_env = None
        for env in self.environments:
            if env.get("name") == env_name:
                target_env = env
                break

        if not target_env:
            print(f"Error: Environment '{env_name}' not found")
            print("Available environments:")
            for env in self.environments:
                print(f"  - {env.get('name', 'unknown')}")
            return

        print(f"Switching to: {env_name}")
        self.switch_to_environment(target_env)

    def list_environments(self) -> None:
        """List all available environments."""
        if not self.environments:
            print("No environments found")
            return

        print("Available environments:")
        print("-" * 40)

        for env in self.environments:
            name = env.get("name", "unknown")
            display_name = env.get("display_name", name)
            role = env.get("role", "unknown")
            language = env.get("language", "unknown")

            print(f"{name:20} | {role:12} | {language:10} | {display_name}")


def main():
    """Main entry point."""
    # Change to the home-manager config directory
    home_manager_dir = Path.home() / ".config" / "home-manager"
    os.chdir(home_manager_dir)

    processor = EnvironmentProcessor()

    # Handle command line arguments
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()

        if command in ["--help", "-h", "help"]:
            print("Usage:")
            print(f"  {sys.argv[0]}                    # Process all environments")
            print(f"  {sys.argv[0]} list               # List all environments")
            print(
                f"  {sys.argv[0]} switch <env_name>  # Switch to specific environment"
            )
            print(f"  {sys.argv[0]} --help             # Show this help")
            return

        elif command == "list":
            processor.load_config()
            processor.list_environments()
            return

        elif command == "switch":
            if len(sys.argv) < 3:
                print("Error: switch command requires an environment name")
                print(f"Usage: {sys.argv[0]} switch <env_name>")
                return

            env_name = sys.argv[2]
            processor.load_config()
            processor.switch_environment(env_name)
            return
        else:
            print(f"Unknown command: {command}")
            print(f"Use '{sys.argv[0]} --help' for usage information")
            return

    # Default action: process all environments
    processor.load_config()
    processor.process_all_environments()


if __name__ == "__main__":
    main()
