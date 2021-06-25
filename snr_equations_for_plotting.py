############################################### SNR Analysis ##########################################################
# These equations for SNR come from the Signal to Noise Ratio Analysis Plan
# Link: https://docs.google.com/document/d/1idc3v_UskPmZQoNl5HFGgbXdpNweEMwqTM8wsZyl6rk/edit

import numpy as np
import math
import os
from BrokeTran import BrokeTran
from plots_config import parse_config
from scipy.integrate import cumtrapz
from scipy.interpolate import interp1d
from background_reflectance import background_reflectance

def signal_to_noise(season='winter', spectral_res=2, transmittance=0.75, zenith=150.73, altitude=499.71, t_int=0.1667):
    cfg = parse_config(season, spectral_res, transmittance, zenith, altitude, t_int)

    if not os.path.exists(cfg.outputs_path):
        os.mkdir(cfg.outputs_path)

    broketran = BrokeTran(cfg)
    spec_res_series, L_radiance, L_transmittance = broketran.run()
    for i in range(0, len(L_radiance)):
        L_radiance[i] = L_radiance[i] * (1e6 * 1e2 * 1e2)  # L_target is in W/cm^2/micron/sr

    L_radiance = np.asarray(L_radiance)
    L_transmittance = np.asarray(L_transmittance)

    radiance_interp = interp1d(np.arange(L_radiance.size), L_radiance)
    L_radiance = radiance_interp(np.linspace(0, L_radiance.size - 1, L_transmittance.size))
    L_target = np.multiply(L_radiance, L_transmittance)

    for i in range(0, len(spec_res_series)):
        spec_res_series[i] = spec_res_series[i] / (1e6)

    ### Target Signal Calculation
    f_sys = (cfg.focal_length / (1e3)) / (cfg.d_ap / (1e3))
    quant_eff = np.linspace(cfg.eta_lower, cfg.eta_upper, len(spec_res_series))
    area_detector = cfg.x_pixels * (cfg.pixel_pitch / 1e6) * cfg.y_pixels * (cfg.pixel_pitch / 1e6)
    signal_const = (area_detector * math.pi * (1 - cfg.epsilon) * cfg.t_int) / (4 * (f_sys ** 2) * cfg.h * cfg.c)
    signal_integrand = (np.multiply(np.multiply(quant_eff, L_target), np.asarray(spec_res_series)) * cfg.opt_transmittance)
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
    quant_noise = cfg.well_depth / (2 ** (cfg.dynamic_range) * np.sqrt(12))
    dark_current = cfg.dark_current * (1e-9) * (6.242e18) * (area_detector * 1e2 * 1e2)
    dark_noise = dark_current * cfg.t_int
    total_noise = np.sqrt(signal_target + signal_background + quant_noise ** 2 + dark_noise + cfg.readout_noise ** 2)

    ### Signal to Noise Ratio Calculation
    print("Calculating Signal to Noise Ratio...")
    if not cfg.decibels:
        signal_to_noise = np.divide((signal_target - signal_background), total_noise)
    else:
        signal_to_noise = 20 * np.log10(np.divide((signal_target - signal_background), total_noise))
    print("Signal to Noise: %.2f" % np.max(signal_to_noise))
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