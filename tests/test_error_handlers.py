import logging

from starlette.testclient import TestClient

logger = logging.getLogger(__name__)

def test_default_exception_handled():
    from basehttpmiddleware_missedexception.main import app
    client = TestClient(app, raise_server_exceptions=False)

    response = client.get('/raise-exception')

    logger.info(f"Response body: {response.content}")

    assert response.status_code == 500
    assert 'Content-Type' in response.headers
    assert response.headers['Content-Type'] == 'application/json'
    assert response.json() == {
        'error': 'HandledError',
        'error_description': 'Unknown error obtained by the ServerErrorHandler'
    }
