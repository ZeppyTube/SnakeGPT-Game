import subprocess

def run_script():
    while True:
        process = subprocess.Popen(['python', 'main_menu.py'], stdout=subprocess.PIPE)
        process.wait()
        if process.returncode != 42:
            break

if __name__ == "__main__":
    run_script()
