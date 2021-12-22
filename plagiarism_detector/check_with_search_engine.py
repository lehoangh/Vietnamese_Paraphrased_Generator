from plagiarism_detector import copy_of_querrycrawler

import nltk

def check_2(searchString):
    output = []
    for s in nltk.sent_tokenize(searchString):
        if(len(s)==0):
            continue
        is_plagiarism_bing, link = copy_of_querrycrawler.querry_bing(s.strip())
        # print('Plagiarised: ', is_plagiarism)
        is_plagiarism_google, link = copy_of_querrycrawler.querry_google(s.strip())
        # print('Plagiarised: ', is_plagiarism)
        if is_plagiarism_google or is_plagiarism_bing:
            output.append((s, True))
        else:
            output.append((s, False))
    return output
    
