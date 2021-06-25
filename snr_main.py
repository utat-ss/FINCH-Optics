from snr_equations import signal_to_noise
import os
from datetime import datetime
import matplotlib.pyplot as plt
from print_config import print_config

if __name__ == "__main__":
    '''
    Use the config.py file to change parameters. If you want to instead generate trends based on transmittance, season,
    spectral resolution, or orbital parameters, use the snr_plots.py script. This file generates a single plot of signal 
    to noise ratio over the specified spectral range.
    
    Assumptions:
        - Optical transmittance is constant over the spectral range.
        - Quantum efficiency linearly decays over the spectral range.
    '''
    main = True
    spectral_series, snr, cfg = signal_to_noise()

    plt.figure()
    plt.plot(spectral_series[:-1], snr)
    plt.xlabel('Spectral Resolution (nm)')
    plt.ylabel('Signal to Noise Ratio')
    plt.title('Signal to Noise Ratio over the Spectral Range ')
    save_path = os.path.join(cfg.outputs_path, "snr_plot")
    if not os.path.exists(save_path):
        os.mkdir(save_path)
    now = str(datetime.now())[:-7]
    now = now.replace(" ", "_")
    now = now.replace(":", "")
    save_fig = os.path.join(save_path, 'snr_(%s).png' % now)
    plt.savefig(save_fig)
    plt.show()

    if cfg.print_config:
        print_config(cfg, path=save_path, time=now)

