import subprocess
import os,sys
import random,re
# Input data to be provided to script.py

os.system('cls')

for i in ["1.) check expected testcase", "2.) just get result"]:
    print(i)
mode = int(input('Which one do you want to use?: ')) - 1
exit() if not(mode in [i for i in range(2)]) else ""

def filegetter() -> str:
    counter = 0
    filelist = []
    for path, subdirs, files in os.walk(os.getcwd()):
        for name in files:
            if ".py" in name[-3:] and not(name in __file__):
                print(f'{counter + 1}.) ',end="")
                print(os.path.join(path, name))
                filelist.append(os.path.join(path, name))
                counter += 1
        # exit()
    pyfile = int(input("Select which file you want to test: "))
    if pyfile > len(filelist) or pyfile <= 0:
        os.system('cls')
        print("Index out of range")
        exit()
    pyfile = filelist[pyfile - 1]
    os.system('cls')
    return pyfile
def testcasechk(pyfile=""):
    counter = 0
    os.system('cls')
    filelist = []
    if pyfile == "":
        pyfile = filegetter()
    os.system('cls')
    print(f'======= {os.path.basename(pyfile)} =======')
    testcase = int(input("How much testcase you wanna test?: "))
    testcaseinput = []
    expected = [] if mode == 0 else False
    for i in range(testcase):
        os.system('cls')
        print("====================== Input Session ======================")
        print(f'Testcase #{i+1}:')
        print("When you want to end this testcase input, type '<<END>>' to input field.")
        print("If you want to random integer in [x,y], used <<!randint(x,y)>> or <<!randfloat(x,y).zf>> for random float with z decimal point")
        inp = []
        while True:
            a = input("Input here:")
            if a == "<<END>>":
                testcaseinput.append(inp)
                break
            if "<<!randint(" in a and ")>>" in a:
                b = re.match(r"<<!randint\((\d+),(\d+)\)>>",a)
                inp.append(random.randint(int(b.group(1)), int(b.group(2))))
                continue
            elif "<<!randfloat(" in a and "f>>" in a:
                b = re.match(r"<<!rand\((\d+(?:\.\d+)?),(\d+(?:\.\d+)?)\)(?:\.(\d+)?[if]+)>>", a)
                import math
                inp.append(math.floor(random.uniform(float(b.group(1)),float(re.group(2))),int(b.group(3)) if b.group(3) else 18))
                continue
            inp.append(a)
        if mode == 0:
            os.system('cls')
            print("====================== Expected Output Session ======================")
            print(f'Testcase #{i+1}:')
            print("When you want to end this testcase input, type '<<END>>' to input field.")
            exp = []
            while True:
                a = input("Expected output here:")
                if a == "<<END>>":
                    expected.append(exp)
                    break
                exp.append(a)
    testcaseoutput = []
    import time
    for i in range(testcase):
        starttime = time.time()
        process = subprocess.Popen(['python', pyfile], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Pass input to the subprocess line by line
        for l in testcaseinput[i]:
            input_line_bytes = str(l).encode('utf-8')
            process.stdin.write(input_line_bytes)
            process.stdin.write(b'\n')
            process.stdin.flush()

        # Close the stdin to signal that all input has been provided
        process.stdin.close()

        # Capture the output
        output_bytes, error_bytes = process.communicate()
        endtime = time.time()
        exectime = endtime - starttime
        # Decode the output from bytes to string
        output_str = output_bytes.decode('utf-8')
        error_str = error_bytes.decode('utf-8')

        # Split the output into lines
        output_lines = output_str.splitlines()

        # Print each line of output
        otp = {'output':[], 'error': "",'executetime': exectime}
        if len(output_lines) != 0:
            for line in output_lines:
                otp["output"].append(line)
        else:
            otp["output"] == ""
        otp["error"] = "-" if error_str == "" else error_str
        testcaseoutput.append(otp)

    os.system('cls')
    for i in range(testcase):
        print("============================")
        print(f'Testcase #{i+1}')
        print('-Input-')
        for j in testcaseinput[i]:
            print(j)
        if mode == 1:
            print('-Output-')
            for j in testcaseoutput[i]["output"]:
                print(j)
            print("-Error-")
            print(testcaseoutput[i]["error"])
        else:
            correct = True
            print("-Testcase checked-")
            try:
                for j in range(max(len(expected[i]), len(testcaseoutput[i]['output']))):
                    if expected[i][j] != testcaseoutput[i]['output'][j]:
                        correct = False
                        break
            except:
                correct = False
            print("Result:", ("✅" if correct else "❌"))
            
        print("-Execution Time-")
        print(testcaseoutput[i]["executetime"], 'seconds')
        print("============================")
    input("Press the Enter key to exit: ") 

def testcasecheckercreator(pyfile=""):
    '''s'''
    os.system('cls')
    if pyfile == "":
        pyfile = filegetter()
    if os.path.exists(f'{os.path.splitext(os.path.basename(pyfile))[0]}_testcase_checker') == False:
        os.makedirs(f'{os.path.splitext(os.path.basename(pyfile))[0]}_testcase_checker')
    curpath = os.path.join(os.path.split(pyfile)[0],f'{os.path.splitext(os.path.basename(pyfile))[0]}_testcase_checker')
    os.system(f'copy {pyfile} {os.path.join(curpath,os.path.basename(pyfile))}')
if len(sys.argv) != 1:
    for i in sys.argv[1:]:
        if mode == 2:
            testcasecheckercreator(i)
        else:
            testcasechk(i)
else:
    testcasechk() if mode != 2 else testcasecheckercreator()