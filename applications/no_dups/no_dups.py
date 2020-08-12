def no_dups(s):
    # Your code here
    d = dict()
    words = s.split()

    for word in words:
        if word in d:
            continue
        else: 
            d[word] = 1

    new_string = [x for x in d]

    return " ".join(new_string) 


if __name__ == "__main__":
    print(no_dups(""))
    print(no_dups("hello"))
    print(no_dups("hello hello"))
    print(no_dups("cats dogs fish cats dogs"))
    print(no_dups("spam spam spam eggs spam sausage spam spam and spam"))