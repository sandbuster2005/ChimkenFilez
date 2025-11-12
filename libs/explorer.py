import os
import pwd
from utils import *
class File_Explorer:
        def __init__(self,path):
            if path:
                self.path = path
                self.user = pwd.getpwuid( os.getuid() ).pw_name
            else:
                self.path = ""

            #self.term_size = os.get_terminal_size()
            self.files = []
            self.folders = []
            self.extensions = []

        def get_files(self):
            files = os.listdir(self.path)
            self.files = [ x for x in files if os.path.isfile( self.path + "/" + x ) ]
            self.get_extensions()
            self.get_file_info()

        def get_folders(self):
            folders = os.listdir(self.path)
            self.folders = [ x for x in folders if os.path.isdir( self.path + "/" + x)]

        def get_extensions(self):
            for y,x in enumerate( self.files ):
                if "." in x:
                    extension = x.rsplit(".",1) [1]
                else:
                    extension = ""

                if extension not in self.extensions:
                    self.extensions.append(extension)

                self.files[y] = [ x, extension ]

            print(self.files)


        def open_file(self):
            pass

        def get_file_info(self):
            for y,x in enumerate(self.files):
                info = os.stat( self.path + "/" +  x[0] )

                size = info.st_size # convert bytes to kb ,mb ...
                size = convertion( size )

                last_edit = info.st_mtime # format time
                size =

                owner = info.st_uid
                owner = pwd.getpwuid( owner ).pw_name

                perm = oct(info.st_mode)[-3:]

                print(size,owner,last_edit,perm)

        def get_folder_info(self):
            pass

        def get_input(self):
            pass

        def scroll_text(self):
            pass

        def display(self):
            pass

        def main(self):
            pass

ob = File_Explorer("/home/sand/ChimkenMuziks")
ob.get_files()
ob.get_folders()