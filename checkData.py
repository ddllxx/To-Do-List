# check if the str is num
def checkNumStr(str):
    for c in str:
        if not (ord('0') <= ord(c) and ord(c) <= ord('9')):
            return False
    return True

# check date
def checkDateStr(timeStr):
    data = timeStr.split('-')
    if len(data) != 3:
        return False
    year = data[0]
    month = data[1]
    day = data[2]
    if not checkNumStr(year) or not checkNumStr(month) or not checkNumStr(day):
        return False
    year = int(year)
    month = int(month)
    day = int(day)

    def checkRange(l, r, v):
        if v < l or v > r:
            return False
        return True
    
    if not checkRange(1000, 3000, year) or not checkRange(1, 12, month) or not checkRange(1, 31, day):
        return False

    flag = int(year % 400 == 0 or (year % 4 == 0 and year % 100 != 0))
    monthDays = [31, 28 + flag, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if day > monthDays[month - 1]:
        return False
    return True

# for test
if __name__ == '__main__':
    print(checkDateStr('2022-2-3'))
    print(checkDateStr('2002-9-80'))
    print(checkDateStr('2000-2-29'))
    print(checkDateStr('2100-2-29'))