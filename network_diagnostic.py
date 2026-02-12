#!/usr/bin/env python3

import argparse
import json
import socket
import subprocess
import ssl
import datetime
import concurrent.futures
import sys

try:
    import requests
except ImportError:
    print("Please install requests: pip3 install requests")
    sys.exit(1)


# ---------- Colors ----------
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    END = '\033[0m'


# ---------- DNS Check ----------
def dns_check(host):
    try:
        ip = socket.gethostbyname(host)
        return {"ip": ip}
    except Exception as e:
        return {"error": str(e)}


# ---------- Ping Check ----------
def ping_check(host, timeout):
    try:
        result = subprocess.run(
            ["ping", "-c", "1", "-W", str(timeout), host],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            for line in result.stdout.split("\n"):
                if "time=" in line:
                    latency = line.split("time=")[-1].split()[0]
                    return {"latency_ms": latency}

        return {"error": "Host unreachable"}

    except Exception as e:
        return {"error": str(e)}


# ---------- TCP Port Check ----------
def tcp_check(host, port, timeout):
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except:
        return False


# ---------- HTTP Check ----------
def http_check(url, timeout):
    try:
        response = requests.get(url, timeout=timeout)
        return {
            "status_code": response.status_code,
            "reason": response.reason
        }
    except Exception as e:
        return {"error": str(e)}


# ---------- SSL Check ----------
def ssl_check(host, timeout):
    try:
        context = ssl.create_default_context()

        with socket.create_connection((host, 443), timeout=timeout) as sock:
            with context.wrap_socket(sock, server_hostname=host) as ssock:
                cert = ssock.getpeercert()

                expiry_date = datetime.datetime.strptime(
                    cert['notAfter'],
                    '%b %d %H:%M:%S %Y %Z'
                )

                days_left = (expiry_date - datetime.datetime.utcnow()).days

                return {"days_to_expiry": days_left}

    except Exception as e:
        return {"error": str(e)}


# ---------- Extract Host ----------
def extract_host(url):
    return url.replace("https://", "").replace("http://", "").split("/")[0]


# ---------- Diagnose ----------
def diagnose(url, timeout, retries):
    result = {"url": url}

    host = extract_host(url)

    for attempt in range(retries):
        try:
            result["dns"] = dns_check(host)

            if "error" in result["dns"]:
                return result

            ip = result["dns"]["ip"]

            result["ping"] = ping_check(ip, timeout)
            result["tcp_80"] = tcp_check(ip, 80, timeout)
            result["tcp_443"] = tcp_check(ip, 443, timeout)
            result["http"] = http_check(url, timeout)

            if url.startswith("https"):
                result["ssl"] = ssl_check(host, timeout)

            return result

        except Exception as e:
            if attempt == retries - 1:
                result["error"] = str(e)

    return result


# ---------- Print Summary ----------
def print_summary(results):
    print("\n========== Network Diagnostic Summary ==========\n")

    success = True

    for res in results:
        has_error = (
            "error" in res
            or "error" in res.get("dns", {})
            or "error" in res.get("http", {})
        )

        color = Colors.GREEN if not has_error else Colors.RED
        status = "OK" if not has_error else "FAILED"

        print(f"{res['url']} -> {color}{status}{Colors.END}")

        print(" DNS:", res.get("dns"))
        print(" Ping:", res.get("ping"))
        print(" TCP 80:", res.get("tcp_80"))
        print(" TCP 443:", res.get("tcp_443"))
        print(" HTTP:", res.get("http"))

        if "ssl" in res:
            print(" SSL:", res.get("ssl"))

        print("-" * 50)

        if has_error:
            success = False

    return success


# ---------- Main ----------
def main():
    parser = argparse.ArgumentParser(description="Network Diagnostic Tool")

    parser.add_argument(
        "--url",
        nargs="+",
        required=True,
        help="Enter one or more URLs"
    )

    parser.add_argument(
        "--timeout",
        type=int,
        default=5,
        help="Timeout in seconds"
    )

    parser.add_argument(
        "--retry",
        type=int,
        default=2,
        help="Retry attempts"
    )

    args = parser.parse_args()

    # Run in parallel
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(diagnose, url, args.timeout, args.retry)
            for url in args.url
        ]

        results = [f.result() for f in futures]

    # Save JSON report
    with open("report.json", "w") as f:
        json.dump(results, f, indent=4)

    success = print_summary(results)

    print("\nReport saved as report.json\n")

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
