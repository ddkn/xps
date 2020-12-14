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
imfp.py
-------

Equations relating to the Inelastic Mean Free Path (IMFP) of electrons [1]

References
..........
.. [1] IMFP TPP-2M (TPP-2 modified eqution)
    S. Tanuma, C. J. Powell, D. R. Penn: Surf. Interf. Anal.,Vol. 21, 165 (1994)
"""

from numpy import log as _log
from numpy import sqrt as _sqrt

def imfp_TPP2M(energy_k, rho, molar_mass, n_valence, energy_bg,
        units='angstroms'):
    """The TPP-2M is the modified TPP-2 equation for estimating inelastic
    mean free paths (IMFP) [1]

    Parameters
    ----------
    energy_k : float
        Kinetic energy [eV]
    rho : float
        Density (g/cm**3)
    molar_mass : float
        Atomic or molar mass
    n_valence : float
        Valence electrons
    energy_bg : float
        Bandgap energy [eV]
    units : str
        'angstroms' or 'si' (the default is 'angstroms')

    Returns
    -------
    float
        Inelastic mean free path (IMFP)

    References
    --------
    .. [1] S. Tanuma, C. J. Powell, D. R. Penn: Surf. Interf. Anal.,Vol. 21, 165 (1994)
    """
    # NOTE gamma, betaM, u, c, d are fitting parameters as in ref.
    u = n_valence*rho/molar_mass
    c = 1.97 - 0.91*u
    d = 53.4 - 20.8*u

    energy_plasmon = _sqrt(829.4*u)

    gamma = 0.191*rho**-0.50
    betaM = -0.10 + 0.944/_sqrt(energy_plasmon**2 + energy_bg**2)
    betaM += 0.069*rho**0.1

    imfp = energy_k
    imfp /= (energy_plasmon**2*(betaM*_log(gamma*energy_k) - c/energy_k+ d/energy_k**2))

    if units.lower() == 'si':
        # Convert to meters
        return imfp*1E-10
    # Leave units unmodified in Angstroms
    return imfp

if __name__ == '__main__':
    pass

