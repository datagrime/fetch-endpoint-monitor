# Fetch Endpoint Monitor

## Cloning the Repository

1. Clone the repository:
    ```sh
    git clone https://github.com/datagrime/fetch-endpoint-monitor.git
    cd fetch-endpoint-monitor
    ```

## Installing Poetry

1. Install Poetry by following the instructions on [python-poetry.org](https://python-poetry.org/docs/#installation).
    ```sh
    curl -sSL https://install.python-poetry.org | python3 -
    ```
2. Add Poetry to your PATH:
    ```sh
    export PATH="$HOME/.poetry/bin:$PATH"
    ```

## Running the Python Script with Poetry


1. Install the required dependencies:
    ```sh
    poetry install
    ```
2. Run the Python script:
    ```sh
    poetry run python python/main.py [CONFIG_FILE]
    ```
    - If no `CONFIG_FILE` is provided, the script will default to using [example.yaml](http://_vscodecontentref_/0).

## Installing Go

1. Download and install Go from [golang.org](https://golang.org/dl/).
2. Follow the instructions for your operating system to complete the installation.

## Running the Go Script

1. Navigate to the directory containing the Go script:
    ```sh
    cd go
    ```
2. Build the Go script:
    ```sh
    go build -o monitor main.go
    ```
3. Run the monitor with the default YAML file:
    ```sh
    ./monitor ../example.yaml
    ```
4. Run the monitor with a custom YAML file:
    ```sh
    ./monitor path/to/custom.yaml
    ```