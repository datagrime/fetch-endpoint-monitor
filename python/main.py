import sys
import asyncio
import aiohttp
import json
import time
import yaml
from urllib.parse import urlparse
from collections import defaultdict

def load_yaml(config_file_path):
    """Load YAML configuration from file."""
    try:
        with open(config_file_path, 'r') as f:
            endpoints = yaml.safe_load(f)
        if not isinstance(endpoints, list):
            print("Invalid YAML format: expected a list of endpoints.")
            return []
        return [ep for ep in endpoints if ep.get("url") and ep.get("name")]
    except Exception as e:
        print(f"Error loading YAML file: {e}")
        return []

async def check_endpoint(session, endpoint):
    """Check the status of a single endpoint asynchronously."""
    url = endpoint.get("url")
    try:
        start_time = time.monotonic()
        async with session.request(
            method=endpoint.get("method", "GET").upper(),
            url=url,
            headers=endpoint.get("headers", {}),
            json=json.loads(endpoint["body"]) if "body" in endpoint else None,
            timeout=aiohttp.ClientTimeout(total=4.5)
        ) as response:
            latency = (time.monotonic() - start_time) * 1000
            is_up = 200 <= response.status < 300 and latency < 500
            return url, is_up
    except asyncio.CancelledError:
        raise
    except Exception:
        return url, False

async def monitor_endpoints(config_file_path):
    """Main monitoring loop with concurrent health checks."""
    endpoints = load_yaml(config_file_path)
    if not endpoints:
        print("No valid endpoints to monitor.")
        return

    # Track domains in order of first appearance
    domains_order = []
    seen_domains = set()
    for endpoint in endpoints:
        domain = urlparse(endpoint["url"]).netloc
        if domain not in seen_domains:
            seen_domains.add(domain)
            domains_order.append(domain)

    domain_stats = defaultdict(lambda: {"total": 0, "up": 0})

    session = aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=100))
    
    try:
        while True:
            cycle_start = time.monotonic()
            
            # Process all endpoints concurrently
            results = await asyncio.gather(
                *(check_endpoint(session, ep) for ep in endpoints),
                return_exceptions=True
            )
            
            # Update statistics
            for result in results:
                if isinstance(result, Exception):
                    continue
                url, is_up = result
                domain = urlparse(url).netloc
                domain_stats[domain]["total"] += 1
                domain_stats[domain]["up"] += is_up
            
            # Calculate and display percentages
            for domain in domains_order:
                stats = domain_stats[domain]
                percent = round((stats["up"] / stats["total"]) * 100) if stats["total"] else 0
                print(f"{domain} has {percent}% availability percentage")
            
            # Maintain 15-second cycle
            elapsed = time.monotonic() - cycle_start
            await asyncio.sleep(max(0.0, 15 - elapsed))

    except asyncio.CancelledError:
        print("\nMonitoring stopped.")
    except KeyboardInterrupt:
        print("\nCTRL+C received. Exiting gracefully...")
    finally:
        await session.close()

async def main():
    """Run monitoring with config file argument handling."""
    if len(sys.argv) > 2:
        print("Usage: python main.py [CONFIG_FILE]")
        sys.exit(1)
    
    config_file = sys.argv[1] if len(sys.argv) == 2 else "endpoint.yaml"
    
    try:
        await monitor_endpoints(config_file)
    except KeyboardInterrupt:
        print("\nCTRL+C received. Exiting gracefully...")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nProgram terminated by user.")