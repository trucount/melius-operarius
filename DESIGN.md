# Melius Engine Design

## Overview
Melius Engine is an autonomous AI agent designed to run as a GitHub Action every 7 minutes. It analyzes the repository, identifies improvements, applies changes, and verifies them.

## Core Components
1.  **GitHub Action Workflow**: Scheduled to run every 7 minutes.
2.  **Agent Core**: Python-based system that manages the lifecycle of an improvement cycle.
3.  **LLM Interface**: Connects to OpenRouter with support for multiple API keys and fallback models.
4.  **File Manager**: Handles reading and writing files outside the `melius-engine` directory.
5.  **State Manager**: Tracks history, logs, to-dos, and errors.

## Directory Structure
- `melius-engine/`: Contains the agent's source code.
- `log/`: Stores improvement logs.
- `to-do/`: Stores pending improvements or errors to be addressed.
- `error/`: Stores persistent errors.
- `history/`: Stores chat history between the system and LLM.

## Agent Workflow
1.  **Initialization**: Load API keys and history. Check for existing to-dos or errors.
2.  **Analysis**: Scan all files (excluding `melius-engine`).
3.  **Planning**: LLM identifies improvements and logs them in `/log`.
4.  **Execution**: LLM edits files one by one.
5.  **Verification**: System checks if improvements were applied and if errors were introduced.
6.  **Error Handling**: If an error is found, the LLM attempts to fix it once.
7.  **Final Logging**: If errors persist, log to `/error`. If improvements are pending, log to `/to-do`.

## LLM Communication
- **Format**: Strict JSON.
- **Role**: System acts as the orchestrator; LLM acts as the intelligence.
- **Fallback**: Rotates through 5 API keys and a list of free models on failure.
