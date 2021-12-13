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
