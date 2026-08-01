"""
Supabase client wrapper using direct PostgREST HTTP calls.

supabase-py v2 uses httpx which fails on Vercel serverless with
'[Errno 16] Device or resource busy'. This wrapper uses `requests`
(which works reliably on Vercel) to make direct PostgREST API calls.
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.environ.get("SUPABASE_URL", "")
SUPABASE_SERVICE_KEY = os.environ.get("SUPABASE_SERVICE_KEY", "")


class SupabaseTable:
    """Minimal PostgREST query builder that mirrors supabase-py's API."""

    def __init__(self, table_name: str, url: str, key: str):
        self._table = table_name
        self._base = f"{url}/rest/v1/{table_name}"
        self._headers = {
            "apikey": key,
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
            "Prefer": "return=representation",
        }
        self._params = {}
        self._method = "GET"
        self._body = None

    def select(self, columns: str = "*"):
        self._method = "GET"
        self._params["select"] = columns
        return self

    def insert(self, data: dict | list):
        self._method = "POST"
        self._body = data
        return self

    def update(self, data: dict):
        self._method = "PATCH"
        self._body = data
        return self

    def delete(self):
        self._method = "DELETE"
        return self

    def eq(self, column: str, value):
        self._params[column] = f"eq.{value}"
        return self

    def neq(self, column: str, value):
        self._params[column] = f"neq.{value}"
        return self

    def like(self, column: str, pattern: str):
        self._params[column] = f"like.{pattern}"
        return self

    def ilike(self, column: str, pattern: str):
        self._params[column] = f"ilike.{pattern}"
        return self

    def gt(self, column: str, value):
        self._params[column] = f"gt.{value}"
        return self

    def gte(self, column: str, value):
        self._params[column] = f"gte.{value}"
        return self

    def lt(self, column: str, value):
        self._params[column] = f"lt.{value}"
        return self

    def lte(self, column: str, value):
        self._params[column] = f"lte.{value}"
        return self

    def in_(self, column: str, values: list):
        formatted = ",".join(str(v) for v in values)
        self._params[column] = f"in.({formatted})"
        return self

    def order(self, column: str, desc: bool = False):
        direction = "desc" if desc else "asc"
        self._params["order"] = f"{column}.{direction}"
        return self

    def limit(self, count: int):
        self._headers["Range"] = f"0-{count - 1}"
        return self

    def range(self, start: int, end: int):
        self._headers["Range"] = f"{start}-{end}"
        return self

    def execute(self):
        if self._method == "GET":
            resp = requests.get(self._base, headers=self._headers, params=self._params, timeout=15)
        elif self._method == "POST":
            resp = requests.post(self._base, headers=self._headers, params=self._params, json=self._body, timeout=15)
        elif self._method == "PATCH":
            resp = requests.patch(self._base, headers=self._headers, params=self._params, json=self._body, timeout=15)
        elif self._method == "DELETE":
            resp = requests.delete(self._base, headers=self._headers, params=self._params, timeout=15)
        else:
            raise ValueError(f"Unsupported method: {self._method}")

        resp.raise_for_status()

        return _SupabaseResponse(resp.json() if resp.text else [])


class _SupabaseResponse:
    """Mimics the supabase-py response object."""
    def __init__(self, data):
        self.data = data


class SupabaseClient:
    """Lightweight Supabase client using direct PostgREST REST calls."""

    def __init__(self, url: str, key: str):
        self._url = url.rstrip("/")
        self._key = key

    def table(self, table_name: str) -> SupabaseTable:
        return SupabaseTable(table_name, self._url, self._key)

    def rpc(self, function_name: str, params: dict = None):
        """Call a Supabase RPC (database function)."""
        url = f"{self._url}/rest/v1/rpc/{function_name}"
        headers = {
            "apikey": self._key,
            "Authorization": f"Bearer {self._key}",
            "Content-Type": "application/json",
        }
        resp = requests.post(url, headers=headers, json=params or {}, timeout=15)
        resp.raise_for_status()
        return _SupabaseResponse(resp.json() if resp.text else [])


_client: SupabaseClient | None = None


def get_supabase() -> SupabaseClient:
    """Get singleton Supabase client instance."""
    global _client
    if _client is None:
        if not SUPABASE_URL or not SUPABASE_SERVICE_KEY:
            raise ValueError(
                "SUPABASE_URL and SUPABASE_SERVICE_KEY must be set in .env"
            )
        _client = SupabaseClient(SUPABASE_URL, SUPABASE_SERVICE_KEY)
    return _client
