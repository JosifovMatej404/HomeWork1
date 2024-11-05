import requests

def get_html_page(url):
    try:
        response = requests.get(url)
        # Check if the request was successful
        if response.status_code == 200:
            return response.text
        else:
            print(f"Failed to fetch the page. Status code: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None