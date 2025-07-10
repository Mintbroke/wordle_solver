words = []

with open("dictionary.txt", 'r') as f:
    for word in f:
        words.append(word.strip())
        
freqs = [{} for i in range(5)]

for word in words:
    for i in range(5):
        if(word[i] in freqs[i]):
            freqs[i][word[i]] += 1
        else:
            freqs[i][word[i]] = 1


def get_freqs(word: str) -> int:
    freq = 0
    for i in range(5):
        freq += freqs[i][word[i]]
    return freq

def get_uniques(word: str) -> int:
    unique = 0
    seen = set()
    for i in range(5):
        if(word[i] not in seen):
            unique += 1
            seen.add(word[i])
    return unique

def get_guess(valid = None) -> str:
    best_word = ""
    best_score = 0
    most_unique = 0
    if(not valid):
        #print("not valid")
        for word in words:
            score = get_freqs(word)
            unique = get_uniques(word)
            if(unique > most_unique):
                best_word = word
                best_score = score
                most_unique = unique
            elif(unique == most_unique):
                if(score > best_score):
                    best_score = score
                    best_word = word
                
    else:
        #print("valid")
        for word in valid:
            unique = get_uniques(word[0])
            if(unique > most_unique):
                best_word = word[0]
                best_score = word[1]
                most_unique = unique
            elif(unique == most_unique):
                if(word[1] > best_score):
                    best_word = word[0]
                    best_score = word[1]
                    most_unique = unique

    print(f"Best guess: {best_word}")
    return best_word
        


def wordle():
    must_be = [0 for i in range(5)]
    not_exist = set()
    might_be = {}
    eliminated = [set() for i in range(5)]
    guessed = set()

    valid_words = None
    valid_words_tmp = []
    
    for i in range(6):
        valid_words = valid_words_tmp
        valid_words_tmp = []

        
        print(f"valid_words: {valid_words}")
        print(f"must_be: {must_be}")
        print(f"might_be: {might_be}")
        print(f"not_exist: {not_exist}")
        
        
        guess = get_guess(valid_words)
        guessed.add(guess)
        guess_result = str(input("Enter the result (0 for no, 1 for somewhere else, 2 for yes): "))

        for i in range(5):
            # does not exist
            if(guess_result[i] == '0' and guess[i] not in must_be and guess[i] not in might_be):
                not_exist.add(guess[i])

            # exists somewhere else
            elif(guess_result[i] == '1'):
                if(guess[i] in might_be):
                    might_be[guess[i]].append(i)
                else:
                    might_be[guess[i]] = [i]
                if(guess[i] in not_exist):
                    not_exist.remove(guess[i])

            # must be
            elif(guess_result[i] == '2'):
                must_be[i] = guess[i]
                if(guess[i] in not_exist):
                    not_exist.remove(guess[i])
                    for index in range(len(guess)):
                        if(index != i and guess[i] == guess[index]):
                            eliminated[index].add(guess[i])


        for word in words:
            valid = True

            # if already guessed
            if(word in guessed):
                continue
            
            for i in range(5):
                # if must doesn't match
                if(must_be[i] != 0 and word[i] != must_be[i]):
                    valid = False
                    break

                if(word[i] in eliminated[i]):
                    valid = False
                    break

                # if contains not_exist letters
                if(word[i] in not_exist):
                    valid = False
                    break

                # if might be letter already tried in position
                if(word[i] in might_be):
                    if(i in might_be[word[i]]):
                        valid = False
                        break

                # if eliminated
                if(word[i] in eliminated[i]):
                    valid = False
                    break

            # if might_be letter not in word
            if(valid):
                for i in might_be:
                    if(i not in word):
                        valid = False
                        break
                if(valid):
                    valid_words_tmp.append((word, get_freqs(word)))
            

if __name__ == "__main__":
    while(True):
        try:
            wordle()
        except:
            print("----------------------------------------------------------------")
            print("---------------------------restart------------------------------")
            print("----------------------------------------------------------------")
                
