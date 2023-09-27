import io
import chess
import chess.svg
import chess.engine
import cairosvg
from PIL import Image
from inky.auto import auto

WHITE = (255,255,255)

def display_image(image: Image):
    inky = auto() # requires i2c interface enabled
    blank_img = Image.new('RGB', inky.resolution,WHITE)
    resized_img = image.resize(480,480) # make room for other content
    blank_img.paste(resized_img, (0,0))
    inky.set_image(blank_img)
    inky.show()

def uci_to_san(uci_moves, initial_position_fen):
    board = chess.Board(initial_position_fen)
    san_moves = []

    for move_uci in uci_moves.split():
        move = chess.Move.from_uci(move_uci)
        san_move = board.san(move)
        board.push(move)
        san_moves.append(san_move)

    return san_moves, board
    
def svg_to_png(svg_content):
    try:
        # Convert SVG content to a PNG in memory
        png_data = cairosvg.svg2png(bytestring=svg_content)

        # Convert PNG data to a PIL Image object
        with Image.open(io.BytesIO(png_data)) as img:
            display_image(img)
        return True
    except Exception as e:
        print(f"Error converting SVG to PNG: {str(e)}")
        return False
    

def generate_chessboard_image(board):
    # Create an empty chessboard image
    board_image = chess.svg.board(board=board)
    svg_to_png(board_image)

# Example usage
# uci_moves = "e8d7 a2e6 d7d8 f7f8"
uci_moves = "e8d7"
# initial_position_fen = chess.STARTING_FEN
initial_position_fen = "q3k1nr/1pp1nQpp/3p4/1P2p3/4P3/B1PP1b2/B5PP/5K2 b k - 0 17"

# san_moves, final_board = uci_to_san(uci_moves, initial_position_fen)
san_moves, final_board = uci_to_san(uci_moves, initial_position_fen)
generate_chessboard_image(final_board)
