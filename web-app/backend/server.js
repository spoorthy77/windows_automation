const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');
const { spawn } = require('child_process');
const path = require('path');

const app = express();
const PORT = 5000;

// Middleware
app.use(cors());
app.use(bodyParser.json());

// Path to Python automation project
const PYTHON_PROJECT_PATH = path.join(__dirname, '..', '..');
const PYTHON_ENV = path.join(PYTHON_PROJECT_PATH, 'automation_env', 'Scripts', 'python.exe');

// API endpoint to process commands
app.post('/api/command', async (req, res) => {
    const { command } = req.body;

    if (!command) {
        return res.status(400).json({ error: 'Command is required' });
    }

    try {
        // Create a temporary Python script to execute the command
        const pythonScript = `
import sys
sys.path.append('${PYTHON_PROJECT_PATH.replace(/\\/g, '\\\\')}')
from command_parser import parse_command

command = """${command.replace(/"/g, '\\"')}"""
result = parse_command(command)
print(result)
`;

        const python = spawn(PYTHON_ENV, ['-c', pythonScript], {
            cwd: PYTHON_PROJECT_PATH
        });

        let output = '';
        let errorOutput = '';

        python.stdout.on('data', (data) => {
            output += data.toString();
        });

        python.stderr.on('data', (data) => {
            errorOutput += data.toString();
        });

        python.on('close', (code) => {
            if (code !== 0 && errorOutput) {
                return res.status(500).json({ 
                    error: 'Command execution failed', 
                    details: errorOutput 
                });
            }

            // Handle special responses
            const response = output.trim();
            
            if (response === 'EXIT') {
                return res.json({ 
                    response: '👋 Goodbye! Refresh the page to start a new session.',
                    special: 'EXIT'
                });
            }

            if (response === 'CLEAR') {
                return res.json({ 
                    response: '🧹 Chat cleared!',
                    special: 'CLEAR'
                });
            }

            res.json({ response });
        });

    } catch (error) {
        console.error('Error:', error);
        res.status(500).json({ 
            error: 'Internal server error', 
            details: error.message 
        });
    }
});

// Health check endpoint
app.get('/api/health', (req, res) => {
    res.json({ status: 'OK', message: 'Windows Automation Backend is running' });
});

app.listen(PORT, () => {
    console.log(`🚀 Backend server running on http://localhost:${PORT}`);
    console.log(`📡 API endpoint: http://localhost:${PORT}/api/command`);
    console.log(`🐍 Python path: ${PYTHON_ENV}`);
});
