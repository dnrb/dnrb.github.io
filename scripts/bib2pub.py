import bibtexparser
import sys
import re

def sub_authorchains(a):
	a = re.sub('\n', ' ', a)
	asplit = re.split(r'\s+and\s+',a)
	if len(asplit) > 1:
		return ', '.join(asplit[:-1]) + ' and ' + asplit[-1]
	else:
		return a

fn = sys.argv[1]
bibs = bibtexparser.loads(open(fn).read())
for e in bibs.entries:
	strbuf = ''
	#print(e)
	strbuf += '---\n'
	if 'author' in e: strbuf += 'author: %s\n' % sub_authorchains(e['author'])
	if 'year' in e: strbuf += 'year: %s\n' % e['year']
	if 'title' in e: strbuf += 'title: %s\n' % e['title']
	if e['ENTRYTYPE'] == 'incollection':
		strbuf += 'category: proceedings\n'
		if 'editor' in e: strbuf += 'editor: %s\n' % sub_authorchains(e['editor'])
		if 'booktitle' in e: strbuf += 'booktitle: %s\n' % e['booktitle']
	elif e['ENTRYTYPE'] == 'article':
		strbuf += 'category: journal\n'
		if 'journal' in e: strbuf += 'journal: %s\n' % e['journal']
	else: print(e)
	if 'pages' in e: strbuf += 'pages: %s\n' % e['pages']		
	if 'url' in e: strbuf += 'permalink: %s\n' % e['url']
	if 'abstract' in e: strbuf += 'abstract: %s\n' % e['abstract']
	strbuf += '---'
	with open('../_publications/%s-%s.md' % (e['year'], e['title']), 'w') as fout:
		fout.write(strbuf)
	#print(strbuf)