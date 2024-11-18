import requests
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class ExternalGroceryService:
    def __init__(self):
        self.base_url = settings.EXTERNAL_API_URL
        self.headers = {
            "Content-Type": "application/json",
        }

    def create_shopping_list(self, items):
        """
        Sends a shopping list to the external grocery service.

        Args:
            items (list): A list of dictionaries representing items.
                          Example format: [{"name": "Milk", "quantity": 2}, {"name": "Eggs", "quantity": 12}]

        Returns:
            dict: Response from the external service (or mock response).
        """
        url = f"{self.base_url}/api/shopping-cart"
        print(url)
        payload = {"items": items}

        try:
            logger.info("Sending request to external API: %s", url)
            logger.info("Payload: %s", payload)

            response = requests.post(url, json=payload, headers=self.headers)
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx, 5xx)

            logger.info("External API response: %s", response.json())
            return response.json()

        except requests.exceptions.RequestException as e:
            # Log the error and return a failure message
            logger.error("Error interacting with the external grocery service: %s", e)
            return {"error": "Failed to create shopping list in the external service"}
