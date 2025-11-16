import os
import pwd
import time
from utils import *
from terminal import ReadChar, Key
class FileExplorer:
        def __init__(self,path):
            if path:
                self.path = path
                self.user = pwd.getpwuid( os.getuid() ).pw_name

            else:
                self.path = ""

            self.input = ""
            #self.term_size = os.get_terminal_size()
            self.files = []
            self.folders = []
            self.extensions = []
            self.pos = 0
            self.move = 0
            self.stay = True
            self.chrs = [ chr( x ) for x in range( 32, 127 ) ]

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

        def interact(self):
            pass

        def close(self):
            pass

        def execute(self):
            pass
        def get_file_info(self):
            for y,x in enumerate(self.files):
                info = os.stat( self.path + "/" +  x[0] )

                size = info.st_size # convert bytes to kb ,mb ...
                size = convertion( size )
                self.files[y].append(size)

                last_edit = info.st_mtime # format time
                last_edit = time.strftime("%Y-%m-%d %H:%M:%S", time.strptime( time.ctime ( last_edit ) ) )
                self.files[y].append(last_edit)

                owner = info.st_uid
                owner = pwd.getpwuid( owner ).pw_name
                self.files[y].append(owner)

                perm = oct(info.st_mode)[-3:]
                perm = get_perm( perm )
                self.files[y].append(perm)


        def get_folder_info(self):
            pass

        def get_input(self):
            with ReadChar() as Input:
               while self.stay:
                    a = Input.key()

                    if a == Key.DOWN:
                        self.pos = max( 0 , self.pos - 1 )

                    elif a == Key.UP:
                        self.pos = min( len(self.folders ) + len( self.files )  , self.pos + 1 )

                    elif a == Key.LEFT:
                        self.move = -1
                        self.interact()

                    elif a == Key.RIGHT:
                        self.move = 1
                        self.interact()

                    elif a == Key.ENTER:
                        if self.input == "":
                            self.close()

                        else:
                            self.execute()

                    elif a == Key.BACKSPACE:
                        self.input = self.input[ :-1 ]
                        print( self.input )

                    elif a == Key.DELETE:
                        self.input = ""
                        print(self.input)

                    elif a == Key.ESC:
                        self.stay = False

                    elif a in self.chrs:
                        self.input += a
                        print(self.input)

        def display(self):
            pass

        def main(self):
            pass

ob = FileExplorer("/home/sand/ChimkenMuziks")

ob.get_folders()
ob.get_input()