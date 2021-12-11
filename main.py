from api_mock import create_app
import logging

app = create_app()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.debug("Starting api at 127.0.0.1:5000/api/v1")

app.run(debug=True)
