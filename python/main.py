import sys
import asyncio
import aiohttp
import yaml
import time
from urllib.parse import urlparse
from collections import OrderedDict

# Load YAML configuration from a file
async def load_yaml(file_path):
    try:
        with open(file_path, 'r') as f:
            endpoints = yaml.safe_load(f) or []
        return [ep for ep in endpoints if "url" in ep and "name" in ep]
    except Exception as e:
        print(f"Error loading YAML file: {e}")
        return []

# Check the health of an endpoint asynchronously
async def check_endpoint(session, endpoint):
    url = endpoint["url"]
    method = endpoint.get("method", "GET").upper()
    headers = endpoint.get("headers", {})
    body = endpoint.get("body")

    try:
        start_time = time.monotonic()
        async with session.request(method, url, headers=headers, json=body, timeout=aiohttp.ClientTimeout(total=4.5)) as response:
            latency = (time.monotonic() - start_time) * 1000  # Convert latency to ms
            return url, 200 <= response.status < 300 and latency < 500
    except aiohttp.ClientError as e:
        print(f"Request error for {url}: {e}")
    except asyncio.TimeoutError:
        print(f"Timeout error for {url}")
    except Exception as e:
        print(f"Unexpected error for {url}: {e}")

    return url, False  # Mark as DOWN if an exception occurs

# Monitor endpoints by sending health checks
async def monitor_endpoints(endpoints):
    domain_stats = OrderedDict() # Track availability stats by domain

    # Create a single HTTP session for all monitoring cycles
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit_per_host=5)) as session:
        try:
            while True:
                cycle_start = time.monotonic()    

                # Execute health checks concurrently
                tasks = [asyncio.create_task(check_endpoint(session, ep)) for ep in endpoints]
                results = await asyncio.gather(*tasks, return_exceptions=True)

                # Reset domain stats for each cycle
                for url, is_up in filter(lambda r: isinstance(r, tuple), results):
                    domain = urlparse(url).netloc
                    if domain not in domain_stats:
                        domain_stats[domain] = {"total": 0, "up": 0}
                    domain_stats[domain]["total"] += 1
                    domain_stats[domain]["up"] += is_up

                # Log availability percentage
                for domain, stats in domain_stats.items():
                    print(f"{domain} has {round((stats['up'] / stats['total']) * 100)}% availability")

                await asyncio.sleep(max(0, 15 - (time.monotonic() - cycle_start)))
        except (asyncio.CancelledError, KeyboardInterrupt):
            print("\nMonitor stopped.")

# Main entry point of the script to load and monitor endpoints
async def main():
    if len(sys.argv) > 2:
        print("Usage: python main.py [CONFIG_FILE]")
        sys.exit(1)

    file_path = sys.argv[1] if len(sys.argv) == 2 else "example.yaml"
    endpoints = await load_yaml(file_path) # Load endpoints from a YAML file

    if not endpoints:
        print("No valid endpoints to monitor.")
        return

    await monitor_endpoints(endpoints)  # Pass already loaded endpoints

# Run the script asynchronously
if __name__ == "__main__":
    asyncio.run(main())