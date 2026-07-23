#!/usr/bin/env python
# GN-build equivalent of build_embedded_loc.bat: produce embedded.loc from
# rufus.loc by dropping the MSG_9xx (Windows AppStore/debug) messages.
# Upstream's alternative embedded.sed rule also strips comments and the en-US
# UI section, but the runtime parser handles those fine, so the simpler .bat
# filtering is what gets embedded (byte-identical to FINDSTR /v MSG_9).
#
# Two copies are written:
#   argv[2]: ../res/loc/embedded.loc in the SOURCE tree, where rufus.rc's
#            relative RCDATA reference resolves (same place the .bat and the
#            autotools rule put it; the path is gitignored upstream).
#   argv[3]: the GN-declared output under the build dir, which ninja tracks
#            for freshness (GN forbids declaring source-tree outputs).

import sys


def main():
    src, tree_out, gen_out = sys.argv[1:4]
    with open(src, "rb") as f:
        lines = f.read().splitlines(keepends=True)
    data = b"".join(l for l in lines if b"MSG_9" not in l)
    for path in (tree_out, gen_out):
        with open(path, "wb") as f:
            f.write(data)
    return 0


if __name__ == "__main__":
    sys.exit(main())
