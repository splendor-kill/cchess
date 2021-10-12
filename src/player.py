class Player:
    def __init__(self, env, id_):
        self._env = env
        self._id_ = id_

    def make_decision(self):
        raise NotImplementedError('leave the chance to successors')


class Human(Player):
    def __init__(self, env, id_):
        super().__init__(env, id_)

    def make_decision(self):
        self.env.render()

        ak, arg1, arg2 = None, None, None
        while True:
            directive = input('what do you want? ')
            directive = directive.split()

            try:
                pass
            except Exception as e:
                print(e)

        return ak, arg1, arg2


class NoBrain(Player):
    def __init__(self, env, id_):
        super().__init__(env, id_)

    def make_decision(self):
        pass
