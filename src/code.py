import requests
import re
from bs4 import BeautifulSoup
from bs4.element import Comment
from pathos.multiprocessing import ProcessingPool as Pool
from toolz.sandbox.parallel import fold
import sys
import os
import json

visited = set()


def extract_domain(url):
    if url is None:
        return ''
    domain_regex = re.compile(r"https?:\/\/w{0,3}\.?(\w+)\.+")
    result = domain_regex.search(url)
    return result.group(1) if result else ""


def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


def extract_text(html_file):
    soup = BeautifulSoup(html_file, 'html.parser')
    filtered_tags = filter(tag_visible, soup.findAll(text=True))
    clean_text = u" ".join(t.strip() for t in filtered_tags)
    count = {}
    for s in clean_text.split():
        if s in count.keys():
            count[s] += 1
        else:
            count[s] = 1
    # print(count)
    return count


def scrap_site(url):
    domain = extract_domain(url)
    if url in visited:
        return False, '', []
    visited.add(url)
    try:
        response = requests.get(url)
    except:
        return False, '', []
    soup = BeautifulSoup(response.text, 'html.parser')
    nodes_internal = []
    # print(domain)
    for link in soup.find_all('a'):
        href = link.get('href')
        # print(f'href {href}')
        if href is not None and href.startswith('/'):
            nodes_internal.append(f'{url}{href[1:]}')
        elif extract_domain(href) == domain:
            nodes_internal.append(href)
    return True, response.text, nodes_internal


def combiner(dic1, dic2):
    combined = {}
    for k, v in dic1.items():
        combined[k] = v

    for k, v in dic2.items():
        if k in combined.keys():
            combined[k] += v
        else:
            combined[k] = v
    return combined


def process_site(site):
    number_of_iterations = 1
    nodes = [site]
    html_content = []
    with Pool() as p:
        while len(nodes) > 0 and number_of_iterations <= 5:
            print("***************************")
            print(
                f'number of iterations: {number_of_iterations} number of nodes: {len(nodes)} number of text files {len(html_content)}')
            sys.stdout.flush()
            number_of_iterations += 1
            scrapped = p.imap(scrap_site, nodes)
            nodes = []
            # print(scrapped)
            for s in scrapped:
                if s[0]:
                    html_content.append(s[1])
                    nodes = s[2]
        text = p.imap(extract_text, html_content)
        folded = fold(combiner, text, map=p.imap)
        # print(f'summary of site {site}:\n {folded}')
        print(f'writing file of site {site}: output/{extract_domain(site)}.txt')
        with open(f'output/{extract_domain(site)}.txt', 'w', encoding='UTF-8') as convert_file:
            convert_file.write(json.dumps(folded))
        return folded


try:
    file_path = os.environ['input_file']
except:
    file_path = input('enter file path: ')
print(f'input file {file_path}')
with open(file_path) as inputFile:
    if not os.path.exists('output'):
        os.mkdir('output')
    sites = list(map(lambda x: x.strip(), inputFile.readlines()))

    # we can't use pool of pool
    # we will get an error AssertionError: daemonic processes are not allowed to have children
    sites_summary = list(map(process_site, sites))
    all_sites = fold(combiner, sites_summary, map=Pool().imap)
    with open(f'output/all.txt', 'w', encoding='utf-8') as convert_file:
        convert_file.write(json.dumps(all_sites))

    # print(f'all summary:\n {all_sites}')
print("finished")
