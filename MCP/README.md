# MCP Servers for AI-Assisted Network Operations

This component is maintained in a separate repository:

## [network-mcp-docker-suite](https://github.com/pamosima/network-mcp-docker-suite)

Docker-based MCP server suite for AIOps - enabling AI-driven network operations through:

| Server | Port | Purpose |
|--------|------|---------|
| **Catalyst Center MCP** | 8002 | Enterprise network management, device inventory, assurance data |
| **NetBox MCP** | 8001 | DCIM/IPAM documentation, infrastructure source of truth |
| **IOS XE MCP** | 8003 | Direct SSH-based device configuration and troubleshooting |

### Quick Start

```bash
# Clone the MCP server suite
git clone https://github.com/pamosima/network-mcp-docker-suite.git
cd network-mcp-docker-suite

# Configure and deploy
cp .env.example .env
# Edit .env with your credentials
./deploy.sh start cisco
```

For full documentation, visit the [Network MCP Docker Suite repository](https://github.com/pamosima/network-mcp-docker-suite).
