# FUZZY SEARCH
# Returns true if each character in pattern is found in the string sequentially
def fuzzy_match_simple(pattern, string):
    pattern_idx = 0
    pattern_length = len(pattern)
    str_idx = 0
    str_length = len(string)

    while pattern_idx != pattern_length and str_idx != str_length:
        pattern_char = pattern[pattern_idx].lower()
        str_char = string[str_idx].lower()
        if pattern_char == str_char:
            pattern_idx += 1
        str_idx += 1
    return (pattern_length != 0
            and str_length != 0
            and pattern_idx == pattern_length)


def fuzzy_match(pattern, string):
    # Bonus Constants
    ADJACENCY_BONUS = 5
    SEPERATOR_BONUS = 10
    CAMEL_BONUS = 10
    LEADING_LETTER_PENALTY = -3
    MAX_LEADING_LETTER_PENALTY = -9
    UNMATCHED_LETTER_PENALTY = -1

    # Loop variables
    score = 0
    pattern_idx = 0
    pattern_length = len(pattern)
    str_idx = 0
    str_length = len(string)
    prev_matched = False
    prev_lower = False
    prev_seperator = True  # Set True so that first letter gets seperator bonus

    # Use best matched letter if multiple letters match
    best_letter = None
    best_lower = None
    best_letter_idx = None
    best_letter_score = 0

    matched_indices = []

    # Looping over strings
    while str_idx != str_length:
        if pattern_idx == pattern_length:
            pattern_char = ''
        else:
            pattern_char = pattern[pattern_idx]

        str_char = string[str_idx]

        if pattern_char:
            pattern_lower = pattern_char.lower()
        else:
            pattern_lower = ''
        str_lower = str_char.lower()
        str_upper = str_char.upper()

        next_match = pattern_char and pattern_lower == str_lower
        rematch = best_letter and best_lower == str_lower

        advanced = next_match and best_letter
        pattern_repeat = best_letter and pattern_char and best_lower == pattern_lower
        if(advanced or pattern_repeat):
            score += best_letter_score
            matched_indices.append(best_letter_idx)
            best_letter = ''
            best_lower = ''
            best_letter_idx = ''
            best_letter_score = 0

        if next_match or rematch:
            new_score = 0

            # Apply penalty for each letter b4 the pattern match
            # ALso, since penalties are -ve, max gives smallest penalty
            if pattern_idx == 0:
                penalty = max(str_idx * LEADING_LETTER_PENALTY, MAX_LEADING_LETTER_PENALTY)
                score += penalty

            # Apply bonus for consecutive matches
            if prev_matched:
                new_score += ADJACENCY_BONUS

            # Apply bonus for matches after a seperator
            if prev_seperator:
                new_score += SEPERATOR_BONUS

            # Apply bonus for camelCase matches
            if prev_lower and str_char == str_upper and str_lower != str_upper:
                new_score += CAMEL_BONUS

            # Update patter index IFF the next pattern letter was matched
            if next_match:
                pattern_idx += 1

            # Update best letter in str which may be for a "next" letter or a "rematch"
            if new_score >= best_letter_score:
                if best_letter:
                    score += UNMATCHED_LETTER_PENALTY
                best_letter = str_char
                best_lower = best_letter.lower()
                best_letter_idx = str_idx
                best_letter_score = new_score

            prev_matched = True

        else:
            # Appending unmatched chars
            score += UNMATCHED_LETTER_PENALTY
            prev_matched = False

        prev_lower = str_char == str_lower and str_lower != str_upper
        prev_seperator = str_char == '_' or str_char == ' '

        str_idx += 1

    # Apply score for last match
    if best_letter:
        score += best_letter_score
        matched_indices.append(best_letter_idx)

    matched = pattern_idx == pattern_length
    return (matched, score)


def main():
    # If doing simple, print alphabetically
    result = fuzzy_match_simple('pattern', 'StringToMatchPattern.tsx')
    print(result)
    # If doing complex, print ranked
    result = fuzzy_match('pattern', 'StringToMatchPattern.tsx')
    print(result)


if __name__ == "__main__":
    main()
