"""
config.py

Configuration file for the Optical System Optimizer program.
All config settings can be run through the command line using `sys_optim.sh`

Author(s): Ginny Guo, Jennifer Zhang, Shiqi Xu
"""

import argparse

def parse_config():
    """Sets up configurability of inputs to System Optimizer program through terminal.
    """

    parser = argparse.ArgumentParser()

    parser.add_argument("--spectral_lower", type=float, default=1590, 
                        help='wavelength (nm)')
    parser.add_argument("--spectral_upper", type=float, default=1680, 
                        help='wavelength (nm)')
    parser.add_argument("--spectral_res", type=float, default=1.5, 
                        help='spectral resolution (nm)')
    # parser.add_argument()
    