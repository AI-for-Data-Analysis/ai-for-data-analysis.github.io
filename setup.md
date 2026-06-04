# Setup

This page will walk you through installing the required software, setting up an environment, and installing and configuring the AI agent (Codex) we will use for this workshop series.

```{admonition} Special Note for Windows Users
:class: note

For this workshop, you will need a working Python programming environment where you can create virtual environments and run Jupyter notebooks.

If you do not already have this set up, we recommend that **Windows users use the Windows Subsystem for Linux (WSL)** for the workshop. WSL lets you run a Linux environment on Windows, which is often easier for Python development.

Most Windows users should be able to install **Ubuntu for WSL** directly from the Microsoft Store using this link: [Ubuntu/WSL](https://apps.microsoft.com/detail/9PDXGNCFSCZV?hl=en-us&gl=US&ocid=pdpshare). After installing it, you can start your Linux shell by searching for **“Ubuntu”** in the Windows search bar.

If the Microsoft Store installation does not work, follow Microsoft’s more detailed WSL installation instructions here: [Install WSL](https://learn.microsoft.com/en-us/windows/wsl/install).

You may also want to install [Windows Terminal](https://apps.microsoft.com/detail/9N0DX20HK701?hl=en-us&gl=US&ocid=pdpshare), which provides a nicer interface for using WSL and other command-line tools.
```

```{admonition} Download the Workshop Setup Installer
:class: tip

Download the [workshop setup installer](student-setup.zip) now, but do not run it yet. This page first walks you through computer-level setup: WSL if needed, Python, npm, Codex, and the Codex Jupyter connector.

Later, in the AI provider access section, you will use the installer to create the workshop-specific Python/Jupyter environment and Codex API key configuration.
```

## Set Up Your Development Environment

In this section, you will check that the basic tools needed for the workshop are installed and available on your computer. You will run these checks from a terminal, which is the program we will use to type setup commands.

Start by opening a terminal for your operating system.

::::{tab-set}

:::{tab-item} Mac
:sync: mac

Open the **Terminal** app.

:::

:::{tab-item} WSL/Linux
:sync: wsl-linux

Open your Linux terminal.

* **Windows users using WSL:** open **Ubuntu** from the Windows search bar, or open **Windows Terminal** and choose your Ubuntu/WSL profile.
* **Linux users:** open your usual terminal application.

Windows users should run the commands on this page **inside the Ubuntu/WSL terminal**, not in PowerShell or Command Prompt.

:::

::::

Once your terminal is open, use the commands below to check that each required tool is installed.

### Python

You will need **Python 3.11 or newer**.

Check your Python version with:

::::{tab-set}

:::{tab-item} Mac
:sync: mac

```bash
python3 --version
```

:::

:::{tab-item} WSL/Linux
:sync: wsl-linux

```bash
python3 --version
```

:::

::::

You should see a version number beginning with `3.11` or higher.

If Python is not installed, or if your version is older than Python 3.11, install a newer version before continuing.

::::{tab-set}

:::{tab-item} Mac
:sync: mac

Install Python from [python.org](https://www.python.org/downloads/) or with a package manager such as Homebrew.

After installing Python, run the version check again.

:::

:::{tab-item} WSL/Linux
:sync: wsl-linux

Install Python inside your Linux environment. On Ubuntu/WSL, you can usually install Python with:

```bash
sudo apt update
sudo apt install python3 python3-venv python3-pip
```

After installing Python, run the version check again.

:::

::::

#### Python virtual environment and pip support

In addition to Python itself, you will need support for virtual environments and `pip`, Python's package installer.

Check that you can create virtual environments with:

```bash
python3 -m venv --help
```

Check that `pip` is available with:

```bash
python3 -m pip --version
```

If both commands work, you can continue.

::::{tab-set}

:::{tab-item} Mac
:sync: mac

If `venv` or `pip` is missing, reinstall Python from [python.org](https://www.python.org/downloads/) or use your package manager to install a complete Python distribution.

:::

:::{tab-item} WSL/Linux
:sync: wsl-linux

If `venv` or `pip` is missing, install them inside your Linux environment:

```bash
sudo apt update
sudo apt install python3-venv python3-pip
```

After installing them, run the checks again.

:::

::::

### Node.js and npm

You will also need **Node.js** and **npm** to install Codex. `npm` is the package manager used to install many command-line tools written for the JavaScript ecosystem.

Check that Node.js is installed with:

```bash
node --version
```

Check that `npm` is installed with:

```bash
npm --version
```

If both commands print version numbers, you can continue.

::::{tab-set}

:::{tab-item} Mac
:sync: mac

If Node.js or `npm` is missing, install Node.js from [nodejs.org](https://nodejs.org/) or with a package manager such as Homebrew.

After installing Node.js, run the checks again.

:::

:::{tab-item} WSL/Linux
:sync: wsl-linux

If Node.js or `npm` is missing, install them inside your Linux environment. On Ubuntu/WSL, you can usually install them with:

```bash
sudo apt update
sudo apt install nodejs npm
```

After installing Node.js and `npm`, run the checks again.

:::

::::

### Code editor

We recommend using **Visual Studio Code (VS Code)** as your code editor for this workshop.

VS Code gives you a convenient place to edit files, open a terminal, work with notebooks, and view the workshop files.

::::{tab-set}

:::{tab-item} Mac
:sync: mac

Install VS Code from [code.visualstudio.com](https://code.visualstudio.com/).

You should be able to open VS Code as an application. 
During the workshop, it will be useful to be able to open VS Code from the terminal. 
[Follow these instructions](https://code.visualstudio.com/docs/setup/mac#_launch-vs-code-from-the-command-line) to enable opening code from your terminal

After it is enabled, you should be able to open VS Code using the command

```bash
code --version
```

:::

:::{tab-item} WSL/Linux
:sync: wsl-linux

**Windows users using WSL:** install VS Code on Windows from [code.visualstudio.com](https://code.visualstudio.com/), not inside WSL.

Then install the [Remote Development extension pack](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.vscode-remote-extensionpack)in VS Code. This allows VS Code to open and edit files inside your Ubuntu/WSL environment.

After installing VS Code and the extension, open your Ubuntu/WSL terminal and check that VS Code can be opened from the terminal:

```bash
code --version
```

Later, after you download and open the workshop materials, you will be able to open the project in VS Code from inside the project folder with:

```bash
code .
```

**Linux users:** install VS Code from [code.visualstudio.com](https://code.visualstudio.com/) or use your preferred code editor.

:::

::::

### Install Codex

Install the Codex command-line tool with npm:

```bash
npm install -g @openai/codex
```

If this command fails with a permissions error, use the steps in [Troubleshoot npm global installs](#troubleshoot-npm-global-installs), then run the install command again.

(troubleshoot-npm-global-installs)=
#### Troubleshoot npm global installs

Codex is installed as a global npm package. On some systems, global npm installs fail because the default global install folder requires administrator permissions.

:::{warning}
Do not run the commands in this section unless an `npm install -g` command fails with a permissions error. If the global install command works, skip this section.
:::

If `npm install -g` fails because npm cannot write to the global install folder, configure npm to install global packages into a folder in your home directory, then try the failed install command again.

::::{tab-set}

:::{tab-item} Mac
:sync: mac

```bash
mkdir -p ~/.local
npm config set prefix ~/.local
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zprofile
source ~/.zprofile
```

:::

:::{tab-item} WSL/Linux
:sync: wsl-linux

```bash
mkdir -p ~/.local
npm config set prefix ~/.local
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.profile
source ~/.profile
```

:::

::::

Then check that the `codex` command is available:

```bash
codex --version
```

If your terminal says that `codex` was not found, close and reopen your terminal, then try the version check again.

You will also need to install a connector for Codex and the Jupyter Lab interface:

```bash
npm install -g @zed-industries/codex-acp
```

If this command fails with a permissions error, use the steps in [Troubleshoot npm global installs](#troubleshoot-npm-global-installs), then run the install command again.

#### AI provider access

This workshop uses **Codex**, OpenAI's coding agent. 
You will be using Codex both in the JupyterLab interface with the JupyterAI plugin and in the command line interface.
Some Duke departments cover access to ChatGPT. If you are able to get ChatGPT access through Duke without paying out of pocket, please [set it up through Duke Software Manager](https://oit.duke.edu/service/chatgpt-edu/) before the workshop.

If your department does not cover access, you do not need to pay for ChatGPT for this workshop unless you want to. We will also provide a workshop API key that you can use instead; [skip to the workshop API key setup](#workshop-api-key-setup).

Open Codex by typing `codex` into your terminal.

The first time you open Codex, choose the first option, **Sign in with ChatGPT**. This will open a web page where you should log in to ChatGPT using your Duke NetID.

:::{note}
If you cannot get ChatGPT access, or if access would require you to pay and you do not want to, use the workshop API key setup below.
:::

After logging in, check your login status:

```bash
codex login status
```

If ChatGPT login works, you can use Codex normally.

```bash
codex exec "Reply with only: Codex is working" --skip-git-repo-check
```

(workshop-api-key-setup)=
##### Workshop API key setup

We will provide API keys to all workshop participants. Set up the workshop API key configuration even if ChatGPT login works for you. This gives you a backup provider if ChatGPT login is unavailable or if you run out of usage during the workshop.

After you have installed Python, npm, Codex, and the Codex Jupyter connector, use the [workshop setup installer](student-setup.zip). The zip includes a `README.md`, a `requirements.txt` for testing JupyterLab and Jupyter AI, and a script that creates the workshop Codex LiteLLM configuration after you paste in your API key.

Move the downloaded zip file to the folder where you want to create your workshop setup, or retrieve it again from the terminal with `curl`. Replace `PASTE_STUDENT_SETUP_ZIP_URL_HERE` with the published link to `student-setup.zip`.

```bash
SETUP_ZIP_URL="PASTE_STUDENT_SETUP_ZIP_URL_HERE"
curl -L "$SETUP_ZIP_URL" -o student-setup.zip
unzip student-setup.zip
cd student-setup
```

:::{tip}
In WSL, you can open the current Linux folder in Windows File Explorer with:

```bash
explorer.exe .
```

You can also open a specific path by replacing `.` with that path.
:::

Then create the Python environment and install the Jupyter/data-analysis packages:

```bash
bash scripts/setup_python_environment.sh
```

Then run the Codex API key setup script:

```bash
python scripts/setup_codex_litellm.py
```

When prompted, paste the API key provided by the workshop instructors.

The script creates a separate Codex home directory named `~/.codex-litellm`. Codex will still use your regular `~/.codex` folder by default and will use `~/.codex-litellm` only when you explicitly launch it that way.

Then test the workshop API key configuration:

```bash
CODEX_HOME="$HOME/.codex-litellm" codex exec "Reply with only: Codex is working" --skip-git-repo-check
```

To test Jupyter AI with the workshop API key configuration, start JupyterLab from the `student-setup` folder with `CODEX_HOME` set:

```bash
CODEX_HOME="$HOME/.codex-litellm" jupyter lab
```

In Jupyter AI, use the regular `Codex` persona. Because JupyterLab was launched with `CODEX_HOME="$HOME/.codex-litellm"`, that Codex persona will use the workshop API key configuration.

````{admonition} Optional shortcut
:class: tip

A shell function is a shortcut in your terminal. The function below creates a command named `litellm` that runs one command with the workshop Codex configuration.

This does not permanently set `CODEX_HOME`. It sets `CODEX_HOME` only for the command you run after `litellm`.

::::{tab-set}

:::{tab-item} Mac
:sync: mac

```bash
cat >> ~/.zshrc <<'EOF'
litellm() {
  CODEX_HOME="$HOME/.codex-litellm" "$@"
}
EOF
source ~/.zshrc
```

:::

:::{tab-item} WSL/Linux
:sync: wsl-linux

```bash
cat >> ~/.bashrc <<'EOF'
litellm() {
  CODEX_HOME="$HOME/.codex-litellm" "$@"
}
EOF
source ~/.bashrc
```

:::

::::

After adding the function, you can start JupyterLab with the workshop API key configuration by running:

```bash
litellm jupyter lab
```

You can also test Codex with:

```bash
litellm codex exec "Reply with only: Codex is working" --skip-git-repo-check
```
````

During the workshop, use normal Codex for ChatGPT login when available. Launch commands with `CODEX_HOME="$HOME/.codex-litellm"` when you need the workshop API key.

## Obtaining Workshop Materials

Workshop materials will be distributed separately. For now, use the [student setup zip](student-setup.zip) to verify that your environment can run JupyterLab, Jupyter AI, and the workshop Codex API key configuration.

### Create a virtual environment

The workshop materials you created contain a list of Python packages that should be installed. 
We will use a Python virtual environment for these packages. 
You should execute the following commands from the repository root.
Create a virtual environment for the workshop project:

```bash
python3 -m venv .venv
```

Then activate the virtual environment:

::::{tab-set}

:::{tab-item} Mac
:sync: mac

```bash
source .venv/bin/activate
```

:::

:::{tab-item} WSL/Linux
:sync: wsl-linux

```bash
source .venv/bin/activate
```

:::

::::

After activation, you should see `(.venv)` at the beginning of your terminal prompt.

### Install Python packages

Install the required Python packages from `requirements.txt`:

```bash
python -m pip install -r requirements.txt
```

## Checklist

Before the workshop, open your terminal and run these checks to confirm your setup.

### Run from any folder in your terminal

```bash
python3 --version        # should show Python 3.11 or newer
python3 -m venv --help   # should show venv help text
python3 -m pip --version # should show a pip version
node --version           # should show a Node.js version
npm --version            # should show an npm version
codex --version          # should show a Codex version
codex exec "Reply with only: Codex is working" --skip-git-repo-check # should return: Codex is working
```

Check the workshop API key setup:

```bash
CODEX_HOME="$HOME/.codex-litellm" codex exec "Reply with only: Codex is working" --skip-git-repo-check # should return: Codex is working
```

### Run from the workshop materials folder in your terminal

Move into the folder where you downloaded and unzipped the workshop materials. Replace `path/to/workshop-materials` with the actual path to your folder.

```bash
cd path/to/workshop-materials
```

Check that the expected files and folders are present.

```bash
ls                  # should show the workshop files
ls .venv            # should show the virtual environment folder contents
ls requirements.txt # should show requirements.txt
```

Activate the virtual environment.

```bash
source .venv/bin/activate
```

After activation, run these checks.

```bash
python --version        # should show Python 3.11 or newer
python -m pip --version # should show pip from the virtual environment
python -m pip check     # should show: No broken requirements found.
jupyter lab --version   # should show a JupyterLab version
CODEX_HOME="$HOME/.codex-litellm" jupyter lab # should open JupyterLab with the workshop Codex configuration
```
