from plagiarism_detector import copy_of_querrycrawler
import nltk
if __name__ == '__main__':
  nltk.download('punkt')
  searchString = 'Một số người đang cùng nhau đá bóng trên cát ngoài biển . Một cầu thủ ném bóng đang chuẩn bị ném bóng'
  sentence_list = nltk.tokenize.sent_tokenize(searchString)

  for s in sentence_list:
    print(s.strip())
    if(len(s)==0):
      continue
    is_plagiarism, link = copy_of_querrycrawler.querry_bing(s.strip())
    print('Plagiarised: ', is_plagiarism)
    is_plagiarism, link = copy_of_querrycrawler.querry_google(s.strip())
    print('Plagiarised: ', is_plagiarism)