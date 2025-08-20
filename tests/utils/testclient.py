import json

class Testclient:
    def __init__(self, client, auth_headers=None):
        self.client = client
        self.default_headers = auth_headers or {}
    
    def _make_headers(self, headers=None):
        """Merge default headers with provided headers."""
        final_headers = self.default_headers.copy()
        if headers:
            final_headers.update(headers)
        return final_headers
    
    def get(self, url, headers=None):
        """Make GET request."""
        return self.client.get(
            url,
            headers=self._make_headers(headers)
        )
    
    def post(self, url, data=None, headers=None):
        """Make POST request."""
        return self.client.post(
            url,
            data=json.dumps(data) if data else None,
            headers=self._make_headers(headers),
            content_type='application/json'
        )
    
    def delete(self, url, headers=None):
        """Make DELETE request."""
        return self.client.delete(
            url,
            headers=self._make_headers(headers)
        )
    
    def assert_status(self, response, expected_status):
        """Assert response status code."""
        assert response.status_code == expected_status, \
            f"Expected status {expected_status}, got {response.status_code}. Response: {response.get_data(as_text=True)}"
    
    def assert_json(self, response, expected_data=None):
        """Assert response is JSON and optionally check data."""
        assert response.content_type == 'application/json'
        data = response.get_json()
        
        if expected_data:
            if isinstance(expected_data, dict):
                for key, value in expected_data.items():
                    assert data.get(key) == value, \
                        f"Key '{key}': expected {value}, got {data.get(key)}"
            else:
                assert data == expected_data
        
        return data