import requests
import getpass
import subprocess
from urllib.request import urlretrieve

def update_app():
    url = 'https://github.com/SpencerReno/EntourageApp/raw/main/EntourageDirectors.exe'

    print('File Downloading')

    usrname = getpass.getuser()
    destination = f'C:\\Windows\\Temp\\EntourageApp.exe'

    download = urlretrieve(url, destination)

    print('File downloaded')
    delete_old()


def delete_old():
    try:
        cmd = f'C:\\Program Files (x86)\\EntourageDirectors\\unins000.exe'

        returned_value = subprocess.call(cmd, shell=True)  # returns the exit code in unix
        print('returned value:', returned_value)

        install_new()
    except:
        install_new()
def install_new():
    usrname = getpass.getuser()
    subprocess.Popen(r'C:\Windows\Temp\EntourageApp.exe')

    # cmd = f'C:\\Windows\\Temp EntourageApp.exe'

    # returned_value = subprocess.call(cmd, shell=True)  # returns the exit code in unix
    # print('returned value:', returned_value)


update_app()