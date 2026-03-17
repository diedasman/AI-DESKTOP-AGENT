#!/bin/bash
cd ~/AI-DESKTOP-AGENT
source venv/bin/activate

# Kill old Ollama server if running
OLD_PID=$(lsof -t -i:11434)
if [ ! -z "$OLD_PID" ]; then
    echo "Killing old Ollama server (PID $OLD_PID)..."
    kill -9 $OLD_PID
fi

# Start Ollama server
echo "Starting Ollama server..."
ollama serve &
sleep 3  # give it time to start

# Run the agent
python -m cue.main