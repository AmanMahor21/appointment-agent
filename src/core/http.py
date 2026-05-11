import logging
from typing import Optional, Any
import httpx

# logging.basicConfig(filename="app.log", level=logging.INFO,
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

logger = logging.getLogger(__name__)


class APIClient:

    def __init__(self, timeout: float = 10.0):
        self.timeout = timeout

    async def http(self, url: str, method: str = "GET", json: Optional[any] = None) -> dict[Any]:

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:

                req_method = getattr(client, method.lower())

                response = await req_method(
                    url,
                    json=json
                )

                response.raise_for_status()

                data = response.json()
                return data

        except httpx.TimeoutException:
            logger.exception("Request timeout: %s", url)
            raise

        except httpx.HTTPStatusError as e:
            logger.exception("HTTP status error: %s | %s",
                             url, e.response.text)
            raise

        except httpx.HTTPError as e:
            logger.exception("HTTP error: %s | %s", url, e)
            raise

        except Exception:
            logger.exception("Unexpected error: %s", url)
            raise
