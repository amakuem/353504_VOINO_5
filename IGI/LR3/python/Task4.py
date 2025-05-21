
def Task4_func():
    """Analyze a predefined text for various properties.

    This function processes a hardcoded text to:
    a) Count how many words have the minimum length.
    b) List all words followed by a comma.
    c) Find the longest word ending with 'y'.
    The results of each analysis are printed.
    """
    text = ("So she was considering in her own mind, as well as she could, for the hot day made her feel "
            "very sleepy and stupid, whether the pleasure of making a daisy-chain would be worth the trouble "
            "of getting up and picking the daisies, when suddenly a White Rabbit with pink eyes ran close by her.")

 
    words_with_punct = text.split()
    print(words_with_punct)
    all_words = []
    words_followed_by_comma = []

    for element in words_with_punct:
        if element.endswith(','):
            word = element[:-1] 
            words_followed_by_comma.append(word)  
            all_words.append(word) 
        elif element.endswith('.'):
            word = element[:-1]  
            all_words.append(word) 
        else:
            word = element 
            all_words.append(word)  

   
    lengths = [len(word) for word in all_words]  
    min_len = min(lengths)  
    count_min = lengths.count(min_len)  
    print("The number of words with the minimum length:", count_min)

   
    print("Words followed by a comma:")
    for word in words_followed_by_comma:
        print(word)

    
    candidates = [word for word in all_words if word.lower().endswith('y')]  # Фильтруем слова на 'y'
    if candidates:
        longest_word = max(candidates, key=len)  # Находим самое длинное
        print("The longest word ending in 'y':", longest_word)
    else:
        print("There are no words ending in 'y'")