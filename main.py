from engine import Engine
import chess
from colorama import Fore, Style, init
import sys
import os
from typing import List, Tuple

VERBOSE = False

break_length = 90
break_char = "="
break_line = break_char * break_length

init()

def print_move_diff(moves: dict, mismatch_moves: List):
    if len(mismatch_moves) > 0:
        print(Fore.RED + "Mismatched Moves:")
        print(Fore.RED + " ".join(mismatch_moves) + Style.RESET_ALL)

    for move, amount in moves.items():
        message = f"{move}: {amount}"
        color = Fore.GREEN if amount == 0 else Fore.RED
        if move in mismatch_moves:
            color = Fore.BLUE

        print(color + message + Style.RESET_ALL)

def biggest_move_difference(moves1: dict, moves2: dict):
    mismatch_moves = []
    def compare_moves(pairs: List[Tuple], move_dict: dict):
        for move, amount in pairs:
            if move not in move_dict:
                mismatch_moves.append(move)

    moves1_pairs = moves1.items()
    moves2_pairs = moves2.items()

    compare_moves(moves1_pairs, moves2)
    compare_moves(moves2_pairs, moves1)

    moves = {}
    for move, amount in moves1.items():
        if move in moves2:
            moves[move] = amount - moves2[move]
        else:
            moves[move] = amount
    return [max(moves.items(), key=lambda x: x[1]), moves, mismatch_moves]

def print_failed_fen(moves: List):
    board = chess.Board()

    for idx, move in enumerate(moves):
        if idx == len(moves) - 1:
            break
        board.push(chess.Move.from_uci(move))

    print(f"FEN: {board.board_fen()}")

def search_move_differences(stockfish: Engine, custom_engine: Engine, FEN: str, max_depth: int) -> bool:
    moves = []
    success = True

    for depth in range(max_depth, 0, -1):
        print(f"{break_line}\n")

        print(f"Depth: {depth} | FEN: {FEN}")

        stockfish.load_position(FEN, moves)
        custom_engine.load_position(FEN, moves)

        perft1 = stockfish.perft(depth)
        print(f"Stockfish Perft: {perft1['nodes']}")

        perft2 = custom_engine.perft(depth)
        print(f"Anonymous Engine Perft: {perft2['nodes']}")
        
        big_move, diff_moves, mismatch_moves = biggest_move_difference(perft1["moves"], perft2["moves"])

        print_move_diff(moves=diff_moves, mismatch_moves=mismatch_moves)

        moves.append(big_move[0]) 

        print(f"\n{break_line}\n")

        if perft1["nodes"] == perft2["nodes"]:
            break
        
        success = False

        if big_move[1] == 0:
            print(Fore.RED + "Unequal Move Generation Resulted In Equal Move Counts" + Style.RESET_ALL)
            break
        
        if len(mismatch_moves) > 0:
            break           
    
    if success is False:
        print_failed_fen(moves)
        print(f"Moves: {' '.join(moves)}")

    return success      

def print_start():
    print(f"{break_line}\n")
    print("Perft Validator")
    print(f"\n{break_line}\n")

def print_end(result: bool):
    print(f"\n{break_line}\n")

    if result is True:
        print(Fore.GREEN + f"Move Generation Validated" + Style.RESET_ALL)
    else:
        print(Fore.RED + f"Move Generation Failed" + Style.RESET_ALL)

    print(f"\n{break_line}")

def main(stockfish_path: str, custom_engine_path: str, FEN: str, depth: int):
    global VERBOSE

    stockfish = Engine(verbose=VERBOSE,name="Stockfish", engine_path=stockfish_path)
    custom_engine = Engine(verbose=VERBOSE,name="Anonymous Engine", engine_path=custom_engine_path)

    result = search_move_differences(stockfish=stockfish, custom_engine=custom_engine, 
                                     FEN=FEN, max_depth=depth)
    
    print_end(result)

if __name__ == "__main__":
    print_start()

    if len(sys.argv) < 4:
        raise ValueError("Missing Required Custom Engine Path")
    
    stockfish_path = f"{os.getcwd()}/Stockfish/stockfish"
    custom_engine_path = f"{os.getcwd()}/{sys.argv[1]}"
    FEN = sys.argv[2]
    depth = int(sys.argv[3])

    if '-v' in sys.argv:
        VERBOSE = True

    try:
        board = chess.Board(FEN)
    except ValueError as e:
        print("Invalid FEN:", e)

    main(
        stockfish_path=stockfish_path, 
        custom_engine_path=custom_engine_path, 
        FEN=FEN,
        depth=depth
    )