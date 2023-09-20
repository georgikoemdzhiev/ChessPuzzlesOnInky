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
        # with Image.open(io.BytesIO(png_data)) as img:
        #     img.save(output_file, 'PNG')
    
        png_to_bmp(png_data, "output.bmp")
        return True
    except Exception as e:
        print(f"Error converting SVG to PNG: {str(e)}")
        return False
    

def generate_chessboard_image(board):
    # Create an empty chessboard image
    board_image = chess.svg.board(board=board)
    # with open('board_image.svg', 'w') as outputfile:
    #     outputfile.write(board_image)
    svg_to_png(board_image,"output.png")
    # TODO write logic to convert SVG to BMP
    # # Convert the SVG image to BMP using PIL
    # with Image.open(io.BytesIO(board_image.encode('utf-8'))) as img:
    #     img.save("chessboard.bmp", "BMP")


# Example usage
uci_moves = "e2e4 e7e5 g1f3"
initial_position_fen = chess.STARTING_FEN

san_moves, final_board = uci_to_san(uci_moves, initial_position_fen)
generate_chessboard_image(final_board)
