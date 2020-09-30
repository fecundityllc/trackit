import os
import re
import subprocess
import sys
from collections import defaultdict
from os.path import abspath
from typing import Dict, List, Union, cast


def get_ftype(fpath: str, use_shebang: bool) -> str:
    ext = os.path.splitext(fpath)[1]
    if ext:
        return ext[1:]
    elif use_shebang:
        # opening a file may throw an OSError
        with open(fpath) as f:
            first_line = f.readline()
            if re.search(r'^#!.*\bpython', first_line):
                return 'py'
            elif re.search(r'^#!.*sh', first_line):
                return 'sh'
            elif re.search(r'^#!.*\bperl', first_line):
                return 'pl'
            elif re.search(r'^#!.*\bnode', first_line):
                return 'js'
            elif re.search(r'^#!.*\bruby', first_line):
                return 'rb'
            elif re.search(r'^#!', first_line):
                args = (fpath, first_line)
                msg = 'Error: Unknown shebang in file "%s":\n%s' % args
                print(msg, file=sys.stderr)
                return ''
            else:
                return ''
    else:
        return ''


def get_files_by_type(file_type: str,
                      exclude: List[str] = None,
                      targets: List[str] = None) -> List[str]:
    exclude = exclude or []
    listing = list_files(ftypes=[file_type], exclude=exclude, targets=targets)
    listing = cast(List[str], listing)
    return listing


def list_files(
        targets: List[str] = None,
        ftypes: List[str] = None,
        use_shebang: bool = True,
        modified_only: bool = False,
        exclude: List[str] = None,
        group_by_ftype: bool = False,
        extless_only: bool = False
        ) -> Union[Dict[str, List[str]], List[str]]:
    """
    List files tracked by git.

    Returns a list of files which are either in targets or in directories in
    targets.  If targets is [], list of all tracked files in current directory
    is returned.

    Other arguments: ftypes - List of file types on which to filter the search.
    If ftypes is [], all files are included.  use_shebang - Determine file type
    of extensionless files from their shebang.  modified_only - Only include
    files which have been modified.  exclude - List of paths to be excluded,
    relative to repository root.  group_by_ftype - If True, returns a dict of
    lists keyed by file type.  If False, returns a flat list of files.
    extless_only - Only include extensionless files in output.
    """
    if targets is None:
        targets = []

    if ftypes is None:
        ftypes = []

    if exclude is None:
        exclude = []

    ftypes = [x.strip('.') for x in ftypes]
    ftypes_set = set(ftypes)

    # Really this is all bytes -- it's a file path -- but we get paths in
    # sys.argv as str, so that battle is already lost.  Settle for hoping
    # everything is UTF-8.
    cmd = ['git', 'rev-parse', '--show-toplevel']
    repository_root = subprocess.check_output(cmd).strip().decode('utf-8')
    exclude_abspaths = [os.path.normpath(os.path.join(repository_root, fpath))
                        for fpath in exclude]

    cmd = ['git', 'ls-files'] + targets
    if modified_only:
        cmd.append('-m')

    result = subprocess.check_output(cmd, universal_newlines=True).split('\n')
    files_gen = (x.strip() for x in result)
    # throw away empty lines and non-files (like symlinks)
    files = list(filter(os.path.isfile, files_gen))

    result_dict = defaultdict(list)  # type: Dict[str, List[str]]
    result_list = []  # type: List[str]

    for fpath in files:
        # this will take a long time if exclude is very large
        ext = os.path.splitext(fpath)[1]
        if extless_only and ext:
            continue
        absfpath = abspath(fpath)
        if any(absfpath == expath or absfpath.startswith(expath + '/')
               for expath in exclude_abspaths):
            continue

        if ftypes or group_by_ftype:
            try:
                filetype = get_ftype(fpath, use_shebang)
            except (OSError, UnicodeDecodeError) as e:
                etype = e.__class__.__name__
                args = (etype, fpath)
                msg = 'Error: %s while determining type of file "%s":' % args
                print(msg, file=sys.stderr)
                print(e, file=sys.stderr)
                filetype = ''
            if ftypes and filetype not in ftypes_set:
                continue

        if group_by_ftype:
            result_dict[filetype].append(fpath)
        else:
            result_list.append(fpath)

    if group_by_ftype:
        return result_dict
    else:
        return result_list
