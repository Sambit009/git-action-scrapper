import requests
import re
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as ureq
import yaml

def get_urls():
    req_url="https://ebazhanov.github.io/linkedin-skill-assessments-quizzes/"
    uclient = ureq(req_url)
    list_Page = uclient.read()
    listpage_html = bs(list_Page, "html.parser")
    all_class=listpage_html.find("table")
    all_a=all_class.find_all('a')
    urls = []
    #print(all_a)
    for a_tag in all_a:
        url = a_tag['href']
        if not url.startswith('https'):
            url = "https://ebazhanov.github.io/"+url
            if url.endswith('.html'):
                urls.append(url)
    return urls
def get_expertise(url):
    url_list=url.split('/')
    #print(url_list)
    for url_text in url_list:
        if url_text.endswith('.html'):
            new_url=url_text.replace('-quiz.html','')
            expertise=new_url.capitalize()
    return expertise

def get_question(questions,options,question_list,expertise):
    for i in range(0,len(questions)):
        ques = questions[i].text
        clean_question=re.sub('^.*?. ',' ',ques).strip()
        question_dict={}
        question_dict['expertise']=expertise
        question_dict['question']=clean_question
        try:
            all_options=options[i].find_all('li')
            question_dict['option_1'] = all_options[0].text
            question_dict['option_2'] = all_options[1].text
            question_dict['option_3']= all_options[2].text
            question_dict['option_4'] = all_options[3].text
            for op in all_options:
                if op.find('input').has_attr('checked'):
                    correct_answer = op.text
                    question_dict['correct_answer']=correct_answer
        except:
            try:
                correct_answer =''
                option_1 = ''
                option_2 = ''
                option_3 = ''
                option_4 = ''
            except:
                continue
        question_list.append(question_dict)
    
def get_detail():
    question_list=[]
    urls=[]
    urls=get_urls()
    for url in urls:
        expertise=get_expertise(url)
        uclient = ureq(url)
        q_detail_Page = uclient.read()
        q_detailspage_html = bs(q_detail_Page, "html.parser")
        questions = q_detailspage_html.find_all("h4")
        options = q_detailspage_html.find_all("ul")
        get_question(questions,options,question_list,expertise)
        with open(r'C:\Users\HP\Desktop\chiku\linkedin-skill-assessments-quizzes-master\django\store_file1.yaml', 'w') as file:
            documents = yaml.dump(question_list, file)
        
            





get_detail()
    
