# Fetch Endpoint Monitor

## Getting Started

Clone this repo to your machine:

```sh
git clone https://github.com/datagrime/fetch-endpoint-monitor.git
cd fetch-endpoint-monitor
```

Works on **Windows, macOS, and Linux**.

## Prerequisite: Install Python

Make sure **Python 3.7 or newer** is installed before proceeding. Check by running:
```sh
python --version
```

## Install Poetry (Dependency Manager)

Poetry manages Python dependencies. Install it based on your platform:

### macOS & Linux
```sh
curl -sSL https://install.python-poetry.org | python3 -
export PATH="$HOME/.poetry/bin:$PATH"
```

### Windows (PowerShell)
```powershell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
```
Restart your terminal or manually add `C:\Users\YourUser\.poetry\bin` to your system `Path`.

## Run the Python Script

1. Install dependencies:
    ```sh
    poetry install
    ```
2. Run the script:
    ```sh
    poetry run python python/main.py [CONFIG_FILE]
    ```
    - Defaults to `example.yaml` if no config file is provided.

## Install Go

Get Go for your platform:
- **Windows:** Download from [golang.org](https://golang.org/dl/) and install.
- **macOS (Homebrew):**
  ```sh
  brew install go
  ```
- **Linux:**
  ```sh
  sudo apt install golang-go  # Debian/Ubuntu
  ```

Verify Go installation:
```sh
go version
```

## Run the Go Script

1. Go to the script directory:
    ```sh
    cd go
    ```
2. Build the executable:
    ```sh
    go build -o monitor main.go
    ```
3. Run it with a config file:
    ```sh
    ./monitor ../example.yaml  # Default config
    ./monitor path/to/[CONFIG_FILE]  # Custom config
    ```
    **Windows users** run `monitor.exe` instead.


