# ⚡ RenameBot

> Ultra-fast Telegram RenameBot with auto-rename, metadata injection, custom thumbnails & channel forwarding

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Pyrogram](https://img.shields.io/badge/Pyrogram-Latest-green.svg)](https://pyrogram.org/)

## 📋 Features

- ⚡ **Ultra-Fast Processing** - Lightning-quick file renaming with 200 concurrent workers
- 🏷️ **Auto-Rename** - Automatically rename files as documents or videos
- 📝 **Metadata Injection** - Add custom metadata (title, author, artist) to files using FFmpeg
- 🖼️ **Custom Thumbnails** - Set and use custom thumbnails for your renamed files
- 📤 **Channel Forwarding** - Auto-forward renamed files to your designated channel
- 📄 **Dual Format Support** - Handle both document and video file formats
- ✨ **Custom Captions** - Set custom captions with dynamic variables (`{name}`, `{size}`)
- 🔐 **User Database** - Track users and their custom settings with MongoDB support
- 🎬 **FFmpeg Integration** - Advanced media processing and metadata manipulation

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- Telegram Bot Token (from [@BotFather](https://t.me/botfather))
- Telegram API credentials (API_ID & API_HASH from [my.telegram.org](https://my.telegram.org/))
- FFmpeg installed (for metadata injection)
- Docker (optional, for containerized deployment)

### Installation

#### Method 1: Local Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/Beesonn/RenameBot.git
   cd RenameBot
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install FFmpeg**
   - **Ubuntu/Debian**: `sudo apt-get install ffmpeg`
   - **macOS**: `brew install ffmpeg`
   - **Windows**: Download from [ffmpeg.org](https://ffmpeg.org/download.html)

5. **Set environment variables**
   ```bash
   export API_ID=your_api_id
   export API_HASH=your_api_hash
   export BOT_TOKEN=your_bot_token
   ```

6. **Run the bot**
   ```bash
   python -m bot
   ```

#### Method 2: Docker Deployment

1. **Build the image**
   ```bash
   docker build -t renamebot .
   ```

2. **Run the container**
   ```bash
   docker run -e API_ID=your_api_id \
     -e API_HASH=your_api_hash \
     -e BOT_TOKEN=your_bot_token \
     renamebot
   ```

## 📖 Usage

### Basic Commands

Send a file (document or video) to the bot to start renaming:

- **`/start`** - Initialize the bot and view the main menu
- **`/help`** - View detailed help and command information

### Configuration Commands

- **`/setchannel`** - Set the channel where renamed files are forwarded
  - Bot must be an admin with posting permissions in the channel

- **`/delchannel`** - Remove the channel setting (files go back to PM)

- **`/setcaption`** - Set custom captions for files
  - Use `{name}` - file name without extension
  - Use `{size}` - file size in human-readable format
  - Example: `/setcaption 📁 File: {name}\n📊 Size: {size}`

- **`/delcaption`** - Remove custom caption

- **`/setmetadata`** - Add metadata to files (title, author, artist)
  - Example: `/setmetadata Uploaded by @FileRenameebot`

- **`/delmetadata`** - Remove metadata setting

- **`/autorename`** - Enable automatic renaming mode
  - Choose between Document or Video format
  - Files are automatically renamed and uploaded without manual input

- **`/setthumb`** - Set custom thumbnail by sending a photo

- **`/delthumb`** - Remove custom thumbnail

### Workflow

1. **Manual Rename**
   - Send a file → Provide new filename → Select format (Document/Video) → Done!

2. **Auto-Rename**
   - Enable `/autorename` and select format
   - Send files → Bot automatically renames, adds metadata, applies thumbnail
   - Files are uploaded to PM or your channel

3. **Metadata & Captions**
   - Configure `/setmetadata` and `/setcaption`
   - Metadata is embedded in file (requires FFmpeg)
   - Captions are added to Telegram messages

## 🏗️ Project Structure

```
RenameBot/
├── bot/
│   ├── __init__.py          # Bot initialization and configuration
│   ├── __main__.py          # Entry point
│   ├── alt/                 # Helper functions and utilities
│   ├── database/            # Database operations
│   └── plugins/
│       ├── rename.py        # Core renaming logic
│       ├── start.py         # Start and help commands
│       ├── set_channel.py   # Channel management
│       └── utils_cmds.py    # Utility commands
├── Dockerfile              # Container configuration
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `API_ID` | Telegram API ID | ✅ Yes |
| `API_HASH` | Telegram API Hash | ✅ Yes |
| `BOT_TOKEN` | Bot token from BotFather | ✅ Yes |

### Bot Configuration

Edit `bot/__init__.py` to customize:
- Number of workers (default: 200)
- Sleep threshold (default: 15)
- Plugins root directory

## 📦 Dependencies

- **pyrogram** - Telegram Bot API framework
- **kurigram** - Additional utilities
- **tgcrypto** - Telegram encryption
- **motor** - Async MongoDB driver (for database operations)

See `requirements.txt` for exact versions.

## ⚠️ Important Notes

### File Size Limits
- Maximum file size for renaming: **2GB**
- Larger files will be rejected with a notification

### Metadata Processing
- Metadata injection uses FFmpeg and re-encodes the file
- This increases processing time and file size
- Metadata is embedded in: title, author, artist, and stream-specific tags

### Channel Forwarding
- Bot must be added to the channel as an **Admin**
- Bot must have **Post Messages** permission
- If forwarding fails, files are sent to PM instead

### Filename Cleaning (Auto-Rename)
The auto-rename function removes:
- Telegram handles (@username)
- URLs
- Common spam words (join, channel, download, exclusive, etc.)
- Extra spaces and special characters

## 🤝 Support

- **Support Chat**: [@XBOTSUPPORTS](https://t.me/XBOTSUPPORTS)
- **Update Channel**: [@BeesonsBots](https://t.me/BeesonsBots)
- **Demo Bot**: [@FileRenameebot](https://t.me/FileRenameebot)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🎯 Performance

- **Workers**: 200 concurrent operations
- **Max Upload Speed**: Limited by Telegram API
- **Processing Speed**: Near-instant file renaming
- **Metadata Processing**: Depends on file size (FFmpeg operation)

## 🐛 Troubleshooting

### Bot doesn't respond
- Verify API_ID, API_HASH, and BOT_TOKEN are correct
- Check internet connection
- Ensure the bot is added as a private user

### Metadata not added
- Install FFmpeg: `sudo apt-get install ffmpeg`
- Check FFmpeg is in PATH: `ffmpeg -version`
- Verify file is not corrupted

### Channel forwarding fails
- Confirm bot is admin in the target channel
- Check bot has "Post Messages" permission
- Verify channel ID is correct

### Files exceed 2GB limit
- File size limit is enforced for performance
- Consider splitting large files

## 🚦 Status

- ✅ Core functionality working
- ✅ Metadata injection functional
- ✅ Channel forwarding implemented
- ✅ Custom thumbnails supported
- ✅ Auto-rename mode available

---

**Made with ❤️ by [Beesonn](https://github.com/Beesonn)**

