import os
from time import sleep
import pyttsx3

engine = pyttsx3.init()
# engine.setProperty('voice', engine.getProperty('voices')[0].id)
engine.setProperty('voice', engine.getProperty('voices')[1].id)
engine.setProperty('rate', 175)


def main_output(output, prompt_only):
    global voice_disabled
    print(output)
    if voice_disabled == 0 and not prompt_only:
        engine.say(output)
        engine.runAndWait()



def action_change_detect(source, errors):
    main_output("A change detected in File {}.\nError Format : {}".format(os.path.basename(source), str(errors[0])),
                False)
    F_system.database[os.path.abspath(source)].stat_update(source, errors)


def error_file_not_init(source):
    main_output("File [{}] not found in the initialized database. Initializing now...".format(os.path.basename(source)),
                False)
    F_system.file_initialize(source)


def error_file_no_exist(source):
    main_output("File [{}] not found".format(os.path.basename(source)), False)


def error_target_no_exist(target):
    main_output(f"Target {os.path.basename(target)} doesn't exist.", False)


class F_system:
    files = set()
    database = {}

    def __init__(self, source):
        self.source = source
        # self.name = os.path.basename(source) -------------- > currently not needed
        self.size = os.stat(source)[6]
        self.owner = os.stat(source)[4]
        self.l_access = os.stat(source)[7]  # last_access
        main_output("File [{}] has been initialized.".format(os.path.basename(source)), True)

    @classmethod
    def file_initialize(cls, source):
        F_system.files.add(source)
        F_system.database[os.path.abspath(source)] = F_system(source)

    def __eq__(self, other):
        test_dic = {}
        changes = []
        test_dic["source"] = self.source == os.path.abspath(other)
        # test_dic["name"] = self.name == os.path.basename(other)
        test_dic["size"] = self.size == os.stat(other)[6]
        test_dic["owner"] = self.owner == os.stat(other)[4]
        test_dic["l_access"] = self.l_access == os.stat(other)[7]
        for test in test_dic:
            if not test_dic[test]:
                changes.append(test)
        return changes

    def stat_update(self, f, corrections):
        _temp_dic = {"source": os.path.abspath(f), "name": os.path.basename(f), "size": os.stat(f)[6],
                     "owner": os.stat(f)[4], "l_access": os.stat(f)[7]}
        for stat in corrections:
            self.__setattr__(stat, _temp_dic[stat])


observe_loop = 0
target_source = ""
voice_disabled = 0
exit_loop_onError = 0


def tree_profiler(path):
    try:
        os.chdir(path)
    except PermissionError:
        main_output(
            "The current user [{}] doesn't have access to the  Directory [{}]\n".format(os.environ["username"], path),
            False)
        sleep(3)
        return

    for file in os.listdir(path):
        if os.path.isfile(file):
            ## main_output("File found : {}".format(file))
            yield os.path.abspath(file)
        elif os.path.isdir(file):
            ## main_output("--------------------\nDir found : [{}]\n--------------------\n".format(file))
            yield from tree_profiler(os.path.abspath(file))
            os.chdir("..")


def init_database_create(st_location):
    for file in tree_profiler(st_location):
        F_system.file_initialize(str(file))
        # main_output("New File found {}. Initializing".format(os.path.basename(file)), False)
        # sleep(1)


# noinspection PyTypeChecker
def observe_target_file_cycle(target):
    rel_obj = F_system.database[os.path.abspath(target)]
    changes = rel_obj == target
    if len(changes) != 0:
        action_change_detect(target, changes)



def observe_target_dir_cycle(target):
    for file in tree_profiler(target):
        if os.path.isfile(file):
            # Checking if the file is in the database
            if file not in F_system.files:
                error_file_not_init(os.path.abspath(file))
                if exit_loop_onError == 1:
                    return 9
            else:
                observe_target_file_cycle(file)
    return 0


def observe(target_abs):
    # Checking if the dir/file exist
    if not os.path.exists(target_abs):
        error_target_no_exist(target_abs)
        return
    global observe_loop
    observe_loop = 1
    main_output("\n---------------------------------------------------\nObserving File [{}] beginning..."
                "\n---------------------------------------------------".format(os.path.basename(target_abs)), False)

    if os.path.isfile(target_abs):
        # Checking if the file is in the database
        if target_abs not in F_system.files:
            error_file_not_init(target_abs)
            return
        while observe_loop == 1:
            observe_target_file_cycle(target_abs)

    elif os.path.isdir(target_abs):
        while observe_loop == 1:
            s = observe_target_dir_cycle(target_abs)
            if s == 9 & exit_loop_onError == 1:
                break


if __name__ == "__main__":
    # The target folder structure Root
    target_source = ".\\test"
    init_database_create(target_source)
    print("\n-------------------------------------------------------------\n")
    observe(os.path.abspath(target_source))

