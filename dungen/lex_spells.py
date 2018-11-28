"""Functions to process strings/tokens for spells."""
# Reference: Jay Conrod's A simple interpreter from scratch in Python (part 1)
# https://www.jayconrod.com/posts/37/a-simple-interpreter-from-scratch-in-python-part-1

import sys
import re

token_types = [
	(r'[ \n\t]+',    None),
	(r'\(',          'RESERVED'),
	(r'\)',          'RESERVED'),
	(r';',           'RESERVED'),
	(r'\+',          'RESERVED'),
	(r'-',           'RESERVED'),
	(r'~',           'RESERVED'),
	(r'\*',          'RESERVED'),
	(r'/',           'RESERVED'),
	(r'<=',          'RESERVED'),
	(r'<',           'RESERVED'),
	(r'>=',          'RESERVED'),
	(r'>',           'RESERVED'),
	(r'!=',          'RESERVED'),
	(r'==',          'RESERVED'),
	(r'=',           'RESERVED'),
	(r'&',           'RESERVED'),
	(r'\|',          'RESERVED'),
	(r'!',           'RESERVED'),
	(r'if(?!\w)',    'RESERVED'),
	(r'\{',          'RESERVED'),
	(r'\}',          'RESERVED'),
	(r'while(?!\w)', 'RESERVED'),
	(r'var(?!\w)',   'RESERVED'),
	(r',',           'RESERVED'),
	
	(r'health(?!\w)',         'STATS'),
	(r'maxhealth(?!\w)',      'STATS'),
	(r'mana(?!\w)',           'STATS'),
	(r'x(?!\w)',              'STATS'),
	(r'y(?!\w)',              'STATS'),
	
	(r'is_monster(?!\w)',      'FUNC'),
	(r'is_wall(?!\w)',         'FUNC'),
	(r'in_fov(?!\w)',          'FUNC'),
	
	(r'hit(?!\w)',           'ACTION'),
	
	(r'[0-9]+',                 'NUM'),
	(r'[A-Za-z_][A-Za-z0-9_]*', 'VAR')
]

def lex(string):
	"""Return tokens from string using regular expressions.
	
	If invalid characters used, stop.
	"""
	
	i = 0
	tokens = []
	while i < len(string):
		for token_type in token_types:
			tok = re.compile(token_type[0])
			obj = tok.match(string[i:])
			if obj:
				if token_type[1]:
					tokens.append((obj.group(0), token_type[1]))
				i = i + obj.end()
				break
		else:
			sys.exit("Illegal characters used\n" + string[i:])
	return tokens
	
def lex_if(tokens):
	"""Return condition, true_stmnt, false_stmnt, end_index
	
	tokens: list of tokens starting with 'if'
	
	condition: list of tokens for the conditional expression
	true_stmnt: list of tokens to be executed if condition
	false_stmnt: list of tokens to be executed if not condition
	end_index: index of last }
	"""
	
	b = 0
	c = 0
	tokenlist = []
	for i in range(len(tokens)):
		tokenlist.append(tokens[i][0])
	start = [0,0,-1]
	end = [0,0,0]
	for i in range(len(tokens)):
		if tokenlist[i] is '{':
			b += 1
			if b is 1:
				start[c] = i+1
		elif tokenlist[i] is '}':
			b -= 1
			if b is 0:
				end[c] = i
				if end[c] == start[c]:
					sys.exit("Empty clause/condition")
				c += 1
		else:
			if c == 3 or c == 2 and b == 0:
				break
			if c == 1 and b==0:
				sys.exit("Missing clause after\n" + ' '.join(tokenlist[:end[0]+1]))
			
	cond = tokens[start[0]:end[0]]
	comm1 = tokens[start[1]:end[1]]
	if start[2] is -1:
		comm2 = None
		en = end[1]
	else:
		comm2 = tokens[start[2]:end[2]]
		en = end[2]
	return cond, comm1, comm2, en	
	
def lex_while(tokens):
	"""Return condition, stmnts, end_index
	
	tokens: list of tokens starting with 'while'
	
	condition: list of tokens for the conditional expression
	stmnts: list of tokens in the while body
	end_index: index of last }
	"""
	
	b = 0
	c = 0
	tokenlist = []
	for i in range(len(tokens)):
		tokenlist.append(tokens[i][0])
	start = [0,0]
	end = [0,0]
	for i in range(len(tokens)):
		if tokenlist[i] is '{':
			b += 1
			if b is 1:
				start[c] = i+1
		elif tokenlist[i] is '}':
			b -= 1
			if b == 0:
				end[c] = i
				if end[c] == start[c]:
					sys.exit("Empty clause/condition\n"+' '.join(tokenlist[:i+1]))
				c += 1
		elif c == 1 and b == 0:
			sys.exit("Missing clause after\n" + ' '.join(tokenlist[:end[0]+1]))
		if c is 2:
			break
	cond = tokens[start[0]:end[0]]
	comm = tokens[start[1]:end[1]]
	return cond, comm, end[1]