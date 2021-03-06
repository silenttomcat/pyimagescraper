import requests
import re
import os
from multiprocessing.dummy import Pool as ThreadPool

def fetch_image_urls(pages=1,key = "cat"):
    url_beauty = "https://pic.sogou.com/napi/pc/searchList?mode=2&start={}&xml_len=48&query={}"
    pattern_beauty = r'"locImageLink":.*?(https:.*?)",'
    num = 0
    image_list = []
    for i in range(0,pages):
        url = url_beauty.format(num,key)
        num += 48
        try:
            r_images = requests.get(url)
            image_list += re.findall(pattern_beauty,r_images.text,re.DOTALL)
        except Exception as e:
            print(e)
            
    return image_list
    
def add_exinfo_to_imglist(image_list,key,path):
    tmp_list = []
    n = 0
    for imgurl in image_list:
        n = n + 1
        imgurl = "{}@TOMYAN@{}@TOMYAN@{}".format(imgurl,os.path.join(path,key),n)
        tmp_list.append(imgurl)
    return tmp_list 

def save_a_image(imgurl):
    imgurl,path,n = imgurl.split("@TOMYAN@")
    print ("saving image {}".format(n))
    try:
        r = requests.get(imgurl,stream = True)
        with open(os.path.join(path,"{}.jpg".format(n)),"wb") as f:
            for chunk in r:
                f.write(chunk)  
    except Exception as e:
        print (e)
        return False
    return True        

def save_images(image_list=[],key = "cat",path="."):
    if not os.path.exists(os.path.join(path,key)):
        os.mkdir(os.path.join(path,key))  
    pool = ThreadPool(10)
    results = pool.map(save_a_image, image_list)
    pool.close()
    pool.join()
    return results       
            
def fetch_images_with_sogou_search(key="cat",pages=1,path="."):
    try:
        image_list = fetch_image_urls(pages=pages,key=key)
        image_list = add_exinfo_to_imglist(image_list,key,path)
        save_images(image_list=image_list,key = key,path=path)
        return True
    except Exception as e:
        print(e)
        return False
            
if __name__ == "__main__":
    pages = 10
    key = "cat"
    path = "d:\\test"
    print (fetch_images_with_sogou_search(key=key,pages=pages,path=path))
