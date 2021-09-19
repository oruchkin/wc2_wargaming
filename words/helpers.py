# fucntions here:

# word counter from query - returns dict {"word":"count"}
def counter(query_text):
    reader = query_text
    dictionary = {}
    temp_word = ""
    for n in reader:
        i = n.lower()
        if i.isalpha():
             temp_word = temp_word + i
        else:
            if temp_word in dictionary:
                dictionary[temp_word] += 1
                temp_word = ""
            else:
                dictionary[temp_word] = int(1)
                temp_word = ""
                                
    # words to delete            
    keys = ["", "s", "t", "re", "m", "ll", "d", "o"]
    for i in keys:
        if i in dictionary:
            del dictionary[i]
                
    return dictionary
