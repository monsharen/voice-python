def scienceToString(number):
    number,exponent = number.split('e')
    if number > 0 :
        outputkey = str([0]*number+"."+"0")
    elif number < 0 :
        outputkey = 1