# ISC License
#
# Copyright 2019 David Kalliecharan <dave@dal.ca>
#
# Permission to use, copy, modify, and distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY
# SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION
# OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN
# CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
"""
sfwagner.py
-----------

X-Ray photoelectron spectroscopy (XPS) Wagner sensitivity factors (sf), this
is required for any corrections on any XPS machine.

The xps/data/sfwagner.db contains data for the Wagner sensitivity factors and
is reproduced and provided here for non-profit use with permission of the
publisher John Wiley & Sons Ltd. [1]

*Appendix 5: Empirically derived set of atomic sensitivity factors for XPS*,
p511-514, Published by J. Wiley and Sons in 1983, ISBN 0-471-26279,
Copyright (c) 1983 by John Wiley & Sons Ltd.

For non-profit use as a framework of system calls or as a reference. This
permission does not include the right to grant others permission to photocopy
or otherwise reproduce this material except for accessible versions made by
non-profit organizations serving the blind, visually impaired and other
persons with print disabilities (VIPs).

The original set of data first appeared in the following resource:
C. D. Wagner, L. E. Davis, M. V. Zeller, J. A. Taylor, R. M. Raymond and L. H. Gale,
Surf. Interface Anal., 3. 211 (1981)

Any use of this data must include the citation above and below in any work.

References
..........

.. [1] "Practical Surface Analysis by Auger and X-ray Photoelectron Spectroscopy",
    D. Briggs and M. P. Seah,
"""
import os.path as _path
import sqlite3 as _sqlite3

ROOTPATH = _path.dirname(_path.abspath(__file__))
DATAPATH = _path.join(ROOTPATH, 'data')

SFWAGNER_DB = _path.join(DATAPATH, 'sfwagner.db')

class SensitivityFactors():
    """Generates object of elements with orbitals and sensitivity factors for
    area and height.
    """
    def __init__(self):
        conn = _sqlite3.connect(SFWAGNER_DB)
        cur = conn.cursor()
        query = 'SELECT DISTINCT element FROM wagner'
        element = [row[0] for row in cur.execute(query)]
        for e in element:
            query = 'SELECT shell FROM wagner WHERE element=="{elem}"'
            shell = [row[0] for row in cur.execute(query.format(elem=e))]
            shell_dict = {}
            for s in shell:
                shell_dict[s] = dict()
                query = 'SELECT area, height FROM wagner WHERE element=="{elem}" AND shell=="{sh}"'
                res = cur.execute(query.format(elem=e, sh=s))
                area, height = res.fetchone()
                if area is not None:
                    shell_dict[s]['area'] = area
                if height is not None:
                    shell_dict[s]['height'] = height
            setattr(self, e, shell_dict)


if __name__ == '__main__':
    pass

