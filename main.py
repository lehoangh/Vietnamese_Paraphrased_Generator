from plagiarism_detector import copy_of_querrycrawler

if __name__ == '__main__':

  searchString = 'Một số người đang cùng nhau đá bóng trên cát ngoài biển . Một cầu thủ ném bóng đang chuẩn bị ném bóng'

  for s in searchString.split('.'):
    print(s.strip())
    if(len(s)==0):
      continue
    print('Plagiarised: ', copy_of_querrycrawler.querry_bing(s.strip())[0]=='null')
    print('Plagiarised: ', copy_of_querrycrawler.querry_google(s.strip())[0]=='null')