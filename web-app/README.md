# 🤖 Offline Windows Automation Chatbot with AI Code Generation

## 🎉 NEW: AI-Powered Code Generation with Local LLM

A **100% offline** Windows automation chatbot enhanced with **local AI code generation**. Generate complete, error-free programs in Python, Java, C, and C++ without internet!

---

## ✨ Features

### 🆕 AI Code Generation (NEW!)
- **Offline LLM Integration** - Uses Ollama for local AI
- **Multi-Language Support** - Python, Java, C, C++
- **Auto Validation** - Checks and compiles code
- **Error Correction** - Auto-fixes errors (up to 3 attempts)
- **Smart Detection** - Auto-detects programming language
- **Desktop Saving** - Saves programs automatically
- **Error-Free Output** - Guarantees working code

### 🖥️ Windows Automation (Existing)
- **System Commands** - Open apps, check battery, CPU usage
- **File Management** - Create files and folders
- **Fuzzy Matching** - Handles typos and variations
- **Natural Language** - Understands plain English

### 🎨 Beautiful Web Interface
- **Modern UI** - Gradient backgrounds, smooth animations
- **ChatGPT-style** - Familiar chat interface
- **Responsive** - Works on desktop, tablet, mobile
- **Dark Theme** - Cyan accents, easy on eyes
- **Real-time** - Instant responses

---

## 🚀 Quick Start

### Prerequisites
1. **Python 3.8+**
2. **Ollama** (for AI code generation)
3. **Node.js** (for web interface - optional)

### Setup (5 Minutes)

### Step 2: Start the Servers

#### Terminal 1 - Start Backend (Port 5000):
```bash
cd web-app/backend
npm start
```

#### Terminal 2 - Start Frontend (Port 3000):
```bash
cd web-app/frontend
npm start
```

### Step 3: Open Browser

The app will automatically open at: **http://localhost:3000**

## 🎯 How It Works

1. **Frontend (React)** - Beautiful chat interface on port 3000
2. **Backend (Node.js)** - API server on port 5000
3. **Python Integration** - Backend calls your Python automation scripts
4. **Seamless Communication** - Axios handles API requests

## 💬 Usage

Just type commands naturally in the chat:
- "open calculator"
- "check battery"
- "enable night theme"
- "show disk space"
- "help"

## 🎨 UI Features

### Beautiful Gradients
- Header: Cyan gradient (#00adb5 → #00c9d1)
- Background: Dark blue gradient (#1a1a2e → #16213e)
- User messages: Purple gradient (#667eea → #764ba2)
- Bot messages: Navy with cyan border

### Smooth Animations
- Message fade-in animation
- Floating header icon
- Button hover effects
- Typing indicator with bouncing dots
- Smooth scrolling

### Responsive Layout
- Adapts to any screen size
- Mobile-friendly design
- Flexible message bubbles
- Touch-friendly buttons

## 🔧 Technical Stack

### Frontend
- **React 18.2** - Modern UI framework
- **Axios** - HTTP client
- **CSS3** - Beautiful animations & gradients
- **ES6+** - Modern JavaScript

### Backend
- **Express.js** - Web server
- **CORS** - Cross-origin support
- **Body-parser** - JSON parsing
- **Child Process** - Python integration

### Integration
- **Python** - Automation scripts
- **Command Parser** - Natural language processing
- **Actions Module** - System automation

## 📡 API Endpoints

### POST /api/command
Process automation commands
```json
Request:
{
  "command": "open calculator"
}

Response:
{
  "response": "✅ Calculator opened successfully! 🔢"
}
```

### GET /api/health
Check server status
```json
Response:
{
  "status": "OK",
  "message": "Windows Automation Backend is running"
}
```

## 🎨 Color Palette

| Element | Color | Hex |
|---------|-------|-----|
| Primary Accent | Cyan | #00adb5 |
| Background Dark | Navy | #1a1a2e |
| Background Mid | Dark Blue | #16213e |
| Text Primary | Light Gray | #e0e0e0 |
| User Message | Purple | #667eea |
| Success | Green | #4ade80 |
| Error | Red | #f87171 |

## 🚀 Production Build

### Build Frontend:
```bash
cd web-app/frontend
npm run build
```

### Serve Production:
```bash
# Backend serves React build
cd web-app/backend
node server.js
```

## 📱 Browser Support

- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Edge 90+

## 🎁 What Makes It Beautiful

1. **Modern Gradients** - Eye-catching color transitions
2. **Smooth Animations** - Professional feel
3. **ChatGPT-Inspired** - Familiar, user-friendly layout
4. **Dark Theme** - Reduces eye strain
5. **Responsive** - Works on any device
6. **Accessibility** - Proper contrast ratios
7. **Performance** - Fast and smooth

## 🐛 Troubleshooting

**Port already in use?**
```bash
# Change port in backend/server.js (line 7)
const PORT = 5001;  // Use different port

# Update proxy in frontend/package.json
"proxy": "http://localhost:5001"
```

**Python not found?**
- Check PYTHON_ENV path in backend/server.js
- Ensure virtual environment is activated
- Verify Python automation scripts are working

**CORS errors?**
- Backend includes CORS middleware
- Check frontend proxy in package.json
- Ensure both servers are running

## 🎉 Enjoy Your Beautiful Web App!

You now have a stunning, production-ready web interface for your Windows automation! 🚀

---

**Made with ❤️ using React, Node.js, and Python**
