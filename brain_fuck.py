import sys
import argparse


# local exceptions
class LoopSyntaxException(Exception):
    pass


class NegativePointerException(Exception):
    pass


class NegativeValueException(Exception):
    pass


class OverflowException(Exception):
    pass


class TypeException(Exception):
    pass


def brainfuck(text_script, memory_size=30000):
    # set the BrainFuck operators list
    bfoperators = ['<', '>', '+', '-', ',', '.', '[', ']']

    # extract only the BrainFuck operators {> < + - , . [ ]} from text_script
    bfscript = [s for s in text_script if s in bfoperators]

    # save BrainFuck script length
    n = len(bfscript)
    if n == 0:
        exit()

    # verify for syntactical loop errors (check that all loops begins
    # with a '[' and ends with a ']'). also create a loop map dictionary
    loopcounter = 0
    loop_map = {}
    loop_stack = []
    code_ptr = 0

    while loopcounter >= 0 and n - code_ptr:
        if bfscript[code_ptr] == '[':
            loopcounter += 1
            loop_stack.append(code_ptr)
        elif bfscript[code_ptr] == ']':
            loopcounter -= 1
            loop_start = loop_stack.pop()
            loop_map[code_ptr] = loop_start - 1
            loop_map[loop_start] = code_ptr
        code_ptr += 1

    # raise loop syntax errors
    if loopcounter != 0 and n == code_ptr:
        raise LoopSyntaxException('The amount of "]" and "[" do not match.')
    if loopcounter == 1 and code_ptr != n:
        raise LoopSyntaxException('There is a "[" missing at the beginning.')

    # set up memory
    bfmemory = [0] * memory_size

    # initialize pointers
    code_ptr = 0
    mem_ptr = 0

    # run the BrainFuck script with a BrainFuck interpreter
    while n - code_ptr:
        # move memory pointer forward
        if bfscript[code_ptr] == '>':
            mem_ptr += 1
        # move memory pointer backward
        elif bfscript[code_ptr] == '<':
            mem_ptr -= 1
            if mem_ptr < 0:
                raise NegativePointerException('Memory pointer must be positive integer.')
        # add +1
        elif bfscript[code_ptr] == '+':
            bfmemory[mem_ptr] += 1
            if bfmemory[mem_ptr] > 1114111:
                raise OverflowException('Can handle only unicode integers (< 1,114,111).')
        # add -1
        elif bfscript[code_ptr] == '-':
            bfmemory[mem_ptr] -= 1
            if bfmemory[mem_ptr] < 0:
                raise NegativeValueException('Can handle only positive integers.')
        # read value
        elif bfscript[code_ptr] == ',':
            num = sys.stdin.read(1)
            if type(num) != int:
                raise TypeException('Input should be an int')
            else:
                bfmemory[mem_ptr] = num
        # write value
        elif bfscript[code_ptr] == '.':
            sys.stdout.write(chr(bfmemory[mem_ptr]))
        # start loop
        elif bfscript[code_ptr] == '[':
            if bfmemory[mem_ptr] == 0:
                code_ptr = loop_map[code_ptr]
        # end loop
        elif bfscript[code_ptr] == ']':
            code_ptr = loop_map[code_ptr]

        code_ptr += 1
    sys.stdout.write('\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='A Python BrainFuck interpreter implementation.')
    # Arguments
    parser.add_argument('-file', type=str,
                        help='The path to the file you want to interpret with BrainFuck interpreter.')
    parser.add_argument('-memory_size', type=int, default=30000,
                        help='The size of memory being used (list length).')

    args = parser.parse_args()
    with open(args.file, 'r') as file:
        text = file.read()
        try:
            print('Reading with BrainFuck...')
            brainfuck(text, memory_size=args.memory_size)
        except IOError as e:
            print('Error in reading file: {}'.format(args.file))
            exit()






