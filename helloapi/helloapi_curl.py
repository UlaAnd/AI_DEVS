import subprocess


def get_auth(apikey='1f47a064-eb87-4b92-b1fb-47bc007f2360'):
    # Tworzenie komendy curl jako listy argumentów
    curl_command = [
        'curl',
        '-d', f'{{"apikey":"{apikey}"}}',
        'https://zadania.aidevs.pl/token/helloapi'
    ]
    try:
        # Uruchomienie polecenia curl
        result = subprocess.run(curl_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        # Wyświetlenie wyniku polecenia
        print("Output:", result.stdout)
        return result.stdout
    except subprocess.CalledProcessError as e:
        # Obsługa błędów, jeśli polecenie curl zakończy się błędem
        print("Błąd:", e.stderr)


def get_task():
    auth = get_auth()
    token = auth.get("token")

    curl_command = [
        'curl',
        f'https://zadania.aidevs.pl/task/{token}'
    ]
    try:
        result = subprocess.run(curl_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        print("Output:", result.stdout)
        return [result.stdout, token]
    except subprocess.CalledProcessError as e:
        print("Błąd:", e.stderr)


def post_answer():
    task = get_task()
    cookie = task[0].get("cookie")
    curl_command = [
        'curl',
        '-d', f'{{"answer": "{cookie}"}}',

        f'https://zadania.aidevs.pl/answer/{task[1]}'
    ]
    try:
        result = subprocess.run(curl_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        print("Output:", result.stdout)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print("Błąd:", e.stderr)

# my_response = {
#     "code": 0,
#     "msg": "OK",
#     "token": "7c8cc7bcb889e98566698a80f3ce047464728ead"
# }
#
# def get_token2():
#     token = my_response.get("token")
#     print(f'mój token: {token}')