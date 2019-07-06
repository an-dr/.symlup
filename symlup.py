import os
import time
import pathlib
from pyclass_json import Json

SYMLINK_LIST_FILENAME = ".symlinks.json"
SYMLINK_LIST_FILE_DEFAULT = """\
{
    "default": 
    {
        "C:/home":"C:/Users/dongr"
    }
}
"""
HOME = pathlib.Path("~").expanduser()

syml_file = HOME.joinpath(SYMLINK_LIST_FILENAME)
syml_json = Json()


class SymlUp:
    def __init__(self):
        self.file = HOME.joinpath(SYMLINK_LIST_FILENAME)
        self.json = None  # type: Json()
        self.read = False

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
                        raise Exception("That destination (%s) is already using in other group: \n"
                                        "%s: %s -> %s" % (link_dst, group, link_src, link_dst))

    def _is_read(self):
        if not self.read:
            raise IOError(".symlinks.json is not read")
        else:
            return True

    def _remove(self, group, symlink):
        try:
            self.json[group].pop(symlink)
            pathlib.Path(symlink).unlink()
        except KeyError:
            print("Nothing to delete")
        except Exception as e:
            print(e)

    @staticmethod
    def _is_src_exist(src):
        if not pathlib.Path(src).exists():
            raise NotADirectoryError("Source %s is not exists" % src)

    @staticmethod
    def _is_dst_file_or_dir(dst):
        if (not dst.is_symlink) and (dst.is_file() or dst.is_dir()):
            print("Destination %s is a file or dir" % dst)
            return

    @staticmethod
    def symlink(src_path, dst_path):
        src = pathlib.Path(src_path)
        dst = pathlib.Path(dst_path)
        SymlUp._is_src_exist(src)
        SymlUp._is_dst_file_or_dir(dst)
        if dst.is_symlink():
            dst.unlink()
        os.symlink(src, dst)
        print("Set %s -> %s" % (src, dst))

    def init(self):
        self.json = Json(SYMLINK_LIST_FILE_DEFAULT)
        self._write()

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
            self.apply_jsongroup(symlink_group)
        except Exception as e:
            print(e)

    def remove_link(self, dst):
        for group in self.json.keys():
            if dst in self.json[group].keys():
                self._remove(group, dst)
                self._write()
                print("Removed: %s" % dst)
                return
        print("There is no that symlink")

    def apply_jsongroup(self, symlink_group):
        self._is_read()
        g = self.json[symlink_group]  # type: dict
        for dst, src in g.items():
            try:
                self.symlink(src, dst)
            except Exception as e:
                print(e)

    def apply_json(self, symlink_group=None):
        self._is_read()
        if symlink_group:
            self.apply_jsongroup(symlink_group)
        else:
            for group in self.json.keys():
                self.apply_jsongroup(group)


if __name__ == "__main__":
    # set_symlinks()
    obj = SymlUp()
    # obj.init()
    obj._read()
    obj.apply_json()
    obj.upd_link("esp", "C:/esp/tools/msys2_esp_pack/20180110", "C:/msys33")
    obj.remove_link("C:/msys33")
    # with open()
    # os.symlink("C:/", "C:/Users/dongr/c")
    print("Done!")
    time.sleep(5)
