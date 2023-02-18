firstname = input("Enter your name")

print("Greetings,")
print(firstname)

print("\\nAssignment")
x = 10
y = 5
z = "A string is stored in z"

print("\\x is")
print(x)

print("\\y is")
print(y)

print("\\z is")
print(z)


print("\\n\\nArtihmetic")
print("x + y is")
a = x + y
print(a)

print("\\nx - y is")
a = x - y
print(a)

print("\\nx * y is")
a = x * y
print(a)


print("\\nx / y is")
a = x / y
print(a)


print("\\n\\nConditionals")
if x > y:
    print("x is greater than y")
elif x < y:
    print("x is less than y")
else:
    print("x and y are equal")


print("\\n\\nLoops")
print("Print z, x times")
for i in range(x):
    print(z)


print("\\n\\nPrint 10 even numbers")
for i in range(2, 10, 2):
    print(i)

print("\\n\\nPrint odd numbers decreasing order")
for i in range(10, 2, -2):
    print(i)

print("\\n\\nNested structure")
c = 10
if c == 10:
    k = 0
    while k < 10:
        print(k)
        k += 1
else:
    print("The else statement")