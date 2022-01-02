############################################### SNR Analysis ##########################################################
# These equations for SNR come from the Signal to Noise Ratio Analysis Plan
# Link: https://docs.google.com/document/d/1idc3v_UskPmZQoNl5HFGgbXdpNweEMwqTM8wsZyl6rk/edit

import numpy as np
import math
import os
import sys
from Broketran.BrokeTran import BrokeTran
from config import parse_config
from scipy.integrate import cumtrapz
from scipy.interpolate import interp1d
from background_reflectance import background_reflectance

def signal_to_noise():

    cfg = parse_config()

    if not os.path.exists(cfg.outputs_path):
        os.mkdir(cfg.outputs_path)

    broketran = BrokeTran(cfg)
    spec_res_series, L_radiance, L_transmittance = broketran.run()
    for i in range(0, len(L_radiance)):
        L_radiance[i] = L_radiance[i] * (1e6 * 1e2 * 1e2)     # L_target is in W/cm^2/micron/sr

    L_radiance = np.asarray(L_radiance)
    L_transmittance = np.asarray(L_transmittance)

    radiance_interp = interp1d(np.arange(L_radiance.size), L_radiance)
    L_radiance = radiance_interp(np.linspace(0, L_radiance.size - 1, L_transmittance.size))
    L_target = np.multiply(L_radiance, L_transmittance)

    for i in range(0, len(spec_res_series)):
        spec_res_series[i] = spec_res_series[i] / (1e6)



    ### Target Signal Calculation
    f_sys = (cfg.focal_length / (1e3)) / (cfg.d_ap / (1e3))
    quant_eff = efficiency_curves('qe', cfg.sensor, spec_res_series, cfg)
    diffraction_eff = efficiency_curves('de', cfg.grating, spec_res_series, cfg)
    opt_transmittance = efficiency_curves('transmittance', 'foreoptics', spec_res_series, cfg) * efficiency_curves('transmittance', 'collimator', spec_res_series, cfg) * efficiency_curves('transmittance', 'collimator', spec_res_series, cfg) * efficiency_curves('transmittance', 'diverging', spec_res_series, cfg) * efficiency_curves('transmittance', 'filter', spec_res_series, cfg)
    # diffraction_eff = np.linspace(cfg.de_lower, cfg.de_upper, len(spec_res_series))
    area_detector = cfg.x_pixels * (cfg.pixel_pitch / 1e6) * cfg.y_pixels * (cfg.pixel_pitch / 1e6)
    signal_const = (area_detector * math.pi * (1 - cfg.epsilon) * cfg.t_int)/(4 * (f_sys**2) * cfg.h * cfg.c)
    signal_integrand = (np.multiply(np.multiply(np.multiply(quant_eff, L_target), diffraction_eff), np.asarray(spec_res_series)) * opt_transmittance)
    signal_int = cumtrapz(signal_integrand, spec_res_series)
    for i in range(len(signal_int)-1, 0, -1):
        signal_int[i] = signal_int[i] - signal_int[i-1]
    signal_target = signal_const * signal_int

    ### Background Signal Calculation
    if cfg.background:
        signal_background = background_reflectance(cfg.season) * signal_target
    else:
        signal_background = 0


    ### Noise Calculation
    quant_noise = cfg.well_depth / (2**(cfg.dynamic_range) * np.sqrt(12))
    dark_current = cfg.dark_current * (1e-9) * (6.242e18) * (area_detector * 1e2 * 1e2)
    dark_noise = dark_current * cfg.t_int
    total_noise = np.sqrt(signal_target + signal_background + quant_noise**2 + dark_noise + cfg.readout_noise**2)

    lea_noise = lea_pn(cfg, signal_target)
    print("Signal: ", signal_target)

    ### Signal to Noise Ratio Calculation
    print("Calculating Signal to Noise Ratio...")
    if not cfg.decibels:
        signal_to_noise = np.divide((signal_target - signal_background), total_noise)
    else:
        signal_to_noise = 20 * np.log10(np.divide((signal_target - signal_background), total_noise))
    diff_band_1 = []
    diff_band_2 = []
    diff_band_3 = []
    for i in spec_res_series:
        diff_band_1.append(abs(i - 1.610e-6))
        diff_band_2.append(abs(i - 1.650e-6))
        diff_band_3.append(abs(i - 1.670e-6))
    print("Signal to Noise at 1610nm: %.2f" % signal_to_noise[diff_band_1.index(min(diff_band_1))])
    print("Signal to Noise at 1650nm: %.2f" % signal_to_noise[diff_band_2.index(min(diff_band_2))])
    print("Signal to Noise at 1670nm: %.2f" % signal_to_noise[diff_band_3.index(min(diff_band_3))])
    return spec_res_series, signal_to_noise, cfg


def efficiency_curves(type, unit, spec_res_series, cfg):
    if type == "qe":
        if unit == "flirtau":
            qe = []
            # These values were generated from an efficiency curve provided by Lane Rubin from FLIR.
            # These values were estimated from the plot in increments of 50nm, starting at 900nm and ending at 1700nm.
            qe_curve = [[901e-9, 0.03], [950e-9, 0.8], [1000e-9, 0.82], [1050e-9, 0.835], [1100e-9, 0.84], [1150e-9, 0.84], [1200e-9, 0.85], [1250e-9, 0.84], [1300e-9, 0.84], [1350e-9, 0.84], [1400e-9, 0.83], [1450e-9, 0.81], [1500e-9, 0.79], [1550e-9, 0.77], [1600e-9, 0.75], [1650e-9, 0.69], [1699e-9, 0.50]]
            for idx in range(0, len(qe_curve)):
                if qe_curve[idx][0] >= min(spec_res_series) and qe_curve[idx][0] <= max(spec_res_series):
                    qe.append(qe_curve[idx][1])
            qe = np.asarray(qe)
            qe_interp_func = interp1d(np.arange(qe.size), qe)
            qe_interp = qe_interp_func(np.linspace(0, qe.size - 1, np.asarray(spec_res_series).size))
            return qe_interp
        else:
            print(f"ERROR: Sensor Name {unit} is not supported.")
    elif type == "de":
        if unit == "wasatch900":
            de = []
            # These values were generated from an efficiency curve provided by Neil Anderson from Wasatch.
            # These values were estimated from the plot in increments of 50nm, starting at 900nm and ending at 1700nm.
            de_curve = [[901e-9, 0.05], [950e-9, 0.10], [1000e-9, 0.15], [1050e-9, 0.20], [1100e-9, 0.25], [1150e-9, 0.30], [1200e-9, 0.35], [1250e-9, 0.40], [1300e-9, 0.45], [1350e-9, 0.50], [1400e-9, 0.55], [1450e-9, 0.60], [1500e-9, 0.65], [1550e-9, 0.70], [1600e-9, 0.80], [1650e-9, 0.84], [1699e-9, 0.81]]
            for idx in range(0, len(de_curve)):
                if de_curve[idx][0] >= min(spec_res_series) and de_curve[idx][0] <= max(spec_res_series):
                    de.append(de_curve[idx][1])
            de = np.asarray(de)
            de_interp_func = interp1d(np.arange(de.size), de)
            de_interp = de_interp_func(np.linspace(0, de.size - 1, np.asarray(spec_res_series).size))
            return de_interp
        else:
            print(f"ERROR: diffraction grating {unit} is not supported.")
    elif type == "transmittance":
        if unit == "foreoptics":
            transmittance = cfg.foreoptics_transmittance
            return transmittance
        elif unit == "collimator":
            transmittance = cfg.collimator_transmittance
            return transmittance
        elif unit == "diverging":
            transmittance = cfg.diverging_transmittance
            return transmittance
        elif unit == "filter":
            transmittance = []
            if min(spec_res_series) == 900 and max(spec_res_series) == 1700:
                transmittance = 1.00
                return transmittance
            else:
                for idx in range(0, len(spec_res_series)):
                    transmittance.append(cfg.filter_transmittance)
                transmittance = np.asarray(transmittance)
                return transmittance

def lea_pn(cfg, signal_target):
    spectral_res_series = np.arange(cfg.lambda_min, cfg.lambda_max, cfg.spectral_res)
    photon_noise = interp1d(np.arange(signal_target.size),signal_target)
    lea_pn = photon_noise(np.linspace(0,signal_target.size-1,spectral_res_series.size))
    lea_pn = np.sqrt(lea_pn)
    return lea_pn


