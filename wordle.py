import requests
import re

r = requests.get(
    'https://raw.githubusercontent.com/tabatkins/wordle-list/main/words')

words_string = str(r.content, 'utf-8')


def green_letters(input, letter_positions):

    if letter_positions == '':
        return input

    res = input
    green_input = letter_positions.split(', ')

    green_input = [[x[0], int(x[1])-1] for x in list(green_input)]

    for g in green_input:
        new_str = str()
        letter = g[0]
        position = g[1]
        for i in range(5):
            if i == position:
                new_str += letter
            else:
                new_str += '.'

        res = '\n'.join(re.findall(f'{new_str}', res))

    return res


def not_contain(input, letters):
    if letters == '':
        return input
    letters = "".join(set(letters))

    regex = f'\\b[^{letters}]*\\b'
    res = '\n'.join(re.findall(f'{regex}', input))
    res = re.sub('\n+', '\n', res)
    return res


def eliminate_used_yellow(input, letter, positions):

    res = input
    positions = [int(x)-1 for x in list(positions)]

    all_regex = list()
    for j in positions:
        new_str = str()
        for i in range(5):
            if i == j:
                new_str += f'[^{letter}]'
            else:
                new_str += '.'

        all_regex.append(new_str)

    all_regex = [f'\\b{x}\\b' for x in all_regex]

    for regex in all_regex:
        res = '\n'.join(re.findall(f'{regex}', res))
    return res


def find_potential_words_yellow(input, letter, positions):
    all_regex = list()
    positions = [int(x)-1 for x in list(positions)]
    positions = [x for x in range(5) if x not in positions]

    for j in positions:
        new_str = str()
        for i in range(5):
            if i == j:
                new_str += letter
            else:
                new_str += '.'

        all_regex.append(new_str)

    regex = "\\b"
    for x in all_regex:
        regex += x + '\\b|\\b'
    regex = regex[:-3]

    res = '\n'.join(re.findall(f'{regex}', input))
    return res


def yellow_letters(input, letter_positions):
    if letter_positions == '':
        return input

    yellow_input = letter_positions.split(', ')
    yellow_list = [list(filter(None, re.split('(\d+)', y)))
                   for y in yellow_input]

    res = input
    for y in yellow_list:
        res = eliminate_used_yellow(res, y[0], y[1])
        res = find_potential_words_yellow(res, y[0], y[1])

    return res


def efficiency(input, limit=None):
    # create a dictionary of how many times each letter appears in the set
    letters = input.replace('\n', '')

    lett_dict = dict()
    for x in letters:
        if x not in lett_dict:
            lett_dict[x] = 1
        else:
            lett_dict[x] += 1

    # create a list for holding the scores
    scores = list()

    # split up the words into a list
    word_list = input.split('\n')
    word_list = [x for x in word_list if x != '']

    # cycle through each word
    for word in word_list:
        score = 0

        # tracking is so in a word with double letters, each letter is only counted once
        tracking = str()

        # for each letter in word, assign the dict's point value
        for x in range(5):
            if word[x] not in tracking:
                score += lett_dict[word[x]]
            else:
                continue
            tracking += word[x]

        scores.append([word, score])
        scores.sort(key=lambda x: x[1], reverse=True)

    # get total_points for divisor
    total_points = sum([x[1] for x in scores])

    # divide score of each word/total points to get percentage
    for item in scores:
        item[1] = round(item[1]*100/total_points, 4)


    # determine how many scores to display
    scores = scores[:limit]

    # create a list of scores to return
    # buff and cnt help give the same ranking to ties
    final = str()
    buff = scores[0][1]
    cnt = 0
    for i, item in enumerate(scores):
        if i == 0:
            final += f'{i+1}. {item[0]} {item[1]}%\n'
        elif item[1] == buff:
            cnt += 1
            final += f'{i+1-cnt}. {item[0]} {item[1]}%\n'
        else:
            final += f'{i+1}. {item[0]} {item[1]}%\n'
            buff = item[1]
            cnt = 0

    return final








############################
# -------------------------#


letters_not_in_answer = ''
green = ''
yellow = ''


# -------------------------#
############################

words_string = not_contain(words_string, letters_not_in_answer)
words_string = green_letters(words_string, green)
words_string = yellow_letters(words_string, yellow)







eff = efficiency(words_string, limit=100)


print(eff)
