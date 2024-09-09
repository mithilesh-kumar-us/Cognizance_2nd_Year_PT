a=input("")
a=a.split()
a=[int(x) for x in a]
values=input("")
values=values.split()
values=[int(x) for x in values]
values.sort()
n=a[0]
k=a[1]
t=1
count =0
for i in range(0, n):
    if t == n+1:
        break
    for j in range(t, n):
        diff= values[j]-values[i]
        if (diff)==k:
            t=j+1
            count=count+1
            break
        elif (diff)> k:
            t=j
            break
print(count)

