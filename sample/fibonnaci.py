print("Fibonnaci numbers")
a = 0
b = 1

n = 15

if n == 0:
    print(a)
    print(b)

    for i in range(2, n):
        next = a + b
        a = b
        b = next
        print(next)

elif n == 2:
    print(a)
    print(b)

else:
    print(a)
