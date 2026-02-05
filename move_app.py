import shutil
import os

# Use raw strings for paths
src = r"d:\code_git\django\api_product\products"
dst = r"d:\code_git\django\products"

def move_app():
    if not os.path.exists(src):
        print(f"Source {src} does not exist!")
        return

    if os.path.exists(dst):
        print(f"Destination {dst} already exists.")
        # If it exists, maybe we already moved it partially?
        # But list_dir showed it missing.
        # Just in case, if empty, remove it.
        try:
            if not os.listdir(dst):
                print("Removing empty destination...")
                os.rmdir(dst)
        except:
            pass

    try:
        shutil.move(src, dst)
        print(f"Successfully moved {src} to {dst}")
    except Exception as e:
        print(f"Error moving directory: {e}")

if __name__ == "__main__":
    move_app()
