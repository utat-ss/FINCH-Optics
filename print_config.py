import os
from datetime import date
import numpy as np

def print_config(cfg, plot="", path="", time=""):
    if plot != "" and time == "":
        config_print = os.path.join(path, "config_%s.txt" % plot)
    elif plot == "" and time != "":
        config_print = os.path.join(path, "config_%s.txt" % time)
    else:
        config_print = os.path.join(path, "config_%s_(%s).txt" % (plot, time))

    ### CONFIG CONTENT ###
    general_title = "---------------- GENERAL PARAMETERS ----------------\n"
    general_params = np.asarray([['Print Config', cfg.print_config, ''],
                                 ['Background', cfg.background, ''],
                                 ['Decibels', cfg.decibels, '']])

    signal_title = "---------------- SIGNAL PARAMETERS ----------------\n"
    signal_params = np.asarray([['Optical Transmittance', cfg.opt_transmittance, ''],
                ['X Pixels', cfg.x_pixels, ''],
                ['Y Pixels', cfg.y_pixels, ''],
                ['Pixel Pitch', cfg.pixel_pitch, 'um'],
                ['Integration Time', cfg.t_int, 's'],
                ['Focal Length', cfg.focal_length, ''],
                ['Aperture Diameter', cfg.d_ap, 'mm'],
                ['Fraction of Aperture Blocked', cfg.epsilon, ''],
                ['Planck Constant', cfg.h, 'Js'],
                ['Speed of Light', cfg.c, 'm/s'],
                ['Quantum Efficiency at Lower Spectral Bound', cfg.eta_lower, ''],
                ['Quantum Efficiency at Upper Spectral Bound', cfg.eta_upper, '']])

    noise_title = "---------------- NOISE PARAMETERS ----------------\n"
    noise_params = np.asarray([['Well Depth', cfg.well_depth, 'e-/pixel'],
                ['Dynamic Range', cfg.dynamic_range, 'bit'],
                ['Dark Current', cfg.dark_current, 'e-/pixel/second'],
                ['Readout Noise', cfg.readout_noise, 'e-/pixel']])

    file_title = "---------------- FILE PATHS ----------------\n"
    file_params = np.asarray([['ChromeDriver path', cfg.chromedriver, ''],
                ['Orbital Parameters CSV Path', cfg.orbit_params_path, ''],
                ['Output Plots Path', cfg.outputs_path, '']])

    modtran_title = "---------------- MODTRAN PARAMETERS ----------------\n"
    modtran_params = np.asarray([['Spectral Resolution', cfg.spectral_res, 'nm'],
                                ['Spectral Range Lower Bound', cfg.lambda_min, 'nm'],
                                ['Spectral Range Upper Bound', cfg.lambda_max, 'nm'],
                                ['Season', cfg.season, ''],
                                ['Carbon Dioxide', cfg.carbon_dioxide, 'ppmv'],
                                ['Carbon Monoxide', cfg.carbon_monoxide, 'ppmv'],
                                ['Methane', cfg.methane, 'ppmv'],
                                ['Aerosol Model', cfg.aerosol, ''],
                                ['Visibility', cfg.visibility, 'km'],
                                ['Spectral Units', cfg.spectral_units, ''],
                                ['Save Plots', cfg.plots_save, '']])


    config_print = open(config_print, 'a')
    config_print.write(general_title)
    for i in range (0, general_params.shape[0]):
        print_str = general_params[i, 0] + ": " + str(general_params[i, 1]) + " " + str(general_params[i, 2]) + "\n"
        config_print.write(print_str)

    config_print.write("\n")
    config_print.write(signal_title)
    for i in range(0, signal_params.shape[0]):
        print_str = signal_params[i, 0] + ": " + str(signal_params[i, 1]) + " " + str(signal_params[i, 2]) +"\n"
        config_print.write(print_str)

    config_print.write("\n")
    config_print.write(noise_title)
    for i in range(0, noise_params.shape[0]):
        print_str = noise_params[i, 0] + ": " + str(noise_params[i, 1]) + " " + str(noise_params[i, 2]) + "\n"
        config_print.write(print_str)

    config_print.write("\n")
    config_print.write(file_title)
    for i in range(0, file_params.shape[0]):
        print_str = file_params[i, 0] + ": " + str(file_params[i, 1]) + " " + str(file_params[i, 2]) + "\n"
        config_print.write(print_str)

    config_print.write("\n")
    config_print.write(modtran_title)
    for i in range(0, modtran_params.shape[0]):
        print_str = modtran_params[i, 0] + ": " + str(modtran_params[i, 1]) + " " + str(modtran_params[i, 2]) + "\n"
        config_print.write(print_str)

    config_print.close()