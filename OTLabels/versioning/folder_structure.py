"""
"""

import os
import re
import shutil


class FolderStructure:
    """ """

    def __init__(self, path: str, documentation_file_path: str, test: bool = False):
        self.path = path
        self.documentation_file_path = documentation_file_path
        # self.ordered_files = self._read_directory_contents()
        # self._create_json_structure()

        with open(documentation_file_path, "a") as f:
            f.write("START" + "\n")

    # METHODS ACCESSIBLE FROM OUTSIDE --------------------------------------------------

    def create_folders(
        self, alternative_path: None | str = None, test: None | bool = False
    ) -> None:
        """
        copy all data at given path to folder into new folder with name folder_name
        --> apply data structure


        INPUT PARAMETERS
        - alternative_path: set directory where data should be copied to (optional)
        - test: prevent modifications to directory, only output in console

        DATA STRUCTURE
        + YYYY-MM-DD_CameraName
        |_ images
        |_ labels
        |_ pre-annotations
        |_ unkown

        + _error_files
        |_ images
        |_ labels
        |_ pre-annotations
        |_ unkown

        """

        for date, camera, dirpath, file in self._get_DATExCAMERA():
            # set original file path
            original_file = os.path.join(dirpath, file)

            if alternative_path is None:
                # go back one folder
                alternative_path = os.path.abspath(os.path.join(self.path, ".."))

            if (os.path.exists(alternative_path) is False) and (test is False):
                os.makedirs(alternative_path)
                print(alternative_path, "created")

            if date == "error" and camera == "error":
                # error folder name
                new_folder_name = "_error_files"

            else:
                # new folder name
                new_folder_name = date + "_" + camera

            new_folder_path = os.path.join(alternative_path, new_folder_name)

            # --------------------

            # determine subfolder for file
            file_extension = os.path.splitext(file)[1]

            if file_extension in [".jpg", ".jpeg", ".png"] is True:
                # if picture, move to folder "images"
                subfolder_name = "images"

            elif (file_extension in [".txt"] is True) and (file[:6].isdigit() is True):
                # if file name starts with 6 digits, move to folder "labels"
                subfolder_name = "labels"

            elif (file_extension in [".txt"] is True) and (file[:6].isdigit() is False):
                # if file name doesn't start with 6 digits, move to folder
                # "pre-annotations"
                subfolder_name = "pre-annotations"

            else:
                subfolder_name = "unknown"

            # cut beginning digits if labels already created
            file = self._remove_filename_first_digits(file)
            # --------------------

            # create directory with new folder if doesn't exist yet
            if (os.path.exists(new_folder_path) is False) and (test is False):
                os.makedirs(new_folder_path)
                print(new_folder_path, "created")

            # create directory with new subfolder if doesn't exist yet
            new_subfolder_path = os.path.join(new_folder_path, subfolder_name)

            if (os.path.exists(new_subfolder_path) is False) and (test is False):
                os.makedirs(new_subfolder_path)
                print(new_subfolder_path, "created")

            copy_file = os.path.join(new_subfolder_path, file)

            try:
                if (os.path.exists(copy_file) is False) and (test is False):
                    print("file copied from", original_file, "to", copy_file)
                    with open(self.documentation_file_path, "a") as f:
                        f.write(
                            "create_folders ----- "
                            + "file copied from "
                            + original_file
                            + " to "
                            + copy_file
                            + "\n"
                        )
                    shutil.copy(original_file, copy_file)
                else:
                    with open(self.documentation_file_path, "a") as f:
                        f.write(
                            "create_folders ----- file already existent at "
                            + copy_file
                            + "\n"
                        )
                    print("file already existent at", copy_file)

            except UnboundLocalError:
                print("fehler", date, camera, original_file)
                with open(self.documentation_file_path, "a") as f:
                    f.write(
                        "create_folders ----- fehler "
                        + date
                        + " "
                        + camera
                        + " "
                        + original_file
                        + "\n"
                    )

    def show_folder_combinations(self) -> list:
        """
        Returns a summary of all folders that are about to be created
        for files at the folder given in class initialization
        """

        return self._get_DATExCAMERA()

    # METHODS NOT ACCESSIBLE FROM OUTSIDE --------------------------------------

    def _get_DATExCAMERA(self) -> list:
        """
        For a given path to folder, returns Date and Camera in list

        if file name doesn't fit the standard pattern, assign it to error folder

        --------
        RETURN array in format
        [[Datum1, Cam1, Pfad1, Dateiname1] ... ]
        ['2023-10-25', 'otcamera-tud03', '/Volumes/platomo data/Produkte/
        OpenTrafficCam/OTLabels/Training/Daten/_temp-OP2019'
        ,'otcamera-tud03_FR20_2023-10-25_08-15-00.mp4_00_01_552023-11-02-16h27m16s309.txt']
        """

        date_camera_list = []

        print("load files...")
        with open(self.documentation_file_path, "a") as f:
            f.write("load files..." + r"\n")

        for dirpath, dirnames, filenames in os.walk(self.path):
            for file in filenames:
                try:
                    date = self._get_DATE(file)
                    camera = self._get_CAMERA(file)
                    date_camera_list.extend([[date, camera, dirpath, file]])
                except UnboundLocalError:
                    # print('Cannot detect [date, camera] for', file)
                    date_camera_list.extend([["error", "error", dirpath, file]])

        print("Data loaded")
        with open(self.documentation_file_path, "a") as f:
            f.write("Data loaded" + "\n")
        # if filter_duplicates == True:
        #    date_camera_list = np.unique(date_camera_list, axis=0)

        return date_camera_list

    def _get_DATE(self, file_name: str, position: int = 0) -> str:
        """
        For a given file_name, returns date YYYY-MM-DD or YYYY-DD-MM at
          occurence position x
        --> default, first occurrence

        """
        date_pattern = r"\d{4}[/-]\d{2}[/-]\d{2}"

        dates = re.findall(date_pattern, file_name)

        try:
            date = dates[position]

        except IndexError:
            pass

        return date

    def _get_CAMERA(self, file_name: str) -> str:
        """
        For a given file_name, returns CAMERA name
        --> Assumption: two options
            [1] Camera name located before Date
            [2] Camera name located before Frame Rate (FRxx)
        """

        file_name_sep = file_name.split(sep="_")

        index_at_date = file_name_sep.index(self._get_DATE(file_name))

        index_before_date = index_at_date - 1

        # check assumptions
        framerate_pattern = re.compile(r"[F][R]\d*")

        if framerate_pattern.match(file_name_sep[index_before_date]) is None:
            # assumption 1: camera name located before date

            camera_name = file_name_sep[index_before_date]

        else:
            # assumption 2: camera name located after frame rate
            camera_name = file_name_sep[index_before_date - 1]

        return camera_name

    def _remove_filename_first_digits(self, file_name) -> str:
        """
        from filename like "000000_OTCamera03_FR20_..." remove "000000_" if exists

        RETURN new file_name
        """

        pattern = r"\d{6}[/_]"

        #  Will return all the strings that are matched

        try:
            print(re.findall(pattern, file_name[:7])[0], "removed from", file_name)
            with open(self.documentation_file_path, "a") as f:
                f.write(
                    "_remove_filename_first_digits ----- "
                    + re.findall(pattern, file_name[:7])[0]
                    + " removed from "
                    + file_name
                    + r"\n"
                )
            return file_name[7:]

        except IndexError:
            return file_name
