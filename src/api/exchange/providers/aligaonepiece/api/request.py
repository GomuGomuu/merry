import logging
import requests

logger = logging.getLogger(__name__)


def _make_request_url(endpoint: str, base_url: str = None, endpoint_params: str = None):
    if endpoint_params:
        return f"{base_url}/{endpoint.format(endpoint_params)}"
    return f"{base_url}/{endpoint}"


def request(
    method: str,
    url: str,
    endpoint: str,
    endpoint_params: str = None,
    body: dict = None,
    headers: dict = None,
    **kwargs,
):
    request_url = _make_request_url(
        endpoint=endpoint, base_url=url, endpoint_params=endpoint_params
    )

    try:
        response = requests.post(
            url=request_url,
            json=body,
        )
        if response.status_code != 200:
            logger.error(
                f"Request to {request_url} failed with status code: {response.status_code}"
            )
            response.raise_for_status()

        return response.json()
    except Exception as e:
        logger.error(f"Request to {request_url} failed with errors: {e}")
        raise e
