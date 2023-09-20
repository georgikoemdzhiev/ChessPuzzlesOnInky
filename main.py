import io
import chess
import chess.svg
import chess.engine
import cairosvg
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

def png_to_bmp(png_file, output_file):
    try:
        # Open the PNG image
        with Image.open(png_file) as img:
            # Convert and save it as BMP
            img.save(output_file, 'BMP')
        
        return True
    except Exception as e:
        print(f"Error converting PNG to BMP: {str(e)}")
        return False
    
def svg_to_png(svg_content, output_file):
    try:
        # Convert SVG content to a PNG in memory
        png_data = cairosvg.svg2png(bytestring=svg_content)

        # Convert PNG data to a PIL Image object
        with Image.open(io.BytesIO(png_data)) as img:
            img.save(output_file, 'PNG')
    
        png_to_bmp("output.png", "output.bmp")
        return True
    except Exception as e:
        print(f"Error converting SVG to PNG: {str(e)}")
        return False
    

def generate_chessboard_image(board):
    # Create an empty chessboard image
    board_image = chess.svg.board(board=board)
    svg_to_png(board_image,"output.png")


# Example usage
uci_moves = "e8d7 a2e6 d7d8 f7f8"
# initial_position_fen = chess.STARTING_FEN
initial_position_fen = "q3k1nr/1pp1nQpp/3p4/1P2p3/4P3/B1PP1b2/B5PP/5K2 b k - 0 17"

san_moves, final_board = uci_to_san(uci_moves, initial_position_fen)
generate_chessboard_image(final_board)
