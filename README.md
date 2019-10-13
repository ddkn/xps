# X-ray photoelectron spectroscopy (XPS)

## Future

* Docmuentation (priority)
* Add database of inelastic mean free path (IMFP) of common materials

## X-ray Photonelectron Spectroscopy

### Example

An example analyzing a Ge peak fit within CasaXPS.

    import xps

    # Shortcut for the XPS machine at Dalhousie
    # xps_mach = 'Dalhousie'
    # mach = xps.MACH_PARAM[xps_mach]
    mach = {
        'coef' : [0.9033, -4.0724, 5.0677, 1.1066],
        'scale'     : 0.01,
        'work_func' : 4.6,
    }
    hv = xps.photon_energy['Al']

    # Pass energy [eV], found from XPS operator
    pe = 30

    sfwagner_Ge = xps.sf.Ge['3d']['area']

    data = xps.parser.CasaXPS('Ge_example.csv')

    # Labels defined by user in CasaXPS fits
    pk_lbl = 'Ge 3d'
    be = data.binding_energy(pk_lbl)
    area = data.area(pk_lbl)

    ke = xps.kinetic_energy(be, hv, mach['work_func'])

    t_fn = xps.transmission(ke, pe, mach['coef'], mach['scale'])
    t_fn_wagner = 1/ke # Proportional to 1/KE

    sf_mach = xps.sf_machine(sfwagner_Ge, t_fn, t_fn_wagner)

    pk_corr = xps.peak_correction(area, sf_mach)

    # NOTE Use the xps.XPSPeak(...) helper for convienence
    # analyzed_Ge = xps.XPSPeak(pk_lbl, be, area, sfwagner_Ge, hv, pe, mach)

    # NOTE Returns pandas.DataFrame with all parameters calculated.
    # The user can also query parameters individually
    # df = analyzed_Ge.get_data()

### Matrix Factor corrections

If using multple elements within a matrix (e.g. an alloy), you can utilize the
`xps.matrix_factor` function. You require the inelastic mean free path
of electron scattering (*imfp*) of both species in bulk and the density, as
well as the *imfp* of the matrix at the measured kinetic energies of both
elements. For example, if you have two corrected peaks: `pk_Mn_corr`, and
`pk_Ge_corr`. The *imfp* can be calculated using the TPP-2M equation for
inelastic mean free path, found in the following reference:

S. Tanuma, C. J. Powel, D. R. Penn, *Surf. Interf. Anal.*, Vol 21, 165 (1994)


    import xps
    # pk_Mn_corr and pk_Ge_corr calculated as in the example above

    # a is the kinetic energy used to determine imfp of Ge in Bulk
    imfp_matrix_a = 21.17
    imfp_Ge_a = 29.84
    rho_Ge_a = 5.32

    # b is the kinetic energy used to determine imfp of Mn in Bulk
    imfp_matrix_b = 14.17
    imfp_Mn_b = 14.87
    rho_Mn_b = 7.43

    mat_fact = xps.matrix_factor(imfp_Ge_a, imfp_Mn_b,
                                 mfp_matrix_a, mfp_matrix_b,
                                 rho_Ge_a, rho_Mn_b)
    relative_pk_Ge_corr = (pk_Ge_corr/pk_Mn_corr)*mat_fact

    # NOTE because Mn is used as the normalizing component we can use its
    # corrected peak value directly, all other elements require the matrix
    # factor correction
    print('Ratios of Mn and Ge in MnGe matrix')
    print('Mn : {:0.4e}'.format(pk_Mn_corr))
    print('Ge : {:0.4e}'.format(relative_pk_Ge_corr))

### sfwagner.{db,py}: Empirically derived set of atomic sensitivity factors for XPS

The data in Appendix 5 is reproduced and provided here for non-profit use with
permission of the publisher John Wiley & Sons Ltd.

"Practical Surface Analysis by Auger and X-ray Photoelectron Spectroscopy",
D. Briggs and M. P. Seah,
Appendix 5, p511-514,
Published by J. Wiley and Sons in 1983, ISBN 0-471-26279

Copyright (c) 1983 by John Wiley & Sons Ltd.

The original set of data first appeared in the following resource:
C. D. Wagner, L. E. Davis, M. V. Zeller, J. A. Taylor, R. M. Raymond and L. H. Gale,
Surf. Interface Anal., 3. 211 (1981)

Any use of this data must include the citations above in any work.

## Electron Inelastic Mean Free Path (IMFP)
Electron IMFP can be calculated from using the Tanuma, Powel, Penn modified
(TPP-2M) equation derived from equations (3), (4b,c,d,e) and (8) in the
following reference:

S. Tanuma, C. J. Powel, D. R. Penn, *Surf. Interf. Anal.*, Vol 21, 165 (1994)

For convienence the IMFP TPP-2M equation is located in `xps.scatter` and
can be used as such:

    from xps import scatter

    # Mn example
    kinetic_energy = 1000 # Can be calculated from xps.kinetic_energy

    rho = 7.43         # [g/cc]
    Nv = 7             # valence electrons
    M = 53.938         # atomic mass
    bandgap_energy = 0 # [eV]

    # Return SI units [m]
    imfp_Mn = scatter.imfp_TPP2M(kinetic_energy, rho, M, Nv,
                                 bandgap_energy, 'SI')

The value here can be used in the `xps.matrix_factor` calculations
outlined above.
