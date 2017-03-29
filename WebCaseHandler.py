import os, glob
import timeit
import ProjectAERIS

cwd = os.getcwd()

inputPath = cwd + '/uploads'

outputPath = cwd + '/WebPostProcessing'

configFilePath = cwd + '/uploads'

def main():
    # count = 0
    for jsonfile in glob.glob(os.path.join(configFilePath, '*.json')):
        WebconfigFilePath = jsonfile
    for filename in glob.glob(os.path.join(inputPath, '*.txt')):
        lastFolderIdx = filename.rfind(r'/')
        outputFileName = filename[lastFolderIdx + 1:-4]
        print 'outputFileName', outputPath + r'/' + outputFileName + '.xml'
        print 'filename: ', filename, 'outputpath: ', outputPath + r'/' + outputFileName + '_Intermediate.xml', 'configpath: ', WebconfigFilePath
        ProjectAERIS.main(filename, outputPath + r'/' + outputFileName + '_Intermediate.xml', WebconfigFilePath)


if __name__ == '__main__':
    main()
