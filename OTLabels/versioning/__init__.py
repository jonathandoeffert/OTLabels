"""
Description
"""

from versioning.folder_structure import FolderStructure

if __name__ == "__main__":
    path = r"/Volumes/platomo data/Produkte/OpenTrafficCam/OTLabels/Training/Daten"
    directory_path = path + r"/_temp-OP2019"
    new_directory_path = path + r"/_temp-test-storage"

    documentation_file_path = (
        r"/home/jonathandoeffert/OTLabels/OTLabels/versioning/documentation.txt"
    )

    fs = FolderStructure(directory_path, documentation_file_path)

    # print(fs.show_folder_combinations())
    fs.create_folders(alternative_path=new_directory_path, test=False)

    print("finish")

    # get list of directories

    # get list of unique combinations DATUM x CAMERA
    # each combination DATUM x CAMERA
    #   CREATE folder and subfolders "images", "pre-anotations" and "labels"
    #   COPY images (and remove 6 digits in the start) -> remove Duplikate
    #   COPY pre-annotations
    #   COPY labels (and remove 6 digits in the start)

    """
        for file_name in return_directory_contents(directory_path):
            create_json_structure(file_name, json_file)
    """

"""    # Get the list of all files and directories
    dir_list = os.listdir(directory_path)
    print("Files and directories in '", directory_path, "' :")
    # prints all files
    print(dir_list)"""
