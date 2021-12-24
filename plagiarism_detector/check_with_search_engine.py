from plagiarism_detector import copy_of_querrycrawler

import nltk

def check_2(searchString, is_check1=False):
    output = []
    if is_check1:
        output_1 = searchString
        for sent, is_plagrism in output_1:
            if is_plagrism:
                output.append((sent, True))
            else:
                is_plagiarism_bing, link = copy_of_querrycrawler.querry_bing(sent.strip())
                # print('Plagiarised: ', is_plagiarism)
                is_plagiarism_google, link = copy_of_querrycrawler.querry_google(sent.strip())
                # print('Plagiarised: ', is_plagiarism)
                if is_plagiarism_google or is_plagiarism_bing:
                    output.append((sent, True))
                else:
                    output.append((sent, False))
    else:
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

def check_1(source_text,para_text):
    
    output_1 = []
    
    for para_sentence in nltk.sent_tokenize(para_text):
        is_plag = False
        for source_sentence in nltk.sent_tokenize(source_text):
            if is_plag:
                continue
            if(len(source_sentence)==0 or len(para_sentence)==0):
                continue
            if copy_of_querrycrawler.check1(source_sentence.strip(),para_sentence.strip()):
                is_plag = True
        if is_plag:
            output_1.append((para_sentence, True))
        else:
            output_1.append((para_sentence, False))
    return output_1

def double_check(source_text,para_text):
    if source_text is None:
        output_1 = check_2(para_text)
        return output_1
    else:
        output_1 = check_1(source_text,para_text)
        output_2 = check_2(output_1, is_check1=True)
        return output_2