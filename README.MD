# Fetch Endpoint Monitor

## Cloning the Repository

To get started, clone the repository on your local machine:

```sh
git clone https://github.com/datagrime/fetch-endpoint-monitor.git
cd fetch-endpoint-monitor
```

This works on **Windows (Git Bash, PowerShell, WSL), macOS, and Linux**.

## Prerequisite: Python Installation

Poetry requires **Python 3.7 or newer** to be installed on your system.

## Installing Poetry

### Install Poetry (Python Dependency Manager)
Before installing Poetry, make sure **Python 3.7 or newer** is installed on your system. You can check this by running:
```sh
python --version
```
 or 
```sh
python3 --version
```


Poetry is used for managing Python dependencies. Follow these platform-specific instructions:

### macOS & Linux

1. Install Poetry:
    ```sh
    curl -sSL https://install.python-poetry.org | python3 -
    ```
2. Add Poetry to your PATH:
    ```sh
    export PATH="$HOME/.poetry/bin:$PATH"
    ```
    Add this line to `~/.bashrc`, `~/.bash_profile`, or `~/.zshrc` to make it persistent.

### Windows (PowerShell)

1. Install Poetry:
    ```powershell
    (Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
    ```
2. Add Poetry to your PATH by restarting your terminal or manually adding `C:\Users\YourUser\.poetry\bin` to the `Path` environment variable.

## Running the Python Script with Poetry

Once Poetry is installed, install dependencies and run the script:

1. Install required dependencies:
    ```sh
    poetry install
    ```
2. Run the script:
    ```sh
    poetry run python python/main.py [CONFIG_FILE]
    ```
    - If no `CONFIG_FILE` is provided, the script will default to using `example.yaml`.

## Installing Go

Download and install Go based on your platform:

- **Windows:** Download from [golang.org](https://golang.org/dl/) and install it.
- **macOS (Homebrew):**
  ```sh
  brew install go
  ```
- **Linux:**
  ```sh
  sudo apt install golang-go  # Debian/Ubuntu
  sudo dnf install golang      # Fedora
  sudo pacman -S go            # Arch
  ```

Ensure `go` is accessible in your terminal by running:
```sh
go version
```

## Running the Go Script

1. Navigate to the Go script directory:
    ```sh
    cd go
    ```
2. Build the Go executable:
    ```sh
    go build -o monitor main.go
    ```
3. Run the monitor with a configuration file:
    ```sh
    ./monitor ../example.yaml  # Default YAML file
    ./monitor path/to/[CONFIG_FILE]  # Custom YAML file
    ```
    **Windows users** should run `monitor.exe` instead of `./monitor`.

---

With these steps, users on **Windows, macOS, and Linux** should be able to set up and run the Fetch Endpoint Monitor seamlessly!

