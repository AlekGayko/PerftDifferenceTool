from subprocess import Popen, PIPE
from threading import Thread
from os import getcwd, set_blocking
from time import sleep
from typing import List
import chess

class Engine:
    def __init__(self, name: str, engine_path: str, verbose: bool = False):
        self.name = name
        self.process = None
        self.verbose = verbose

        self.init_process(engine_path=engine_path)

    def init_process(self, engine_path: str):
        # Open pipe to subprocess
        self.process = Popen(
            [engine_path], 
            stdin=PIPE,
            stdout=PIPE,
            stderr=PIPE,
            text=True
        )
        # Set no blocking to eventually stop listening to process
        set_blocking(self.process.stdout.fileno(), False)

    # Cleanup listening thread and terminate process    
    def cleanup(self) -> None:
        if self.process is not None:
            self.process.terminate()
            self.process = None
            
    # Destructor cleans up            
    def __del__(self):
        self.cleanup()

    def write_to_process(self, command: str):
        if self.verbose:
            print(f"Sending to {self.name}: {command}")

        self.process.stdin.write(f"{command}\r\n")
        self.process.stdin.flush()

    def load_position(self, FEN: str, moves: List[str] = None):
        command = f"position fen {FEN}"

        if moves is not None and len(moves) > 0:
            command += " moves "
            command += " ".join(moves)

        self.write_to_process(command)

    def parse_perft_output(self, output: str):
        split_arr = output.split(":")

        if len(split_arr) != 2:
            return None, 0

        first, second = split_arr
        first = first.strip()
        second = second.strip()

        if first == "Nodes searched":
            return first, int(second)
        else:
            try:
                move = chess.Move.from_uci(first)
                return first, int(second)
            except ValueError:
                return None, 0


    def perft(self, depth: int) -> dict[str, int]:
        self.write_to_process(f"go perft {depth}")

        moves = {}
        nodes_searched = 0

        self.listening = True
        # Listen until stoplistening
        while self.listening:
            try:
                # Read incoming line
                output = self.process.stdout.readline()
                # If proces teminated unexpectedly, stop listening
                if self.process.poll() is not None:
                    raise ChildProcessError("Process Terminated")
                # Check if output is best route
                if output:
                    if self.verbose:
                        print(f"Received: {output.strip()}")

                    c_type, amount = self.parse_perft_output(output=output)

                    if c_type == "Nodes searched":
                        self.listening = False
                        break
                    elif c_type is None:
                        pass
                    else:
                        moves[c_type] = amount
                        nodes_searched += amount
                # If no response, sleep to avoid constant checking
                else:
                    sleep(0.01)      
            # Handle BlockingIOError associated with non blocking readline                    
            except BlockingIOError:
                print('err')

        return { "moves": moves, "nodes": nodes_searched }