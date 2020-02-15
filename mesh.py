from mmRemote import *
import os
import mm
import sys
import subprocess32
from subprocess32 import Popen, PIPE, STDOUT
import time


class Mesh(object):
    def __init__(self, PLY_File):
        self.PLY_File = PLY_File
        self.remote = mmRemote()
        self.cmd = mmapi.StoredCommands()
        # self.PLY_File = str(sys.argv[1])  # filename of PLY file
        self.File_Dir = '/Users/trav/Desktop/Python/ARSCAN/PLY_Files/' + self.PLY_File
        self.Input_Dir = '/Users/trav/Desktop/Python/ARSCAN/meshlab.app/Contents/MacOS/'  # current location of STL file
        self.Output_Dir = '/Users/trav/Desktop/Python/ARSCAN/STL_Files/'  # location to export file to
        self.USDZ_OutDir = '/Users/trav/Desktop/Python/ARSCAN/USDZ_Files/'  # location to export file to
        self.USDZ_File = os.path.splitext(self.PLY_File)[0] + '.usdz'
        self.STL_File = os.path.splitext(self.PLY_File)[0] + '.stl'

        self.autoML()

    def autoML(self):
        cmd1 = 'cd ' + self.Input_Dir
        cmd2 = './meshlabserver -i ' + self.File_Dir + ' -o ' + self.STL_File + ' -s automl.mlx'
        final = Popen("{}; {}".format(cmd1, cmd2), shell=True, stdin=PIPE,
                      stdout=PIPE, stderr=STDOUT, close_fds=True)
        stdout, nothing = final.communicate()
        log = open('log', 'w')
        log.write(stdout)
        log.close()

        self.openFile()

    def openFile(self):
        time.sleep(1)
        # open Meshmixer
        subprocess32.run('open -a Meshmixer ' + self.Input_Dir + self.STL_File, shell=True)

        self.Apply_Profile()

    def Apply_Profile(self):
        time.sleep(1)
        # initialize connection
        self.remote.connect()
        # apply commands
        self.cmd.AppendBeginToolCommand("makeSolid")
        self.cmd.AppendToolParameterCommand('solidType', 1)
        self.cmd.AppendToolParameterCommand('solidResolution', 250)
        self.cmd.AppendCompleteToolCommand("accept")
        self.cmd.AppendBeginToolCommand('separateShells')
        self.cmd.AppendCompleteToolCommand("accept")
        self.remote.runCommand(self.cmd)

        self.Save_File()

    def Save_File(self):
        save_path = self.Output_Dir + self.STL_File
        # request list of objects in scene
        objects = mm.list_objects(self.remote)
        # select main object in list
        main_obj = objects[1]
        select_list = [main_obj]
        mm.select_objects(self.remote, select_list)
        # export to output directory
        mm.export_mesh(self.remote, save_path)

        self.Close_Program()

    def Close_Program(self):
        time.sleep(1)
        # terminate connection
        self.remote.shutdown()
        # close Meshmixer
        subprocess32.run('pkill -x meshmixer', shell=True)

        self.USDZ_Convert()

    def USDZ_Convert(self):
        time.sleep(1)
        cmd1 = 'cd /Users/trav/Desktop/Python/ARSCAN/usdpython/'

        cmd2 = './stl_to_usdz.sh ' + self.Output_Dir + self.STL_File + ' ' + self.USDZ_OutDir + self.USDZ_File

        final = Popen("{}; {}".format(cmd1, cmd2), shell=True, stdin=PIPE,
                      stdout=PIPE, stderr=STDOUT, close_fds=True)
        stdout, nothing = final.communicate()
        log = open('log', 'w')
        log.write(stdout)
        log.close()
        #subprocess32.run('./stl_to_usdz.sh Riddy.stl Riddy.usdz', shell=True)


# Open Terminal at 'ARSCAN' folder and enter command 'python mesh.py <filename>.stl'
# Make sure the STL file you wish to export is in the defined input directory
# Must include 'ARSCAN' folder in the defined output directory
Mesh('Riddy.ply')
