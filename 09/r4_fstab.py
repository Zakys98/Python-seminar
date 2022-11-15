from typing import Tuple, List

# Write a non-validating parser for the ‹fstab› file, which in
# traditional UNIXes contains information about filesystems. The
# format is as follows:
#
# Comments start with ‹#› and extend until the end of line.
# Comments, additional whitespace, and blank lines are ignored.
# After comments and blanks are stripped, each line of the file
# describes a single filesystem. Each such description has 6
# columns:
#
#  1. the device (path to a block device or an UUID),
#  2. the mount point,
#  3. the file system type,
#  4. a comma-separated list of mount options,
#  5. dump frequency in days (a non-negative integer, optional),
#  6. file system check pass number (same).
#
# The type below describes the form in which to return the parsed
# data. If items 5 or 6 are missing, set them to 0.

FS = Tuple[ str, str, str, List[ str ], int, int ]

def read_fstab( path: str ) -> List[ FS ]:
    entries: list[FS] = []
    with open(path, 'r') as src:
        for line in src:
            if not line.strip() or line.startswith('#'):
                continue
            items: list[str] = line.strip().split()
            freq = int(items[4]) if len(items) > 5 else 0
            number = int(items[5]) if len(items) > 6 else 0
            entries.append((items[0], items[1], items[2], items[3].split(','), freq, number))
    return entries

def test_1() -> None:
    fs = read_fstab( 'zz.fstab_1.txt' )
    assert len( fs ) == 6, len( fs )

    dev, path, fstype, opts, freq, fsck = fs[ 2 ]
    assert dev == 'aae75c8d6a816625.d', dev
    assert path == '/usr', path
    assert opts == [ 'rw', 'wxallowed', 'nodev' ], opts
    assert freq == 1, freq
    assert fsck == 2, fsck

    dev, path, fstype, opts, freq, fsck = fs[ 4 ]
    assert dev == 'b31cc4c312d35c29.e', dev
    assert path == '/var/postgresql', path
    assert fstype == 'ffs'
    assert opts == [ 'rw', 'nodev', 'noatime', 'softdep', 'noauto' ]

def test_2() -> None:
    fs = read_fstab( 'zz.fstab_2.txt' )
    assert len( fs ) == 10, len( fs )

    dev, path, fstype, opts, freq, fsck = fs[ 5 ]
    assert dev == '/dev/mapper/vg_aisa-msgidcache', dev
    assert path == '/var/msgidcache', path
    assert opts == [ 'defaults', 'nosuid', 'noexec' ], opts
    assert freq == 1, freq
    assert fsck == 2, fsck

    dev, path, fstype, opts, freq, fsck = fs[ 0 ]
    assert dev == 'UUID=e12b47cf-d174-468d-ac3e-dd25e7327d42', dev
    assert path == '/', path
    assert fstype == 'ext4'
    assert opts == [ 'defaults' ]

if __name__ == '__main__':
    test_1()
    test_2()
