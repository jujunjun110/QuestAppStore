import subprocess
from subprocess import run
import sys


def main():
    run(["mkdir -p apps".split(" ")])
    cmd = "adb shell pm list packages".split(" ")
    packages = run(cmd, stdout=subprocess.PIPE).stdout.decode("utf-8").split("\n")

    developers = ["jujunjun110", "MESON", "DefaultCompany", "Hancho"]
    target_packages = extract_target_packages(packages, developers)
    print(target_packages)

    for package in target_packages:
        pull_package(package)
        uninstall_package(package)


def extract_target_packages(packages, developers):
    return sum([[p.replace("package:", "") for p in packages if d in p] for d in developers], [])


def pull_package(package):
    res = run(["adb", "shell", "pm", "path", package], stdout=subprocess.PIPE)
    path = res.stdout.decode("utf-8").replace("package:", "").replace("\n", "")
    run(["adb", "pull", path, f"./apps/{package}.apk"])


def uninstall_package(package):
    run(["adb", "uninstall", package])


if __name__ == "__main__":
    main()
