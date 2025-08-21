#!/bin/bash

# Regenerates Emacs desktop files based on first parameter

set -e

# Common MimeType definition
MIME_TYPE="text/english;text/plain;text/x-makefile;text/x-c++hdr;text/x-c++src;text/x-chdr;text/x-csrc;text/x-java;text/x-moc;text/x-pascal;text/x-tcl;text/x-tex;application/x-shellscript;text/x-c;text/x-c++;"

# Function to generate standard Emacs desktop file
generate_emacs_desktop() {
    local env_name="$1"
    local filename="emacs-${env_name}.desktop"
    
    # Write the desktop file directly without complex escaping
    cat > "$filename" << 'EOF'
[Desktop Entry]
Name=Emacs ENV_NAME (Client)
GenericName=Text Editor
Comment=Edit text
MimeType=MIME_TYPE_PLACEHOLDER
Exec=sh -c "if [ -n \\"\\$*\\" ]; then exec env EMACS_ENV=ENV_NAME emacsclient -s ENV_NAME --alternate-editor= --display=\\"\\$DISPLAY\\" \\"\\$@\\"; else exec env EMACS_ENV=ENV_NAME emacsclient -s ENV_NAME --alternate-editor= --create-frame; fi" placeholder %F
Icon=emacs
Type=Application
Terminal=false
Categories=Development;TextEditor;
StartupNotify=true
StartupWMClass=Emacs
Keywords=emacsclient;
Actions=new-window;new-instance;

[Desktop Action new-window]
Name=New Window
Exec=/usr/bin/emacsclient -s ENV_NAME --alternate-editor= --create-frame %F

[Desktop Action new-instance]
Name=New Instance
Exec=emacs %F
EOF
    
    # Replace placeholders with actual values using a different delimiter
    sed -i "s|ENV_NAME|${env_name}|g" "$filename"
    sed -i "s|MIME_TYPE_PLACEHOLDER|${MIME_TYPE}|g" "$filename"
    
    # Capitalize the first letter for the display name
    local display_name="${env_name^}"
    sed -i "s|Emacs ${env_name} (Client)|Emacs ${display_name} (Client)|" "$filename"
    
    echo "Generated ${filename}"
}

# Check if environment name is provided as first parameter
if [ -z "$1" ]; then
    echo "Usage: $0 <environment_name>"
    echo "Example: $0 canopy"
    exit 1
fi

env_name="$1"
echo "Generating desktop file for environment: $env_name"

generate_emacs_desktop "$env_name"
cp "emacs-${env_name}.desktop" ~/.local/share/applications/

echo "Desktop file for $env_name generated successfully!"
