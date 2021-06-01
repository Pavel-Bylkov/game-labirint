n, k = int(input()), int(input())
num = [i for i in range(1, n + 1)]
print(num)
start = k - 1
while len(num) > k and k != 1:
    rm = [i for i in range(start, len(num), k)]
    start = k - (len(num) - start) % k
    print(start, num)
    num = [num[i] for i in range(len(num)) if i not in rm]
while len(num) > 2:
    print(start, num)
    num.pop(start)
    start = k - (len(num) - start) % k - 1

print(start, (num * (k//2 + 1))[start])