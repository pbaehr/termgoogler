import argparse
import urllib2
from BeautifulSoup import BeautifulSoup as soup
import os

def read_terms(filename):
    f = open(filename, 'r')
    return [line.strip() for line in f]

def term_to_link(term):
    urlopener = urllib2.build_opener()
    urlopener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) '
                             'AppleWebKit/535.19 (KHTML, like Gecko) '
                             'Chrome/18.0.1025.168 Safari/535.19')]
    if term.find(' ') > 0:
        term = ('"%s"' % term).replace(' ', '+')
    google_results = urlopener.open('https://www.google.com/search?q=%s' % term)
    page = soup(google_results.read())
    try:
        first_result = page.find('div', id='ires').find('h3', 'r').find('a')['href']
    except AttributeError:
        return None
    return first_result

def generate_linked_terms(filename, out_file):
    out_file = open(out_file, 'w')
    out_file.write('<html><head><title>%s:'
                   'Linked Terms</title></head><body><ul>' % filename)
    for term in read_terms(filename):
        link = term_to_link(term)
        if link:
            out_file.write('<li><a href="%s">%s</a></li>' % (link, term))
        else:
            out_file.write('<li>%s</li>' % term)
    out_file.write('</ul></body></html>')
    out_file.close()

if __name__ == '__main__':
    current_path = os.path.dirname(os.path.realpath(__file__))
    arg_parser = argparse.ArgumentParser(description='Convert a list of terms'
                                         'to a list of links using Google\'s'
                                         'first result.')
    arg_parser.add_argument('filename', type=str,
                            help='Input file; a list of terms, one per line')
    arg_parser.add_argument('--output', default='%s\\out.html' % current_path,
                            help='Ouput filename')
    args = arg_parser.parse_args()
    generate_linked_terms(args.filename, args.output)
