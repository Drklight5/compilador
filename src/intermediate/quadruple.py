class Quadruple:
    def __init__(self, op, left, right, result):
        self.op = op
        self.left = left
        self.right = right
        self.result = result

    def __repr__(self):
        left   = str(self.left)   if self.left   is not None else '_'
        right  = str(self.right)  if self.right  is not None else '_'
        result = str(self.result) if self.result is not None else '_'
        return f'({self.op}, {left}, {right}, {result})'
