def pseudo(n):
    number = int(n)
    already_seen = []
    counter = 0
    
    while number not in already_seen:
        already_seen.append(number)
        number = int(str(number * number).zfill(12)[3:9])
    return already_seen
def pseudo_test(seed_number):
    #seed_number = int(input("Please enter a six-digit number:\n[####] "))
    number = seed_number
    already_seen = set()
    counter = 0

    while number not in already_seen:
        counter += 1
        already_seen.add(number)
        number = int(str(number * number).zfill(12)[3:9])  # zfill adds padding of zeroes

    print(f"We began with {seed_number} and"
          f" have repeated ourselves after {counter} steps"
          f" with {number}.")
    return counter
def seed_to_input(seed):
    return [i%5 for i in pseudo(seed)]        
        
