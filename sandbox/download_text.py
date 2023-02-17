import requests

r = requests.get(
    'https://raw.githubusercontent.com/tabatkins/wordle-list/main/words')
with open("words_string.txt", "w") as f:
    f.write(r.text)
