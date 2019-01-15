from bs4 import BeautifulSoup
import urllib.request
import os
import re

ROOT_URL = 'http://www.threatexpert.com/'
URL = 'http://www.threatexpert.com/reports.aspx'

def get_html(web_url):
	wp = urllib.request.urlopen(web_url)
	html = wp.read()
	return html

def get_detail(url,the_name):
	html=get_html(url)
	bs = BeautifulSoup(html, 'lxml')
	
	alias_tag = bs.find('li', text = re.compile('Alias'))
	if (alias_tag==None ):
		return the_name	
	if (alias_tag.next_sibling==None ):
		return the_name	
	if (alias_tag.next_sibling.next_sibling == None):
		return the_name
	name_list = alias_tag.next_sibling.next_sibling
	name_list = name_list.findAll('li')
	result_list = []
	text = ''	
	for item in name_list:
		if item.next.name == 'a':
			result_list.append(remove_bracket(item.next.next))
		elif '<em>' in str(item.next):
			result_list.append(remove_bracket(item.next.next + item.next.next_sibling))
		else:
			result_list.append(remove_bracket(item.next))

	result_list=', '.join(result_list)

	return result_list







def remove_bracket(text):
	if '[' in text:
		L = text.index('[')
		text = text[0:L]
		return text.strip()
	else:
		return text	

	


def get_reosurce_list(html):
    bs = BeautifulSoup(html, 'lxml')

    date_list   = bs.findAll('td', {'width': '150px'})
    risk_list   = bs.findAll('td', {'width': '40px'})
    origin_list = bs.findAll('td', {'width': '20px'})

    for i in range(0, len(date_list)):
        the_date = date_list[i].next
        the_risk = risk_list[i].next['src'].replace('./resources/', '').replace('.gif', '')
        the_name = origin_list[i].next_sibling.next.next.next.next
        
        the_origin = 'n/a'
        if origin_list[i].next.has_attr('alt') :
            the_origin = origin_list[i].next['alt']
        detail_link = ROOT_URL + origin_list[i].next_sibling.next.next['href']
        if the_name.find('..')!=-1 and the_name.find('..') != None:
            the_name=get_detail(detail_link,the_name)
        if the_name.find('..') == None:
            the_name=the_name.next
        output = '\"' + the_date + '\"' + ','
        output = output + '\"' + the_risk + '\"' + ','
        output = output + '\"' + the_origin + '\"' + ','
        output = output + '\"' + the_name+ '\"' + ','
        output = output + '\"' + detail_link + '\"'
        
        print(output)




for page_num in range(1, 11):
    web_url = URL + '?page=' + str(page_num)
    html = get_html(web_url)
    get_reosurce_list(html)




