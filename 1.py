import bitstring
import math
import struct
from codecs import decode


def addition(num1, num2):
    result = ''
    carry = 0

    for i in range(len(num1) - 1, -1, -1):
        r = carry
        r += 1 if num1[i] == '1' else 0
        r += 1 if num2[i] == '1' else 0
        result = ('1' if r % 2 == 1 else '0') + result

        carry = 0 if r < 2 else 1

    if carry != 0:
        result = '1' + result

    if len(result) > len(num1):
        return result[1:len(num1)+1]
    else:
        return result



def int_to_bin(num):
    binary = format(num, 'b')
    new_num = binary.zfill(32)
    if num < 0:
        new_num = '0' + new_num[1::]
        new_num = negative(new_num)
    return new_num


def float_to_bin(f):
    return bitstring.BitArray(float=f, length=32).bin


def negative(num):
    result = ''
    for i in range(0, len(num)):
        if num[i] == '0':
            result += '1'
        else:
            result += '0'
    if len(num) == 32:
        one = int_to_bin(1)
    elif len(num) == 64:
        one = int_to_bin(0) + int_to_bin(1)
    elif len(num) == 25:
        one = int_to_bin(1)[7:]
    result = addition(result, one)
    return result



def bin_to_int(b):
    return bitstring.BitArray(bin=(b)).int



def substraction(num1, num2):
    result = addition(num1, negative(num2))
    if len(result) > len(num1):
        return result[1:len(num1)+1]
    else:
        return result


def shift_right(num):
    if num[0] == '1':
        result = '1' + num[0:len(num)-1]
    else:
        result = '0' + num[0:len(num)-1]
    return result

def bin_to_float(float_num):
    if float_num == 0:
        return 0
    elif float_num == math.inf:
        return math.inf
    sign = 0
    if float_num[0] == '1':
        float_num = '0' + float_num[1:]
        sign = 1
    answer = bitstring.BitArray(bin=float_num).int
    answer = decode('%%0%dx' % (4 << 1) % answer, 'hex')[-4:]

    answer = struct.unpack('>f', answer)[0]
    if sign:
        return -answer
    else:
        return answer

def Booth(multiplicand, multiplier, size):
    product = ''
    result_list = []
    mult = ''
    for j in range(0, size):
        product += '0'
    result_list.append(product)
    result_list.append(multiplier + '0')
    for i in range(0, size):
        if result_list[1][-2:] == '10':
             result_list[0] = substraction(result_list[0], multiplicand)
        if result_list[1][-2:] == '01':
            result_list[0] = addition(result_list[0], multiplicand)

        mult = result_list[0] + result_list[1]
        mult = shift_right(mult)
        result_list[0], result_list[1] = mult[0:size], mult[size:]

    return mult[0:size*2]

a = 146
b = 1548
print("A * B = ", a*b)

a = int_to_bin(a)
b = int_to_bin(b)

print("Booth multiplication: ", bin_to_int(Booth(a, b, 32)))
print(Booth(a, b, 32))

def Division(dividend, divisor):
    quotient = ''
    divis = ''
    divid = ''
    divis += divisor
    for j in range(0, 32):
        divis += '0'
        divid += '0'
    divid += dividend
    for i in range(0, 33):
        if divis > divid:
            quotient += '0'
            divis = shift_right(divis)
        else:
            divid = substraction(divid, divis)
            quotient += '1'
            divis = shift_right(divis)
    return bin_to_int(quotient), bin_to_int(divid),quotient,divid


d1 = 17588
d2 = 3
print("d1 // d2 : ", d1 / d2)
d1 = int_to_bin(d1)
d2 = int_to_bin(d2)

print('(Quotient, Remainder): ', Division(d1, d2))





def Float_multiplication(num1, num2):
    e = 0
    zero_value = (num1[1:9] == '00000000' or num2[1:9] == '00000000')
    inf_value = (num1[1:9] == '11111111' or num2[1:9] == '11111111')
    s = num1[0] != num2[0]

    if zero_value:
        return 0
    elif inf_value:
        return math.inf

    m = Booth('01' + num1[9:], '01' + num2[9:], 25)

    e = bin_to_int('0' + num1[1:9]) + bin_to_int('0' + num2[1:9]) - 127

    if m[2] == '1':
        e += 1

    if e > 255:
        return math.inf
    elif e < 0:
        return 0
    
    if s:
        s = '1'
    else:
        s = '0'

    return s + int_to_bin(e)[24:] + m[3:26]

h1 = 153.12
h2 = 345.61
print("h1 * h2: ", h1 * h2)

print("Float multiplication: d1 * d2 : ", bin_to_float(Float_multiplication(float_to_bin(h1), float_to_bin(h2))))