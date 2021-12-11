import os
import tempfile
import pytest
import json

from api_mock import create_app


@pytest.fixture
def authenticated_client():
    app = create_app()

    with app.test_client() as client:
        client.environ_base[
            "HTTP_AUTHORIZATION"
        ] = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.W9wGb8Cs1SoCoiJ6WRzK6NMg7xed7PBNYJpBNIoD_G8"
        yield client


def test_hello(authenticated_client):
    response = authenticated_client.get("/api/v1/devices/")
    device_data = json.loads(response.data)

    thermostat_data = {
        "id": "e4d197aa-fa13-4255-b395-63268be12515",
        "name": "Living Room",
        "type": "thermostat",
        "location": "Living Room",
        "status": "on",
        "provisioned": True,
    }
    assert device_data[0] == thermostat_data
