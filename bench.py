import argparse
import re
from pathlib import Path

import requests
import time
import concurrent.futures

# Регулярное выражение для проверки формата URL
URL_REGEX = re.compile(r'^https?://[^\s/$.?#].[^\s]*$')


def validate_url(url: str):
    """Проверяет, соответствует ли URL формату http:// или https://."""
    return bool(URL_REGEX.match(url))


def test_host(host: str, count: int):
    success = 0
    failed = 0
    errors = 0
    times = []

    for _ in range(count):
        try:
            start_time = time.time()
            response = requests.get(host, timeout=3)
            elapsed_time = time.time() - start_time
            times.append(elapsed_time)

            if response.status_code >= 400:
                failed += 1
            else:
                success += 1
        except requests.exceptions.RequestException as e:
            errors += 1
            print(f"Error occurred while requesting {host}: {e}")

    if times:
        min_time = min(times)
        max_time = max(times)
        avg_time = sum(times) / len(times)
    else:
        min_time = max_time = avg_time = 0

    return {
        "Host": host,
        "Success": success,
        "Failed": failed,
        "Errors": errors,
        "Min": min_time,
        "Max": max_time,
        "Avg": avg_time
    }


def read_file(path: Path):
    with open(path, 'r') as file:
        hosts = file.read().split('\n')
    return hosts


def write_file(path: Path, text_result: str):
    with open(path, 'a+') as file:
        file.write(text_result)


def test_host_and_print_data(host: str, count: int, file_output: Path) -> str:
    stats = test_host(host, count)
    text_result = ""
    text_result += f"Statistics for host: {stats['Host']}"
    text_result += f"\nSuccess: {stats['Success']}"
    text_result += f"\nFailed: {stats['Failed']}"
    text_result += f"\nErrors: {stats['Errors']}"
    text_result += f"\nMin time: {stats['Min']:.4f} seconds"
    text_result += f"\nMax time: {stats['Max']:.4f} seconds"
    text_result += f"\nAvg time: {stats['Avg']:.4f} seconds\n"
    if file_output is not None:
        write_file(file_output, text_result)
        return ""
    return text_result


def main():
    parser = argparse.ArgumentParser(description="HTTP Server Availability Tester")
    parser.add_argument("-H", "--hosts", type=str, help="Comma-separated list of hosts to test")
    parser.add_argument("-C", "--count", type=int, default=1, help="Number of requests to send to each host")
    parser.add_argument("-F", "--file", type=Path, help="The file from which the hosts will be read for testing")
    parser.add_argument("-O", "--output", type=Path, help="Writing output information to a file")

    args = parser.parse_args()
    hosts = []
    if args.hosts is not None:
        hosts: str = args.hosts.split(',')
    count: int = args.count
    file_read: Path = args.file
    file_output: Path = args.output

    # Проверка параметров
    if args.count < 1:
        parser.error("Count must be a positive integer.")

    if (args.hosts and args.file) or (args.hosts is None and args.file is None):
        parser.error("Specify only one of -H/--hosts or -F/--file.")

    if file_read is not None:
        hosts = read_file(file_read)

    futures = []
    results = []

    with concurrent.futures.ThreadPoolExecutor() as executor:
        for host in hosts:
            if validate_url(host):
                host = host
                futures.append(
                    executor.submit(test_host_and_print_data, host, count, file_output)
                )

        for i, future in enumerate(concurrent.futures.as_completed(futures)):
            result = future.result()
            results.append(result)

    for text_result in results:
        print(text_result, end='')


if __name__ == "__main__":
    main()
