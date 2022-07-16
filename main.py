from art import CALCULATOR, SCREEN_LENGTH
from readchar import readkey

DELETE = "\x1b\x5b\x33\x7e"
BACKSPACE = '\x7f'
EXIT = "\x1b\x1b"
ENTER = '\x0d', '='

def format_num(num): 
    if num[-2:] == '.0': return num[:-2]
    else: return num

operations = {
    "+": lambda num_1, num_2: format_num(str(float(num_1) + float(num_2))),
    "-": lambda num_1, num_2: format_num(str(float(num_1) - float(num_2))),
    "*": lambda num_1, num_2: format_num(str(float(num_1) * float(num_2))),
    "/": lambda num_1, num_2: format_num(str(float(num_1) / float(num_2)))
}

# Lambda functions
prt = lambda str: print(str, end = '', flush = True)

def move_cursor(x, y,):
    UP = "\x1b\x5b\x41"
    DOWN = "\x1b\x5b\x42"
    LEFT = "\x1b\x5b\x44"
    RIGHT = "\x1b\x5b\x43"
    
    if y > 0: prt(UP * y)
    elif y < 0: prt(DOWN * -y)
    
    if x > 0: prt(RIGHT * x)
    elif x < 0: prt(LEFT * -x)

def print_calculator():
    prt(CALCULATOR)
    move_cursor(-3, 11)

def print_num(num, del_amount = 0):
    if del_amount < 0: del_amount = 0
    move_cursor(-(len(num) + del_amount), 0)
    prt(' ' * del_amount + num)

def print_history(num = '', operator = ''):
    history = num + ' ' + operator
    move_cursor(-SCREEN_LENGTH, 1)
    prt(history + ' ' * (SCREEN_LENGTH - len(history)))
    move_cursor(0, -1)

def update_operator(operator, num_len):
    move_distance = SCREEN_LENGTH - num_len - 1
    move_cursor(-move_distance, 1)
    prt(operator)
    move_cursor(move_distance - 1, -1)

def exit_program(del_amount):
    print_history('', '')
    print_num("GOOD BYE", del_amount)
    move_cursor(2, -11)
    print()

def get_num(num = '0', del_amount = 0):
    print_num(num, del_amount)

    is_integer = True
    if num == '0.': is_integer = False # Decimal transition mid operation
    
    while True:
        input = readkey()
        # Input is a number - append it
        if input.isnumeric() and len(num) < SCREEN_LENGTH - 2:
            if num == '0': num = input
            else: num += input
            print_num(num)

        # Input is an operator - exit
        elif input in operations:
            # Removing trailing zeroes in num if it is a decimal number
            if not is_integer:
                prev_len = len(num)
                num = num.rstrip('0').rstrip('.')
                print_num(num, prev_len - len(num))
            return (num, input)

        # Input is a point - decimal numbers
        elif input == '.':
            if is_integer:
                num += input
                print_num(num)
                is_integer = False

        # Input is a backspace - delete a digit
        elif input == BACKSPACE:
            if len(num) == 1:
                num = '0'
                print_num(num)
            elif num != '0':
                if num[-1] == '.': 
                    is_integer = True
                num = num[:-1]
                print_num(num, 1)

        # Input is the deletion key - delete the entire number
        elif input == DELETE:
            # Clear the whole input if delete is pressed when num is 0
            if num == '0':
                print_history('', '')
                return('', '')
            
            is_integer = True
            prev_len = len(num)
            num = '0'
            print_num(num, prev_len - 1)
        
        # Input is exit - stop the program: operator = "EXIT"
        elif input == EXIT: return(num, "EXIT")

        # Input is the enter/equals key - 
        elif input in ENTER: return(num, "=")
        
def get_num_2(num_1, operator, print = True):
    if num_1 == '': return('', '', '')
    if print: print_history(num_1, operator)
    
    input = readkey()
    while not input.isnumeric():
        # Input is an operator - update operator if it changed
        if input != operator and input in operations:
            operator = input

            # Reset print_history after doing a run with "=" for operator_2
            if not print: print_history(num_1,'')
            update_operator(operator, len(num_1))

        # Double enter after changing signs
        # elif input in ENTER:            
        #     return(num_1, operator, '=')
        
        # Input is a decimal point - float activated mid operations
        elif input == '.':
            input = '0.'
            break
            
        # Input is a backspace - clear the input from the previous input
        elif input == BACKSPACE:
            input = '0'
            break

        # Input is delete - clear the input completely
        elif input == DELETE:
            print_num('0', len(num_1) - 1)
            print_history('', '')
            return('', '', '')

        # Input is exit - stop the program: operator = "EXIT"
        elif input == EXIT: return('',"EXIT",'')

        input = readkey()
    # Deleting print_history after a new number is entered after hitting enter
    if operator == '=': print_history('', '')

    # Getting the second number
    (num_2, next_operator) = get_num(input, len(num_1) - 1)
    return (num_2, operator, next_operator)
        
def calculator(num_1 = '', operator_1 = '', num_2 = '', print = True):
    # Getting num_1 if it is empty 
    if num_1 == '': (num_1, operator_1) = get_num()
    
    # The exit key was pressed while getting the numbers: return to main
    if operator_1 == "EXIT":
        exit_program(len(num_1) - 8)
        return

    # Getting num_2
    (num_2, operator_1, operator_2) = get_num_2(num_1, operator_1, print)
    if not print: print = True # Setting print back to true after changing it
        
    # The exit key was pressed while getting the operators: return to main
    if operator_1 == "EXIT":
        exit_program(len(num_1) - 8)
        return

    # Calculating the result if num_2 is not empty
    if num_2 != '':
        if operator_1 == '=': 
            result = num_2
        else:
            result = operations[operator_1](num_1, num_2)
            print_num(result, len(num_2) - len(result))

            # Printing the whole equation if operator_2 is the equal sign
            if operator_2 == '=':
                print_history(f"{num_1} {operator_1} {num_2}", '=')
                print = False
                
    # If num_2 is empty, then result must be empty
    else: result = ''

    # Recursion - the result is not num_1
    calculator(result, operator_2, print = print)
    
    
# MAIN ----------------------------------------------------------------------------------
print_calculator()
calculator()


# Finished:
#    * input number
#    * backspace
#    * exit 
#    * decimals
#    * deletion
#    * enter/ equals

# TO DO:
#    * negation
#    * number limits
#        # large numbers
#        # small numbers
#        # irrational/ repeating decinmals
#    * no space for entire eq: num_1 + num_2