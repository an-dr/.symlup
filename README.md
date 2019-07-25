# symlup

Small mutiplatform script for working with symlinks using $HOME/.symlinks.json for register all of them

Format: 
``` json
{
    "group1": {"dst1":"src1", "srcN":"dstN"},
    "groupN": {}
}
```

## Links

* [Main hand-written page](docs/main_page.md)
* [Auto-generated documentation](docs/generated.md)

## Features

* Multiplatform
* Binaries (could add to $Path)
* Duplicates checking
* Every link going through `$HOME/.symlinks.json`, you could manage all of them anytime

## Requirements

* Python 3
* Click python library

## Instalation

Just clone this repo to any folder (e.g $HOME/.symlup)

## Usage

```bash
symlup.py apply [OPTIONS]
  apply all json symlinks
Options:
  -g, --symlink_group TEXT  Symlink group
  --help                    Show this message and exit.


symlup.py json [OPTIONS]
  open json file

Options:
  --help  Show this message and exit.


symlup.py remove [OPTIONS]
  remove symlink

Options:
  -d, --dst TEXT  Destination path  [required]
  --help          Show this message and exit.


symlup.py update [OPTIONS]
  update or add a symlink

Options:
  -g, --symlink_group TEXT  Symlink group  [required]
  -s, --src TEXT            Source path  [required]
  -d, --dst TEXT            Destination path  [required]
  --help                    Show this message and exit.
```

## Json example (based on $HOME/.symlinks.json)

```json
{
    "default": {
        "C:/OneDrive": "C:/Users/dongr/OneDrive",
        "C:/Users/dongr/Documents": "C:/Users/dongr/OneDrive/Documents",
        "C:/Users/dongr/Pictures": "C:/Users/dongr/OneDrive/Pictures",
        "C:/home": "C:/Users/dongr"
    },
    "esp": {
        "C:/msys32": "C:/esp/tools/msys2_esp_pack/20180110",
        "~/esp/esp-idf": "C:/esp/masters/esp-idf",
        "~/esp/openocd-esp32": "C:/esp/tools/openocd/openocd-esp32-win32-0.10.0-esp32-20190708",
        "~/esp/xtensa-esp32-elf": "C:/msys32/opt/xtensa-esp32-elf"
    },
    "python": {
        "C:/Python27/python2.exe": "C:/Python27/python.exe",
        "C:/Python37/python3.exe": "C:/Python37/python.exe",
        "C:/PythonLinks/Python": "C:/Python37"
    }
}
```