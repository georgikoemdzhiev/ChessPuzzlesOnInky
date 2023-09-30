# file_downloader.py

import os
import requests
import zstandard as zstd
import shutil

class FileDownloader:
    def __init__(self, url, output_file_path):
        self.url = url
        self.output_file_path = output_file_path

    def file_exists(self):
        return os.path.exists(self.output_file_path)

    def download_file(self):
        if self.file_exists():
            print(f"File {self.output_file_path} already exists. Skipping download.")
            return True

        try:
            response = requests.get(self.url, stream=True)

            if response.status_code == 200:
                with open(self.output_file_path, "wb") as output_file:
                    for chunk in response.iter_content(chunk_size=128):
                        output_file.write(chunk)

                return True
            else:
                print(f"Failed to download: Status code {response.status_code}")
                return False

        except requests.RequestException as e:
            print(f"Request Exception: {str(e)}")
            return False

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return False

    def unzip_file(self, output_unzipped_path):
        if not self.file_exists():
            print(f"File {self.output_file_path} does not exist.")
            return False

        if os.path.exists(output_unzipped_path):
            print(f"Unzipped file {output_unzipped_path} already exists. Skipping unzip.")
            return True

        try:
            with open(self.output_file_path, 'rb') as zst_file:
                with open(output_unzipped_path, 'wb') as output_csv_file:
                    dctx = zstd.ZstdDecompressor()
                    reader = dctx.stream_reader(zst_file)
                    shutil.copyfileobj(reader, output_csv_file)

            return True

        except Exception as e:
            print(f"An error occurred during unzip: {str(e)}")
            return False
