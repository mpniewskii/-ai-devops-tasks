#!/usr/bin/env python3
"""Command-line manager for common Jenkins API operations."""

import argparse
import json
import os
import sys
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urljoin
from urllib.request import HTTPBasicAuthHandler, HTTPPasswordMgrWithDefaultRealm
from urllib.request import Request, build_opener


class JenkinsApiError(Exception):
    """Raised when Jenkins returns an invalid response or an API error."""


class JenkinsClient:
    def __init__(self, base_url: str, username: str, api_token: str, timeout: int = 15):
        self.base_url = base_url.rstrip("/") + "/"
        self.timeout = timeout
        password_manager = HTTPPasswordMgrWithDefaultRealm()
        password_manager.add_password(None, self.base_url, username, api_token)
        auth_handler = HTTPBasicAuthHandler(password_manager)
        self.opener = build_opener(auth_handler)

    def request(self, path: str, method: str = "GET") -> tuple[bytes, dict[str, str]]:
        request = Request(urljoin(self.base_url, path), method=method)
        try:
            with self.opener.open(request, timeout=self.timeout) as response:
                return response.read(), dict(response.headers)
        except HTTPError as error:
            body = error.read().decode("utf-8", errors="replace").strip()
            detail = f": {body[:200]}" if body else ""
            raise JenkinsApiError(
                f"Jenkins zwrócił HTTP {error.code} ({error.reason}){detail}"
            ) from error
        except URLError as error:
            raise JenkinsApiError(f"Nie można połączyć się z Jenkinsem: {error.reason}") from error

    def get_json(self, path: str) -> Any:
        body, _ = self.request(path)
        try:
            return json.loads(body.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            raise JenkinsApiError("Jenkins zwrócił nieprawidłowy dokument JSON.") from error

    def list_jobs(self) -> list[dict[str, Any]]:
        data = self.get_json("api/json?tree=jobs[name,url,color,lastBuild[number,result,timestamp,duration,url]]")
        jobs = data.get("jobs")
        if not isinstance(jobs, list):
            raise JenkinsApiError("Odpowiedź API nie zawiera listy jobs.")
        return jobs

    def trigger_job(self, job_name: str) -> str:
        job_path = "/".join(f"job/{quote(part, safe='')}" for part in job_name.split("/"))
        crumb_body, _ = self.request("crumbIssuer/api/json")
        try:
            crumb_data = json.loads(crumb_body.decode("utf-8"))
            crumb_field = crumb_data["crumbRequestField"]
            crumb = crumb_data["crumb"]
        except (UnicodeDecodeError, json.JSONDecodeError, KeyError) as error:
            raise JenkinsApiError("Nie udało się odczytać CSRF crumb z Jenkinsa.") from error

        request = Request(
            urljoin(self.base_url, f"{job_path}/build"),
            data=b"",
            method="POST",
            headers={crumb_field: crumb},
        )
        try:
            with self.opener.open(request, timeout=self.timeout) as response:
                queue_url = response.headers.get("Location", "")
                return queue_url or "Zadanie zostało uruchomione."
        except HTTPError as error:
            body = error.read().decode("utf-8", errors="replace").strip()
            detail = f": {body[:200]}" if body else ""
            raise JenkinsApiError(
                f"Nie udało się uruchomić joba (HTTP {error.code}){detail}"
            ) from error
        except URLError as error:
            raise JenkinsApiError(f"Nie można uruchomić joba: {error.reason}") from error


def build_client(args: argparse.Namespace) -> JenkinsClient:
    username = args.username or os.environ.get("JENKINS_USER")
    api_token = args.api_token or os.environ.get("JENKINS_API_TOKEN")
    if not username:
        raise JenkinsApiError("Podaj użytkownika przez --username lub JENKINS_USER.")
    if not api_token:
        raise JenkinsApiError(
            "Podaj token API przez --api-token lub JENKINS_API_TOKEN."
        )
    return JenkinsClient(args.url, username, api_token, args.timeout)


def print_jobs(jobs: list[dict[str, Any]]) -> None:
    if not jobs:
        print("Brak zadań Jenkins.")
        return
    for job in jobs:
        build = job.get("lastBuild") or {}
        print(
            f"{job.get('name', '<bez nazwy>')} | "
            f"status: {build.get('result') or job.get('color', 'UNKNOWN')} | "
            f"ostatni build: {build.get('number', 'brak')}"
        )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Zarządzanie Jenkins API.")
    parser.add_argument(
        "--url",
        default=os.environ.get("JENKINS_URL"),
        help="Adres Jenkinsa (domyślnie: zmienna JENKINS_URL).",
    )
    parser.add_argument("--username", help="Nazwa użytkownika Jenkins.")
    parser.add_argument("--api-token", help="Token API Jenkins.")
    parser.add_argument("--timeout", type=int, default=15, help="Timeout żądania w sekundach.")
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("list", help="Wyświetla wszystkie joby i status ostatniego builda.")
    run_parser = subparsers.add_parser("run", help="Uruchamia wskazany job.")
    run_parser.add_argument("job_name", help="Nazwa joba, także w formacie folder/job.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not args.url:
        print("Podaj adres przez --url lub JENKINS_URL.", file=sys.stderr)
        return 2
    try:
        client = build_client(args)
        if args.command == "list":
            print_jobs(client.list_jobs())
        else:
            print(client.trigger_job(args.job_name))
        return 0
    except JenkinsApiError as error:
        print(f"Błąd: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
