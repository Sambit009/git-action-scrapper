import requests
import re
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as req
import yaml


def get_urls():
    req_url = "https://ebazhanov.github.io/linkedin-skill-assessments-quizzes/"
    client = req(req_url)
    main_page = client.read()
    main_page_html = bs(main_page, "html.parser")
    all_class = main_page_html.find("table")
    all_a = all_class.find_all('a')
    urls = []
    #print(all_a)
    for a_tag in all_a:
        url = a_tag['href']
        if not url.startswith('https'):
            url = "https://ebazhanov.github.io/"+url
            if url.endswith('.html'):
                urls.append(url)
    #print(urls)
    return urls
	    
def parse_expertise(expertise_page_html,url):
    url_list = url.split('/')
    for url_text in url_list:
        if url_text.endswith('.html'):
            url_list.remove(url_text)
        new_url = '/'.join(url_list)
    questions_html = expertise_page_html.find_all("h4")
    section_html = expertise_page_html.find("section")
    if section_html.find("h2"):
        expertise = section_html.find("h2").text
    elif section_html.find("h1"):
        expertise = section_html.find("h1").text
    elif section_html.find("h3"):
        expertise = section_html.find("h3").text
    options = expertise_page_html.find_all("ul")
    question_block = expertise_page_html.find("h4")
    question_list = []
    question_dict = {}
    for i in range(0,len(questions_html)):
        raw_question = question_block.text
        question = re.sub('^.*?. ',' ',raw_question).strip()
        question_dict['question'] = question
        all_option_html = question_block.find_next("ul")
        all_option = all_option_html.find_all('li')
        i=1
        try:
            question_dict['option_1'] = all_option[0].text
            question_dict['option_2'] = all_option[1].text
            question_dict['option_3'] = all_option[2].text
            question_dict['option_4'] = all_option[3].text
            for option in all_option:
                if option.find('input').has_attr('checked'):
                    correct_answer = option.text
                    if correct_answer == all_option[0].text:
                        question_dict['ans'] = 'option_1'
                    elif correct_answer == all_option[1].text:
                        question_dict['ans'] = 'option_2'
                    elif correct_answer == all_option[2].text:
                        question_dict['ans'] = 'option_3'
                    elif correct_answer == all_option[3].text:
                        question_dict['ans'] = 'option_4'
                    else:
                        question_dict['ans'] = ''                
        except:
            try:
                correct_answer =''
                option_1 = ''
                option_2 = ''
                option_3 = ''
                option_4 = ''
            except:
                continue
        if question_block.find_next().name == 'p':
            p_class = question_block.find_next()
            if p_class.find_next().name == 'img':
                #print('image found')
                img = p_class.next['src']
                img_url = new_url +'/' + img
                question_dict['question_img'] = img_url
                
                #print(img_url)
                #print(question_dict)
        question_dict_1 = question_dict.copy()
        question_list.append(question_dict_1)
        question_block = question_block.find_next("h4")
        
    return question_list,expertise
        
def main():
    questions = {}
    urls = get_urls()
    for url in urls:
        try:
            client = req(url)
        except:
            continue
        expertise_page = client.read()
        expertise_page_html = bs(expertise_page, "html.parser")
        question_list,expertise = parse_expertise(expertise_page_html,url)
        questions[expertise] = question_list
        #print(questions)
        with open(r'screening\questions\questions.yaml', 'w',encoding = "utf-8") as file:
            documents = yaml.dump(questions, file,allow_unicode = True)
   
    
        
    
        
main()  
