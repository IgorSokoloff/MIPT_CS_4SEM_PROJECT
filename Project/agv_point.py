a1 = [8, 7, 6, 7, 8, 7,9,8,5 ]  # 1sem
a2 = [6,8,5,7,9,8,6,8]          # 2sem
a3 = [8,3,8,7,10,10,8]          # 3sem


a = a1 + a2+ a3


def avg_10(a):
    return sum(a)/len(a)



def avg_5(a):
    b = []
    for i in a:
        if (8 <= a[i] <= 10):
            b.append(5)
        if 5 <= a[i] <= 7:
            b.append(4)

        if 3 <= a[i] <= 4:
            b.append(3)

        if 0 <= a[i] <= 2:
            b.append(2)

    return sum(b)/len(b)

print ( avg_10(a) )

print ( avg_5(a) )