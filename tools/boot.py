import random
import sys
import time

from tools import colors as col


def start_boot():
    print("\033[2J\033[H\033[?25l", end="")

    tasks = ["Loading Kernel..", "Initializing OS..", "Starting MutOS....", "Loading Drivers...", "Settings MutOS...", "Loading TUI", "Loading CKernel..", "Loading Runtime...", "Loading Profile...", "Loading MBF..", "Loading GCC...", "Loading Python...", "Loading MutOS system...", "drivers MutBeep..", "Developer NN..", "Creating Session MP", "Loading MutSH..."]

    for task in tasks:
        progress = 0
        while progress <= 100:
            filled = int(20 * progress // 100)

            bar = f"{col.MAGENTA}{'+' * filled}{col.BLACK}{'+' * (20 - filled)}{col.RESET}"

            print(
                f"\r{col.MAGENTA}●{col.RESET} {task:<25} [{bar}] {progress}%",
                end="",
                flush=True,
            )

            if progress == 100:
                break

            progress += random.randint(45, 65)
            if progress > 100:
                progress = 100

            time.sleep(random.uniform(0.10, 0.15))

        print()

    print(f"\n{col.MAGENTA}${col.RESET} MutOS loaded successfully.\n\033[?25h")

    time.sleep(2)

    sys.stdout.write("\033[2J\033[H")
    sys.stdout.flush()

    return
