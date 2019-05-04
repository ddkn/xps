# ISC License
#
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
xps.py

X-Ray photoelectron spectroscopy (XPS) helper functions to adjust the
machine dependent intensities to Wagner intensities
"""

__author__  = 'David Kalliecharan'
__license__ = 'ISC License'
__status__  = 'Development'

from numpy import log10, poly1d

PHOTON_ENERGY = {
    'Mg' : 1253.6, # eV
}

MACH_PARAM = {
    'Dalhousie': {
        'coefficients' : [0.9033, -4.0724, 5.0677, 1.1066],
        'scale'        : 0.01,
        'work_func'    : 4.6,
    }
}

def kinetic_energy(be, hv, psi):
    """Calculates the kinetic energy (KE) with a Mg source (Dalhousie default):

    be  : binding energy (BE [eV])
    psi : Work function (Psi [eV])
    hv  : Phonton energy (h*nu [eV])
    """
    return hv - be - psi


def transmission(ke, pe, a, scale):
    """Dalhousie standard for the Transmission function

    ke    : Kinetic energy (KE [eV])
    pe    : Pass Energy (PE [eV])
    a     : List of coefficients for series expansion, _NOTE_ coefficents are
            reversed such that (aN, ..., a0) -> aN*x**N + ... + a0
            See documentation on numpy.poly1d
    scale : required scaling factor according to Avantage software
    """
    poly = poly1d(a)
    x = log10(ke/pe)
    y = poly(x)
    return scale*pe*10**y


def sf_machine(sf_wagner, transmission_xps, transmission_wagner):
    """Sensitivity factor for XPS machine correction from the Wagner XPS machine

    sf_wagner              : Wagner sensitivity factor
    transmission_mach      : Transmission function for the selected element
    transmission_wagner    : Wagner transmission function for the selected
                             element.
                             Proportional to 1/(kinetic_energy) [1/eV]
    """
    return sf_wagner*transmission_xps/transmission_wagner


def peak_correction(peak_area, sf_machine):
    """Corrected intensity of peak fitting by scaling to the sensitivity
    factor of the machine.

    peak_area   : peak area [CPS*eV]
    sf_machine  : sensitivity factor of xps machine
    """
    return peak_area/sf_machine


def matrix_factor(alpha, beta, matrix_alpha, matrix_beta):
    """Determines the matrix multiplicity factor. Mean free path values can be
found using an external program QUASES-IMFP-TPP2M.

    alpha            : Mean free path of alpha, eg. \lambda(KE_{Mn 2p3/2})
    beta             : Mean free path of beta, eg. \lambda(KE_{Co 2p3/2})
    matrix_alpha     : Mean free path of matrix with kinetic energy of alpha
                       \lambda_matirx(KE_{Mn 2p3/2})
    matrix_beta      : Mean free path of matrix with kinetic energy of beta
                       \lambda_matirx(KE_{Co 2p3/2})
    """
    return (matrix_alpha*beta)/(matrix_beta*alpha)


class XPSPeak():
    """XPSPeakBase class that conveniently wraps the base functions into an object
    """
    def __init__(self, be, peak_area, sf_elem, hv, pe, a, scale, alpha=1,
            beta=1, matrix_alpha=1, matrix_beta=1, *args, **kws):
        self.__be = be
        self.__pk = pk
        self.__sf_elem = sf_elem
        self.__hv = hv
        self.__pe = pe
        self.__a = a
        self.__scale = scale
        self.__alpha = alpha
        self.__beta = beta
        self.__matrix_alpha = matrix_alpha
        self.__matrix_beta = matrix_beta
        self.__args = args
        self.__kws = kws

    def get_kinetic_energy(self):
        return kinetic_energy(self.__be, self.__hv, self.__psi)

    def get_transmission(self):
        return transmission(self.__ke, self.__pe, self.__a, self.__scale)

    def get_sf_machine(self):
        ke = self.get_kinetic_energy()
        transmission_wagner = 1/ke # proportional to 1/KE
        if 'transmission_wagner' in kws:
            self.transmission_wagner = kws['transmission_wagner']

        tx_xps = self.get_transmission()

        return sf_machine(self.__sf_elem, tx_xps, transmission_wagner)

    def get_matrix_factor(self):
        return matrix_factor(self.__alpha, self.__beta, self.__matrix_alpha,
                             self.__matrix_beta)

    def get_peak_correction(self):
        ke = self.get_kinetic_energy()
        tx = self.get_transmission()
        sf_mach = self.get_sf_machine()

        return peak_correction(self.__peak_area, sf_mach)

    def get_mach_params(self):
        params = {
            'photon_energy' : self.__hv,
            'pass_energy'   : self.__pe,
            'coefficients'  : self.__a,
            'scale'         : self.__scale,
        }

        return params

    def get_all(self, array_true=False):
        data_dict = {
            'binding_energy'    : self.__be,
            'kinetic_energy'    : self.get_kinetic_energy(),
            'transmission_func' : self.get_transmission(),
            'sf_machine'        : self.get_sf_machine(),
            'matrix_factor'     : self.get_matrix_factor(),
            'peak_corrected'    : self.get_peak_correction(),
        }

        if array_true == True:
            header = []
            values = []
            for k, v in data_dict.iter():
                header.append(k)
                values.append(v)
            format = ['f8' for i in range(len(values))]
            data_arr = np.rec.fromrecords(values, header, format)

            return data_arr
        return data_dict


if __name__ == '__main__':
    pass

