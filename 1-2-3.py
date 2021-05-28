def read_number(line, index):
  number = 0
  while index < len(line) and line[index].isdigit():
    number = number * 10 + int(line[index])
    index += 1
  if index < len(line) and line[index] == '.':
    index += 1
    decimal = 0.1
    while index < len(line) and line[index].isdigit():
      number += int(line[index]) * decimal
      decimal /= 10
      index += 1
  token = {'type': 'NUMBER', 'number': number}
  return token, index


def read_plus(line, index):
  token = {'type': 'PLUS'}
  return token, index + 1


def read_minus(line, index):
  token = {'type': 'MINUS'}
  return token, index + 1


def read_multi(line, index):
  token = {'type': 'MULTI'}
  return token, index + 1

  
def read_divide(line, index):
  token = {'type': 'DIVIDE'}
  return token, index + 1

  
def read_exponent(line, index):
  token = {'type': 'EXPONENT'}
  return token, index + 2


def read_open_parentheses(line, index):
  token = {'type': 'OPEN_PARENTHESES'}
  return token, index + 1

  
def read_close_parentheses(line, index):
  token = {'type': 'CLOSE_PARENTHESES'}
  return token, index + 1


def tokenize(line):
  tokens = []
  index = 0
  while index < len(line):
    if line[index].isdigit():
      (token, index) = read_number(line, index)
    elif line[index] == '+':
      (token, index) = read_plus(line, index)
    elif line[index] == '-':
      (token, index) = read_minus(line, index)
    elif line[index:index+2] == '**':
      (token, index) = read_exponent(line, index)
    elif line[index] == '*':
      (token, index) = read_multi(line, index)
    elif line[index] == '/':
      (token, index) = read_divide(line, index)
    elif line[index] == '(':
      (token, index) = read_open_parentheses(line, index)
    elif line[index] == ')':
      (token, index) = read_close_parentheses(line, index)
    else:
      print('Invalid character found: ' + line[index])
      exit(1)
    tokens.append(token)
  return tokens


def evaluate_expression(tokens, index):
  (number, index) = evaluate_term(tokens, index)
  expression = number
  while index < len(tokens) and (tokens[index]['type'] == 'PLUS' or tokens[index]['type'] == 'MINUS'):
    if tokens[index]['type'] == 'PLUS':
      (number, index) = evaluate_term(tokens, index + 1)
      expression += number
    else:
      (number, index) = evaluate_term(tokens, index + 1)
      expression -= number
  return (expression, index)


def evaluate_term(tokens, index):
  (number, index) = evaluate_exponent(tokens, index)
  term = number
  while index < len(tokens) and (tokens[index]['type'] == 'MULTI' or tokens[index]['type'] == 'DIVIDE'):
    if tokens[index]['type'] == 'MULTI':
      (number, index) = evaluate_exponent(tokens, index + 1)
      term *= number
    else:
      (number, index) = evaluate_exponent(tokens, index + 1)
      if number == 0:
        print('ZeroDivisionError: division by zero')
        exit(1)
      term /= number
  return (term, index)


def evaluate_exponent(tokens, index):
  (number, index) = evaluate_factor(tokens, index)
  exponent = number
  while index < len(tokens) and (tokens[index]['type'] == 'EXPONENT'):
      (number, index) = evaluate_expression(tokens, index + 1)
      exponent **= number
  return (exponent, index)


def evaluate_factor(tokens, index):
  if tokens[index]['type'] == 'NUMBER':
    return (tokens[index]['number'], index + 1)
  if tokens[index]['type'] == 'OPEN_PARENTHESES':
    (number, index) = evaluate_expression(tokens, index + 1)
    if tokens[index]['type'] == 'CLOSE_PARENTHESES':
      return (number, index + 1)
    print('NotFoundError: )')
    exit(1)
  print('NotFoundError: factor')
  exit(1)


def evaluate(tokens):
  (number, index) = evaluate_expression(tokens, 0)
  return number


def test(line):
  tokens = tokenize(line)
  actual_answer = evaluate(tokens)
  expected_answer = eval(line)
  if abs(actual_answer - expected_answer) < 1e-8:
    print("PASS! (%s = %f)" % (line, expected_answer))
  else:
    print("FAIL! (%s should be %f but was %f)" % (line, expected_answer, actual_answer))


# Add more tests to this function :)
def run_test():
  print("==== Test started! ====")
  test("1+1")
  test("2-3")
  test("4*5")
  test("6/7")
  test("1.0+1.2")
  test("1.0-1.2")
  test("1.0*1.2")
  test("1.0/1.2")
  test("1.2*2.3-3.4*4.5-5.6/6.7+1.2/2.3")
  test("(1+2)*3")
  test("(4+5)/6")
  test("7**(1+2)")
  test("3/(4+5)")
  test("4**3**2")
  print("==== Test finished! ====\n")

run_test()

"""
while True:
  print('> ', end="")
  line = input()
  tokens = tokenize(line)
  answer = evaluate(tokens)
  print("answer = %f\n" % answer)
"""
