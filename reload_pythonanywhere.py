import requests

def reload_webapp():
    username = "khaledmashoor99998"
    token = "10161cae20dd2984c9d70899b17182ab102996e5"
    
    print("Reloading web app...")
    response = requests.post(
        f'https://www.pythonanywhere.com/api/v0/user/{username}/webapps/{username}.pythonanywhere.com/reload/',
        headers={'Authorization': f'Token {token}'}
    )
    
    if response.status_code == 200:
        print("Web app reloaded successfully!")
    else:
        print(f"Failed to reload web app: {response.content}")

if __name__ == '__main__':
    reload_webapp()