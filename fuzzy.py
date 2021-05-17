# FUZZY SEARCH
# Returns true if each character in pattern is found in the string sequentially

# Bonus Constants
ADJACENCY_BONUS = 5
SEPERATOR_BONUS = 10
CAMEL_BONUS = 10
LEADING_LETTER_PENALTY = -3
MAX_LEADING_LETTER_PENALTY = -9
UNMATCHED_LETTER_PENALTY = -1

def fuzzy_match(pattern, string):
    # Loop variables
    score = 0
    pattern_idx = 0
    pattern_length = len(pattern)
    prev_matched = False
    prev_lower = False
    prev_seperator = True  # Set True so that first letter gets seperator bonus

    # Use best matched letter if multiple letters match
    best_letter = None
    best_lower = None
    best_letter_score = 0


    # Looping over strings
    for (str_idx, str_char) in enumerate(string):

        pattern_char = '' if pattern_idx == pattern_length else pattern[pattern_idx]
        pattern_lower = pattern_char.lower() 

        str_lower = str_char.lower()
        str_upper = str_char.upper()

        next_match = pattern_char and pattern_lower == str_lower
        rematch = best_letter and best_lower == str_lower

        advanced = next_match and best_letter
        pattern_repeat = best_letter and pattern_char and best_lower == pattern_lower
        if(advanced or pattern_repeat):
            score += best_letter_score
            best_letter = ''
            best_lower = ''
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
            if prev_lower and str_char == str_upper:
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
                best_letter_score = new_score

            prev_matched = True

        else:
            # Appending unmatched chars
            score += UNMATCHED_LETTER_PENALTY
            prev_matched = False

        prev_lower = str_char == str_lower
        prev_seperator = str_char == '_' or str_char == ' '


    # Apply score for last match
    if best_letter:
        score += best_letter_score 

    return (pattern_idx == pattern_length, score)

