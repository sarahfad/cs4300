import pytest
import requests
import task7
from task7 import get_status, get_encoding, post_json

# helpers to mock requests
class DummyResponse:
    def __init__(self, status_code=200, encoding="utf-8", json_data=None, raise_http=False):
        self.status_code = status_code
        self.encoding = encoding
        self._json_data = json_data
        self._raise_http = raise_http
        self.seen_json = None
        self.seen_headers = None

    def raise_for_status(self):
        if self._raise_http:
            raise requests.HTTPError(f"HTTP {self.status_code}")

    def json(self):
        if isinstance(self._json_data, Exception):
            raise self._json_data
        return self._json_data

def fake_get_factory(resp):
    def fake_get(url):
        return resp
    return fake_get

def fake_post_factory(resp):
    def fake_post(url, json=None, headers=None):
        resp.seen_json = json
        resp.seen_headers = headers
        return resp
    return fake_post

#tests

def test_get_status_ok_and_error(monkeypatch):
    ok = DummyResponse(status_code=204)
    monkeypatch.setattr(requests, "get", fake_get_factory(ok))
    assert get_status("http://x") == 204

    err = DummyResponse(status_code=404, raise_http=True)
    monkeypatch.setattr(requests, "get", fake_get_factory(err))
    with pytest.raises(requests.HTTPError):
        get_status("http://x")

def test_get_encoding_ok_and_error(monkeypatch):
    resp = DummyResponse(encoding="windows-1252")
    monkeypatch.setattr(requests, "get", fake_get_factory(resp))
    assert get_encoding("http://x/enc") == "windows-1252"

    err = DummyResponse(status_code=500, raise_http=True)
    monkeypatch.setattr(requests, "get", fake_get_factory(err))
    with pytest.raises(requests.HTTPError):
        get_encoding("http://x/enc")

def test_post_json_success_and_headers(monkeypatch):
    resp = DummyResponse(json_data={"ok": True})
    monkeypatch.setattr(requests, "post", fake_post_factory(resp))
    out = post_json("http://x/api", {"a": 1})
    assert out == {"ok": True}
    assert resp.seen_json == {"a": 1}
    assert resp.seen_headers and resp.seen_headers.get("Content-Type") == "application/json"

def test_post_json_http_error_and_bad_json(monkeypatch):
    err = DummyResponse(status_code=500, raise_http=True)
    monkeypatch.setattr(requests, "post", fake_post_factory(err))
    with pytest.raises(requests.HTTPError):
        post_json("http://x/api", {"a": 1})

    bad = DummyResponse(json_data=ValueError("not json"))
    monkeypatch.setattr(requests, "post", fake_post_factory(bad))
    with pytest.raises(ValueError):
        post_json("http://x/api", {"a": 1})
