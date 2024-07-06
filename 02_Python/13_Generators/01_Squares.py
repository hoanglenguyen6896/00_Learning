def gensquares(N):
    for num in range(0,N):
        yield num ** 2

if __name__ == '__main__':
    for x in gensquares(10):
        print(x)

