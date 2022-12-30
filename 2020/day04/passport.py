import re

# filename = '2020/day04/test1.txt'
# filename = '2020/day04/test2.txt'
# filename = '2020/day04/test3.txt'
filename = '2020/day04/input.txt'

passports = []
with open(filename, 'r') as f:
    line = f.readline()
    passport = {}
    passports.append(passport)
    while line:
        line = line.strip()
        if len(line) == 0:
            passport = {}
            passports.append(passport)
        else:
            fields = line.split()
            for field in fields:
                kv = field.split(':')
                passport[kv[0]] = kv[1]
        line = f.readline()

num_valid = 0
for passport in passports:
    if len(passport) == 8 or len(passport) == 7 and 'cid' not in passport.keys():
        num_valid += 1

print(f'Part 1: {num_valid}')

hcl_prog = re.compile(r'#[0-9a-f]{6}')
pid_prog = re.compile(r'[0-9]{9}')

num_valid = 0
for passport in passports:
    valid = True
    # print(f'Checking passport: {passport}')
    if (len(passport) > 8 or len(passport) < 7
            or len(passport) == 7 and 'cid' in passport.keys()):
        print(f'  - Invaliid due to missing fields: {len(passport)}')
        valid = False
    else:
        for k, v in passport.items():
            if k == 'byr':
                byr = int(v)
                if byr < 1920 or byr > 2002:
                    print(f'  - Invalid birth year: {byr}')
                    valid = False
                    break
            elif k == 'iyr':
                iyr = int(v)
                if iyr < 2010 or iyr > 2020:
                    print(f'  - Invalid issue year: {iyr}')
                    valid = False
                    break
            elif k == 'eyr':
                eyr = int(v)
                if eyr < 2020 or eyr > 2030:
                    print(f'  - Invalid expiry year: {eyr}')
                    valid = False
                    break
            elif k == 'hgt':
                if len(v) < 3:
                    print(f'  - Invalid height: {v}')
                    valid = False
                    break
                hgt = int(v[:-2])
                unit = v[-2:]
                if (unit == 'in' and (hgt < 59 or hgt > 76)
                        or unit == 'cm' and (hgt < 150 or hgt > 193)):
                    print(f'  - Invalid height: {v}')
                    valid = False
                    break
            elif k == 'hcl':
                if not hcl_prog.fullmatch(v):
                    print(f'  - Invalid hair color: {v}')
                    valid = False
                    break
            elif k == 'ecl':
                if v not in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']:
                    print(f'  - Invalid eye color: {v}')
                    valid = False
                    break
            elif k == 'pid':
                if not pid_prog.fullmatch(v):
                    print(f'  - Invalid passport id: {v}')
                    valid = False
                    break
            elif k == 'cid':
                pass
            else:
                print(f'  - Unknown field name {k}: {v}')
                valid = False
                break
    if valid:
        num_valid += 1

print(f'Part 2: {num_valid}')