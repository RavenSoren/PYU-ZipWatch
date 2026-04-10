import os
import time
import zipfile
from pathlib import Path
from python.util import Util



def unzip_to_folder(zip_path, target_folder):
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(target_folder)
    except Exception as e:
        print("Error unzipping:", e)



def auto_unzip_monitor(download_folder, target_folder):
    try:
        download_folder = Path(download_folder)
        target_folder = Path(target_folder)

        if not target_folder.exists():
            target_folder.mkdir(parents=True, exist_ok=True)

        processed = set()

        print(f"Watching: {download_folder}")
        print(f"Saving to: {target_folder}")

        while True:
            for file in download_folder.iterdir():
                if file.suffix.lower() == ".zip" and file not in processed:

                    folder_name = file.stem + "_" + Util.rand_string(6)
                    extract_path = target_folder / folder_name
                    extract_path.mkdir(parents=True, exist_ok=True)

                    unzip_to_folder(str(file), str(extract_path))

                    print(f"Extracted {file.name} → {extract_path}")

                    try:
                        file.unlink()
                        print(f"Deleted original zip: {file.name}")
                    except Exception as e:
                        print(f"Could not delete {file.name}:", e)

                    processed.add(file)

            time.sleep(3)

    except KeyboardInterrupt:
        print("Stopped.")

    except Exception as e:
        print("Error:", e)
        time.sleep(3)



def main():
    downloads = Path.home() / "Downloads"
    documents = Path.home() / "Documents" / "Unzipped"

    auto_unzip_monitor(downloads, documents)



if __name__ == "__main__":
    main()
