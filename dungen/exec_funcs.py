from lexer import lex, lex_if, lex_while
from action_funcs import action
from error_check import check_expression
import sys

def evalone(token, stats, var_dict):
	"""Return token (containing value) of NUM type."""	
	value, type = token
	if type == 'NUM':
		return (int(value), 'NUM')
	elif type == 'STATS':
		return (stats[value], 'NUM')
	elif type == 'VAR':
		for i in range(len(var_dict) - 1, -1, -1):
			if value in var_dict[i]:
				return(var_dict[i][value], 'NUM')
		sys.exit('Variable {} not defined'.format(value))
	else:
		sys.exit('INVALID!')
				
def evaluate_not(token, stats, var_dict):
	"""Return NOT token of value of token."""
	if evalone(token, stats, var_dict)[0] == 0:
		return (1, 'NUM')
	else:
		return (0, 'NUM')

def evaluate_bin(token1, op, token2, stats, var_dict):
	"""Return token containing value of a binary expression."""
	arg1, op, arg2 = evalone(token1, stats, var_dict)[0], op[0], evalone(token2, stats, var_dict)[0]
	if (op == '+'): return (arg1 + arg2, 'NUM')
	if (op == '-'): return (arg1 - arg2, 'NUM')
	if (op == '*'): return (arg1 * arg2, 'NUM')
	if (op == '/'): return (arg1 // arg2, 'NUM')
	if (op == '>='): return (1, 'NUM') if arg1 >= arg2 else (0, 'NUM')
	if (op == '>'): return (1, 'NUM') if arg1 > arg2 else (0, 'NUM')
	if (op == '<='): return (1, 'NUM') if arg1 <= arg2 else (0, 'NUM')
	if (op == '<'): return (1, 'NUM') if arg1 < arg2 else (0, 'NUM')
	if (op == '=='): return (1, 'NUM') if arg1 == arg2 else (0, 'NUM')
	if (op == '!='): return (1, 'NUM') if arg1 != arg2 else (0, 'NUM')
	if (op == '&'): return (1, 'NUM') if arg1 * arg2 != 0 else (0, 'NUM')
	if (op == '|'): return (1, 'NUM') if arg1 or arg2 else (0, 'NUM')
	
def topost(token_list):
	"""Return list of tokens in postfix."""
	opstack = []
	output = []
	priority = {'|': -4, '&': -3, '!': -2, '==': -1, '!=': -1, '>': 0, '>=': 0, '<': 0, '<=':0, '+': 1, '-': 1, '*': 2, '/': 2, '~': 3, '(': 4}
	for i in token_list:
		if i[0] == ')':
			while opstack[-1][0] != '(':
				output.append(opstack.pop())
			opstack.pop()
		elif i[0] in ['|','&','~','!','+','-','*','/','(','==', '!=', '>=', '>', '<=', '<']:
			while opstack and priority[opstack[-1][0]] >= priority[i[0]] and opstack[-1][0] is not '(':
				output.append(opstack.pop())
			opstack.append(i)			
		else:
			output.append(i)
		
	while opstack:
		output.append(opstack.pop())
	
	return output
	
def evaluate(tokens, stats, var_dict):
	"""Return an int value (NOT a token) of expression."""
	check_expression(tokens)
	postfix = topost(tokens)
	opstack = []
	for i in postfix:
		if i[0] is '!':
			a = opstack.pop()
			opstack.append(evaluate_not(a, stats, var_dict))
		elif i[0] is '~':
			a = opstack.pop()
			opstack.append((-evalone(a, stats, var_dict)[0], 'NUM'))
		elif i[0] in ['|','&','+','-','*','/','==', '!=', '>=', '>', '<=', '<']:
			b = opstack.pop()
			a = opstack.pop()
			opstack.append(evaluate_bin(a, i, b, stats, var_dict))
		else:
			opstack.append(i)
	return evalone(opstack[0], stats, var_dict)[0]

def store(monster, exp, stats, var_dict, player, results):
	"""Perform the store operation.
	
	Raises exceptions when
	* Variable already defined in the last scope
	* Trying to store when variable not defined
	"""
	
	if exp[0][0] == 'var':
		lhs = exp[1][0]
		rhs = evaluate(exp[3:], stats, var_dict)
		if lhs in var_dict[-1]:
			sys.exit('Variable {} already defined'.format(lhs))
		var_dict[-1][lhs] = rhs
	elif exp[0][1] == 'STATS':
		lhs = exp[0][0]
		rhs = evaluate(exp[2:], stats, var_dict)
		stats[lhs] = rhs
		monster.update_stats(player, stats, results)
	else:
		lhs = exp[0][0]
		rhs = evaluate(exp[2:], stats, var_dict)
		for i in range(len(var_dict) - 1, -1, -1):
			if lhs in var_dict[i]:
				var_dict[i][lhs] = rhs
				break
		else:
			sys.exit('Variable {} not defined'.format(lhs))
	
def param_gen(raw_params, stats, var_dict):
	"""Return list of final parameters for an action."""
	if len(raw_params) == 0:
		return []
	raw_params = [(',', 'RESERVED')] + raw_params + [(',', 'RESERVED')]
	params = []
	comma_indices = [i for i, j in enumerate(raw_params) if j == (',', 'RESERVED')]
	for x in range(len(comma_indices)-1):
		start = comma_indices[x] + 1
		end = comma_indices[x+1]
		params.append(evaluate(raw_params[start:end], stats, var_dict))
	return params
	
def iffunc(monster, tokens, stats, var_dict, player, map, results):
	"""Execute the if-else block and return the index from where control must resume."""
	var_dict.append({})
	cond, comm1, comm2, end = lex_if(tokens)
	if evaluate(cond, stats, var_dict) != 0:
		execute(monster, comm1, stats, var_dict, player, map, results)
	elif comm2:
		execute(monster, comm2, stats, var_dict, player, map, results)
	var_dict.pop()
	return end
	
def whilefunc(monster, tokens, stats, var_dict, player, map, results):
	"""Execute the while loop and return the index from where control must resume."""
	cond, comm, end = lex_while(tokens)
	var_dict.append({})
	while evaluate(cond, stats, var_dict) != 0:		
		execute(monster, comm, stats, var_dict, player, map, results)		
	var_dict.pop()
	return end
	
def execute(monster, tokens, stats, var_dict, player, map, results):
	"""Execute tokens."""
	curr = 0
	tokenlist = []
	tokentype = []
	
	for i in range(len(tokens)):
		tokenlist.append(tokens[i][0])
		tokentype.append(tokens[i][1])
	while curr < len(tokens):
		try:
			end = tokenlist.index(';', curr)
		except:
			end = len(tokenlist)
		if tokentype[curr] == 'ACTION':
			if tokenlist[curr+1] == '(' and tokenlist[end-1] == ')':
				if player.hp > 0 and monster.hp > 0:
					params = param_gen(tokens[curr+2:end-1], stats, var_dict)
					action(monster, tokenlist[curr], params, player, map, results)
					stats = monster.getstats(player)
			else:
				sys.exit("Bad syntax for action: " + ' '.join(tokenlist[curr:end]))
		elif tokenlist[curr] == 'if':
			end = iffunc(monster, tokens[curr:], stats, var_dict, player, map, results) + curr
		elif tokenlist[curr] == 'while':
			end = whilefunc(monster, tokens[curr:], stats, var_dict, player, map, results) + curr
		elif '=' in tokenlist[curr:end]:
			store(monster, tokens[curr:end], stats, var_dict, player, results)
		else:
			sys.exit("Bad statement: " + ' '.join(tokenlist[curr:end+1]))
		curr = end + 1
	
def exec1(monster, string, stats, player, map, results):
	"""Start execution of string."""
	tokens = lex(string)
	assert type(stats) == dict
	var_dict = [{}]
	execute(monster, tokens, stats, var_dict, player, map, results)