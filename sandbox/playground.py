import requests
import re

r = requests.get(
    'https://raw.githubusercontent.com/tabatkins/wordle-list/main/words')

words_string = str(r.content, 'utf-8')

words_string = 'masts\namour\nramen\nharem\nhitch\npenis\nspine\nmiser\ngreat\ngrape'
# words_string = 'abcde\nabcdz\nedcda\nabcxy\nabwuv\naqrst\najjjz'


letters = 'gp'
unique_letter_positions = 'e5'
# unique_letter_positions = ''

if unique_letter_positions == '':
    unique_list = list()
else:
    unique_input = unique_letter_positions.split(', ')
    unique_list = [list(filter(None, re.split('(\d+)', u)))
                   for u in unique_input]
    for item in unique_list:
        item[1] = int(item[1]) - 1

res = '\n'.join(re.findall(f'\w*[{letters}]\w*', words_string))
res = res.split('\n')

scores = list()

for word in res:
    score = 0
    for i in range(len(letters)):
        if letters[i] in word:
            score += 1
    scores.append([word, score])


for word_score in scores:
    for item in unique_list:
        i = item[1]
        if word_score[0][i] == item[0]:
            word_score[1] += 1


scores.sort(key=lambda x: x[1], reverse=True)
scores = scores[:15]


final = str()
buff = scores[0][1]
cnt = 0
for i, item in enumerate(scores):
    if item[1] > 1:
        pt = 'points'
    else:
        pt = 'point'
    if i == 0:
        final += f'{i+1}. {item[0]} - {item[1]} {pt}\n'
    elif item[1] == buff:
        cnt += 1
        final += f'{i+1-cnt}. {item[0]} - {item[1]} {pt}\n'
    else:
        final += f'{i+1}. {item[0]} - {item[1]} {pt}\n'
        buff = item[1]
        cnt = 0


print(final)

