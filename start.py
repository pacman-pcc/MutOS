import os
import readline
import shutil
import signal
import subprocess
import sys

import psutil

from help import help as hl
from tools import boot
from tools import colors as col
from tools import mutfetch as mf

path = os.getcwd()
old_path = None

# ------------------------[SETTINGS]-----------------------------------------
mbfi_path = "/mnt/games/MutOS/mbf/./mbfi" # Interpretator MBF
games_folder_path = "/mnt/games/MutOS/games/" # Games directory
drivers_folder_path = "/mnt/games/MutOS/drivers/" # Mini-Drivers directory
editor = "Micro" # Editor (Vim, Nano, Micro)
# ---------------------------------------------------------------------------

def clear_console(): # Clear console
    sys.stdout.write("\033[3J\033[H\033[2J")
    sys.stdout.flush()


def ignore_ctrl_c(signum, frame): # Anti CTRL+C
    pass


signal.signal(signal.SIGINT, ignore_ctrl_c)


def editor_mut():
    editor_file = input("Enter edit file > ")
    try:    
        if editor == "Nano":
            subprocess.run(["nano", editor_file])
        elif editor == "Vim":
            subprocess.run(["vim", editor_file])
        elif editor == "Micro":
            subprocess.run(["micro", editor_file])
        else:
            print(col.RED + "MUT: Not found text editor." + col.RESET)
    except Exception as e:
        print(col.RED + f"MUT: Error: {e}" + col.RESET)

def ls_command(): # LS
    try:
        items = os.listdir(".")

        items.sort(key=lambda x: (not os.path.isdir(x), x.lower()))

        if not items:
            return

        output_parts = []
        for item in items:
            if os.path.isdir(item):
                output_parts.append(f"{col.MAGENTA}{item}/{col.RESET}")
            else:
                if item.endswith(".mbf"):
                    output_parts.append(f"{col.GREEN}{item}{col.RESET}")
                else:
                    output_parts.append(f"{col.WHITE}{item}{col.RESET}")

        print("   " + "  ".join(output_parts))
    except Exception as e:
        print(f"{col.RED}MUT: Error: {e}{col.RESET}")

def start_notify():
    subprocess.run([drivers_folder_path + "./notify"])


def games_start():
    list_games = """
    > ++ LIST GAMES ++ <<

    1 | Snake = sn
    2 | Cube 3D = c3d (CTRL+C exit)
    """
    print(list_games)
    games_choice = input("Enter choice number/name > ")
    try:
        if games_choice == "sn" or games_choice == "1":
            subprocess.run([f"{games_folder_path}" + "./snake"])
        elif games_choice == "c3d" or games_choice == "2":
            subprocess.run([f"{games_folder_path}" + "./cube"])
        else:
            print(col.RED + f"MUT: Game {games_choice} not found." + col.RESET)
    except Exception as e:
        print(col.RED + f"MUT: Error: {e}" + col.RESET)


boot.start_boot()
start_notify()

clear_console()


def main():
    global path
    while True:
        print(f"{path}")
        input_commands = input(col.MAGENTA + "    / " + col.RESET).strip()

        if input_commands == "> ++":
            try:
                global old_path

                cd_change = input("Directory > ")

                current_before_change = os.getcwd()

                if not cd_change:
                    os.chdir(os.path.expanduser("~"))
                    path = os.getcwd()
                    old_path = current_before_change
                elif cd_change == "<":
                    if old_path is None:
                        print(col.RED + "MUT: None old path" + col.RESET)
                    else:
                        try:
                            os.chdir(old_path)
                            path = os.getcwd()
                            current_before_change = os.getcwd()
                            old_path = current_before_change
                        except Exception as e:
                            print(col.RED + f"MUT: Error: {e}" + col.RESET)
                else:
                    os.chdir(cd_change)
                    path = os.getcwd()
                    old_path = current_before_change
                    print(col.GREEN + "Sucessfully change directory." + col.RESET)
            except Exception as e:
                print(col.RED + f"MUT: Error {e}" + col.RESET)
        elif input_commands == "fm +":
            mf.mutfetch()
        elif input_commands == "cl":
            clear_console()
        elif input_commands == "mbfi":
            args_mbfi = input("File > ").split()
            try:
                subprocess.run(["./mbfi"] + args_mbfi)
            except Exception as e:
                print(col.RED + f"MUT: Error: {e}" + col.RESET)

        elif input_commands == "><":
            ls_command()
        elif input_commands == "gl":
            games_start()
        elif input_commands == "ex":
            exit()

        elif input_commands == "md +":
            md_choice_one = input("Enter name dir > ").strip()
            try:
                os.mkdir(md_choice_one)
                print(col.GREEN + f"Folder {md_choice_one} created." + col.RESET)
            except Exception as e:
                print(col.RED + f"MUT: Error: {e}" + col.RESET)
        elif input_commands == "md ++":
            md_choice_two = input("Enter name dirs > ").strip()
            try:
                os.makedirs(md_choice_two)
                print(col.GREEN + f"Directory {md_choice_two} created.")
            except Exception as e:
                print(col.RED + f"MUT: Error: {e}" + col.RESET)

        elif input_commands == "terminate":
            file_terminated = input("File in directory > ").strip()

            try:
                if os.path.isfile(file_terminated):
                    os.remove(file_terminated)
                    print(f"{col.RED}File {file_terminated} terminated. {col.RESET}")
                elif os.path.isdir(file_terminated):
                    shutil.rmtree(file_terminated)
                    print(f"{col.RED}Dir {file_terminated} terminated. {col.RESET}")
                else:
                    print(f"{col.RED}MUT: File not found. {col.RESET}")
            except Exception as e:
                print(col.RED + f"MUT: Error: {e}" + col.RESET)
        elif input_commands == ">>>":
            file_read = input("Reading file > ").strip()
            try:
                with open(file_read, "r", encoding="utf-8") as f:
                    content = f.read()
                    print(
                        col.MAGENTA
                        + f"Contents in {file_read}\n{content}"
                        + col.RESET
                    )
            except Exception as e:
                print(col.RED + f"MUT: Error: {e}")
        elif input_commands == "mv >":
            old_Path_mv = input("Old path move > ").strip()
            new_Path_mv = input("New path move > ").strip()
            try:
                shutil.move(old_Path_mv, new_Path_mv)
                print(
                    col.GREEN + f"Moved of {old_Path_mv} to {new_Path_mv}." + col.RESET
                )
            except Exception as e:
                print(col.RED + f"MUT: Error: {e}")
        elif input_commands == "!?":
            old_name = input("Old name > ").strip()
            new_name = input("New name > ").strip()
            try:
                os.rename(old_name, new_name)
                print(col.RED + f"Renamed of {old_name} to {new_name}." + col.RESET)
            except Exception as e:
                print(col.RED + f"MUT: Error: {e}")

        elif input_commands == "pl":
            try:
                for proc in psutil.process_iter(
                    ["pid", "name", "cpu_percent", "memory_info"]
                ):
                    print(
                        col.MAGENTA
                        + f"PID: {proc.info['pid']}, Name: {proc.info['name']}, CPU%: {proc.info['cpu_percent']}%, Memory: {proc.info['memory_info'].rss / (1024 * 1024):.2f} MB"
                        + col.RESET
                    )
            except Exception as e:
                print(col.RED + f"MUT: Error: {e}")
        elif input_commands == "del":
            kill_input = input("Enter PID or process name > ").strip()
            try:
                if kill_input.isdigit():
                    pid = int(kill_input)
                    proc = psutil.Process(pid)
                    proc.terminate()
                else:
                    found = False
                    for proc in psutil.process_iter(["pid", "name"]):
                        if proc.info["name"].lower() == kill_input.lower():
                            proc.terminate()
                            print(
                                col.GREEN
                                + f"Process '{kill_input}' with PID {proc.info['pid']} terminated."
                                + col.RESET
                            )
                            found = True
                    if not found:
                        print(
                            col.RED + f"Process '{kill_input}' not found." + col.RESET
                        )
            except Exception as e:
                print(col.RED + f"MUT: Error: {e}")

        elif input_commands == "sap":
            goto_input = input("File/folder > ").strip()
            found_files = False
            try:
                for root, dirs, files in os.walk("."):
                    for d in dirs:
                        if d.lower() == goto_input.lower():
                            print(
                                col.MAGENTA
                                + f"Found files -> {os.path.join(root, d)}"
                                + col.RESET
                            )
                            found_files = True
                    for f in files:
                        if f.lower() == goto_input.lower():
                            print(
                                col.MAGENTA
                                + f"Found files: {os.path.join(root, f)}"
                                + col.RESET
                            )
                            found_files = True
                if not found_files:
                    print(col.RED + f"{goto_input} not found." + col.RESET)
            except Exception as e:
                print(col.RED + f"MUT: Error: {e}")

        elif input_commands == "hl":
            list_help = """
            [1] -> System
            [2] -> Others
            """
            print(list_help)
            help_change = input("Change help menu > ")
            try:
                if help_change == "1":
                    hl.help_systeming()
                elif help_change == "2":
                    hl.others()
                else:
                    print(col.RED + "Help menu not found" + col.RESET)
            except Exception as e:
                print(col.RED + f"MUT: Error: {e}")

        elif input_commands == "+++":
            file_new_input = input("Enter name file > ")

            try:
                open(file_new_input, 'a').close()
            except Exception as e:
                print(col.RED + f"Mut: Error: {e}")
        elif input_commands == "editor":
            editor_mut()
        elif input_commands == "python":
            file_python = input("Enter file python > ")

            try:
                subprocess.run(["python", file_python])
            except Exception as e:
                print(col.RED + f"MUT: Error: {e}" + col.RESET)
        elif input_commands.startswith("gcc"):
            gcc_lists = input_commands.split()
        
            subprocess.run(gcc_lists)


        elif "enjoy" in input_commands:
            file_enjoy = input_commands.replace("enjoy", "", 1).strip()

            if file_enjoy.startswith("./") and os.path.exists(file_enjoy):
                os.system(file_enjoy)
            else:
                full_path_enjoy = os.path.abspath(file_enjoy)

                if os.path.exists(full_path_enjoy):
                    os.system(full_path_enjoy)
                else:
                    print(file_enjoy)
        else:
            print(col.RED + "MUT: Error : command not found." + col.RESET)


if __name__ == "__main__":
    main()
