import io
import chess
import chess.svg
import chess.engine
import cairosvg
from PIL import Image
from inky.auto import auto
from inky.eeprom import read_eeprom

WHITE = (255,255,255)
PUZZLE_IMAGE_SIZE = (480,480)

def is_inky_connected():
    return read_eeprom() != None

def display_image(image: Image):
    resolution = (800,480)
    blank_img = Image.new('RGB', resolution,WHITE)
    resized_img = image.resize(PUZZLE_IMAGE_SIZE) # make room for other content
    blank_img.paste(resized_img, (0,0))

    if(is_inky_connected()):
        inky = auto() # requires i2c interface enabled
        resolution = inky.resolution
        inky.set_image(blank_img)
        inky.show()
    else:    
        blank_img.show()


def uci_to_san(uci_moves, initial_position_fen):
    board = chess.Board(initial_position_fen)
    san_moves = []

    for move_uci in uci_moves.split():
        move = chess.Move.from_uci(move_uci)
        san_move = board.san(move)
        board.push(move)
        san_moves.append(san_move)

    return san_moves, board
    
def svg_to_png(svg_content) -> Image:
    try:
        # Convert SVG content to a PNG in memory
        png_data = cairosvg.svg2png(bytestring=svg_content)

        # Convert PNG data to a PIL Image object
        image = Image.open(io.BytesIO(png_data))
        return image
    except Exception as e:
        raise Exception(f"Error converting SVG to PNG: {str(e)}")

def generate_chessboard_image(board):
    # Create an empty chessboard image
    board_image = chess.svg.board(board=board)
    return board_image

# Example usage
# uci_moves = "e8d7 a2e6 d7d8 f7f8"
uci_moves = "e8d7"
# initial_position_fen = chess.STARTING_FEN
initial_position_fen = "q3k1nr/1pp1nQpp/3p4/1P2p3/4P3/B1PP1b2/B5PP/5K2 b k - 0 17"

# san_moves, final_board = uci_to_san(uci_moves, initial_position_fen)
san_moves, final_board = uci_to_san(uci_moves, initial_position_fen)
board_image = generate_chessboard_image(final_board)
png_image = svg_to_png(board_image)
display_image(png_image)
