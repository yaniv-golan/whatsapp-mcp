# WhatsApp MCP

A WhatsApp Multi-Client Protocol (MCP) server for integrating WhatsApp with Anthropic's Claude.

## Installation

### Prerequisites

- Go
- Python 3.6+
- Anthropic Claude Desktop app
- UV (Python package manager), install with `curl -LsSf https://astral.sh/uv/install.sh | sh`

### Steps

1. **Clone this repository**

   ```bash
   git clone https://github.com/yourusername/whatsapp-mcp.git
   cd whatsapp-mcp
   ```

2. **Run the WhatsApp bridge**

   Navigate to the whatsapp-bridge directory and run the Go application:

   ```bash
   cd whatsapp-bridge
   go run main.go
   ```

   The first time you run it, you will be prompted to scan a QR code. Scan the QR code with your WhatsApp mobile app to authenticate.

   After approximately 20 days, you will might need to re-authenticate.

3. **Connect to Anthropic Claude**

   Copy the `claude_desktop_config.example.json` file with your updated path to the WhatsApp MCP server to your Claude Desktop configuration directory at:

   ```json
   {
     "mcpServers": {
       "whatsapp": {
         "command": "{{PATH}}/.local/bin/uv",
         "args": [
           "--directory",
           "{{PATH}}/whatsapp-mcp/whatsapp-mcp-server",
           "run",
           "main.py"
         ]
       }
     }
   }
   ```

   Save this as `claude_desktop_config.json` in your Claude Desktop configuration directory at:

   ```
   ~/Library/Application Support/Claude/claude_desktop_config.json
   ```

4. **Restart Claude Desktop**

   Open Claude Desktop and you should now see WhatsApp as an available integration.

## Architecture Overview

This application consists of two main components:

1. **Go WhatsApp Bridge** (`whatsapp-bridge/`): A Go application that connects to WhatsApp's web API, handles authentication via QR code, and stores message history in SQLite. It serves as the bridge between WhatsApp and the MCP server.

2. **Python MCP Server** (`whatsapp-mcp-server/`): A Python server implementing the Model Context Protocol (MCP), which provides standardized tools for Claude to interact with WhatsApp data and send/receive messages.

### WhatsApp Bridge (Go)

The Go application:

- Handles WhatsApp authentication via QR code scanning
- Maintains a persistent connection to WhatsApp's servers
- Processes incoming and outgoing messages
- Stores all chat and message data in a SQLite database (`store/messages.db`)
- Provides endpoints for the Python MCP server to query and send messages

### MCP Server (Python)

The Python server:

- Implements the MCP protocol for Claude integration
- Provides standardized tools for Claude to:
  - Search contacts
  - List messages and chats
  - Retrieve message context
  - Send messages
- Communicates with the Go bridge to access WhatsApp data
- Handles data formatting and presentation for Claude

### Data Storage

- All message history is stored in a SQLite database within the `whatsapp-bridge/store/` directory
- The database maintains tables for chats and messages
- Messages are indexed for efficient searching and retrieval

## Usage

Once connected, you can interact with your WhatsApp contacts through Claude, leveraging Claude's AI capabilities in your WhatsApp conversations.

### MCP Tools

Claude can access the following tools to interact with WhatsApp:

- **search_contacts**: Search for contacts by name or phone number
- **list_messages**: Retrieve messages with optional filters and context
- **list_chats**: List available chats with metadata
- **get_chat**: Get information about a specific chat
- **get_direct_chat_by_contact**: Find a direct chat with a specific contact
- **get_contact_chats**: List all chats involving a specific contact
- **get_last_interaction**: Get the most recent message with a contact
- **get_message_context**: Retrieve context around a specific message
- **send_message**: Send a WhatsApp message to a specified phone number

## Technical Details

### Starting the Service

The application starts both components via the `start.sh` script:

1. The Go bridge launches and connects to WhatsApp
2. The Python MCP server starts and connects to the Go bridge
3. Claude Desktop connects to the MCP server via the configuration

### Communication Flow

1. Claude sends requests to the Python MCP server
2. The MCP server queries the Go bridge for WhatsApp data
3. The Go bridge accesses the SQLite database or the WhatsApp API
4. Data flows back through the chain to Claude
5. When sending messages, the request flows from Claude through the MCP server to the Go bridge and to WhatsApp

## Troubleshooting

- If you encounter permission issues when running uv, you may need to add it to your PATH or use the full path to the executable.
- Make sure both the Go application and the Python server are running for the integration to work properly.

### Authentication Issues

- **QR Code Not Displaying**: If the QR code doesn't appear, try restarting the authentication script. If issues persist, check if your terminal supports displaying QR codes.
- **Authentication Timeout**: If the QR code times out before you can scan it, simply restart the authenticate.sh script.
- **WhatsApp Already Logged In**: If your session is already active, the Go bridge will automatically reconnect without showing a QR code.
- **Device Limit Reached**: WhatsApp limits the number of linked devices. If you reach this limit, you'll need to remove an existing device from WhatsApp on your phone (Settings > Linked Devices).
- **No Messages Loading**: After initial authentication, it can take several minutes for your message history to load, especially if you have many chats.

For additional Claude Desktop integration troubleshooting, see the [MCP documentation](https://modelcontextprotocol.io/quickstart/server#claude-for-desktop-integration-issues). The documentation includes helpful tips for checking logs and resolving common issues.
