# python 3
import os  # to get files names from a directory
import sys  # for python script arguments

def find_imports(file_name, path_files="./", verbose=True):
    """Find imported lib from a .go file"""
    result = []
    with open(path_files+file_name) as fp:              # open file
        read_in_next_line = False
        for line in fp:
            if read_in_next_line:                       # "import (" was detected, read until ")"
                if ")\n" in line:                       # ")" end of import
                    read_in_next_line = False
                if read_in_next_line:
                    sub_details = line.split("\"")      # split on "
                    if verbose:
                        print("//",sub_details[1], " in ", file_name)
                    result.append(sub_details[1])
            details = line.split(" ")
            if "import" in details:                     # look for "import" or "import ("
                if "(\n" in details:
                    read_in_next_line = True
                else:
                    sub_details = details[1].split("\"")
                    if verbose:
                        print("//",sub_details[1], "in", file_name)
                    result.append(sub_details[1])
    return result

def find_all_imports(files_names, path_files="./", verbose=True):
    """List of imported lib from a list of files names"""
    result = []
    for name in files_names:
        if ".go" in name:
            result.extend(find_imports(name, path_files=path_files, verbose=verbose))
    return list(set(result))

def file_with_main(files_names, path_files="./"):
    """ Detect file with "func main()" """
    for name in files_names:                     # for each file name
        with open(path_files+name) as fp:        # open file
            for line in fp:
                if "main()" in line:             # if line contains "main()"
                    return name
    print("//main() was not found")
    return ""

def extract_lines_no_imports(file):
    """ Extract lines from a file, except imports and package"""
    skip_next = False
    lines = []
    for line in file:
        if skip_next:                  # skip the imports
            skip_next = line != ")\n"
        else:
            details = line.split(" ")
            if "package" in details:   # skip package declaration
                pass
            elif "import" in details:
                if "(\n" in details:   # if imports are declared all together - skip until ")"
                    skip_next = True
                else:                  # if "import "stuff"" skip
                    pass
            else:
                lines.append(line)
    return lines

def glue_in_one_list(files, imports, file_main, path_files):
    """ Create a list with every lines contained in the files"""
    blob = []
    blob.append("package main")                # package main
    blob.append("")
    if len(imports) > 0:                       # imports if any
        blob.append("import (")
        for impopo in imports:
            blob.append("\""+impopo+"\"")
        blob.append(")")

    for i in range(len(blob)):  # add "\n" to package & imports
        blob[i] += "\n"

    [blob.append(line) for line in extract_lines_no_imports(open(path_files+file_main))]  # file with main() goes first (arbitrary choice)
    for name in files:
        [blob.append(line) for line in extract_lines_no_imports(open(path_files+name)) if name != file_main]  # the other files

    return blob

def list_to_file(lines, path_output="./", file_output="defaultName.go"):
    """ Write a list to a file"""
    f = open(path_output+file_output,'w+')
    [f.write(line) for line in lines]
    f.close()

def go_files_list(path):
    """ List go files in a directory"""
    files = []
    for (dirpath, dirnames, filenames) in os.walk(path):
        files.extend(filenames)
    return [name for name in files if ".go" in name]

if __name__ == '__main__':
    if len(sys.argv) == 3:
        path_to_files = sys.argv[0]
        path_output = sys.argv[1]
        file_output = sys.argv[2]
    else:
        path_to_files = "../CVS3/"
        path_output = "../"
        file_output = "cvs3_blob.go"
    print("//path_to_files:", path_to_files)
    print("//path_output:  ", path_output)
    print("//file_output:  ", file_output)
    print("")

    files = go_files_list(path_to_files)
    imports = find_all_imports(files, path_files=path_to_files, verbose=False)
    #print("//imports:", imports)
    file_main = file_with_main(files, path_files=path_to_files)
    #print("//main() in:", file_main)
    all_lines = glue_in_one_list(files, imports=imports, file_main=file_main, path_files=path_to_files)
    list_to_file(all_lines, file_output=file_output)

    [print(line) for line in all_lines]
# myscript.py | xsel -b
