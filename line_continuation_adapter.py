class line_continuation_adapter:
    default_cont_fn = lambda line: line.rstrip('\n')[-1:] == '\\'

    def __init__(self, iterable, begin_fn=default_cont_fn, cont_fn=default_cont_fn):
        self.iterable = iterable
        self.begin_fn, self.cont_fn = begin_fn, cont_fn

    def __iter__(self):
        return self

    def __next__(self):
        line = self.iterable.next().rstrip('\n')
        ret = line
        cont = False
        try:
            while (cont or self.begin_fn(line)) and self.cont_fn(line):
                cont = True
                ret = ret[:-1] + '\n'
                line = self.iterable.next().rstrip('\n')
                ret += line
        except StopIteration:
            pass
        return ret + '\n'

    def next(self): return self.__next__()

def test():
    b = lambda line: line[0:2] == '# '
    i = ['0', '# a\\', 'b', 'c', 'd \\', 'e']
    x = [line.rstrip('\n') for line in line_continuation_adapter(iter(i), b)]
    assert x == ['0', '# a\nb', 'c', 'd \\', 'e']
    print('tests passed')

if __name__ == '__main__':
    test()
