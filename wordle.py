import requests
import re
from variables import *

# getting list of all words
with open("words_string.txt", "r") as ws:
    words_string = ws.read()

# replicating for sacrifice word function
complete_words_string = words_string

# getting list of possible answers
with open("possible_answers.txt", "r") as pa:
    possible_answers = pa.read()
possible_answers_list = possible_answers.split('\n')


def not_contain(input, letters):
    # skip function if no letters given
    if letters == '':
        return input

    # remove duplicates and make lowercase
    letters = "".join(set(letters)).lower()

    # create regex and find words that don't contain these letters
    regex = f'\\b[^{letters}]*\\b'
    res = '\n'.join(re.findall(f'{regex}', input))
    res = re.sub('\n+', '\n', res)
    return res


def green_letters(input, letter_positions):

    # skip function if no green letters
    if letter_positions == '':
        return input

    # re-assign variable
    res = input

    # turn letter_positions into list
    green_input = letter_positions.split(', ')

    # in case input doesn't split out letters and multiple numbers
    for i in range(len(green_input)):
        while len(green_input[i]) > 2:
            green_input.append(f'{green_input[i][0]}{green_input[i][-1]}')
            green_input[i] = green_input[i][0:-1]

    # turn position strings into numbers
    green_input = [[x[0].lower(), int(x[1])-1] for x in list(green_input)]

    for g in green_input:
        # create regex string for each letter
        new_str = str()
        letter = g[0]
        position = g[1]
        for i in range(5):
            if i == position:
                new_str += letter
            else:
                new_str += '.'
        # find words with letters in needed position
        res = '\n'.join(re.findall(f'{new_str}', res))

    return res


def eliminate_used_yellow(input, letter, positions):
    # re-assign variable
    res = input

    # turn number strings into indices
    positions = [int(x)-1 for x in list(positions)]

    # create regex to eliminate words that have the letter in the yellow position
    all_regex = list()
    for j in positions:
        new_str = str()
        for i in range(5):
            if i == j:
                new_str += f'[^{letter}]'
            else:
                new_str += '.'

        all_regex.append(new_str)

    # crate a list of regex's to run
    all_regex = [f'\\b{x}\\b' for x in all_regex]
    # run the regexes and rejoin the created list as a string
    for regex in all_regex:
        res = '\n'.join(re.findall(f'{regex}', res))
    return res


def find_potential_words_yellow(input, letter, positions):
    all_regex = list()

    # turn number strings into indices
    positions = [int(x)-1 for x in list(positions)]
    # potential positions for yellow letters
    positions = [x for x in range(5) if x not in positions]

    # create regex for each letter
    for j in positions:
        new_str = str()
        for i in range(5):
            if i == j:
                new_str += letter
            else:
                new_str += '.'

        all_regex.append(new_str)

    regex = "\\b"

    # use the "|" to create a series of "or" regexes
    for x in all_regex:
        regex += x + '\\b|\\b'
    regex = regex[:-3]
    # run the regexes and rejoin the created list as a string
    res = '\n'.join(re.findall(f'{regex}', input))
    return res


def yellow_letters(input, letter_positions):
    # skip function if no yellow letters
    if letter_positions == '':
        return input

    # split letter_positions into list for looping
    yellow_input = letter_positions.split(', ')
    # split the letters from positions
    yellow_list = [list(filter(None, re.split('(\d+)', y)))
                   for y in yellow_input]
    # re-assign input
    res = input

    # run through two yellow functions for each letter and position
    for y in yellow_list:
        res = eliminate_used_yellow(res, y[0].lower(), y[1])
        res = find_potential_words_yellow(res, y[0].lower(), y[1])

    return res


def create_slot_dict(input, slot):
    # adjust index and create empty dictionary
    slot = slot - 1
    slot_dict = dict()

    # create a dictionary counting each time a letter appears in that position
    for word in input:
        if word[slot] not in slot_dict:
            slot_dict[word[slot]] = 1
        else:
            slot_dict[word[slot]] += 1

    return slot_dict


def score_word(word, slot_dicts, total_points):

    # for a word, this function averages the scores for each letter appearing
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

    # create a dictionay with a score for each word
    slot_scores = dict()
    for word in word_list:
        slot_scores.update(score_word(word, slot_dicts, total_points))

    # normalize the scores so they work with percentages
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

    # create total_scores for a divisor
    total_scores = sum(elim_scores.values())

    # divide each word's score by the total
    for k in elim_scores:
        elim_scores[k] = elim_scores.get(k)/total_scores

    # normalize the scores so they work with percentages
    normalization_base = sum(elim_scores.values())

    for k in elim_scores:
        elim_scores[k] = elim_scores.get(k)/normalization_base

    return elim_scores


def check_poss_answer(word):
    # returns a check mark if the word is in the possible answer list
    check = u'\N{check mark}'
    if word in possible_answers_list:
        return f'{check}'
    else:
        return ''


def efficiency(input, limit=None, elim_weight=.05):

    # run the two efficiency methods
    elim = efficiency_elimination(input)
    slot = efficiency_slot(input)

    # provide desired weight to the two efficiency methods
    slot_weight = 1 - elim_weight

    # create a dictionary for the final scores
    scores_dict = dict()
    for k in elim:
        scores_dict[k] = elim[k]*elim_weight + slot[k]*slot_weight

    # convert dictonary of scores into list
    scores = list()
    for key, val in scores_dict.items():
        scores.append([key, val])

    # round the score to 4 decimals
    for item in scores:
        item[1] = round(item[1]*100, 4)

    # sort scores by highest first
    scores.sort(key=lambda x: x[1], reverse=True)

    # determine how many scores to display
    scores = scores[:limit]

    # create a list of scores to return
    # buff and cnt help give the same ranking to ties
    final = str()
    buff = scores[0][1]
    cnt = 0
    for i, item in enumerate(scores):
        if i == 0:
            final += f'{i+1}. {item[0]} {item[1]}% {check_poss_answer(item[0])}\n'
        elif item[1] == buff:
            cnt += 1
            final += f'{i+1-cnt}. {item[0]} {item[1]}% {check_poss_answer(item[0])}\n'
        else:
            final += f'{i+1}. {item[0]} {item[1]}% {check_poss_answer(item[0])}\n'
            buff = item[1]
            cnt = 0

    return final


def sacrifice_word(input, letters, unique_letter_positions):

    letters = letters.lower()

    # create an empty list if no unique_letter_postions
    if unique_letter_positions == '':
        unique_list = list()
    else:
        # create a list for unique_letter_positions
        unique_input = unique_letter_positions.split(', ')
        # create a list for anywhere letters
        unique_list = [list(filter(None, re.split('(\d+)', u)))
                       for u in unique_input]

    # convert string to integer as index
    for item in unique_list:
        item[0] = item[0].lower()
        item[1] = int(item[1]) - 1

    # find words in corpus with desired letters
    res = '\n'.join(re.findall(f'\w*[{letters}]\w*', input))
    res = res.split('\n')

    scores = list()

    # award a point for each time a letter appears
    for word in res:
        score = 0
        for i in range(len(letters)):
            if letters[i] in word:
                score += 1
        scores.append([word, score])

    # award a point for when a unique_letter_position appears in the right place
    for word_score in scores:
        for item in unique_list:
            i = item[1]
            if word_score[0][i] == item[0]:
                word_score[1] += 1
    # sort scores by highest first
    scores.sort(key=lambda x: x[1], reverse=True)
    # display top words
    scores = scores[:30]

    # create a list of scores to return
    # buff and cnt help give the same ranking to ties
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

# run all the functions


# run normal wordle search
if sacrifice_mode == False:
    words_string = not_contain(words_string, letters_not_in_answer)
    words_string = green_letters(words_string, green)
    words_string = yellow_letters(words_string, yellow)
    eff = efficiency(words_string, limit=limit, elim_weight=elim_weight)
    print(eff)

# run sacrifice mode
if sacrifice_mode == True:
    sac_wor = sacrifice_word(complete_words_string, sacrifice_word_letters,
                             sacrifice_unique_letter_positions)
    print(sac_wor)
