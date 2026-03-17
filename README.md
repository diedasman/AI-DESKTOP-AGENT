# CUE – Cognitive User Engine

CUE is a lightweight local AI agent designed to run on small Linux systems like the Raspberry Pi using Ollama-based LLMs.

The goal is to create a modular local AI assistant that can:

* chat with the user
* generate files
* execute tools
* operate as a local automation agent

## Requirements

* Linux (tested on Raspberry Pi OS)
* Python 3.10+
* Ollama installed
* A lightweight model such as:

qwen2.5:1.5b

## Installation

Clone the repo:

```
git clone https://github.com/diedasman/AI-DESKTOP-AGENT.git
```

Run the install script:

```
./scripts/install.sh
```

## Running CUE

```
./scripts/run.sh
```

If you run CUE over SSH, tmux, or on a Raspberry Pi terminal and notice screen flicker, CUE now keeps Rich's full-screen UI but disables background auto-refresh for those remote terminal sessions. You can also force that behavior manually with:

```
CUE_AUTO_REFRESH=0 ./scripts/run.sh
```

## Updating on a device

```
./scripts/update.sh
```

This pulls the newest version from Git and restarts the agent.

## Project Layout

cue/
Core Python modules

scripts/
Deployment and update scripts

examples/
Prompt examples
