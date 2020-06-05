from collections import defaultdict

class SemanticRules():
    def __init__(self):
        self.types = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 'unknown')))
        self.unary_types = defaultdict(lambda: defaultdict(lambda: 'unknown'))
        self.fill_collections()

    def fill_collections(self):
        self.types['+']['int']['int'] = 'int'
        self.types['+']['float']['float'] = 'float'
        self.types['+']['int']['float'] = 'float'
        self.types['+']['float']['int'] = 'float'
        self.types['+']['string']['string'] = 'string'
        self.types['+']['matrix']['matrix'] = 'matrix'

        self.types['-']['int']['int'] = 'int'
        self.types['-']['float']['float'] = 'float'
        self.types['-']['int']['float'] = 'float'
        self.types['-']['float']['int'] = 'float'
        self.types['-']['matrix']['matrix'] = 'matrix'

        self.types['*']['int']['int'] = 'int'
        self.types['*']['float']['float'] = 'float'
        self.types['*']['int']['float'] = 'float'
        self.types['*']['float']['int'] = 'float'
        self.types['*']['matrix']['int'] = 'matrix'
        self.types['*']['int']['matrix'] = 'matrix'
        self.types['*']['matrix']['float'] = 'matrix'
        self.types['*']['float']['matrix'] = 'matrix'
        self.types['*']['matrix']['matrix'] = 'matrix'

        self.types['/']['int']['int'] = 'float'
        self.types['/']['float']['float'] = 'float'
        self.types['/']['int']['float'] = 'float'
        self.types['/']['float']['int'] = 'float'
        self.types['/']['matrix']['int'] = 'matrix'
        self.types['/']['matrix']['float'] = 'matrix'

        self.types['+=']['int']['int'] = 'int'
        self.types['+=']['float']['float'] = 'float'
        self.types['+=']['int']['float'] = 'float'
        self.types['+=']['float']['int'] = 'float'
        self.types['+=']['matrix']['matrix'] = 'matrix'

        self.types['-=']['int']['int'] = 'int'
        self.types['-=']['float']['float'] = 'float'
        self.types['-=']['int']['float'] = 'float'
        self.types['-=']['float']['int'] = 'float'
        self.types['-=']['matrix']['matrix'] = 'matrix'

        self.types['*=']['int']['int'] = 'int'
        self.types['*=']['float']['float'] = 'float'
        self.types['*=']['int']['float'] = 'float'
        self.types['*=']['float']['int'] = 'float'
        self.types['*=']['matrix']['int'] = 'matrix'
        self.types['*=']['matrix']['float'] = 'matrix'
        self.types['*=']['matrix']['matrix'] = 'matrix'

        self.types['/=']['int']['int'] = 'int'
        self.types['/=']['float']['float'] = 'float'
        self.types['/=']['int']['float'] = 'float'
        self.types['/=']['float']['int'] = 'float'
        self.types['/=']['matrix']['int'] = 'matrix'
        self.types['/=']['matrix']['float'] = 'matrix'

        self.types['.+']['matrix']['matrix'] = 'matrix'
        self.types['.+']['matrix']['int'] = 'matrix'
        self.types['.+']['matrix']['int'] = 'matrix'
        self.types['.+']['matrix']['float'] = 'matrix'
        self.types['.+']['int']['matrix'] = 'matrix'
        self.types['.+']['float']['matrix'] = 'matrix'

        self.types['.-']['matrix']['matrix'] = 'matrix'
        self.types['.-']['matrix']['int'] = 'matrix'
        self.types['.-']['matrix']['float'] = 'matrix'
        self.types['.-']['int']['matrix'] = 'matrix'
        self.types['.-']['float']['matrix'] = 'matrix'

        self.types['.*']['matrix']['matrix'] = 'matrix'
        self.types['.*']['matrix']['int'] = 'matrix'
        self.types['.*']['matrix']['float'] = 'matrix'
        self.types['.*']['int']['matrix'] = 'matrix'
        self.types['.*']['float']['matrix'] = 'matrix'

        self.types['./']['matrix']['matrix'] = 'matrix'
        self.types['./']['matrix']['int'] = 'matrix'
        self.types['./']['matrix']['float'] = 'matrix'
        self.types['./']['int']['matrix'] = 'matrix'
        self.types['./']['float']['matrix'] = 'matrix'

        self.types['==']['int']['int'] = 'boolean'
        self.types['==']['float']['float'] = 'boolean'
        self.types['==']['int']['float'] = 'boolean'
        self.types['==']['float']['int'] = 'boolean'
        self.types['==']['string']['string'] = 'boolean'
        self.types['==']['matrix']['matrix'] = 'boolean'

        self.types['!=']['int']['int'] = 'boolean'
        self.types['!=']['float']['float'] = 'boolean'
        self.types['!=']['int']['float'] = 'boolean'
        self.types['!=']['float']['int'] = 'boolean'
        self.types['!=']['string']['string'] = 'boolean'
        self.types['!=']['matrix']['matrix'] = 'boolean'

        self.types['>']['int']['int'] = 'boolean'
        self.types['>']['float']['float'] = 'boolean'
        self.types['>']['int']['float'] = 'boolean'
        self.types['>']['float']['int'] = 'boolean'
        self.types['>']['string']['string'] = 'boolean'
        self.types['>']['matrix']['matrix'] = 'boolean'

        self.types['<']['int']['int'] = 'boolean'
        self.types['<']['float']['float'] = 'boolean'
        self.types['<']['int']['float'] = 'boolean'
        self.types['<']['float']['int'] = 'boolean'
        self.types['<']['string']['string'] = 'boolean'
        self.types['<']['matrix']['matrix'] = 'boolean'

        self.types['>=']['int']['int'] = 'boolean'
        self.types['>=']['float']['float'] = 'boolean'
        self.types['>=']['int']['float'] = 'boolean'
        self.types['>=']['float']['int'] = 'boolean'
        self.types['>=']['string']['string'] = 'boolean'
        self.types['>=']['matrix']['matrix'] = 'boolean'

        self.types['<=']['int']['int'] = 'boolean'
        self.types['<=']['float']['float'] = 'boolean'
        self.types['<=']['int']['float'] = 'boolean'
        self.types['<=']['float']['int'] = 'boolean'
        self.types['<=']['string']['string'] = 'boolean'
        self.types['<=']['matrix']['matrix'] = 'boolean'

        self.unary_types['UMINUS']['int'] = 'int'
        self.unary_types['UMINUS']['float'] = 'float'
        self.unary_types['UMINUS']['matrix'] = 'matrix'

        self.unary_types['TRANSPOSE']['matrix'] = 'matrix'