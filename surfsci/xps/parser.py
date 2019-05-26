# Copyright 2018 David Kalliecharan <dave@dal.ca>
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
parser.py

Parser for XPS files generated from software
"""

__author__  = 'David Kalliecharan'
__license__ = 'ISC License'
__status__  = 'Development'

from pandas import read_csv

class CasaXPS:
    '''CasaXPS class is a parser for an individual file output from CasaXPS
    '''
    def __init__(self, filename, delimiter=',', data_start=7, header_start=2, 
            header_len=4, *args, **kws):
        self.peak_data = read_csv(filename, skiprows=data_start, 
                                 delimiter=delimiter)

        with open(filename, 'r') as f:
            ln = f.readline()
            cyc, scan, elem = ln.strip().strip('"').split(':')
            ln = f.readline()
            _, char_energy, _, acq_time = ln.strip().split(delimiter)
            self.cycle = cyc
            self.scan_type = {scan:elem}
            self.characteristic_energy = float(char_energy)
            self.acq_time = float(acq_time)
        hdr = read_csv(filename, skiprows=header_start, index_col=0,
                       nrows=header_len, delimiter=delimiter)
        col_names = [col for col in hdr if 'unnamed' not in col.lower()]
        self.peak_param = hdr[col_names]
        self.peak_param = self.peak_param.transpose()
        for k in self.peak_param.keys():
            if k in ['Lineshape', 'Name']:
                self.peak_param[k] = self.peak_param[k].astype(str)
                continue
            self.peak_param[k] = self.peak_param[k].astype('float64')
        self.peak_ids = col_names

    def binding_energy(self, peak_id):
        return self.peak_param.loc[peak_id]['Position']
        
    def fwhm(self, peak_id):
        return self.peak_param.loc[peak_id]['FWHM']

    def area(self, peak_id):
        if type(peak_id) == list:
            return sum([self.peak_param.loc[pk]['Area'] for pk in peak_id])
        return self.peak_param.loc[peak_id]['Area']

