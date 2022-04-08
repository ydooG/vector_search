from django.conf import settings


class InvertedIndex(dict):
    def __init__(self, mode='token'):
        super().__init__()
        self.mode = mode
        self._initialize()

    def _initialize(self):
        if self.mode == 'token':
            filename = 'inverted_index.txt'
        elif self.mode == 'lemma':
            filename = 'lemma_inverted_index.txt'
        else:
            raise ValueError(f'Unsupported mode "{self.mode}". Supported modes are "token", "lemma"')
        with open(str(settings.BASE_DIR) + f'/{filename}', mode='r') as file:
            for line in file:
                items = line[:-1].split(': ')
                self[items[0]] = set(map(int, items[1].split(' ')))

    def __getitem__(self, item):
        if item in self.keys():
            return dict.__getitem__(self, item)
        else:
            return set()
