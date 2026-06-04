# AI Accelerator Student Setup

Use this folder to check that your computer is ready for the workshop.

You will set up:

- A Python virtual environment
- JupyterLab
- Jupyter AI
- Common data analysis packages
- Codex access through the workshop LiteLLM API key

## 1. Open a Terminal

Open a terminal and move into this folder.

On macOS or Linux:

```bash
cd path/to/student-setup
```

On Windows, use Ubuntu/WSL for these commands.

## 2. Create a Python Environment

Create a local virtual environment and install the setup packages:

```bash
bash scripts/setup_python_environment.sh
```

This creates `.venv`, installs the packages in `requirements.txt`, and leaves the environment ready for the workshop setup check.

When you open a new terminal, activate the environment again with:

```bash
source .venv/bin/activate
```

If you later receive an updated `requirements.txt`, activate the same `.venv` again and rerun:

```bash
python -m pip install -r requirements.txt
```

## 3. Install Codex

Check whether Codex is already installed:

```bash
codex --version
codex-acp --help
```

If either command is missing, install Codex:

```bash
npm install -g @openai/codex
```

If the global npm install fails with a permissions error, ask for help or configure npm to install global tools into your home directory.

## 4. Configure the Workshop API Key

The workshop will provide you with a LiteLLM API key. Run:

```bash
python scripts/setup_codex_litellm.py
```

When prompted, paste your workshop API key. The script will create:

- `~/.codex-litellm/config.toml`

This file stores the Codex configuration for the workshop API key. Codex will use it only when you launch a command with `CODEX_HOME="$HOME/.codex-litellm"`.

## 5. Test Codex from the Command Line

Run:

```bash
CODEX_HOME="$HOME/.codex-litellm" codex exec "Reply with only: Codex LiteLLM is working" --skip-git-repo-check
```

You should see:

```text
Codex LiteLLM is working
```

If this fails, check that your API key was pasted correctly by rerunning:

```bash
python scripts/setup_codex_litellm.py
```

## 6. Start JupyterLab

Start JupyterLab from this folder with the workshop Codex configuration:

```bash
CODEX_HOME="$HOME/.codex-litellm" jupyter lab
```

Open the URL printed in the terminal. In Jupyter AI, use the regular `Codex` persona; because JupyterLab was launched with `CODEX_HOME="$HOME/.codex-litellm"`, that Codex persona will use the workshop API key configuration.

Try a short message to `Codex`, such as:

```text
Can you reply with only: Jupyter AI is connected
```

Optional: create a shorter command for running tools with the workshop Codex configuration. This is a shell function: a shortcut in your terminal that runs one command with `CODEX_HOME="$HOME/.codex-litellm"` set.

This does not permanently set `CODEX_HOME`. It sets `CODEX_HOME` only for the command you run after `litellm`.

On macOS:

```bash
cat >> ~/.zshrc <<'EOF'
litellm() {
  CODEX_HOME="$HOME/.codex-litellm" "$@"
}
EOF
source ~/.zshrc
```

On WSL/Linux:

```bash
cat >> ~/.bashrc <<'EOF'
litellm() {
  CODEX_HOME="$HOME/.codex-litellm" "$@"
}
EOF
source ~/.bashrc
```

After that, you can start JupyterLab with:

```bash
litellm jupyter lab
```

You can also test Codex with:

```bash
litellm codex exec "Reply with only: Codex is working" --skip-git-repo-check
```

## Notes

- Keep this folder on your computer for the workshop.
- Your `.venv` is tied to this folder. Start JupyterLab from this folder when testing this setup.
- To use the workshop API key in Jupyter AI, start JupyterLab with `CODEX_HOME="$HOME/.codex-litellm" jupyter lab`.
- Do not share your API key or commit it to Git.
