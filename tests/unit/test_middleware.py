from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_proxy_headers_middleware():
    """
    Test that ProxyHeadersMiddleware correctly identifies HTTPS when X-Forwarded-Proto is set.
    """
    # Without headers, it should be http (default in TestClient)
    response_http = client.get("/debug/scheme")
    assert response_http.json()["scheme"] == "http"

    # Simulate a request through a proxy with X-Forwarded-Proto: https
    # Note: Remote ADDR must be trusted. ProxyHeadersMiddleware with trusted_hosts="*" handles this.
    response_https = client.get("/debug/scheme", headers={"X-Forwarded-Proto": "https"})
    assert response_https.status_code == 200
    assert response_https.json()["scheme"] == "https"
    # Inside the app, request.url.scheme should be 'https'
    # Since we can't easily check the internal request object from TestClient response,
    # we rely on the fact that if it's correctly trusted, url_for will generate https URLs.

    # Check if the app runs without error with the configuration added in main.py.
    response_https = client.get(
        "/", headers={"X-Forwarded-Proto": "https", "X-Forwarded-For": "1.2.3.4"}
    )
    assert response_https.status_code == 200
    # Verifying that the middleware is active by checking if the app runs without error
    # with the configuration added in main.py.
