# Claworc - OpenClaw Orchestrator

**Source:** https://github.com/gluk-w/claworc
**Date:** 2026-03-01
**Ownership note:** Community-contributed showcase. Preserve the source attribution and do not rewrite this as the runbook author's personal setup.

## What It Does

Run multiple OpenClaw instances from a single web dashboard.

## Key Features

- **Multi-instance management** - One dashboard for all instances
- **Container isolation** - Each instance in its own container
- **SSH security** - Key-based auth, encrypted API keys
- **Access control** - Admin/user roles, biometric auth
- **Live browser** - Watch agent work in real-time

## Architecture

```
Browser → Control Plane → [SSH tunnel] → Agent Container
                                    → :3000 (VNC)
                                    → :18789 (Gateway)
```

## Security Layers

1. SSH key auth only (no passwords)
2. Key rotation support
3. No direct agent access
4. Per-instance IP whitelist
5. Rate limiting
6. Audit logging
7. Encrypted API keys at rest

## Use Cases

- Team deployment (each person gets own agent)
- Data analysis instance
- IT support bot
- Isolated sensitive operations

## Potential Runbook Fit

- Could use for better security isolation
- Future: multi-user access
- Aligns with runbook security patterns

---

*Alternative to running everything on Raspberry Pi*

---

## Setup Steps

Before using these commands, compare them with the current Claworc repository. This showcase is a starting point, not a guarantee that the upstream project still uses the exact same config.

### Prerequisites

- Docker installed on host machine
- SSH key pair for remote access
- At least 2GB RAM per OpenClaw instance
- Git installed

### Installation

```bash
# Clone the Claworc repository
git clone https://github.com/gluk-w/claworc.git
cd claworc

# Copy example configuration
cp config.example.yaml config.yaml

# Edit configuration with your settings
nano config.yaml
```

### Configuration

```yaml
# config.yaml
instances:
  - name: primary
    container: openclaw-primary
    port: 18789
    ssh_port: 2222
    vnc_port: 3000

  - name: analysis
    container: openclaw-analysis
    port: 18790
    ssh_port: 2223
    vnc_port: 3001

security:
  ssh_key_path: ~/.ssh/id_rsa
  api_key_encryption: enabled
  rate_limit: 100/hour

access_control:
  admin_users:
    - your-email@example.com
  require_biometric: false
```

### Running

```bash
# Start all instances
docker-compose up -d

# Access dashboard
# Open http://localhost:8080 in browser

# View logs
docker-compose logs -f
```

### Verifying Setup

```bash
# Check all containers running
docker ps | grep openclaw

# Test SSH access to instance
ssh -p 2222 user@localhost

# Check gateway health
curl http://localhost:18789/health
```

### Maintenance

```bash
# Stop all instances
docker-compose down

# Update to latest version
git pull
docker-compose pull
docker-compose up -d
```

### Uninstallation

```bash
# Stop and remove containers
docker-compose down -v

# Remove repository
cd ..
rm -rf claworc
```
