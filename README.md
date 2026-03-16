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
git clone https://github.com/YOURNAME/cue-agent.git
cd cue-agent
```

Run the install script:

```
./scripts/install.sh
```

## Running CUE

```
./scripts/run.sh
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