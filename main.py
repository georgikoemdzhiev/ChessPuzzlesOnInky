import io
import linecache
import random
import chess
import chess.svg
import chess.engine
import cairosvg
from PIL import Image, ImageDraw, ImageFont
from inky.auto import auto
from inky.eeprom import read_eeprom
from puzzles_downloader import FileDownloader

PUZZLE_IMAGE_SIZE = (480,480)
PADDING = 5

def is_inky_connected():
    return read_eeprom() != None

def display_image(image: Image, text_to_render):
    resolution = (800,480)
    blank_img = Image.new('RGB', resolution, "white")

    add_text(blank_img, text_to_render)

    resized_img = image.resize(PUZZLE_IMAGE_SIZE) # make room for other content
    blank_img.paste(resized_img, (0,0))

    if(is_inky_connected()):
        inky = auto() # requires i2c interface enabled
        resolution = inky.resolution
        inky.set_image(blank_img)
        inky.show()
    else:    
        blank_img.show()

def add_text(blank_img, text_to_render):
    draw = ImageDraw.Draw(blank_img)
    font = ImageFont.load_default() 
    x, y = 480 + PADDING, 0 + PADDING
    text_color = (0, 0, 0)  # Black color (R, G, B)
    draw.text((x, y), text_to_render, fill=text_color, font=font)

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

def download_chess_puzzles(url, output_file_path, output_csv_path):
    downloader = FileDownloader(url, output_file_path)
    if downloader.download_file():
        print(f"Downloaded {output_file_path}")
    if downloader.unzip_file(output_csv_path):
        print(f"Unzipped to {output_csv_path}")
    else:
        print(f"Failed to unzip {output_file_path}")
    
def read_random_puzzle(csv_file_path, total_number_of_puzzles):

    # Generate a random line number (excluding the header)
    random_line_number = random.randint(2, total_number_of_puzzles)

    # Read the random line from the file
    random_line = linecache.getline(csv_file_path, random_line_number)

    # Parse the CSV data from the line
    random_puzzle = dict(zip(["PuzzleId", "FEN", "Moves", "Rating", "RatingDeviation", "Popularity", "NbPlays", "Themes", "GameUrl", "OpeningTags"], random_line.strip().split(',')))

    return random_puzzle

def debug_print(random_puzzle):
    if random_puzzle:
        print("Random Puzzle:")
        print("Puzzle ID:", random_puzzle["PuzzleId"])
        print("FEN:", random_puzzle["FEN"])
        print("Moves:", random_puzzle["Moves"])
        print("Rating:", random_puzzle["Rating"])
        print("Rating Deviation:", random_puzzle["RatingDeviation"])
        print("Popularity:", random_puzzle["Popularity"])
        print("NbPlays:", random_puzzle["NbPlays"])
        print("Themes:", random_puzzle["Themes"])
        print("Game URL:", random_puzzle["GameUrl"])
        print("Opening Tags:", random_puzzle["OpeningTags"])
    else:
        print("No puzzles found in the CSV file.")

def main():
    TOTAL_NUMBER_OF_PUZZLES = 3_466_049
    url = "https://database.lichess.org/lichess_db_puzzle.csv.zst"
    output_file_path = "lichess_db_puzzle.csv.zst"
    output_csv_path = "lichess_db_puzzle.csv"  # Unzipped CSV file

    download_chess_puzzles(url, output_file_path, output_csv_path)

    random_puzzle = read_random_puzzle(output_csv_path, TOTAL_NUMBER_OF_PUZZLES)

    debug_print(random_puzzle)

    uci_moves = random_puzzle["Moves"].split()[0] # make only the first set of moves
    initial_position_fen = random_puzzle["FEN"]

    san_moves, final_board = uci_to_san(uci_moves, initial_position_fen)
    board_image = generate_chessboard_image(final_board)
    png_image = svg_to_png(board_image)

    print(f"San Moves: {san_moves}")

    text_to_render = f"""Last Move: {san_moves}
Rating: {random_puzzle["Rating"]}
Themes: {random_puzzle["Themes"]}
Game URL: {random_puzzle["GameUrl"]}
"""

    display_image(png_image, text_to_render)


if __name__ == "__main__":
    main()