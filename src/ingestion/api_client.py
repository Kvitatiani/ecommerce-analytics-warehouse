"""API client for fetching raw data from the Platzi Fake Store API.

Provides a generic GET interface used by the bronze ingestion layer
to pull categories, products, and users.
"""

import requests

base_url = "https://api.escuelajs.co/api/v1"

def get_api_data(api_category):
    """Fetch JSON data from the Platzi Fake Store API for a given category.

    Args:
        api_category: The API endpoint path segment (e.g. "products",
            "categories", "users").

    Returns:
        list[dict]: Parsed JSON response as a list of dictionaries,
            or None if the request fails.
    """
    try:
        response = requests.get(f"{base_url}/{api_category}", timeout=10)
        response.raise_for_status()  # Check if the request was successful
        data = response.json()
        return data
    except Exception as e:
        print(f"Error fetching data from API: {e}")
        return None
    
if __name__ == "__main__":
    api_category = "categories"
    categories = get_api_data(api_category)
    if categories:
        print(f"Fetched {len(categories)} categories from the API")
    else:
        print("Failed to fetch categories from the API")