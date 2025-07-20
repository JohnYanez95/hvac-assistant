# WSL2 Setup Guide for HVAC Assistant

## Overview

This guide walks you through setting up Windows Subsystem for Linux 2 (WSL2) for the HVAC Assistant project. WSL2 provides a native Linux environment on Windows, making it ideal for Python/ML development with better Docker integration and simpler dependency management.

## Why WSL2 for This Project

- **Consistent Environment**: Same Python/Java/Hadoop versions everywhere
- **Better Docker Integration**: Native Linux container support
- **Simplified Path Handling**: No Windows/Linux path translation issues
- **Package Management**: Native Linux package managers (apt)
- **Development Tools**: Better terminal, shell scripting, and CLI tools

## Prerequisites

- Windows 10 version 2004+ or Windows 11
- Administrator access
- At least 4GB free disk space

## Installation Steps

### 1. Install WSL2 with Ubuntu

```cmd
# In PowerShell (as Administrator)
wsl --install Ubuntu-22.04
wsl --set-default-version 2
```

**What happens:**
- Downloads and installs WSL2 kernel
- Installs Ubuntu 22.04 LTS distribution
- Sets WSL2 as default version

### 2. Initial Ubuntu Setup

After installation, Ubuntu will prompt for:
- **Username**: Create a UNIX username (doesn't need to match Windows username)
- **Password**: Set a password for sudo commands

**Important WSL Nuances:**
- WSL may start in Windows directories (`/mnt/c/...`) - use `cd ~` to get to Linux home
- Start WSL properly with `wsl ~` (not just `wsl`) to begin in home directory
- Use Windows Terminal for better WSL integration
- Multi-line command pasting works seamlessly

### 3. System Updates

```bash
# Update package lists and upgrade system
sudo apt update && sudo apt upgrade -y
```

### 4. Install Development Dependencies

#### Python 3.10 Installation

```bash
# Install Python 3.10 and development tools
sudo apt install -y software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt install -y python3.10 python3.10-venv python3.10-dev python3-pip
```

**Note**: Ubuntu 22.04 comes with Python 3.10.12 which is compatible with our target 3.10.9

#### Java JDK 19 Installation

```bash
# Create directory and download JDK 19
sudo mkdir -p /opt/java
cd /tmp
wget https://download.oracle.com/java/19/archive/jdk-19.0.2_linux-x64_bin.tar.gz
sudo tar -xzf jdk-19.0.2_linux-x64_bin.tar.gz -C /opt/java/
sudo ln -sf /opt/java/jdk-19.0.2 /opt/java/current
```

#### Hadoop 3.3.5 Installation

```bash
# Download and install Hadoop
sudo mkdir -p /opt/hadoop
wget https://archive.apache.org/dist/hadoop/common/hadoop-3.3.5/hadoop-3.3.5.tar.gz
sudo tar -xzf hadoop-3.3.5.tar.gz -C /opt/hadoop/
sudo ln -sf /opt/hadoop/hadoop-3.3.5 /opt/hadoop/current
```

### 5. Configure Environment Variables

```bash
# Configure environment variables
# Note: ~/.bashrc is your shell configuration file that runs every time you open a terminal
# The >> operator appends these export commands to make variables persistent across sessions
echo 'export JAVA_HOME=/opt/java/current' >> ~/.bashrc
echo 'export HADOOP_HOME=/opt/hadoop/current' >> ~/.bashrc
echo 'export PATH=$PATH:$JAVA_HOME/bin:$HADOOP_HOME/bin' >> ~/.bashrc
source ~/.bashrc  # Reload the configuration to apply changes immediately

# Clean up downloads
rm /tmp/*.tar.gz
```

### 6. Configure Git

```bash
# Configure git (replace with your information)
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
git config --global init.defaultBranch main
```

**Note**: Git comes pre-installed with Ubuntu 22.04

### 7. Clone Project and Setup Virtual Environment

```bash
# Create Repos directory and clone project
mkdir -p ~/Repos
cd ~/Repos
git clone https://github.com/JohnYanez95/hvac-assistant.git
cd hvac-assistant

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install PySpark in virtual environment
pip install pyspark==3.5.2
```

### 8. Docker Installation (Optional)

**Option A: Docker Desktop (Recommended for Windows Users)**

Docker Desktop is the preferred approach for Windows developers because:
- Single installation works across Windows and WSL
- GUI management interface for containers and images
- Automatic WSL2 backend integration
- Better resource management and memory allocation
- Simpler setup and maintenance
- No permission issues or group management needed

**Setup Steps:**
1. Download and install Docker Desktop from https://www.docker.com/products/docker-desktop/
2. In Docker Desktop settings, go to **Resources** → **WSL Integration**
3. Enable integration with Ubuntu-22.04
4. Apply & Restart Docker Desktop
5. Test in WSL: `docker --version`

**Option B: Docker Engine in WSL (Advanced Users)**
```bash
# Install Docker Engine directly in WSL (only if you don't want Docker Desktop)
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Exit and restart WSL to apply group changes
exit
# Then: wsl ~
# Test: docker --version
```

**Note**: Most Windows developers (~80%) use Docker Desktop with WSL integration for the best experience. Choose Docker Engine only if you prefer a pure CLI workflow or have specific requirements.

## Installing Claude Code in WSL

### Node.js Setup (Required for Claude Code)

**⚠️ Important for All Users**: Ubuntu 22.04 comes with Node.js v12.22.9, which is incompatible with Claude Code (requires v18+). You will need to replace Ubuntu's Node.js with a current version. This process may involve package conflicts that require cleanup - this is normal and expected.

**If you already have Node.js installed**, you'll likely need to remove it first (see Troubleshooting section below).

**Option A: NodeSource Repository (Recommended)**
```bash
# Install current Node.js LTS version
curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
sudo apt-get install -y nodejs

# Configure npm global directory
mkdir -p ~/.npm-global
npm config set prefix ~/.npm-global
echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.bashrc
source ~/.bashrc

# Install Claude Code
npm install -g @anthropic-ai/claude-code
```

**Option B: Snap Package (Simpler)**
```bash
# Install Node.js via snap
sudo snap install node --classic

# Configure npm global directory
mkdir -p ~/.npm-global
npm config set prefix ~/.npm-global
echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.bashrc
source ~/.bashrc

# Install Claude Code
npm install -g @anthropic-ai/claude-code
```

**Verify Installation:**
```bash
node --version  # Should show v18+ or v20+
claude --version
```

**Important Note About Ubuntu's Default Node.js:**
Ubuntu 22.04 may come with Node.js v12.22.9 pre-installed or easily installed via `apt`. This version is incompatible with Claude Code (requires v18+). You'll need to replace it with a current version.

### Troubleshooting Node.js Installation Issues

**Problem: Package Conflicts When Installing Node.js**

**⚠️ The Problem:**
You tried to install nodejs and npm via apt, but encountered broken dependencies and conflicts:
- nodejs and npm from Ubuntu's default repos are outdated and incompatible
- npm depends on node-* packages that were not installable
- nodejs and npm also conflicted with each other due to versioning issues and Ubuntu's packaging scheme

**Symptoms:**
```
dpkg: error processing archive ... trying to overwrite '/usr/include/node/common.gypi', 
which is also in package libnode-dev
```

**✅ The Fix: Complete Clean Removal and Proper Installation**
```bash
# Step 1: Fully remove all conflicting packages and configs
sudo apt purge -y nodejs npm        # Fully removed old versions and configs
sudo apt autoremove -y              # Cleared leftover dependencies
sudo apt clean                      # Wiped cached .deb files
sudo apt update --fix-missing       # Fixed the apt index in case of corrupt or missing packages

# Step 2: Install Node.js the proper way via NodeSource
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs

# Step 3: Verify installation
node --version  # Should show v20+
npm --version

# Step 4: Configure npm and install Claude Code
mkdir -p ~/.npm-global
npm config set prefix ~/.npm-global
echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.bashrc
source ~/.bashrc
npm install -g @anthropic-ai/claude-code
```

**Alternative: Use Snap (If NodeSource Still Fails)**
```bash
# Complete removal of all Node.js packages
sudo apt remove --purge nodejs* npm* libnode*
sudo apt autoremove

# Install via snap (isolated, no conflicts)
sudo snap install node --classic

# Configure and install Claude Code
mkdir -p ~/.npm-global
npm config set prefix ~/.npm-global
echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.bashrc
source ~/.bashrc
npm install -g @anthropic-ai/claude-code
```

**Prevention:**
Always check software version requirements before installation and use the appropriate package source from the start.

## VS Code Integration

### Setup VS Code with WSL

1. **Install Extensions**:
   - WSL (ms-vscode-remote.remote-wsl)
   - Remote Development extension pack

2. **Connect to WSL**:
   ```bash
   # From WSL terminal
   cd ~/Repos/hvac-assistant
   source venv/bin/activate
   code .
   ```

3. **Configure Python Environment**:
   - Install Python extension in WSL context
   - Select interpreter: `~/Repos/hvac-assistant/venv/bin/python`

## Verification

### Test Your Environment

```bash
# Check Python version
python3 --version
# Should show: Python 3.10.12

# Check Java version
java -version
# Should show: openjdk version "19.0.2"

# Check PySpark
python3 -c "import pyspark; print(pyspark.__version__)"
# Should show: 3.5.2

# Check environment variables
echo $JAVA_HOME
echo $HADOOP_HOME

# Test Docker (if installed)
docker --version
```

## Troubleshooting

### Common Issues

**WSL starts in wrong directory:**
```bash
# Always use this to start in home directory
wsl ~
# Or add this to ~/.bashrc
echo 'cd ~' >> ~/.bashrc
```

**Permission denied for Docker:**
```bash
# If you installed Docker Engine, restart WSL after adding to docker group
exit
wsl ~
```

**Git shows master instead of main:**
```bash
# Set default branch for new repositories
git config --global init.defaultBranch main
```

**Virtual environment not activating:**
```bash
# Make sure you're in the project directory
cd ~/Repos/hvac-assistant
source venv/bin/activate
```

## File System Navigation

**Key Paths:**
- Linux home: `~/` or `/home/username/`
- Windows files: `/mnt/c/Users/Username/`
- Project location: `~/Repos/hvac-assistant/`

**Accessing Windows files from WSL:**
```bash
# Access your Windows Documents folder
ls /mnt/c/Users/Johnr/Documents/

# Copy files between Windows and WSL
cp /mnt/c/Users/Johnr/file.txt ~/
```

## Performance Tips

- **Keep project files in WSL filesystem** (`~/`) for better performance
- **Use WSL2** instead of WSL1 for Docker compatibility
- **Close unused WSL distributions** to save memory: `wsl --shutdown`

---

## Linux Command Reference

### Essential Commands

| Command | Description | Example |
|---------|-------------|---------|
| `~` | Home directory shortcut | `cd ~` (go to home) |
| `pwd` | Print working directory (current location) | `pwd` |
| `ls` | List files and directories | `ls -la` (detailed list) |
| `cd` | Change directory | `cd ~/Repos` |
| `mkdir` | Create directory | `mkdir -p ~/new/path` |
| `rm` | Remove files/directories | `rm -rf folder/` |
| `cp` | Copy files | `cp file.txt backup.txt` |
| `mv` | Move/rename files | `mv old.txt new.txt` |
| `exit` | Close terminal/logout | `exit` |

### Package Management (apt)

| Command | Description | Example |
|---------|-------------|---------|
| `apt` | Package manager for Ubuntu/Debian | |
| `sudo apt update` | Update package lists | `sudo apt update` |
| `sudo apt upgrade` | Upgrade installed packages | `sudo apt upgrade -y` |
| `sudo apt install` | Install new packages | `sudo apt install git` |
| `sudo apt remove` | Remove packages | `sudo apt remove package-name` |

### File Operations

| Command | Description | Example |
|---------|-------------|---------|
| `cat` | Display file contents | `cat file.txt` |
| `head` | Show first lines of file | `head -10 file.txt` |
| `tail` | Show last lines of file | `tail ~/.bashrc` |
| `grep` | Search text in files | `grep "error" log.txt` |
| `find` | Find files/directories | `find . -name "*.py"` |
| `wget` | Download files from internet | `wget https://example.com/file.zip` |
| `curl` | Transfer data from servers | `curl -fsSL url -o file` |

### Permissions and Users

| Command | Description | Example |
|---------|-------------|---------|
| `sudo` | Run command as administrator | `sudo apt install git` |
| `chmod` | Change file permissions | `chmod +x script.sh` |
| `chown` | Change file ownership | `sudo chown user:group file` |
| `usermod` | Modify user account | `sudo usermod -aG docker $USER` |
| `whoami` | Show current username | `whoami` |
| `groups` | Show user's groups | `groups` |

### Process Management

| Command | Description | Example |
|---------|-------------|---------|
| `ps` | Show running processes | `ps aux` |
| `top` | Show live process activity | `top` |
| `kill` | Terminate process by PID | `kill 1234` |
| `killall` | Terminate process by name | `killall python3` |
| `jobs` | Show background jobs | `jobs` |
| `nohup` | Run command immune to hangups | `nohup python script.py &` |

### Environment and Variables

| Command | Description | Example |
|---------|-------------|---------|
| `echo` | Print text to terminal | `echo "Hello World"` |
| `export` | Set environment variable | `export PATH=$PATH:/new/path` |
| `env` | Show all environment variables | `env` |
| `which` | Show location of command | `which python3` |
| `source` | Execute script in current shell | `source ~/.bashrc` |
| `history` | Show command history | `history` |

### Python-Specific Commands

| Command | Description | Example |
|---------|-------------|---------|
| `python3` | Python 3 interpreter (Linux standard) | `python3 script.py` |
| `python` | May point to Python 2 or 3 (varies) | Usually avoid, use `python3` |
| `pip` | Python package installer | `pip install package` |
| `python3 -m venv` | Create virtual environment | `python3 -m venv myenv` |
| `source venv/bin/activate` | Activate virtual environment | `source venv/bin/activate` |
| `deactivate` | Exit virtual environment | `deactivate` |

### Git Commands

| Command | Description | Example |
|---------|-------------|---------|
| `git clone` | Clone repository | `git clone https://github.com/user/repo.git` |
| `git status` | Show repository status | `git status` |
| `git add` | Stage changes | `git add .` |
| `git commit` | Commit changes | `git commit -m "message"` |
| `git push` | Push to remote | `git push origin main` |
| `git pull` | Pull from remote | `git pull` |
| `git branch` | Show/manage branches | `git branch -a` |

### Docker Commands

| Command | Description | Example |
|---------|-------------|---------|
| `docker --version` | Show Docker version | `docker --version` |
| `docker run` | Run container | `docker run hello-world` |
| `docker ps` | Show running containers | `docker ps -a` |
| `docker images` | Show downloaded images | `docker images` |
| `docker-compose` | Multi-container management | `docker-compose up` |

### File Redirection

| Operator | Description | Example |
|----------|-------------|---------|
| `>` | Redirect output to file (overwrite) | `echo "text" > file.txt` |
| `>>` | Redirect output to file (append) | `echo "text" >> file.txt` |
| `\|` | Pipe output to another command | `ls \| grep "pattern"` |
| `2>` | Redirect error output | `command 2> error.log` |
| `&>` | Redirect both output and errors | `command &> all.log` |

### Special Characters

| Character | Description | Example |
|-----------|-------------|---------|
| `~` | Home directory | `cd ~` |
| `.` | Current directory | `./script.sh` |
| `..` | Parent directory | `cd ..` |
| `/` | Root directory / path separator | `/opt/java/` |
| `*` | Wildcard (matches anything) | `rm *.txt` |
| `$` | Variable prefix | `echo $HOME` |
| `&` | Run command in background | `long-process &` |
| `;` | Command separator | `cd /tmp; ls` |
| `&&` | Run next command if previous succeeds | `make && make install` |

### Key Differences: Windows vs Linux

| Concept | Windows | Linux (WSL) |
|---------|---------|-------------|
| Path separator | `\` (backslash) | `/` (forward slash) |
| Home directory | `C:\Users\Username` | `/home/username` or `~` |
| Admin privileges | "Run as administrator" | `sudo` command |
| Package manager | Windows Store, installers | `apt`, `snap`, etc. |
| File permissions | ACLs | `rwx` permissions |
| Line endings | CRLF (`\r\n`) | LF (`\n`) |
| Case sensitivity | Case-insensitive | Case-sensitive |
| Python command | `python` or `py` | `python3` (python2 vs python3) |

### Tips for Windows Users

1. **Always use `python3`** instead of `python` in Linux
2. **Paths are case-sensitive** - `File.txt` ≠ `file.txt`
3. **Use forward slashes** for paths: `/home/user/file`
4. **No drive letters** - everything starts from `/` (root)
5. **Use `sudo`** instead of "Run as administrator"
6. **Package installation** is usually via `apt install` not downloading `.exe`
7. **Virtual environments** are the standard way to manage Python packages