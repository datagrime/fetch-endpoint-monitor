## Fetch Endpoint Monitor - Quick Start

### Clone the Repository
```sh
git clone https://github.com/datagrime/fetch-endpoint-monitor.git
cd fetch-endpoint-monitor
```

### Install Poetry (Python Dependency Manager)
- **macOS/Linux:**
  ```sh
  curl -sSL https://install.python-poetry.org | python3 -
  export PATH="$HOME/.poetry/bin:$PATH"
  ```
- **Windows (PowerShell):**
  ```powershell
  (Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
  ```

### Run the Python Script
```sh
poetry install
poetry run python python/main.py [CONFIG_FILE]  # Defaults to example.yaml if not provided
```

---

## Install & Run Go Version

### Install Go
- **Windows:** Download from [golang.org](https://golang.org/dl/)
- **macOS (Homebrew):** `brew install go`
- **Linux:** `sudo apt install golang-go`

### Build & Run the Go Script
```sh
cd go
go build -o monitor main.go
./monitor ../example.yaml  # Default YAML
```
*(Windows users run `monitor.exe` instead of `./monitor`)*

