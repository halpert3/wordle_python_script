import requests

r = requests.get(
    'https://gist.githubusercontent.com/cfreshman/d5fb56316158a1575898bba1eed3b5da/raw/25d00e56705240135119d4b604d78c3d30c46094/wordle-nyt-allowed-guesses-update-12546.txt')

words = r.text
print(words)
