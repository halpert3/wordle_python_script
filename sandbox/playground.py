with open("words_string.txt", "r") as ws:
    words_string = ws.read()

list_of_words = words_string.split('\n')

print(len(list_of_words))