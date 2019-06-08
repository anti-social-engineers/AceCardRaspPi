
def lel(e):
    if e == "A":
        return e
    else:
        raise Exception("Ex 1")

def lel2(e):
    if e == "B":
        return e
    else:
        raise Exception("Ex 2")


try:
    lel("A")
    lel2("a")
except Exception as e:
    print(str(e))

