import requests

url = "https://jsonplaceholder.typicode.com/posts"

def get_data():
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print("GET Error:", e)
        return None


def post_data(data):
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print("POST Error:", e)
        return None


data = {
    "title": "AI Engineer",
    "body": "Learning Requests Library",
    "userId": 1
}

# result = post_data(data)
# print(result)

res = get_data()
print(res)