
class Memory:
    def __init__(self, name): # memory name
        self.name = name
        self.symbols = dict()
    def has_key(self, name):  # variable name
        if name in self.symbols:
            return self.symbols[name]
    def get(self, name):         # gets from memory current value of variable <name>
        if self.has_key(name):
            return self.symbols[name]
        return None
    def put(self, name, value):  # puts into memory current value of variable <name>
        self.symbols[name] = value


class MemoryStack:
                                                                             
    def __init__(self, memory=None): # initialize memory stack with memory <memory>
        self.stack = []
        self.stack.append(Memory("global"))

    def get(self, name):             # gets from memory stack current value of variable <name>
        for memory in reversed(self.stack):
            if memory.has_key(name):
                return memory.get(name)
        return None

    def insert(self, name, value): # inserts into memory stack variable <name> with value <value>
        self.stack[-1].put(name,value)

    def set(self, name, value): # sets variable <name> to value <value>
        for memory in reversed(self.stack):
            if memory.has_key(name):
                memory.put(name,value)
                return True
        return False

    def push(self, memory): # pushes memory <memory> onto the stack
        if(memory.instanceof(Memory)):
            self.stack.append(memory)
            return
        raise Exception("Argument is not Memory.class")

    def pop(self):          # pops the top memory from the stack
        self.stack.pop()


