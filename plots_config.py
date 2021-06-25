############################################### SNR Config ##########################################################
# Input the variables here to run through the Signal to Noise Ratio Analysis

import argparse

def parse_config(season='winter', spectral_res=2, transmittance=0.70, zenith=150.73, altitude=499.71, t_int=0.1667):
    parser = argparse.ArgumentParser()

    '''
    This is the config file that goes along with the snr_plots code. Some of the variable arguments to this function can 
    instead be defined in the snr_plots.py function so that you can iterate over arrays of values.
    '''
    # General Configuration
    parser.add_argument("--print_config", type=bool, default=True, help='set to True if you wish to print all these parameters to a text file in the same path as the plot.')
    parser.add_argument("--background", type=bool, default=True, help='set to True if you wish to use the background reflectance in the SNR calculation')
    parser.add_argument("--decibels", type=bool, default=False, help='set to True if you wish to present SNR in decibels')

    # Signal Target
    parser.add_argument("--opt_transmittance", type=float, default=transmittance, help='Transmittance of the entire optical system from 0 to 1')
    parser.add_argument("--x_pixels", type=float, default=640, help='Number of pixels in x-axis on the sensor')
    parser.add_argument("--y_pixels", type=float, default=512, help='Number of pixels in y-axis on the sensor')
    parser.add_argument("--pixel_pitch", type=float, default=15, help='Size of each pixel (um)')
    parser.add_argument("--t_int", type=float, default=t_int, help='Integration Time (s)')
    parser.add_argument("--focal_length", type=float, default=200, help='focal length of the optical system (mm)')
    parser.add_argument("--d_ap", type=float, default=33, help='Diameter of the aperture (mm)')
    parser.add_argument("--epsilon", type=float, default=0.99, help='Fraction of optical aperture area obscured')
    parser.add_argument("--h", type=float, default=6.63e-34, help='Planck constant')
    parser.add_argument("--c", type=float, default=3.00e8, help='Speed of light')
    parser.add_argument("--eta_lower", type=float, default=0.75, help='quantum efficiency at the lower bound of the spectral range')
    parser.add_argument("--eta_upper", type=float, default=0.60, help='quantum efficiency at the upper bound of the spectral range')

    # Noise
    parser.add_argument("--well_depth", type=int, default=19000, help='Full well depth (in e-)')
    parser.add_argument("--dynamic_range", type=int, default=14, help='Dynamic range (in bits)')
    parser.add_argument("--dark_current", type=int, default=10, help='Dark noise (in nA/cm^2)')
    parser.add_argument("--readout_noise", type=int, default=500, help='Readout noise (in e-)')

    # File Paths
    parser.add_argument("--chromedriver", type=str, default='C:/Users/adynxps/Downloads/chromedriver_win32/chromedriver.exe', help='file path of chromedriver.exe')
    parser.add_argument("--orbit_params_path", type=str, default='./Modtran_Graphs/modtran_orbit_params.csv', help='file path of input MODTRAN CSV')
    parser.add_argument("--outputs_path", type=str, default='snr_results', help='file path of output graphs')

    # MODTRAN
    # Visit this link if more explanation of these terms is needed: http://modtran.spectral.com/modtran_home#help
    parser.add_argument("--spectral_res", type=float, default=spectral_res, help='spectral resolution (nm). Write a multiple of 0.5nm between 0 and 8.5nm')
    parser.add_argument("--lambda_min", type=int, default=1590, help='lower bound of spectral range (nm)')
    parser.add_argument("--lambda_max", type=int, default=1680, help='upper bound of spectral range (nm)')
    parser.add_argument("--season", type=str, default=season, help='season list: winter, spring, summer, fall')
    parser.add_argument("--carbon_dioxide", type=float, default=419.05, help='Carbon Dioxide (ppmv)')
    parser.add_argument("--carbon_monoxide", type=float, default=0.1575, help='Carbon Monoxide (ppmv)')
    parser.add_argument("--methane", type=float, default=1.879, help='Methane (ppmv)')
    parser.add_argument("--aerosol", type=str, default="urban", help='Aerosol Model: rural, urban, navy, desert')
    parser.add_argument("--visibility", type=float, default=23.0, help='Visibility based on aerosol concentration')
    parser.add_argument("--zenith", type=float, default=zenith, help='Angle from the sun to the sensor')
    parser.add_argument("--altitude", type=float, default=altitude, help='Height of the sensor above Earth ground level')
    parser.add_argument("--spectral_units", type=str, default="microns", help='Units: wavenumbers, microns')
    parser.add_argument("--plots_save", type=bool, default=False, help='set to True if you want radiance/transmittance plots from MODTRAN')
    parser.add_argument("--headless", type=bool, default=True, help='set to False if you want to see the MODTRAN window as values are being inputted')

    return parser.parse_args()