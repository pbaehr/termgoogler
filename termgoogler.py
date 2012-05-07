import urllib2
from BeautifulSoup import BeautifulSoup as soup

def read_terms(filename):
    f = open(filename, 'r')
    return [line.strip() for line in f]

def term_to_link(term):
    urlopener = urllib2.build_opener()
    urlopener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) '
                             'AppleWebKit/535.19 (KHTML, like Gecko) '
                             'Chrome/18.0.1025.168 Safari/535.19')]
    google_results = urlopener.open('https://www.google.com/search?q=%s' % term)
    page = soup(google_results.read())
    first_result = page.find('div', id='ires').find('h3', 'r').find('a')['href']
    return first_result

def generate_linked_terms(filename, out_file):
    out_file = open(out_file, 'w')
    out_file.write('<html><head><title>%s: Linked Terms</title></head><body><ul>' % filename)
    for term in read_terms(filename):
        out_file.write('<li><a href="%s">%s</a></li>' % (term_to_link(term), term))
    out_file.write('</ul></body></html>')
    out_file.close()
