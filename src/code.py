import requests
import re
from bs4 import BeautifulSoup
from multiprocessing import Pool
import sys

visited = {''}


def extract_domain(url):
    if url is None:
        return ''
    domain_regex = re.compile(r"https?:\/\/w{0,3}\.?(\w+)\.+")
    result = domain_regex.search(url)
    return result.group(1) if result else ""


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


with open("input.txt") as inputFile:
    number_of_iterations = 1
    sites = list(map(lambda x: x.strip(), inputFile.readlines()))
    for site in sites:
        html_content = []
        nodes = [site]
        with Pool() as p:
            while len(nodes) > 0 and number_of_iterations <= 5:
                print("***************************")
                print(f'number of iterations: {number_of_iterations} number of nodes: {len(nodes)} number of text files {len(html_content)}')
                sys.stdout.flush()
                number_of_iterations += 1
                scrapped = list(p.map(scrap_site, nodes))
                nodes = []
                # print(scrapped)
                for s in scrapped:
                    if s[0]:
                        html_content.append(s[1])
                        nodes = s[2]
print("finished")
