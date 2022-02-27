
import os
import shutil
import subprocess

from Extract_openFoam_Data import Extract_openFoam_Data

#openFoam modules
from PyFoam.Execution.ConvergenceRunner import ConvergenceRunner
from PyFoam.Execution.UtilityRunner import UtilityRunner
from PyFoam.LogAnalysis.BoundingLogAnalyzer import BoundingLogAnalyzer
from PyFoam.RunDictionary.SolutionFile import SolutionFile
from PyFoam.RunDictionary.SolutionDirectory import SolutionDirectory

parent_dir = '../BernardCells_T'
timenamearray = [str(i) for i in range(10, 201, 10)]
filter_size = 64
Para_array = range(320, 1001, 20)



os.chdir('../')
os.system('rm -rf BernardCells_T')
os.chdir('source')

os.chdir('BernardCells')
os.popen('blockMesh > log.blockMesh').read()
os.chdir('../')

parent_dir = '../BernardCells_T'
os.makedirs(parent_dir, exist_ok = True)

for Para in Para_array:
    directory = 'BernardCells_T'+str(Para)
    path = os.path.join(parent_dir, directory)
    try:
        shutil.copytree('BernardCells', path)
    except OSError as error:
        print(error)
    
    solver="buoyantPimpleFoam"
    case=path
    #pCmd="calcPressureDifference"
    #mCmd="calcMassFlow"

    dire=SolutionDirectory(case,archive="TVariation")
    sol=SolutionFile(dire.initialDir(),"T")

    print('floor temperature = ', Para)
    sol.replaceBoundary("floor","%f" %(Para))

    # run=ConvergenceRunner(BoundingLogAnalyzer(),argv=[solver,".",case],silent=True)
    # run.start()

    os.chdir(path)
    #os.system('blockMesh > log.blockMesh &')
    os.system('buoyantPimpleFoam > log.buoyantPimpleFoam &')                      #run each case in parallel
    # list_files = subprocess.run(["buoyantPimpleFoam"], stdout=subprocess.DEVNULL)
    os.chdir('../../source')


############## Assembling training and testing data

# Extract_openFoam_Data(parent_dir, Para_array, timenamearray, filter_size)

