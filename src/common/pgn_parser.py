from lark import Lark, Tree, Transformer, Visitor, Token

grammar = r"""
start: pgn+

pgn: options+ moves+ result_line post?

%import common.WS_INLINE -> WSI
%import common.WS
%import common.NEWLINE -> NL
%import common.ESCAPED_STRING -> ESC_STR
%import common.WORD
%import common.INT
%ignore WS

COMMENT: "{" /(.|\n)*?/ "}"
VAR: "(" /(.|\n)*?/ ")"
SCORE: "0-1"|"1-0"|"1/2-1/2"

options: opt_line NL
opt_line: "[" WORD WSI+ ESC_STR "]"

moves: INT "." WSI+ move WSI+ move WS+ VAR? COMMENT?
move: /.{4}/
result_line: INT "." WSI+ (move WS+)? SCORE

post: "="+ NL (/[^\[]+/ NL?)*
"""

pgn_parser = Lark(grammar, start='start')


def get_moves_and_result(pgn_file):
    with open(pgn_file, encoding='GB2312') as f:
        content = f.read()
    tree = pgn_parser.parse(content)

    class MovesResult(Visitor):
        def result_line(self, tree):
            nonlocal result
            for inst in tree.children:
                if isinstance(inst, Token) and inst.type == 'SCORE':
                    result = inst.value

        def move(self, tree):
            nonlocal moves
            mv = tree.children[0]
            moves.append(mv.value)

    moves = []
    result = None
    MovesResult().visit(tree)
    return moves, result


if __name__ == '__main__':
    import sys

    file = sys.argv[1]
    moves, result = get_moves_and_result(file)
    print(result)
    print(moves)
