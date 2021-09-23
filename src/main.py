import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', default='train', choices=['train', 'play'], type=str, help='train or play')

    parser.add_argument('--human_color', default='b', choices=['w', 'b'], type=str, help='w or b')
    args = parser.parse_args()

    if args.mode == 'train':
        pass
    elif args.mode == 'play':
        from ChessGame import ChessGame

        game = ChessGame(args.human_color)
        game.start()
