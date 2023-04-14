from pathlib import Path
import collections
from datetime import datetime
import shutil
from pathlib import Path
import logging
from threading import Thread, RLock

logger_format = ("%(asctime)s [%(levelname)s] - %(name)s - %(funcName)15s:%(lineno)d - %(message)s")
lock = RLock()

fh = logging.FileHandler("clean_folder.log")
fh.setLevel(logging.DEBUG)     
fh.setFormatter(logging.Formatter(logger_format))

sh = logging.StreamHandler()
sh.setLevel(logging.ERROR)   
sh.setFormatter(logging.Formatter(logger_format))

def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(sh)
    logger.addHandler(fh)
    return logger

logger = get_logger(__name__)

CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ?<>,!@#[]№$%^&*()-=; "
LATIN_SYMBOLS = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_","_", "_")
TRANS = {}
for c, l in zip(CYRILLIC_SYMBOLS, LATIN_SYMBOLS):
    TRANS[ord(c)] = l
    TRANS[ord(c.upper())] = l.upper()

dict = {
    "documents": [".doc", ".docx", ".xlsx", ".txt", ".pdf", ".pptx"],
    "audio": [".mp3", ".ogg", ".wav", ".amr"],
    "video": [".avi", ".mp4", ".mov", ".mkv"],
    "images": [".jpeg", ".png", ".jpg", ".svg"],
    "archives": [".zip", ".gz", ".tar"],
}

def file_ex(file, path): #the function checks if a file with this name already exists.
    if file in path.iterdir():
        name = datetime.now().strftime("%d_%m_%Y_%H_%M_%S_%f")
        new_name = file.resolve().stem + f"_{name}_" + file.suffix
        new_path = Path(path, new_name)
        logger.info(f"File with name '{file.resolve().stem}' is already exists and was renamed to {new_name}")
        return new_path
    return file

def fold_create(file, path): #check if the necessary folder exists, if not - create it
    if path.exists():
        Thread(target=folder_sort, args=(lock, file, path)).start()
    else:
        Path(path).mkdir()
        logger.info(f"Folder with name '{path}' was not exist and was created")
        Thread(target=folder_sort, args=(lock, file, path)).start()

def folder_sort(locker, file, path): #changes the name of the file and moves it to the required folder.
    latin_name = normalize(file.name)
    new_file = Path(path, latin_name)
    file_path = file_ex(new_file, path)
    file.replace(file_path)
    logger.info(f"File with name '{file.name}' was removed to {path}")  

def show_result(p):
    total_dict = collections.defaultdict(list) 
    files_dict = collections.defaultdict(list)  
    for item in p.iterdir():
        if item.is_dir():
            for file in item.iterdir():
                if file.is_file():
                    total_dict[item.name].append(file.suffix)
                    files_dict[item.name].append(file.name)
    for k, v in files_dict.items():
        print()
        print(f" Folder '{k}' consists of files: {v}\n")
    print("File sorting successfully completed!")
    print("-"*70)
    print("| {:^14} |{:^9}| {:^40} ".format("Folder", "files", "file's extensions"))
    print("-"*70)
    for key, value in total_dict.items():
        k, a, b = key, len(value), ", ".join(set(value))
        print("| {:<14} |{:^9}| {:<40} ".format(k, a, b))
    print("-"*70)
   
def file_sort(folder ,p): #Checks each folder and file by their extension, organizes file sorting, and changes their names
    for i in p.iterdir():
        if i.name in ("documents", "audio", "video", "images", "archives", "other"): 
            continue
        if i.is_file():
            flag = False  
            for f, suf in dict.items():
                if i.suffix.lower() in suf:
                    path = Path(folder, f)
                    fold_create(i, path)
                    flag = True  
                else:
                    continue
            if not flag:
                path = Path(folder, "other")
                fold_create(i, path)
        elif i.is_dir():
            if len(list(i.iterdir())) != 0:
                file_sort(folder, i)  
            else:
                shutil.rmtree(i)  
                logger.info(f"Empty folder '{i}' was removed") 
    for fold in p.iterdir():
        if fold.name == "archives" and len(list(fold.iterdir())) != 0:
            for arch in fold.iterdir():
                if arch.is_file() and arch.suffix in (".zip", ".gz", ".tar"):
                    try:
                        arch_name = arch.resolve().stem  
                        path_to_unpack = Path(p, "archives", arch_name)  
                        shutil.unpack_archive(arch, path_to_unpack)
                        logger.info(f"Archiv '{arch.name}' was unpacked")
                    except:
                        logger.error(f"Error unpacking the archive '{arch.name}'!")
                    finally:
                        continue
                else:
                    continue
        elif fold.is_dir() and not len(list(fold.iterdir())):
            shutil.rmtree(fold)
            logger.info(f"Empty folder '{fold}' was removed")  

def normalize(name): #replace Cyrillic characters with Latin 
    global TRANS
    logger.info(f"File name '{name}' was normalized")
    return name.translate(TRANS)

def main():
    logger = get_logger(__name__)
    path = input('Enter the path to the folder\n>>>') 
    p = Path(path)
    folder = Path(path)
    try:
        file_sort(folder, p)
    except FileNotFoundError:
        print("The folder was not found.\n")
        logger.error(f"The folder with path '{path}' was not found")
    else:
        return show_result(p)

if __name__ == "__main__":
    main()
  
       
      
