# WSL2 Setup Guide for HVAC Assistant

## Overview

This comprehensive guide walks you through setting up Windows Subsystem for Linux 2 (WSL2) for the HVAC Assistant project, including all the real-world troubleshooting you'll likely encounter. WSL2 provides a native Linux environment on Windows, making it ideal for Python/ML development with better Docker integration and simpler dependency management.

## Why WSL2 for This Project

- **Consistent Environment**: Same Python/Java/Hadoop versions everywhere
- **Better Docker Integration**: Native Linux container support
- **Simplified Path Handling**: No Windows/Linux path translation issues
- **Package Management**: Native Linux package managers (apt)
- **Development Tools**: Better terminal, shell scripting, and CLI tools

---

## Part I: Initial Setup

### Prerequisites

- Windows 10 version 2004+ or Windows 11
- Administrator access
- At least 4GB free disk space

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
# Configure environment variables in ~/.bashrc
echo 'export JAVA_HOME=/opt/java/current' >> ~/.bashrc
echo 'export HADOOP_HOME=/opt/hadoop/current' >> ~/.bashrc
echo 'export PATH=$PATH:$JAVA_HOME/bin:$HADOOP_HOME/bin' >> ~/.bashrc
source ~/.bashrc

# Clean up downloads
rm /tmp/*.tar.gz
```

### 6. Configure Git

```bash
# Configure git (replace with your information)
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
git config --global init.defaultBranch main

# Optional: Cache credentials
git config --global credential.helper store
```

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

### 8. Docker Installation

**Recommended: Docker Desktop**

Docker Desktop is preferred for Windows developers because:
- Single installation works across Windows and WSL
- GUI management interface
- Automatic WSL2 integration
- Better resource management

**Setup Steps:**
1. Download and install Docker Desktop from https://www.docker.com/products/docker-desktop/
2. In Docker Desktop settings, go to **Resources** → **WSL Integration**
3. Enable integration with Ubuntu-22.04
4. Apply & Restart Docker Desktop
5. Restart WSL session: `exit` then `wsl ~`
6. Test in WSL: `docker --version`

**Container Access from Windows Browser:**
When running containers in WSL, use `http://127.0.0.1:PORT` instead of `http://localhost:PORT` to access them from Windows browsers. The `localhost` resolution sometimes fails in the WSL-Windows bridge, while `127.0.0.1` works reliably.

---

## Part II: Installing Claude Code

### Node.js Setup

**⚠️ Critical**: Ubuntu 22.04's default Node.js (v12.22.9) is incompatible with Claude Code (requires v18+).

#### Option A: NodeSource Repository (Recommended)

```bash
# Install current Node.js LTS
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

#### Option B: Snap Package

```bash
# Install Node.js via snap
sudo snap install node --classic

# Configure npm and install Claude Code
mkdir -p ~/.npm-global
npm config set prefix ~/.npm-global
echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.bashrc
source ~/.bashrc
npm install -g @anthropic-ai/claude-code
```

**Verify Installation:**
```bash
node --version  # Should show v18+ or v20+
claude --version
```

---

## Part III: Troubleshooting

### VPN and Claude Code Connectivity Issues

#### Problem 1: Basic VPN Blocking

**Symptoms**: Claude Code shows "offline mode" when VPN is active

**Solution**: Configure VPN split tunneling

**For NordVPN:**
1. **Enable Split Tunneling** in VPN settings
2. **Select "Bypass VPN for selected apps"**
3. **Add these applications**:
   - `powershell.exe` (`C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe`)
   - `wsl.exe` (`C:\Windows\System32\wsl.exe`)

**Test procedure:**
1. Configure split tunneling
2. Close PowerShell completely and open a new one
3. Run `wsl ~`
4. Test: `claude --version`

#### Problem 2: IPv6 Black-hole Issue

**Symptoms**: Even with split tunneling, Claude Code timeouts when connecting

**Root Cause**: VPN providers often don't support IPv6, creating a black-hole where WSL tries IPv6 first (times out), before falling back to IPv4.

**Solution: Disable IPv6 in WSL**

```bash
# Test if IPv6 is the issue (should timeout with VPN on)
curl -6 --connect-timeout 5 https://api.anthropic.com

# Disable IPv6 immediately
sudo sysctl -w net.ipv6.conf.all.disable_ipv6=1
sudo sysctl -w net.ipv6.conf.default.disable_ipv6=1

# Make persistent across reboots
echo 'net.ipv6.conf.all.disable_ipv6=1' | sudo tee /etc/sysctl.d/99-disable-ipv6.conf
echo 'net.ipv6.conf.default.disable_ipv6=1' | sudo tee -a /etc/sysctl.d/99-disable-ipv6.conf

# Restart WSL
exit
```

In PowerShell:
```cmd
wsl --shutdown
wsl ~
```

**Verification:**
```bash
claude --version  # Should connect immediately
```

**Alternative (Less Aggressive): IPv4 Preference**
```bash
# Prefer IPv4 when both IPv4/IPv6 exist, without disabling IPv6
sudo sed -i 's/^#precedence ::ffff:0:0\/96  100/precedence ::ffff:0:0\/96  100/' /etc/gai.conf
```

**Rollback IPv6 Disable:**
```bash
sudo sysctl -w net.ipv6.conf.all.disable_ipv6=0
sudo sysctl -w net.ipv6.conf.default.disable_ipv6=0
sudo rm /etc/sysctl.d/99-disable-ipv6.conf
sudo sysctl --system
```

### Node.js Installation Issues

#### Problem: Package Conflicts

**Symptoms:**
```
dpkg: error processing archive ... trying to overwrite '/usr/include/node/common.gypi', 
which is also in package libnode-dev
```

**Solution: Complete Clean Removal**
```bash
# Remove all conflicting packages
sudo apt purge -y nodejs npm libnode*
sudo apt autoremove -y
sudo apt clean
sudo apt update --fix-missing

# Install via NodeSource
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs

# Configure and install Claude Code
mkdir -p ~/.npm-global
npm config set prefix ~/.npm-global
echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.bashrc
source ~/.bashrc
npm install -g @anthropic-ai/claude-code
```

### GitHub Authentication

**Important**: GitHub no longer accepts passwords - use Personal Access Tokens (PAT):

1. **Create PAT**: GitHub.com → Profile → Settings → Developer settings → Personal access tokens → Generate new token
2. **Scopes**: Check `repo` for full repository access
3. **Usage**: When Git prompts for password, paste your PAT token
4. **Credential Caching**: With `git config --global credential.helper store`, Git saves PAT after first use

**VPN Considerations**: GitHub may re-prompt for credentials when VPN status changes (security feature)

### Common WSL Issues

**WSL starts in wrong directory:**
```bash
# Always start in home directory
wsl ~
```

**Virtual environment not activating:**
```bash
cd ~/Repos/hvac-assistant
source venv/bin/activate
```

**Permission denied for Docker:**
```bash
# Restart WSL after adding to docker group
exit
wsl ~
```

---

## Part IV: Verification & Completion

### Environment Verification

```bash
# Check Python version
python3 --version
# Expected: Python 3.10.12

# Check Java version  
java -version
# Expected: openjdk version "19.0.2"

# Check PySpark
python3 -c "import pyspark; print(pyspark.__version__)"
# Expected: 3.5.2

# Check environment variables
echo $JAVA_HOME
echo $HADOOP_HOME

# Check Docker (if installed)
docker --version

# Check Claude Code
claude --version
```

### VS Code Integration

1. **Install Extensions**:
   - WSL (ms-vscode-remote.remote-wsl)
   - Remote Development extension pack

2. **Connect to WSL**:
   ```bash
   cd ~/Repos/hvac-assistant
   source venv/bin/activate
   code .
   ```

3. **Configure Python Environment**:
   - Install Python extension in WSL context
   - Select interpreter: `~/Repos/hvac-assistant/venv/bin/python`

---

## Setup Completion Checklist

- [ ] WSL2 with Ubuntu 22.04 installed
- [ ] Python 3.10.12 available (`python3 --version`)
- [ ] Java JDK 19 installed (`java -version`)
- [ ] Hadoop 3.3.5 configured (`echo $HADOOP_HOME`)
- [ ] Environment variables set in `~/.bashrc`
- [ ] Git configured with name/email
- [ ] Project cloned to `~/Repos/hvac-assistant/`
- [ ] Virtual environment created and PySpark installed
- [ ] Docker Desktop integrated with WSL (optional)
- [ ] Node.js v18+ installed (`node --version`)
- [ ] Claude Code installed and connecting (`claude --version`)
- [ ] VPN connectivity issues resolved (if applicable)
- [ ] VS Code WSL integration working (optional)

---

## File System Navigation

**Key Paths:**
- Linux home: `~/` or `/home/username/`
- Windows files: `/mnt/c/Users/Username/`
- Project location: `~/Repos/hvac-assistant/`

**Performance Tips:**
- Keep project files in WSL filesystem (`~/`) for better performance
- Use WSL2 for Docker compatibility
- Close unused WSL distributions: `wsl --shutdown`

---

## Linux Command Reference

### Essential Commands

| Command | Description | Example |
|---------|-------------|---------|
| `~` | Home directory shortcut | `cd ~` |
| `pwd` | Print working directory | `pwd` |
| `ls` | List files | `ls -la` |
| `cd` | Change directory | `cd ~/Repos` |
| `mkdir` | Create directory | `mkdir -p ~/new/path` |
| `rm` | Remove files/directories | `rm -rf folder/` |
| `cp` | Copy files | `cp file.txt backup.txt` |
| `mv` | Move/rename files | `mv old.txt new.txt` |

### Package Management

| Command | Description | Example |
|---------|-------------|---------|
| `sudo apt update` | Update package lists | `sudo apt update` |
| `sudo apt upgrade` | Upgrade packages | `sudo apt upgrade -y` |
| `sudo apt install` | Install packages | `sudo apt install git` |
| `sudo apt remove` | Remove packages | `sudo apt remove package` |

### Python Commands

| Command | Description | Example |
|---------|-------------|---------|
| `python3` | Python 3 interpreter | `python3 script.py` |
| `pip` | Package installer | `pip install package` |
| `python3 -m venv` | Create virtual environment | `python3 -m venv myenv` |
| `source venv/bin/activate` | Activate venv | `source venv/bin/activate` |
| `deactivate` | Exit venv | `deactivate` |

### Key Differences: Windows vs Linux

| Concept | Windows | Linux (WSL) |
|---------|---------|-------------|
| Path separator | `\` | `/` |
| Home directory | `C:\Users\Username` | `~` |
| Admin privileges | "Run as administrator" | `sudo` |
| Python command | `python` or `py` | `python3` |
| Case sensitivity | No | Yes |

---

**🎉 Congratulations!** Your WSL2 development environment is now ready for the HVAC Assistant project. You have a robust, Linux-based development setup that handles the complexities of Python/ML development while maintaining compatibility with your Windows workflow.