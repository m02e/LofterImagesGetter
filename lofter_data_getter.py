'''
Created on 2013-6-19

@author: MOZE
'''
from BeautifulSoup import BeautifulSoup
import urllib2
import urllib

def get_images_url_list(lofter_url,is_original = False):
    image_list = []
    soup = BeautifulSoup(urllib2.urlopen(lofter_url,timeout=10).read())
    post_data_list = [ a_link for a_link in soup.findAll('a') \
                      if a_link.get('href')!=None \
                      and str(a_link['href']).count('lofter.com/post')>0 \
                      and a_link.find('img')!=None 
                      ]
    for a_link in post_data_list:
        if not is_original:
            image_list+=[str( a_link.find('img')['src'] )]
        else:
            post_page_url = a_link['href']
            try:
                post_soup = BeautifulSoup(urllib2.urlopen(post_page_url,timeout=10).read())
            except:
                print 'some erro in open ',post_page_url
                continue
            post_page_a_links =  post_soup.findAll('a',attrs={'href':'#'})
            for post_page_a_link in post_page_a_links:
                for img_url in  post_page_a_link.findAll('img'):
                    image_list+=[str(img_url.get('src'))]
    return image_list

def get_all_images_url_list(main_lofter_url,is_original = False):
    all_images_url_list=[]
    is_last_page = False
    page_index = 1
    while not is_last_page:
        page_list = get_images_url_list(main_lofter_url+'?page=%i' % page_index, is_original)
        page_index+=1
        if len(page_list)==0:
            break;
        all_images_url_list+=page_list
    return all_images_url_list

if __name__=='__main__':
    pass
    lofter_url = 'http://mirmoze.lofter.com/'
    images_url_list = get_all_images_url_list(lofter_url,is_original=True)
    for image_url in images_url_list:
        try:
            f = open('/Users/moze/Pictures/lofter/'+image_url.replace('/','-'),'wb')
            f.write( urllib.urlopen(image_url).read())
            f.close()
            print 'download >> '+ image_url.replace('/','-')
        except:
            print 'download erro>> '+ image_url.replace('/','-')
    print 'all finish'
    
    
    
    
    