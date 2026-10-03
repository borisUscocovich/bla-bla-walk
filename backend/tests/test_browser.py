"""Exercise the actual browser map, independent of live source availability."""

import os
import shutil
import socket
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

import pytest
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[2]
pytestmark = pytest.mark.browser


@pytest.fixture(scope="module")
def browser_page():
    """Start the documented server and an installed Chromium for interactions."""
    executable = os.environ.get("CHROMIUM_PATH") or shutil.which("chromium")
    if not executable:
        pytest.skip("Browser checks need installed Chromium or CHROMIUM_PATH")
    with socket.socket() as reservation:
        reservation.bind(("127.0.0.1", 0))
        port = reservation.getsockname()[1]
    server = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "uvicorn",
            "bla_bla_walk.main:app",
            "--app-dir",
            "backend",
            "--host",
            "127.0.0.1",
            "--port",
            str(port),
        ],
        cwd=ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    url = f"http://127.0.0.1:{port}"
    try:
        for _ in range(100):
            try:
                with urllib.request.urlopen(url, timeout=1):
                    break
            except OSError:
                if server.poll() is not None:
                    raise RuntimeError("Test API failed to start") from None
                time.sleep(0.05)
        else:
            raise RuntimeError("Test API did not become ready")
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(executable_path=executable)
            page = browser.new_page(viewport={"width": 1280, "height": 900})
            page.set_default_timeout(10_000)
            page.base_url = url
            # Real basemap request is checked separately; failure is deterministic here.
            page.route("https://wmts.geo.bs.ch/**", lambda route: route.abort())
            yield page
            browser.close()
    finally:
        server.terminate()
        server.wait(timeout=5)


def open_map(page):
    """Wait for the actual API round trip and three keyboard sample controls."""
    page.goto(page.base_url)
    page.wait_for_function(
        "document.querySelector('#api-status').textContent.includes('connected')"
    )
    assert page.locator("#features button").count() == 3


def test_layers_provenance_and_missing_states(browser_page):
    page = browser_page
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    open_map(page)
    page.get_by_role("button", name="Sample sensor A").click()
    assert "28 °C" in page.locator("#details").inner_text()
    assert "Synthetic fixture" in page.locator("#details").inner_text()
    assert "01/10/2026" in page.locator("#details").inner_text()
    toggle = page.get_by_role("checkbox", name="Temperature")
    toggle.uncheck()
    assert page.get_by_role("button", name="Sample sensor A").is_hidden()
    toggle.check()
    page.get_by_role("button", name="Sample sensor B").click()
    assert "Unknown / no value" in page.locator("#details").inner_text()
    page.get_by_role("button", name="Sample fountain A").focus()
    page.keyboard.press("Enter")
    assert "Drinking water" in page.locator("#details").inner_text()
    assert "unknown" in page.locator("#details").inner_text()
    page.wait_for_function(
        "document.querySelector('#basemap-status').textContent.includes('unavailable')"
    )
    assert not errors


def test_api_failure_and_recovery(browser_page):
    page = browser_page
    page.route(
        "**/api/map", lambda route: route.fulfill(status=503, body="Unavailable")
    )
    page.goto(page.base_url)
    page.wait_for_function(
        "document.querySelector('#api-status').textContent.includes('Layers missing')"
    )
    assert page.locator("#features button").count() == 0
    page.unroute("**/api/map")
    page.get_by_role("button", name="Reload layers").click()
    page.wait_for_function(
        "document.querySelector('#api-status').textContent.includes('connected')"
    )
    assert page.locator("#features button").count() == 3


def test_narrow_screen_and_browser_contract(browser_page):
    page = browser_page
    page.set_viewport_size({"width": 390, "height": 844})
    open_map(page)
    assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
    assert page.locator("#map").bounding_box()["height"] >= 400
    result = page.evaluate("""async () => {
      const {parseSnapshot} = await import('/src/api.js');
      const fixture = await (await fetch('/api/map')).json();
      parseSnapshot(fixture);
      const bad = structuredClone(fixture);
      bad.layers[0].features[0].geometry.coordinates = [181, 47];
      try { parseSnapshot(bad); return false; } catch { return true; }
    }""")
    assert result
