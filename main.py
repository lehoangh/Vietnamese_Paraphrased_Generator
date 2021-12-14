import detector

if __name__ == '__main__':

  searchString = 'Một số người đang cùng nhau đá bóng trên cát ngoài biển . Một cầu thủ ném bóng đang chuẩn bị ném bóng'

  for s in searchString.split('.'):
    print(s.strip())
    if(len(s)==0):
      continue
    print('Plagiarised: ', querry(s.strip())=='null')