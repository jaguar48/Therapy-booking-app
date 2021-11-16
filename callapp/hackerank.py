#!/bin/python3

import math
import os
import random
import re
import sys

#
# Complete the 'minimumNumber' function below.
#
# The function is expected to return an INTEGER.
# The function accepts following parameters:
#  1. INTEGER n
#  2. STRING password
#
numbers = "0123456789"
lower_case = "abcdefghijklmnopqrstuvwxyz"
upper_case = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
special_characters = "!@#$%^&*()-+"

def minimumNumber(n, password):
    # Return the minimum number of characters to make the password strong
    num = 0
    for num in numbers:
        if num not in password:
        num = 0
   if not any(num.is_lower for num in password:
        num +=1
   if not any(num.is_upper for num in password:
        return false 
    if not any(num in special_characters for num in password):
        print('the password should have at least one of the symbols $@#')
        return_val=False
    
    return num.max(0,6 -len(password)-n)

if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    n = int(input().strip())

    password = input()

    answer = minimumNumber(n, password)

    fptr.write(str(answer) + '\n')

    fptr.close()
