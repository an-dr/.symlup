import os
import time
import pathlib
import click
from pyclass_json import Json

HOME = pathlib.Path("~").expanduser()
FIRST_CHAR_OK = "    (ok) "
FIRST_CHAR_INFO = "    (!) "
SYMLINK_LIST_FILENAME = ".symlinks.json"
SYMLINK_LIST_FILE_DEFAULT = """\
{
    \"default\": 
    {
        \"C:/home\": \"%s\"
    }
}
""" % str(HOME).replace("\\", "/")

syml_file = HOME.joinpath(SYMLINK_LIST_FILENAME)
syml_json = Json()


class SymlUp:
    def __init__(self):
        self.file = HOME.joinpath(SYMLINK_LIST_FILENAME)
        self.json = None  # type: Json()
        self.read = False
        try:
            self._read()
        except FileNotFoundError:
            self._init()

    def _read(self):
        try:
            with open(self.file) as f:
                self.json = Json(f)
            self.read = True
        except Exception as e:
            raise e

    def _write(self):
        self._is_read()
        with open(self.file, "w") as f:
            f.write(self.json.to_str_formated())
        self.read = True

    def _is_dst_duplicates(self, group2add, dst):
        for group, links in self.json.items():
            if group != group2add:  # interesting only in other groups
                # check that group:
                for link_dst, link_src in links.items():
                    if link_dst == dst:
                        raise Exception(FIRST_CHAR_INFO + "That destination (%s) is already using in other group: \n"
                                                          "%s: %s -> %s" % (link_dst, group, link_src, link_dst))

    def _is_read(self):
        if not self.read:
            raise IOError(FIRST_CHAR_INFO + ".symlinks.json is not read")
        else:
            return True

    def _remove(self, group, symlink):
        try:
            self.json[group].pop(symlink)
            pathlib.Path(symlink).unlink()
        except KeyError:
            print(FIRST_CHAR_INFO + "Nothing to delete")
        except Exception as e:
            print(e)

    @staticmethod
    def _is_src_exist(src):
        if not pathlib.Path(src).exists():
            raise NotADirectoryError(
                FIRST_CHAR_INFO + "Source %s is not exists" % src)

    @staticmethod
    def _is_dst_file_or_dir(dst):
        if (not dst.is_symlink) and (dst.is_file() or dst.is_dir()):
            print(FIRST_CHAR_INFO + "Destination %s is a file or dir" % dst)
            return

    @staticmethod
    def symlink(src_path, dst_path, quiet=False):
        src_path = str(src_path).replace("~", str(HOME)).strip()
        dst_path = str(dst_path).replace("~", str(HOME)).strip()
        src = pathlib.Path(src_path)
        dst = pathlib.Path(dst_path)
        SymlUp._is_src_exist(src)
        SymlUp._is_dst_file_or_dir(dst)
        if dst.is_symlink():
            dst.unlink()
        os.symlink(src, dst)
        if not quiet:
            print(FIRST_CHAR_OK + "Set %s -> %s" % (src, dst))

    def _init(self):
        self.json = Json(SYMLINK_LIST_FILE_DEFAULT)
        self.read = True
        self._write()
        print(FIRST_CHAR_OK + "%s was created in %s:\n %s" %
              (SYMLINK_LIST_FILENAME, HOME, SYMLINK_LIST_FILE_DEFAULT))

    def upd_link(self, symlink_group, src, dst):
        try:
            self._is_read()
            self._is_dst_duplicates(symlink_group, dst)
            SymlUp._is_src_exist(src)
            if not (symlink_group in self.json.keys()):
                self.json.update({symlink_group: {dst: src}})
            else:
                self.json[symlink_group].update({dst: src})
            self._write()
            self._apply_jsongroup(symlink_group, quiet=True)
            print(FIRST_CHAR_OK + "Set %s -> %s" % (src, dst))
        except Exception as e:
            print(e)

    def remove_link(self, dst):
        for group in self.json.keys():
            if dst in self.json[group].keys():
                self._remove(group, dst)
                self._write()
                print(FIRST_CHAR_OK + "Removed: %s" % dst)
                return
        print(FIRST_CHAR_INFO + "There is no that symlink")

    def _apply_jsongroup(self, symlink_group, quiet=False):
        self._is_read()
        g = self.json[symlink_group]  # type: dict
        for dst, src in g.items():
            try:
                self.symlink(src, dst, quiet)
            except Exception as e:
                print(e)

    def apply(self, symlink_group=None):
        self._is_read()
        if symlink_group:
            self._apply_jsongroup(symlink_group)
        else:
            for group in self.json.keys():
                self._apply_jsongroup(group)

    def print(self, group=None):
        if group is None:
            self.json.print()
        else:
            print("Group '%s':" % group)
            g = Json(self.json.get(group))
            g.print()


@click.group()
def cli():
    pass


@cli.command()
@click.option("--symlink_group", "-g", type=str, default=None, required=False, help='Symlink group')


def apply(symlink_group=None):
    """apply current .symlink.json content"""
    SymlUp().apply(symlink_group)


@cli.command()
@click.option("--symlink_group", "-g", type=str, default=None, required=False, help='Symlink group')


def list(symlink_group=None):
    """
print current .symlink.json content
"""
    SymlUp().print(symlink_group)


@cli.command()
def json():
    """
    open json file
    """
    os.system("start " + str(syml_file))


@cli.command()
@click.option("--dst", "-d", prompt='Destination path', type=str, default=None, required=True,
              help='Destination path')
def remove(dst):
    """
    remove entry
    """
    SymlUp().remove_link(dst)


@cli.command()
@click.option("--symlink_group", "-g", prompt='Input group name', type=str, default=None, required=True,
              help='Symlink group')
@click.option("--src", "-s", prompt='Source path', type=str, default=None, required=True, help='Source path')
@click.option("--dst", "-d", prompt='Destination path', type=str, default=None, required=True,
              help='Destination path')
def update(symlink_group, src, dst):
    """add or change symlink"""
    SymlUp().upd_link(symlink_group, src, dst)


if __name__ == "__main__":
    cli()

    # SymlUp().print("python")

    # obj.init()
    # obj.apply_json()
    # SymlUp().upd_link("esp", "C:\\esp\\tools\\openocd-esp32", "~\\esp\\openocd-esp32")
    # obj.remove_link("C:/msys33")
    # with open()
    # os.symlink("C:/", "C:/Users/dongr/c")
    # print("Done!")
    # time.sleep(5)
