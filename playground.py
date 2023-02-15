import re


# word_strings = 'masts\namour\nramen\ntrams\nharem\nhitch\npenis\nspine\nnipes\nmiser'
word_strings = 'abcde\nabcdz\nedcda\nabcxy\nabwuv\naqrst\najjj'


# start efficiency_slot function
def create_slot_dict(input, slot):
    i = slot - 1
    slot_dict = dict()
    while i < len(input):
        if input[i] not in slot_dict:
            slot_dict[input[i]] = 1
        else:
            slot_dict[input[i]] += 1
        i += 6
    return slot_dict


def score_word(word, slot_dicts, total_points):

    # scores = dict()
    # for i in range(5):
    #     scores[word[i]] = slot_dicts[i].get(word[i])/total_points

    scores = list()
    for i in range(5):
        scores.append(slot_dicts[i].get(word[i])/total_points)

    return {word: sum(scores)/total_points}


def efficiency_slot(input):

    # split up the words into a list
    word_list = input.split('\n')
    word_list = [x for x in word_list if x != '']

    # create scoring dictionaries for each slot
    firs = create_slot_dict(input, 1)
    seco = create_slot_dict(input, 2)
    thir = create_slot_dict(input, 3)
    four = create_slot_dict(input, 4)
    fift = create_slot_dict(input, 5)

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


def efficiency(input, limit=None, elim_weight=.5):

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

    print(scores)
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


print(efficiency(word_strings))
