# PyAI
The future arrives, one step at a time.

Running the agent

Chat-only helper (default)

Uses Gemma with the free Google API tier. No tools – just conversation and guidance.

python main_gemma.py


## Installation

Requirements:

- Python 3.12 (or your actual version)
- `pip`
- A Bash-like terminal

Create and activate a virtual environment, then install dependencies:

python3 -m venv .venv

source .venv/bin/activate  # on Windows: .venv\Scripts\activate

pip install -e .

## Configuration

This project uses a `.env` file for secrets (API keys).

1. Create a file named `.env` in the project root.
3. Add your Google API key:

GEMINI_API_KEY="your-key-here"

## Running the agent

The default entrypoint uses Gemma with the free tier:

python main_gemma.py

## How it works

- The agent uses tools defined in the `functions/` directory:
  - `get_files_info.py` – list files in the target project
  - `get_file_content.py` – read the contents of a file
  - `write_file.py` – write changes back to a file
  - `run_python_file.py` – execute a Python file to test changes
- By default it operates on the sample `calculator/` project, but you can point it at other codebases.

## Safety

This is a toy agent. Be careful:

- Don’t point it at important or production code without backups.
- Commit your changes before running the agent so you can revert.
- Limit which directories it can read/write to.

### Misc Config

Non-secret settings (like maximum characters the AI can read) are defined in `config.py`.  

Secrets such as API keys belong in `.env`, not in `config.py`.

Paid models are more reccomended because they have lower rate limits andcan handle more data at once (Tokens)
