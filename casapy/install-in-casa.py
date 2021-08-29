#!/usr/bin/env python
# -*- coding: utf-8 -*-
##********************************************************************************************************************************************************
##
##
##  Script for installing the myXCLASS to CASA interface in CASA
##  Copyright (C) 2012 - 2017  Thomas Moeller
##
##  I. Physikalisches Institut, University of Cologne
##
##
##
##  Versions of the program:
##
##  Who           When         What
##
##  T. Moeller    2013-08-08   initial version
##  T. Moeller    08.11.2017   current version 1.2.5
##
##
##
##  License:
##
##    GNU GENERAL PUBLIC LICENSE
##    Version 3, 29 June 2007
##    (Copyright (C) 2007 Free Software Foundation, Inc. <http://fsf.org/>)
##
##
##    This program is free software: you can redistribute it and/or modify
##    it under the terms of the GNU General Public License as published by
##    the Free Software Foundation, either version 3 of the License, or
##    (at your option) any later version.
##
##    This program is distributed in the hope that it will be useful,
##    but WITHOUT ANY WARRANTY; without even the implied warranty of
##    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##    GNU General Public License for more details.
##
##    You should have received a copy of the GNU General Public License
##    along with this program.  If not, see <http://www.gnu.org/licenses/>.
##
##********************************************************************************************************************************************************


##--------------------------------------------------------------------------------------------------------------------------------------------------------
import os                                                                                   ## import os package
import sys                                                                                  ## import sys package
##--------------------------------------------------------------------------------------------------------------------------------------------------------


##--------------------------------------------------------------------------------------------------------------------------------------------------------
##
## read xml tags with name tagName in xml file GetXMLtag and return contents in ContentsTag
##
def GetXMLtag(xmlFileName, tagName):
    """

input parameters:
-----------------

    - xmlFileName:          path and name of the xml-file

    - tagName:              name of the tag, whose contents is read


output parameters:
------------------

    - ContentsTag:          the contents of the selected tag, always a list, including an entry for each occurance

    """
    ContentsTag = []


    ## read in whole xml-file
    xmlFile = open(xmlFileName)
    ContentsXMLFile = xmlFile.readlines()
    xmlFile.close()


    ## analyze contents of xml file
    for line in ContentsXMLFile:                                                            ## loop over all lines in the xml file
        striplines = line.strip()
        if (not striplines.startswith("<!--")):


            ## get name(s) of exp data file(s)
            if (striplines.find("<" + tagName + ">") > (-1)):                               ## get name of experimental data file
                i = striplines.find(">")
                j = striplines.rfind("<")
                if (i < j):
                    ContentsTag.append(striplines[i + 1:j])                                 ## save name(s) in list

    ## define return value
    return ContentsTag


##--------------------------------------------------------------------------------------------------------------------------------------------------------
##
## write contents in ContentsTag to xml file
##
def WriteXMLtag(xmlFileName, tagName, ContentsTag):
    """

input parameters:
-----------------

    - xmlFileName:          path and name of the xml-file

    - tagName:              name of the tag, whose contents has to be modified

    - ContentsTag:          the new contents of the tag, which has to be always a list, i.e. a content for each occurance of the tag



output parameters:
------------------

    - None

    """


    ## read in whole xml-file
    xmlFile = open(xmlFileName)
    ContentsXMLFile = xmlFile.readlines()
    xmlFile.close()


    ## analyze contents of xml file
    NXF = open(xmlFileName, 'w')                                                            ## open xml file
    counter = (-1)                                                                          ## reset counter
    for line in ContentsXMLFile:                                                            ## loop over all lines in the xml file
        striplines = line.strip()                                                           ## remove leading and trailing blanks
        if (not striplines.startswith("<!--")):                                             ## ignore comments
            if (striplines.find("<" + tagName + ">") > (-1)):                               ## get name of experimental data file
                counter += 1
                i = line.find("<")
                if (i > (-1)):
                    space = line[:i]
                else:
                    space = ""
                NXF.write(space + "<" + tagName + ">" + ContentsTag[counter] + "</" + tagName + ">\n")
            else:
                NXF.write(line)
        else:
            NXF.write(line)
    NXF.close()


    ## define return value
    return
##--------------------------------------------------------------------------------------------------------------------------------------------------------


##--------------------------------------------------------------------------------------------------------------------------------------------------------
##
## Main routine
##
##--------------------------------------------------------------------------------------------------------------------------------------------------------
if (__name__ == '__main__'):


    ## print some help to screen
    helpInformation = """


    myXCLASS to CASA interface:
    ---------------------------


    This file installs the XCLASS-interface, so that you can use it in CASA without any
    additional commands.


    Command line options for this installation script:

        "--nocomp":         MAGIX and myXCLASS program are NOT compiled. (This is useful if you
                            move the XCLASS directory on your system.)

        "--mpi":            Compile option for XCLASS: The standard MAGIX installation and the
                            myXCLASS optimized version of MAGIX are compiled with MPI.

        "--smp":            Compile option for XCLASS: The standard MAGIX installation and the
                            myXCLASS optimized version of MAGIX are compiled with OpenMP.

        "--nocasa":         Do not execute the CASA installation scripts and compile only.

        "--help":           Print this information to screen


    Example:

        python install-in-casa.py --mpi



    IMPORTANT:
    ----------

    Before you start this file, please make sure that the path of the current CASA installation
    directory is already added to the PATH environment variable defined in your .bashrc file!


    Please note:

    - XCLASS requires the gfortran (with OpenMP) and the gcc compiler.

    - The MPI parallized version requries the OpenMPI package as well.

    - Whenever you move the XCLASS-interface directory or when you install a new CASA version,
      please re-execute this file once again.


    """
    print(helpInformation)


    ## get home directory
    HomeDir = str(os.environ.get('HOME',''))

    # Debug:
    # print "HomeDir = ", HomeDir"


    ## get current directory
    myXCLASSDir = os.getcwd() + "/"


    ## define name of database file
    Sqlite3DBFileName = "cdms_sqlite.db"


    ##====================================================================================================================================================
    ## determine compile_flag
    compile_flag = True
    if (os.path.isfile("programs/myXCLASS/src/myNewXCLASS.exe")):
        compile_flag = False

    # Debug:
    # print "compile_flag = ", compile_flag


    ##====================================================================================================================================================
    ## analyze command line arguments
    MAGIXCompilationFlag = "smp"
    NoCASAFlag = False
    if (len(sys.argv) > 1):                                                                 ## check, if command line arguments are defined
        for argument in sys.argv[1:]:                                                       ## loop over all command line arguments


            ##--------------------------------------------------------------------------------------------------------------------------------------------
            ## get run flags
            if (argument.startswith('--')):                                                 ## run flags are marked with "--" characters
                option = argument[2:].strip()                                               ## remove "--" characters and leading and tailing blanks
                option = option.lower()                                                     ## all small letters


                ## do not compile interface
                if (option == "nocomp"):
                    compile_flag = False


                ## get compilation options for MAGIX
                elif (option == "mpi" or option == "smp"):
                    compile_flag = True
                    MAGIXCompilationFlag = option


                ## compile and modify source files but do not call CASA installation routines
                elif (option == "nocasa"):
                    NoCASAFlag = True


                ## do not compile interface
                elif (option == "help"):
                    print(helpInformation)
                    sys.exit(0)


    ##====================================================================================================================================================
    ## define in the following line, where your current CASA version is installed in your HOME directory
    if (not NoCASAFlag):
        CASACall = ["which casa", "which casapy"]
        FoundCASAFlag = False
        for LocalCommand in CASACall:
            cmdString = LocalCommand + " > tmp.out 2>&1"
            os.system(cmdString)
            tmpFile = open("tmp.out")
            CompilerInfo = tmpFile.readlines()
            tmpFile.close()
            os.remove("tmp.out")
            if (CompilerInfo != []):
                FoundCASAFlag = True
                break
        if (not FoundCASAFlag):
            print("\n\nError in the installation script for XCLASS package!")
            print("\n\tCan not execute casa / casapy!")
            print("\n\tPlease modify the PATH environment variable!")
            print("\n\texport PATH=$PATH:/path-to-casa-version/\n\n")
            sys.exit(0)
        else:
            casaHomeInstallationDir = os.path.dirname(os.path.abspath(CompilerInfo[0])) + "/"

        # Debug:
        # print "casaHomeInstallationDir = ", casaHomeInstallationDir, "\n\n\n\n"


        ##------------------------------------------------------------------------------------------------------------------------------------------------
        ## define command for buildmytasks script
        buildmytasksCommand = ""
        buildmytasksCommandList = ["buildmytasks", "../buildmytasks", "bin/buildmytasks"]
        for LocalbuildmytasksCommand in buildmytasksCommandList:
            cmd_string = "which " + LocalbuildmytasksCommand
            ScreenOut = os.popen(cmd_string, 'r', 1)
            buildmytasksInstallationDir = ScreenOut.readline()
            buildmytasksInstallationDir = buildmytasksInstallationDir.strip()
            if (buildmytasksInstallationDir != ""):
                buildmytasksCommand = LocalbuildmytasksCommand
                break
        if (buildmytasksCommand == ""):
            print("\n\nError in the installation script for XCLASS package!")
            print("\n\tCan not execute buildmytasks script!")
            print("\n\tPlease modify the PATH environment variable!")
            print("\n\texport PATH=$PATH:/path-to-casa-version/\n\n")
            sys.exit(0)

        # Debug:
        # print "buildmytasksCommand = ", buildmytasksCommand


    ##====================================================================================================================================================
    ## compile MAGIX und myXCLASS and check if compilation was successfully
    if (compile_flag):


        ## check, if gcc and gfortran compilers are available
        ListOfWarnings = []
        ListOfCommands = ["gcc -v", "gfortran -v"]
        for CompilerID, LocalCommand in enumerate(ListOfCommands):
            cmdString = LocalCommand + " > tmp.out 2>&1"
            os.system(cmdString)
            tmpFile = open("tmp.out")
            CompilerInfo = tmpFile.readlines()
            tmpFile.close()
            os.remove("tmp.out")
            for line in CompilerInfo:
                if (line.find("not found") > (-1)):
                    if (CompilerID == 0):
                        ListOfWarnings.append("gcc")
                    else:
                        ListOfWarnings.append("gfortran")
        if (ListOfWarnings != []):
            print("\n\nError in the installation script for XCLASS package!")
            print("\n\tCan not find " + ListOfWarnings[0] + "",)
            if (len(ListOfWarnings) == 2):
                print("and " + ListOfWarnings[1] + " ",)
            print("compiler!")
            print("\n\tPlease install compiler and re-execute XCLASS installation script!\n\n")
            sys.exit(0)


        ## check, if OpenMPI is available if --mpi is selected
        if (MAGIXCompilationFlag == "mpi"):
            cmdString = "mpif90 -v > tmp.out 2>&1"
            os.system(cmdString)
            tmpFile = open("tmp.out")
            CompilerInfo = tmpFile.readlines()
            tmpFile.close()
            os.remove("tmp.out")
            for line in CompilerInfo:
                if (line.find("not found") > (-1)):
                    print("\n\nError in the installation script for XCLASS package!")
                    print("\n\tCan not find OpenMPI compiler!")
                    print("\n\tPlease install compiler and re-execute XCLASS installation script!\n\n")
                    sys.exit(0)


        ## compile MAGIX and check, if compilation was successfully
        print("\n\n\nCompile MAGIX ..\n\n")
        MAGIXTestDIR = myXCLASSDir + "programs/MAGIX/Modules/Levenberg-Marquardt/bin/"
        cmd_string = "rm -rf " + MAGIXTestDIR + "*.exe"
        os.system(cmd_string)
        cmd_string = "cd " + myXCLASSDir + "programs/MAGIX/; sh install.sh " + MAGIXCompilationFlag + "; cd ../.."
        os.system(cmd_string)
        ListOfFiles = os.listdir(MAGIXTestDIR)
        CounterEXEFiles = 0
        for LocalFile in ListOfFiles:
            if (LocalFile.endswith(".exe")):
                CounterEXEFiles += 1
        if (CounterEXEFiles != 2):
            print("\n\nError in the installation script for XCLASS package!")
            print("\n\tThe compilation of MAGIX failed!")
            print("\n\tPlease take a look at the compiler messages!\n\n")
            sys.exit(0)


        ## compile MAGIX demo model programs and check, if compilation was successfully
        print("\n\n\nCompile MAGIX demo model program ..\n\n")
        MAGIXModelProgTestDIR = myXCLASSDir + "programs/MAGIX/Fit-Functions/Drude-Lorentz_general/bin/"
        cmd_string = "rm -rf " + MAGIXModelProgTestDIR + "*.exe"
        os.system(cmd_string)
        # cmd_string = "cd " + myXCLASSDir + "programs/MAGIX/Fit-Functions/Drude-Lorentz_conv/; make all; "
        cmd_string = "cd " + myXCLASSDir + "programs/MAGIX/Fit-Functions/Drude-Lorentz_general/; make all; cd " + myXCLASSDir
        os.system(cmd_string)
        ListOfFiles = os.listdir(MAGIXModelProgTestDIR)
        CounterEXEFiles = 0
        for LocalFile in ListOfFiles:
            if (LocalFile.endswith(".exe")):
                CounterEXEFiles += 1
        if (CounterEXEFiles != 19):
            print("\n\nError in the installation script for XCLASS package!")
            print("\n\tThe compilation of the MAGIX demo model program failed!")
            print("\n\tPlease take a look at the compiler messages!\n\n")
            sys.exit(0)


        ## compile MAGIX demo model programs and check, if compilation was successfully
        print("\n\n\n\nCompile myXCLASS ..\n\n")
        myXCLASSTestDIR = myXCLASSDir + "programs/myXCLASS/src/"
        cmd_string = "rm -rf " + myXCLASSTestDIR + "*.exe"
        os.system(cmd_string)
        cmd_string = "cd " + myXCLASSDir + "programs/myXCLASS/src/; make all; cd ../../.."  ## compile myXCLASS
        os.system(cmd_string)
        ListOfFiles = os.listdir(myXCLASSTestDIR)
        CounterEXEFiles = 0
        for LocalFile in ListOfFiles:
            if (LocalFile.endswith(".exe")):
                CounterEXEFiles += 1
        if (CounterEXEFiles != 1):
            print("\n\nError in the installation script for XCLASS package!")
            print("\n\tThe compilation of the myXCLASS program failed!")
            print("\n\tPlease take a look at the compiler messages!\n\n")
            sys.exit(0)


    ##====================================================================================================================================================
    ## modifiy the python file for task myXCLASS
    print("Modify python file for task myXCLASS ..",)


    ##----------------------------------------------------------------------------------------------------------------------------------------------------
    ## modify the registration xml file for myXCLASS
    MAGIXRegXML = myXCLASSDir + "programs/MAGIX/Fit-Functions/myXCLASS/xml/myNewXCLASS.xml"
    PathToStartScript = GetXMLtag(MAGIXRegXML, "PathStartScript")
    PathToStartScript = PathToStartScript[0].strip()

    # Debug:
    # print "PathToStartScript = ", PathToStartScript


    ## make path of start script absolute
    i = PathToStartScript.find("programs/MAGIX/Fit-Functions/myXCLASS/bin/start_myNewXCLASS.py")
    if (i > (-1)):
        PathToStartScript = [myXCLASSDir + PathToStartScript[i:]]
    else:
        print("\n\nError in the installation script for XCLASS package!")
        print("\n\tCannot modify the path of the start script for the myXCLASS program in the registration XML file.\ņ")
        sys.exit(0)

    # Debug:
    # print "PathToStartScript = ", PathToStartScript


    ## write new path to registration XML file
    WriteXMLtag(MAGIXRegXML, "PathStartScript", PathToStartScript)


    ## write path of current directory to the execution tag for myXCLASS program
    ExeCommandStartScriptTag = ["python start_myNewXCLASS.py " + myXCLASSDir]
    WriteXMLtag(MAGIXRegXML, "ExeCommandStartScript", ExeCommandStartScriptTag)


    ##----------------------------------------------------------------------------------------------------------------------------------------------------
    ## modify the registration xml file for conventional Drude Lorentz test model
    MAGIXRegXML = myXCLASSDir + "programs/MAGIX/Fit-Functions/Drude-Lorentz_conv/xml/Conventional_Drude-Lorentz.xml"
    PathToStartScript = GetXMLtag(MAGIXRegXML, "PathStartScript")
    PathToStartScript = PathToStartScript[0].strip()

    # Debug:
    # print "PathToStartScript = ", PathToStartScript


    ## make path of start script absolute
    i = PathToStartScript.find("programs/MAGIX/Fit-Functions/Drude-Lorentz_conv/bin/DrudeLorentzConv.exe")
    if (i > (-1)):
        PathToStartScript = [myXCLASSDir + PathToStartScript[i:]]
    else:
        print("\n\nError in the installation script for XCLASS package!")
        print("\n\tCannot modify the path of the conventional Drude Lorenz test model in the registration XML file.\n ")
        sys.exit(0)

    # Debug:
    # print "PathToStartScript = ", PathToStartScript


    ## write new path to registration XML file
    WriteXMLtag(MAGIXRegXML, "PathStartScript", PathToStartScript)


    ##----------------------------------------------------------------------------------------------------------------------------------------------------
    ## modify the registration xml file for generalized Drude Lorentz test model
    MAGIXRegXML = myXCLASSDir + "programs/MAGIX/Fit-Functions/Drude-Lorentz_general/xml/Generalized_Drude-Lorentz__sym__freq-damping+Rp.xml"
    PathToStartScript = GetXMLtag(MAGIXRegXML, "PathStartScript")
    PathToStartScript = PathToStartScript[0].strip()

    # Debug:
    # print "PathToStartScript = ", PathToStartScript


    ## make path of start script absolute
    i = PathToStartScript.find("programs/MAGIX/Fit-Functions/Drude-Lorentz_general/bin/DrudeLorentzGeneral__sym__freq-damping+Rp.exe")
    if (i > (-1)):
        PathToStartScript = [myXCLASSDir + PathToStartScript[i:]]
    else:
        print("\n\nError in the installation script for XCLASS package!")
        print("\n\tCannot modify the path to the generalized Drude Lorenz test model in the registration XML file.\n")
        sys.exit(0)

    # Debug:
    # print "PathToStartScript = ", PathToStartScript


    ## write new path to registration XML file
    WriteXMLtag(MAGIXRegXML, "PathStartScript", PathToStartScript)


    ##----------------------------------------------------------------------------------------------------------------------------------------------------
    ## modifiy file task_myXCLASS.py: Include directory of XCLASS-interface directory


    ## read in old directory to file
    filename = "build_tasks/task_myXCLASS.py"
    pythonFile = open(filename)
    contents = pythonFile.readlines()
    pythonFile.close()


    ## write modified python file
    pythonFile = open(filename, 'w')
    for line in contents:
        if (line.find("XCLASSSystemRootDirectory =") > 0):
            newline = "    XCLASSSystemRootDirectory = " + chr(34) + myXCLASSDir + chr(34)

            # Debug:
            # print newline

            pythonFile.write(newline + "\n")
        else:
            pythonFile.write(line)
    pythonFile.close()

    # Debug:
    # print "myXCLASSDir = ", myXCLASSDir
    print("done!\n")


    ##====================================================================================================================================================
    ## check stand alone installation of numpy, scipy, matplotlib, sqlite3 and qt4 installation
    print("Check availability of required python packages ..",)
    # ListOfPythonPackagesNames = ["numpy", "scipy", "matplotlib", "sqlite3", "PyQt4"]
    ListOfPythonPackagesNames = ["numpy", "scipy", "matplotlib", "sqlite3"]
    ListOfPythonPackagesFlags = []
    ListOfPythonPackagesVersions = []
    ListOfWarnings = []
    for LocalPythonPackage in ListOfPythonPackagesNames:
        LocalFlag = False
        LocalVersion = "none"
        try:
            exec("import " + LocalPythonPackage)
            LocalFlag = True
        except ImportError:
            ListOfWarnings.append("Can not import " + LocalPythonPackage + " package.")
            LocalFlag = False
        if (LocalFlag):
            if (LocalPythonPackage == "numpy" or LocalPythonPackage == "scipy"):
                LocalVersion = eval(LocalPythonPackage + ".version.version")
            elif (LocalPythonPackage == "matplotlib"):
                LocalVersion = eval(LocalPythonPackage + ".__version__")
            elif (LocalPythonPackage == "sqlite3"):
                LocalVersion = eval(LocalPythonPackage + ".version")
            elif (LocalPythonPackage == "PyQt4"):
                LocalVersion = "?"
        ListOfPythonPackagesFlags.append(LocalFlag)
        ListOfPythonPackagesVersions.append(LocalVersion)


    ## check stand alone installation of pyfits / astropy
    try:
        import pyfits
        LocalFlag = True
    except ImportError:
        LocalFlag = False
    if (not LocalFlag):
        try:
            import astropy
            LocalFlag = True
        except ImportError:
            LocalFlag = False
        if (LocalFlag):
            LocalVersion = astropy.__version__
            ListOfPythonPackagesVersions.append(LocalVersion)
        else:
            ListOfWarnings.append("Can not import astropy nor pyfits package.")
    else:
        ListOfPythonPackagesFlags.append(LocalFlag)
        LocalVersion = pyfits.__version__
        ListOfPythonPackagesVersions.append(LocalVersion)


    # Debug:
    #    print "ListOfPythonPackagesNames = ", ListOfPythonPackagesNames
    #    print "ListOfPythonPackagesFlags = ", ListOfPythonPackagesFlags
    #    print "ListOfPythonPackagesVersions = ", ListOfPythonPackagesVersions


    ## print out warning or error depending on CASA flag
    if (ListOfWarnings != []):
        if (NoCASAFlag):
            print("\n\n\nError in the installation script for XCLASS package!")
        else:
            print("\n\nWARNING!\n")
        for line in ListOfWarnings:
            print("\n\t" + line + "!")
        print("\n\tXCLASS can not be used without CASA!\n\n")
        if (NoCASAFlag):
            print("\n\tPlease install the required python packages!\n\n")
            sys.exit(0)
    print("done!\n")


    ##====================================================================================================================================================
    ## execute CASA installation scripts?
    if (not NoCASAFlag):


        ##================================================================================================================================================
        ## the file path-to-casa/lib/libgfortran.so.3 in CASA installation is not compatible, rename symbolic link
        buggyFile = casaHomeInstallationDir + "/lib/"
        if (os.path.isfile(buggyFile + "libgfortran.so.3")):


            ## check write access in directory buggyFile
            if (os.access(buggyFile + "libgfortran.so.3", os.W_OK)):
                print("Check for libgfortran.so.3 library in CASA installation and rename it, if neccessary ..",)
                command_string = "mv " + buggyFile + "libgfortran.so.3 " + buggyFile + "libgfortran__old.so.3"
                os.system(command_string)
                print("done!")
            else:
                print("\n\n\nWARNING:\n\n")
                print("\t\t Can not write to directory " + buggyFile)
                print("\t\t to fix CASA bug.")
                print("\t\t Please, give write access to this directory!")
                sys.exit(0)
        print(" ")


        ##================================================================================================================================================
        ## execute the buildmytasks shell script for each new task
        print("Execute the buildmytasks shell script for each task:")


        ## define list of function names
        ListOfFunctionNames = ["myXCLASS", "LoadASCIIFile", "myXCLASSPlot", "MAGIX", "myXCLASSFit", "myXCLASSMapFit", "myXCLASSMapRedoFit", \
                               "GetTransitions", "ListDatabase", "DatabaseQuery", "UpdateDatabase", "LineIdentification"]

        # Debug:
        # print 'ListOfFunctionNames = ', ListOfFunctionNames


        ## execute buildmytasks shell script for each function
        command_string = "cd " + casaHomeInstallationDir                                    ## go to CASA directory
        os.system(command_string)
        for func in ListOfFunctionNames:                                                    ## loop over all function in the list ListOfFunctionNames
            print("Execute buildmytasks shell script for " + func + " function ..",)
            command_string = "cd " + myXCLASSDir + "build_tasks/; " + buildmytasksCommand + " " + func + " -o=" + func + "_Func.py; cd ../"
            os.system(command_string)
            print("done!")


        ##================================================================================================================================================
        ## create or modify init.py file
        print(" ")


        ## does a init.py file already exsits, if not create new init.py file in .casa directory
        if not(os.path.isfile(HomeDir + "/.casa/init.py")):
            print("Create init.py file in " + HomeDir + "/.casa/ directory ..",)


            ## create init.py file
            InitFile = open(HomeDir + "/.casa/init.py", 'w')
            InitFile.write("__rethrow_casa_exceptions=True\n")
            for func in ListOfFunctionNames:
                newline = "execfile(" + chr(34) + myXCLASSDir + "build_tasks/" + func + "_Func.py" + chr(34) + ")"
                InitFile.write(newline + " \n")
            InitFile.close()
            print("done!")
            print("Now the myXCLASS for CASA interface is available when you start CASA without additional commands!")


        ## if a init.py file already exsits, check if it contains the correct lines
        else:
            print("Check init.py file in " + HomeDir + "/.casa/ directory ..",)


            ## read in whole contents of init.py file
            InitFile = open(HomeDir + "/.casa/init.py")
            contents = InitFile.readlines()
            InitFile.close()


            ## construct help array for line check routine
            FunctionAlreadyAdded = []                                                       ## this list marks an already added execfile-line of a
            for func in ListOfFunctionNames:                                                ## function
                FunctionAlreadyAdded.append(0)


            ## check if lines are correct
            NewContents = []                                                                ## reset new contents of init.py file
            for line in contents:                                                           ## loop over all lines in the init.py file
                AddLineFlag = True                                                          ## flag for add current line to new content
                counterFunc = 0                                                             ## reset counter for functions
                for func in ListOfFunctionNames:                                            ## loop over all functions
                    counterFunc += 1                                                        ## increase counter for functions
                    if (line.find(func) > (-1)):                                            ## check, if current line contains a command for the current
                                                                                            ## function
                        # Debug:
                        # print line.strip()

                        if (FunctionAlreadyAdded[counterFunc - 1] == 0):                    ## check if this lines is not already added to new contents
                            FunctionAlreadyAdded[counterFunc - 1] = 1
                            newline = "execfile(" + chr(34) + myXCLASSDir + "build_tasks/" + func + "_Func.py" + chr(34) + ")\n"
                            NewContents.append(newline)

                            # Debug:
                            # print 'counterFunc = ', counterFunc
                            # print 'func = ', func
                            # print 'FunctionAlreadyAdded = ', FunctionAlreadyAdded
                            # print 'line = ', line.strip()
                            # print 'newline = ', newline.strip()

                        AddLineFlag = False
                        # break

                if (AddLineFlag):
                    NewContents.append(line)


            ## check, if all function calls are added
            if (sum(FunctionAlreadyAdded) != len(FunctionAlreadyAdded)):
                counterFunc = 0                                                             ## reset counter for functions
                for func in ListOfFunctionNames:                                            ## loop over all functions
                    counterFunc += 1                                                        ## increase counter for functions
                    if (FunctionAlreadyAdded[counterFunc - 1] == 0):                        ## check if this lines is not already added to new contents
                        FunctionAlreadyAdded[counterFunc - 1] = 1
                        newline = "execfile(" + chr(34) + myXCLASSDir + "build_tasks/" + func + "_Func.py" + chr(34) + ")\n"
                        NewContents.append(newline)
                

            ## write new contents to file
            InitFile = open(HomeDir + "/.casa/init.py", 'w')
            # InitFile.write("__rethrow_casa_exceptions=True\n")
            for line in NewContents:                                                        ## loop over all new lines in the init.py file
                InitFile.write(line)
            InitFile.close()
            print("done!")


            ## print a message to the screen
            # print "Add lines to init.py file in " + HomeDir + "/.casa/ directory.\n"
            print("Now the XCLASS interface is available whenever you start CASA without additional commands!\n\n")


    ##----------------------------------------------------------------------------------------------------------------------------------------------------
    ## print some comments
    print("\n\nComments:")
    print("---------\n")
    print("\n- In order to simplify the usage of XCLASS without CASA please add the following")
    print("  line to your .bashrc:\n")
    print("\texport XCLASSRootDir=" + myXCLASSDir)
    print("\n\n- To avoid a segmentation fault error message, please unlimit the stack and")
    print("  increase the OpenMP stack size by adding the following lines to your .bashrc:")
    print("\n\tulimit -s unlimited")
    print("\texport KMP_STACKSIZE='4999M'")
    print("\texport OMP_STACKSIZE='4999M'")
    print("\texport GOMP_STACKSIZE='4999M'\n")
    print("  Note, the value '4999M' has to be modified for your system.\n\n")
    print("- Please report all bugs to\n")
    print("\tmoeller@ph1.uni-koeln.de\n\n\n")


##--------------------------------------------------------------------------------------------------------------------------------------------------------
##--------------------------------------------------------------------------------------------------------------------------------------------------------
##--------------------------------------------------------------------------------------------------------------------------------------------------------
