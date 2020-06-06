import subprocess
from subprocess import run
import sys


def main():
    cmd = "adb shell pm list packages".split(" ")
    packages = run(cmd, stdout=subprocess.PIPE).stdout.decode(
        'utf-8').split("\n")

    developers = ["jujunjun110", "MESON"]
    target_packages = extract_target_packages(packages, developers)

    print(target_packages)

    for package in target_packages:
        res = run(["adb", "shell", "pm", "path", package],
                  stdout=subprocess.PIPE)
        path = res.stdout.decode(
            'utf-8').replace("package:", "").replace("\n", "")
        res2 = run(["adb", "pull", path, f"./apps/{package}.apk"])
        run(["adb", "uninstall", package])


def extract_target_packages(packages, developers):
    return sum([[p.replace("package:", "") for p in packages if d in p] for d in developers], [])


if __name__ == "__main__":
    main()
