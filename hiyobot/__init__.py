from collections import namedtuple

__version__ = "4.0.0-alpha.15"

VersionInfo = namedtuple("VersionInfo", "major minor micro releaselevel serial")

version_info = VersionInfo(major=4, minor=0, micro=0, releaselevel="alpha", serial=15)
