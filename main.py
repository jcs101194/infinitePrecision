#!/user/bin/python

# homework will be tested with bad input. It needs to be sanitized
#
#
# Sources used:
#
#   https://docs.python.org/2/library/stdtypes.html#str.zfill
#
#
# Notes:
# -This program will ignore empty lines and not output error messages on them
#  even though there won't be empty lines to handle
#
#                                  Important Functions
#
# __init__ for Integer the parameters for this are a list with only one string like so ["123456"]
# The constructor will then take the list and segment it as needed
#
# print_solve_content_recursively(desired_content, i, list_length, digits_per_node) is another
# important function. This is the best view point to see how the program parses line by line
# and evaluates the equations
#
#
#                                   Important Notes
#
#
# 1. All the parsing functions work relatively well. No need to change them
# 2. The only thing that needs work are the __mult__ and __sub__ methods in the
# Integer class and the recursive functions called in them. __add__ works well.
# 3. Ignore all other "recursive" or "recursively" functions as they all work
# 4. The program passes all the test cases listed on the homework with 3
# digits per node. I haven't tried other values
# 5. You can change the code in however you see fit. I'll have my own copy.
# 6. Please don't hesitate to ask me if you have any questions.
#

import sys

# Note that only one of these three variables should be true
userTestingMode = "true"
scriptTestingMode = "false"
finalMode = "false"

null = 'null'
invalidInput = "Invalid Input"


class Node:

    # Class is called Node and not Digit. Node might hold multiple digits
    # power is an integer that will multiply number according to it's place
    digits_per_node = 0
    backwardsLink = None
    forwardsLink = None
    power = 0
    number = 0

    def __init__(self, desired_integer, desired_power, digits_per_node):

        self.digits_per_node = digits_per_node
        self.number = desired_integer
        self.power = desired_power

        # backwards and forwards link doesn't need to be initialized
        # unlike C/C++


class Integer:

    integer = ""
    number_of_nodes = 0
    digits_per_node = 0

    head = None
    tail = None

    def __init__(self, integer_list, digits_per_node):

        # This function will segment the list as needed.
        # integer_list must be formatted like so ["123456"]
        # after segment_list integer_list will be segmented like
        # so ["123", "456"] depending on digits_per_node

        # Another responsibility of the constructor is to remove
        # extraneous zeros before self.segment_list()

        self.integer = integer_list[0]

        if int(integer_list[0]) == 0:
            self.integer = "0"
            integer_list[0] = "0"

        if int(integer_list[0][0]) == 0:
            desired_integer = str(int(integer_list[0]))
            self.integer = desired_integer
            integer_list[0] = desired_integer

        self.digits_per_node = int(digits_per_node)
        # integer_list = self.remove_extraneous_zeros(integer_list)
        self.segment_list(integer_list, digits_per_node)
        self.append_integer_list_recursively(integer_list, digits_per_node, 0, len(integer_list))

    def __add__(self, second_operand):

        # Line up integers as needed
        if self.number_of_nodes > second_operand.number_of_nodes:
            nodes_needed = self.number_of_nodes - second_operand.number_of_nodes
            second_operand.add_leading_zeros_recursive(0, nodes_needed)

        if self.number_of_nodes < second_operand.number_of_nodes:
            nodes_needed = second_operand.number_of_nodes - self.number_of_nodes
            self.add_leading_zeros_recursive(0, nodes_needed)

        answer_list = [null]*self.number_of_nodes

        answer_integer = self.add_sub_recursive(self, second_operand, self.tail,
                                                second_operand.tail, answer_list, self.number_of_nodes, 0, "true")

        return answer_integer

    def __sub__(self, second_operand):
        answer_list = [null]*self.number_of_nodes
        answer_integer = self.add_sub_recursive(self, second_operand, self.tail,
                                                second_operand.tail, answer_list, self.number_of_nodes, 0, "true")

        return answer_integer

    def add_sub_recursive(self, first_operand, second_operand,
                          current_node_first, current_node_second, answer_list, i, carry, first_call):

        # Note: this if statement must be immutable
        # if i == 0 then every node must be accounted for
        if i == 0:
            return

        # Precondition: Integers must have the same number of nodes for the sake of simplicity
        highest_integer_allowed = pow(10, self.digits_per_node)
        current_answer = current_node_first.number + current_node_second.number

        if carry != 0:
            current_answer = current_answer + carry
            carry = 0

        if current_answer >= highest_integer_allowed:
            modulo = current_answer % highest_integer_allowed
            carry = int((current_answer - modulo)/highest_integer_allowed)
            current_answer = int(current_answer - highest_integer_allowed)

        # pow(10, self.digits_per_node-1 is the smallest value before the
        # the numbers are in danger of padding issues
        if current_answer < pow(10, self.digits_per_node-1):

            # The point of this if statement is to handle padding
            # of small numbers. Do not delete this if statement.

            current_answer = str(current_answer)
            if i != 1:
                # i.e this is not the left most node
                # we can't print ending zeros
                current_answer = current_answer.zfill(self.digits_per_node)
                answer_list[i - 1] = current_answer
            if i == 1:
                # Yet another hail mary. Sometimes when carry is extracted from current_answer
                # it extracts the carry but leaves current_answer below the padding-less zone.
                # A rare bug, indeed. For example, 8923+1405=328 instead of 10328

                # Note: the assumption is that carry != 0
                if int(current_answer) < pow(10, self.digits_per_node-1) and carry != 0:
                    current_answer = current_answer.zfill(self.digits_per_node)
                    answer_list[i - 1] = current_answer
                    answer_list.insert(0, str(carry))

                if int(current_answer) < pow(10, self.digits_per_node-1) and carry == 0:

                    # If this is the last node and the answer is below the padding zone then
                    # don't pad the zeros as it will add extraneous zeros at front.
                    # Another hail mary.
                    answer_list[i - 1] = current_answer

        else:
            answer_list[i-1] = str(current_answer)

            # This next line is also a hail mary. lol
            # Essentially, if there is a remainder at the front of the list
            # and there is no space, then append the needed space at front
            # Edit: This line actually marginally improves accuracy
            if i == 1 and carry != 0:

                # Be advised that list.insert is actually mutates the list
                # as opposed to simply my_list = [foo] + my_list
                # Edit: using list.insert improves accuracy. I'll refrain
                # from using the alternative
                answer_list.insert(0, str(carry))

        self.add_sub_recursive(first_operand, second_operand,
                               current_node_first.backwardsLink, current_node_second.backwardsLink,
                               answer_list, i-1, carry, "false")

        if first_call == "true":

            # the next line is a hail mary. I believe that at this time
            # carry must be accounted for, this the reason for the next line
            carry = 0

            # answer_list is segmented like this [1,2,3]
            # it should be like [123] to pass it to Integer()
            # hence the self.concatenate_list()
            if carry != 0:
                # if carry is not spent add it to the front of the node
                # if it's bigger than highest_integer_allowed then append it
                # to the front of the list (array), else simply added
                carry = int(carry)
                current_answer = int(answer_list[0]) + carry
                if current_answer < highest_integer_allowed:
                    answer_list[0] = str(int(answer_list[0])+carry)
                else:
                    current_answer = int(answer_list[0]) + carry
                    modulo = current_answer % int(highest_integer_allowed)
                    carry = int((current_answer-modulo)/highest_integer_allowed)
                    answer_list[0] = str(int(current_answer-highest_integer_allowed))

                    answer_list.insert(0, str(carry))

            self.concatenate_list(answer_list, 0, len(answer_list))
            return Integer(answer_list, first_operand.digits_per_node)

    def __mul__(self, second_operand):
        answer_list = [0]
        self.multiply_recursive(self.head, second_operand.head, answer_list)
        return Integer(answer_list, self.number_of_nodes)

    def multiply_recursive(self, first_operand_node, second_operand_node, answer_list):

        # first_operand * second_operand
        # Note: (123,000 + 456)(678,000 + 345)
        # Note: that if second_operand_node is None the function is not done,
        # it just resets second_operand_node to be the head. The function ends
        # when first_operand_node is None

        if first_operand_node is None:
            answer_list[0] = str(answer_list[0])
            return

        if second_operand_node is None:
            return

        first_operand = first_operand_node.number*first_operand_node.power
        second_operand = second_operand_node.number*second_operand_node.power
        answer_list[0] += int(first_operand*second_operand)

        self.multiply_recursive(first_operand_node, second_operand_node.forwardsLink, answer_list)

        if first_operand_node is not None and second_operand_node.backwardsLink is None:
            self.multiply_recursive(first_operand_node.forwardsLink, second_operand_node, answer_list)

    def concatenate_list(self, desired_list, i, n):

        if i == n-1:
            del desired_list[1:]
            return
        else:
            desired_list[0] = str(desired_list[0]) + str(desired_list[i+1])
            desired_list[i+1] = null

        self.concatenate_list(desired_list, i+1, n)

    def remove_extraneous_zeros(self, integer_list):

        return self.remove_extraneous_zeros_recursive(list(integer_list[0]), 0, len(integer_list[0]))

    def remove_extraneous_zeros_recursive(self, integer_list, i, n):

        # Precondition: integer_list must be like so ['1', '2', '3']
        if int(integer_list[i]) == 0 and len(integer_list) == 1:

            # This if structure handles the zero cases such as 000 or 0000000
            # Essentially, it stops the function from completely deleting a
            # 00000 like string
            return integer_list

        if int(integer_list[i]) != 0 or i >= n:
            return integer_list

        if int(integer_list[i]) == 0:

            # The implication is that if this if structure is called
            # then a non-zero digit hasn't been scanned yet
            integer_list.pop(i)
            i = i-1

        return self.remove_extraneous_zeros_recursive(integer_list, i+1, n)

    def segment_list(self, integer_list, digits_per_node):

        # Note that at this point integer_list is one string element
        # Post condition: integer_list is segmented before making a linked list out of them
        integer_string = str(integer_list[0])
        integer_string = integer_string[::-1]

        if digits_per_node == 1:
            self.segment_list_recursive(list(integer_string), digits_per_node, 0, 0, len(integer_string), integer_list)
            integer_list.reverse()
            return integer_list
        else:

            # find n
            # note that n has to be +1 to count for remainder, where n == number of segment
            # if remainder is 0 then note that the +1 is extraneous
            string_length = len(integer_string)
            remainder = string_length % int(digits_per_node)
            n = 0

            if remainder != 0:
                n = int((string_length-remainder)/int(digits_per_node))+1
            if remainder == 0:
                n = int((string_length-remainder)/int(digits_per_node))

            self.segment_list_recursive(list(integer_string), digits_per_node, 0, 0, n, integer_list)
            integer_list.reverse()

    def segment_list_recursive(self, integer_array, digits_per_node, i, j, n, integer_list):

        # integer_array is the list segmented into one char per element
        # Note that i must equal n eventually. It must

        if i is n:
            return

        current_tuple = self.fetch_next_characters(integer_array, digits_per_node, j, j+int(digits_per_node), "")
        current_tuple = current_tuple[::-1]

        if i is 0:
            integer_list[i] = current_tuple
        else:
            integer_list.append(current_tuple)

        self.segment_list_recursive(integer_array, digits_per_node, i+1, j+int(digits_per_node), n, integer_list)

    def fetch_next_characters(self, integer_array, digits_per_node, i, n, answer_string):

        # Let's make this function return a string of numbers
        # note that the i can't pass over the array
        if i >= len(integer_array):
            return answer_string
        if i >= n:
            return answer_string

        answer_string += str(integer_array[i])
        return self.fetch_next_characters(integer_array, digits_per_node, i+1, n, answer_string)

    def append_integer_list_recursively(self, desired_integer_list, digits_per_node, i, n):

        # This function takes an integer list and appends them recursively using a helper function
        # digits_per_node is used to determine the decimal place of the node
        # so it is necessary

        if i >= n:
            return
        else:

            # Note that i must never == len(desired_integer_list)
            power = pow(10, ((len(desired_integer_list) - (i+1))*digits_per_node))
            self.append_node(int(desired_integer_list[i]), power, digits_per_node)

        self.append_integer_list_recursively(desired_integer_list, int(digits_per_node), i+1, n)

    def append_node(self, desired_number, desired_power, digits_per_node):

        # At this point desired_number and desired_power must be of type int or float and not string

        if self.head is None:

            self.head = Node(desired_number, desired_power, digits_per_node)
            self.tail = self.head
        else:

            new_node = Node(desired_number, desired_power, digits_per_node)
            self.tail.forwardsLink = new_node
            new_node.backwardsLink = self.tail

            self.tail = self.tail.forwardsLink

        self.number_of_nodes = self.number_of_nodes + 1

    def add_leading_zeros(self):

        # This will append to the front
        new_node = Node(0, 0, self.digits_per_node)
        new_node.forwardsLink = self.head
        new_node.backwardsLink = None
        self.head.backwardsLink = new_node
        self.number_of_nodes = self.number_of_nodes + 1

        self.head = self.head.backwardsLink

    def add_leading_zeros_recursive(self, i, zeros_needed):

        if i >= zeros_needed:
            return

        self.add_leading_zeros()
        self.add_leading_zeros_recursive(i+1, zeros_needed)


def parsefile(argument_list):

    my_file = open(argument_list[0])
    my_content = my_file.readlines()
    print_solve_content_recursively(my_content, 0, len(my_content), argument_list[1])


def is_valid(desired_line):

    # Return true if valid, false if else
    # This will also check for incorrect characters
    desired_list = list(desired_line)
    return is_valid_recursive(desired_list, 0, len(desired_list), False, False, False)


def is_valid_recursive(desired_array, i, n, first_operand_found, operator_found, second_operand_found):

    if i >= n:
        # If not all flags are called, then the line is obviously invalid
        return False

    if first_operand_found and operator_found and second_operand_found:
        return True

    if desired_array[i].isalpha():
        return False

    if desired_array[i].isnumeric() and operator_found is False:
        first_operand_found = True

    if desired_array[i] == "+" or desired_array[i] == "*":
        operator_found = True

    if desired_array[i].isnumeric() and operator_found is True:
        second_operand_found = True

    return is_valid_recursive(desired_array, i+1, n, first_operand_found, operator_found, second_operand_found)


def print_solve_content_recursively(desired_content, i, list_length, digits_per_node):

    if i < list_length:
        # Quangtri: Removed the - 1 so that it will process the last line
        # Quangtri: if evaluate_line returns null, then the line does not have an operator, skip this line
        current_line = desired_content[i]

        if is_valid(current_line):
            current_answer = evaluate_line(current_line, digits_per_node)

            # Remove unneeded whitespaces.
            current_line = current_line.replace("\n", "")
            current_line = current_line.replace(" ", "")
            current_line = current_line.replace("\t", "")

            current_answer = current_line + "=" + str(current_answer.integer)
            print(current_answer)
        else:
            if current_line != "\n":
                print(invalidInput)

        print_solve_content_recursively(desired_content, i+1, list_length, digits_per_node)


def evaluate_line(desired_line, digits_per_node):

    # Note that left_operand and right_operand are both Integer types
    # Quangtri: if operator is not found return null, so the line won't get process further
    operator = return_operator(desired_line)
    answer = -1
    if operator == null:
        return null

    left_operand = return_left_operand(operator, desired_line, digits_per_node)
    right_operand = return_right_operand(operator, desired_line, digits_per_node)

    if operator == "+":
        answer = left_operand + right_operand
    if operator == "-":
        answer = left_operand - right_operand
    if operator == "*":
        answer = left_operand * right_operand

    return answer


def return_left_operand(desired_operator, desired_list, digits_per_node):

    # This function will return an Integer class
    token_list = [null]*100

    return left_operand_recursive(desired_operator, token_list, desired_list, 0, len(desired_list), digits_per_node)


def left_operand_recursive(desired_operator, token_list, desired_list, i, n, digits_per_node):

    # This is the recursive loop for  return_left_operand

    if desired_operator == desired_list[i]:
        utility_string = ''.join(token_list)
        utility_string = utility_string.rstrip(null)
        token_list = utility_string.split()
        answer = Integer(token_list, digits_per_node)

        return answer
    else:
        token_list[i] = desired_list[i]
        return left_operand_recursive(desired_operator, token_list, desired_list, i+1, n, digits_per_node)


def return_operator(desired_list):

    return return_operator_recursive(desired_list, 0, len(desired_list))


def return_operator_recursive(desired_list, i, list_length):

    if i == list_length:
        return null
    if desired_list[i] == '+':
        return '+'
    if desired_list[i] == '-':
        return '-'
    if desired_list[i] == '*':
        return '*'
    if desired_list[i] == '/':
        return '/'

    return return_operator_recursive(desired_list, i+1, list_length)


def return_right_operand(desired_operator, desired_list, digits_per_node):

    # This function will return an Integer class
    token_list = [null]*100

    return right_operand_recursive(desired_operator, token_list, desired_list, 0,
                                   0, len(desired_list), digits_per_node, "false")


def right_operand_recursive(desired_operator, token_list, desired_list, i, j, n, digits_per_node, operator_read):

    # This is the recursive loop for  return_right_operand
    # The right operand terminates with either '\n' or end string
    # This function needs a second iterator, j, because of delineation of the token_list and desired_list

    # Quangtri: I switched the 2 condition statements because i == n need
    #  to be evaluated first to avoid index out of range
    if i == n or desired_list[i] == '\n':
        utility_string = ''.join(token_list)
        utility_string = utility_string.rstrip(null)
        token_list = utility_string.split()
        answer = Integer(token_list, digits_per_node)

        return answer

    if operator_read == "true":
        token_list[j] = desired_list[i]
        j = j + 1

    if desired_operator == desired_list[i]:
        operator_read = "true"

    return right_operand_recursive(desired_operator, token_list, desired_list, i+1,
                                   j, n, digits_per_node, operator_read)


def get_command_line_arguments(argument_list):
    argument_line = sys.argv
    argument_line = argument_line[1]
    string_list = list(argument_line)
    token_list = [null]*40
    recording_flag = "false"

    recursive_string_loop(string_list, 0, 0, len(string_list), token_list, recording_flag, argument_list)

    return 0


def recursive_string_loop(desired_list, i, j, list_length, token_list, recording_flag, argument_list):

    if i < list_length:
        if desired_list[i] == ";":

            argument_list[0] = ''.join(token_list).rstrip(null)

            j = 0
            clear_list(token_list, 0, len(token_list))
            recording_flag = "false"

        if recording_flag == "true":

            token_list[j] = desired_list[i]
            j = j+1

        if desired_list[i] == "=":
            recording_flag = "true"

        recursive_string_loop(desired_list, i+1, j, list_length, token_list, recording_flag, argument_list)

    else:
        argument_list[1] = float(''.join(token_list).rstrip(null))
        return


def clear_list(desired_list, i, list_length):

    if i == list_length:
        return
    else:
        desired_list[i] = null

    clear_list(desired_list, i+1, list_length)


def main():
    # command line argument_list = {'file_name', 'digits_per_node'}
    argument_list = [null, null]
    get_command_line_arguments(argument_list)
    parsefile(argument_list)


# for some reason inserting a main function silenced the weak warnings. lol
main()
