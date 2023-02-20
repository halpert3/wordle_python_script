import requests
import re
from variables import *

# getting list of all words
with open("words_string.txt", "r") as ws:
    words_string = ws.read()

# replicating for sacrifice word function
complete_words_string = words_string


def green_letters(input, letter_positions):

    if letter_positions == '':
        return input

    res = input

    # turn input into list
    green_input = letter_positions.split(', ')

    # in case input doesn't split out letters and multiple numbers
    for i in range(len(green_input)):
        while len(green_input[i]) > 2:
            green_input.append(f'{green_input[i][0]}{green_input[i][-1]}')
            green_input[i] = green_input[i][0:-1]

    # turn position strings into numbers
    green_input = [[x[0].lower(), int(x[1])-1] for x in list(green_input)]

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
    letters = "".join(set(letters)).lower()

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
        res = eliminate_used_yellow(res, y[0].lower(), y[1])
        res = find_potential_words_yellow(res, y[0].lower(), y[1])

    return res


def create_slot_dict(input, slot):
    slot = slot - 1
    slot_dict = dict()

    for word in input:
        if word[slot] not in slot_dict:
            slot_dict[word[slot]] = 1
        else:
            slot_dict[word[slot]] += 1

    return slot_dict


def score_word(word, slot_dicts, total_points):

    scores = list()
    for i in range(5):
        scores.append(slot_dicts[i].get(word[i])/total_points)

    return {word: sum(scores)/total_points}


def efficiency_slot(input):

    # split up the words into a list
    word_list = input.split('\n')
    word_list = [x for x in word_list if x != '']

    # create scoring dictionaries for each slot
    firs = create_slot_dict(word_list, 1)
    seco = create_slot_dict(word_list, 2)
    thir = create_slot_dict(word_list, 3)
    four = create_slot_dict(word_list, 4)
    fift = create_slot_dict(word_list, 5)

    slot_dicts = [firs, seco, thir, four, fift]
    # get total_points for divisor
    total_points = sum(firs.values())
    slot_scores = dict()
    for word in word_list:
        slot_scores.update(score_word(word, slot_dicts, total_points))

    normalization_base = sum(slot_scores.values())

    for k in slot_scores:
        slot_scores[k] = slot_scores.get(k)/normalization_base

    return slot_scores


def efficiency_elimination(input):
    # create a dictionary of how many times each letter appears in the set
    letters = input.replace('\n', '')

    lett_dict = dict()
    for x in letters:
        if x not in lett_dict:
            lett_dict[x] = 1
        else:
            lett_dict[x] += 1

    # split up the words into a list
    word_list = input.split('\n')
    word_list = [x for x in word_list if x != '']

    elim_scores = dict()
    # cycle through each word
    for word in word_list:
        score = 0
        elim_scores[word] = 0
        # tracking is so in a word with double letters, each letter is only counted once
        tracking = str()

        # for each letter in word, assign the dict's point value
        for x in range(5):
            if word[x] not in tracking:
                elim_scores[word] += lett_dict.get(word[x])
            else:
                continue
            tracking += word[x]

    total_scores = sum(elim_scores.values())

    for k in elim_scores:
        elim_scores[k] = elim_scores.get(k)/total_scores

    normalization_base = sum(elim_scores.values())

    for k in elim_scores:
        elim_scores[k] = elim_scores.get(k)/normalization_base

    return elim_scores


def efficiency(input, limit=None, elim_weight=.05):

    slot_weight = 1 - elim_weight

    elim = efficiency_elimination(input)
    slot = efficiency_slot(input)

    scores_dict = dict()
    for k in elim:
        scores_dict[k] = elim[k]*elim_weight + slot[k]*slot_weight

    scores = list()
    for key, val in scores_dict.items():
        scores.append([key, val])

    for item in scores:
        item[1] = round(item[1]*100, 4)

    scores.sort(key=lambda x: x[1], reverse=True)

    # determine how many scores to display
    scores = scores[:limit]

    # determine how many scores to display

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


def sacrifice_word(input, letters, unique_letter_positions):
    if unique_letter_positions == '':
        unique_list = list()
    else:
        unique_input = unique_letter_positions.split(', ')
        unique_list = [list(filter(None, re.split('(\d+)', u)))
                       for u in unique_input]
    for item in unique_list:
        item[1] = int(item[1]) - 1

    res = '\n'.join(re.findall(f'\w*[{letters}]\w*', input))
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
    scores = scores[:20]

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

    return final


if sacrifice_mode == False:
    words_string = not_contain(words_string, letters_not_in_answer)
    words_string = green_letters(words_string, green)
    words_string = yellow_letters(words_string, yellow)
    eff = efficiency(words_string, limit=limit, elim_weight=elim_weight)
    print(eff)
if sacrifice_mode == True:
    sac_wor = sacrifice_word(complete_words_string, sacrifice_word_letters,
                             sacrifice_unique_letter_positions)
    print(sac_wor)
