import os
import sys

def add_alias():
    shell = os.environ.get('SHELL', '').lower()
    
    if 'bash' in shell:
        config_file = os.path.expanduser('~/.bashrc')
        reload_command = 'source ~/.bashrc'
    elif 'zsh' in shell:
        config_file = os.path.expanduser('~/.zshrc')
        reload_command = 'source ~/.zshrc'
    elif 'fish' in shell:
        config_file = os.path.expanduser('~/.config/fish/config.fish')
        reload_command = 'source ~/.config/fish/config.fish'
    else:
        print(f"Unsupported shell: {shell}")
        return
    
    alias = "alias gyatt='python3 gyatt.py'\n"
    
    try:
        with open(config_file, 'a') as file:
            file.write(alias)
        print(f"Alias 'gyatt' added successfully to {config_file}.")
        print(f"Please run the following command to reload your shell config:\n{reload_command}")
        
    except Exception as e:
        print(f"Error adding alias: {e}")

if __name__ == "__main__":
    add_alias()
