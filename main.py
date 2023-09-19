import chess
import chess.engine
from PIL import Image, ImageDraw

def uci_to_san(uci_moves, initial_position_fen):
    board = chess.Board(initial_position_fen)
    san_moves = []

    for move_uci in uci_moves.split():
        move = chess.Move.from_uci(move_uci)
        san_move = board.san(move)
        board.push(move)
        san_moves.append(san_move)

    return san_moves, board

def generate_chessboard_image(board):
    # Create an empty chessboard image
    # board_image = chess.svg.board(board=board)
    chess.svg.piece(chess.Piece.from_symbol("R"))  

    # Convert the SVG image to BMP using PIL
    with Image.open(io.BytesIO(board_image.encode('utf-8'))) as img:
        img.save("chessboard.bmp", "BMP")

# Example usage
uci_moves = "e2e4 e7e5 g1f3"
initial_position_fen = chess.STARTING_FEN

san_moves, final_board = uci_to_san(uci_moves, initial_position_fen)
generate_chessboard_image(final_board)
