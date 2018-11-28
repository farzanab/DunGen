from lex_spells import lex, lex_if, lex_while
from spell_funcs import action, exec_func
from error_check import check_expression
import sys

def simplify(player, tokens, stats, var_dict, map, fov_map, entities, dirn):
	"""Call the appropriate functions to simplify the expression."""
	i = 0
	while i < len(tokens):
		if tokens[i][1] == 'FUNC':
			if tokens[i+1][0] != '(':
				sys.exit("Missing bracket for function call.")
			j = i + 2
			o, c = 1, 0
			while j < len(tokens):
				if tokens[j][0] == '(':
					o += 1
				if tokens[j][0] == ')':
					c += 1
					if o == c:
						break
				j += 1
			params = param_gen(player, tokens[i+2:j], stats, var_dict, map, fov_map, entities, dirn)
			tokens[i] = (exec_func(tokens[i][0], params, map, fov_map, entities, dirn), 'NUM')
			for x in range(j-i):
				del(tokens[i+1])
		i += 1
		
def evalone(player, token, stats, var_dict):
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
				
def evaluate_not(player, token, stats, var_dict):
	"""Return NOT token of value of token."""
	if evalone(player, token, stats, var_dict)[0] == 0:
		return (1, 'NUM')
	else:
		return (0, 'NUM')

def evaluate_bin(player, token1, op, token2, stats, var_dict):
	"""Return token containing value of a binary expression."""
	arg1, op, arg2 = evalone(player, token1, stats, var_dict)[0], op[0], evalone(player, token2, stats, var_dict)[0]
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
	
def evaluate(player, tokens, stats, var_dict, map, fov_map, entities, dirn):
	"""Return an int value (NOT a token) of expression."""
	simplify(player, tokens, stats, var_dict, map, fov_map, entities, dirn)
	check_expression(tokens)
	postfix = topost(tokens)
	opstack = []
	for i in postfix:
		if i[0] is '!':
			a = opstack.pop()
			opstack.append(evaluate_not(player, a, stats, var_dict))
		elif i[0] is '~':
			a = opstack.pop()
			opstack.append((-evalone(player, a, stats, var_dict)[0], 'NUM'))
		elif i[0] in ['|','&','+','-','*','/','==', '!=', '>=', '>', '<=', '<']:
			b = opstack.pop()
			a = opstack.pop()
			opstack.append(evaluate_bin(player, a, i, b, stats, var_dict))
		else:
			opstack.append(i)
	return evalone(player, opstack[0], stats, var_dict)[0]

def store(player, exp, stats, var_dict, map, fov_map, entities, results, dirn):
	"""Perform the store operation.
	
	Raises exceptions when
	* Variable already defined in the last scope
	* Trying to store when variable not defined
	"""
	if exp[0][0] == 'var':
		lhs = exp[1][0]
		rhs = evaluate(player, exp[3:], stats, var_dict, map, fov_map, entities, dirn)
		if lhs in var_dict[-1]:
			sys.exit('Variable {} already defined'.format(lhs))
		var_dict[-1][lhs] = rhs
	elif exp[0][1] in ['STATS', 'LOC']:
		lhs = exp[0][0]
		rhs = evaluate(player, exp[2:], stats, var_dict, map, fov_map, entities, dirn)
		stats[lhs] = rhs
		player.update_stats(stats, results)
	else:
		lhs = exp[0][0]
		rhs = evaluate(player, exp[2:], stats, var_dict, map, fov_map, entities, dirn)
		for i in range(len(var_dict) - 1, -1, -1):
			if lhs in var_dict[i]:
				var_dict[i][lhs] = rhs
				break
		else:
			sys.exit('Variable {} not defined'.format(lhs))
	
def param_gen(player, raw_params, stats, var_dict, map, fov_map, entities, dirn):
	"""Return list of final parameters for an action."""
	if len(raw_params) == 0:
		return []
	raw_params = [(',', 'RESERVED')] + raw_params + [(',', 'RESERVED')]
	params = []
	comma_indices = [i for i, j in enumerate(raw_params) if j == (',', 'RESERVED')]
	for x in range(len(comma_indices)-1):
		start = comma_indices[x] + 1
		end = comma_indices[x+1]
		params.append(evaluate(player, raw_params[start:end], stats, var_dict, map, fov_map, entities, dirn))
	return params
	
def iffunc(player, tokens, name, stats, var_dict, map, fov_map, entities, results, dirn):
	"""Execute the if-else block and return the index from where control must resume."""
	var_dict.append({})
	cond, comm1, comm2, end = lex_if(tokens)
	if evaluate(player, cond, stats, var_dict, map, fov_map, entities, dirn) != 0:
		execute(player, comm1, name, stats, var_dict, map, fov_map, entities, results, dirn)
	elif comm2:
		execute(player, comm2, name, stats, var_dict, map, fov_map, entities, results, dirn)
	var_dict.pop()
	return end
	
def whilefunc(player, tokens, name, stats, var_dict, map, fov_map, entities, results, dirn):
	"""Execute the while loop and return the index from where control must resume."""
	cond, comm, end = lex_while(tokens)
	var_dict.append({})
	while evaluate(player, cond, stats, var_dict, map, fov_map, entities, dirn) != 0:		
		execute(player, comm, name, stats, var_dict, map, fov_map, entities, results, dirn)		
	var_dict.pop()
	return end
	
def execute(player, tokens, name, stats, var_dict, map, fov_map, entities, results, dirn):
	"""Execute tokens."""
	curr = 0
	tokenlist = []
	tokentype = []
	
	for i in range(len(tokens)):
		tokenlist.append(tokens[i][0])
		tokentype.append(tokens[i][1])
	if tokenlist[len(tokens) - 1] not in ['}', ';']:
		try:
			br = len(tokenlist) - tokenlist[::-1].index('}') - 1
		except:
			br = -1
		try:
			sem = len(tokenlist) - tokenlist[::-1].index(';') - 1
		except:
			sem = -1
		start = br if br > sem else sem
		sys.exit("Missing terminator: " + ' '.join(tokenlist[start+1:]))
	while curr < len(tokens):
		try:
			end = tokenlist.index(';', curr)
		except:
			end = len(tokenlist)
		if tokentype[curr] == 'ACTION':
			if tokenlist[curr+1] == '(' and tokenlist[end-1] == ')':
				if player.hp > 0:
					params = param_gen(player, tokens[curr+2:end-1], stats, var_dict, map, fov_map, entities, dirn)
					action(player, tokenlist[curr], params, name, map, entities, results, dirn)
					stats = {'x': stats['x'], 'y': stats['y']}
					stats.update(player.getstats())
			else:
				sys.exit("Bad syntax for action: " + ' '.join(tokenlist[curr:end]))
		elif tokenlist[curr] == 'if':
			end = iffunc(player, tokens[curr:], name, stats, var_dict, map, fov_map, entities, results, dirn) + curr
		elif tokenlist[curr] == 'while':
			end = whilefunc(player, tokens[curr:], name, stats, var_dict, map, fov_map, entities, results, dirn) + curr
		elif '=' in tokenlist[curr:end]:
			store(player, tokens[curr:end], stats, var_dict, map, fov_map, entities, results, dirn)
		else:
			sys.exit("Bad statement: " + ' '.join(tokenlist[curr:end+1]))
		curr = end + 1
	
def exec1(player, string, name, map, fov_map, entities, results, dirn):
	"""Start execution of string."""
	tokens = lex(string)
	stats = {'x': player.x, 'y': player.y}
	stats.update(player.getstats())
	var_dict = [{}]
	execute(player, tokens, name, stats, var_dict, map, fov_map, entities, results, dirn)