from snr_equations_for_plotting import signal_to_noise
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import os
from print_config import print_config

if __name__ == "__main__":
     # Define which plots you would like to show and if you would like to print the config file. Only plot one parameter
     # at a time, we want to keep this analysis as simple as possible.
     # Plots: 'season', 'spectral_res', 'optical_transmittance', 'sensor_zenith', 'sensor_altitude', 't_int', 'frame_rate'

     # --------------------------------------------------------------------------------------------------------------- #
     plot = 't_int'
     print_cfg = True
     orbital_params_path = 'C:/Users/adynxps/OneDrive/University Files/Extracurricular Activities/UTAT/FINCH/Payload Systems/Systems Topics/SNR_Analysis/Optics/Modtran_Graphs/modtran_inputs.csv'
     # --------------------------------------------------------------------------------------------------------------- #

     if plot == 'season':
          plot_list = ['winter', 'spring', 'summer', 'fall']
     elif plot == 'spectral_res':
          plot_list = [1, 2, 3, 4, 5, 6, 7, 8]
     elif plot == 'optical_transmittance':
          plot_list = [0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80]
     elif plot == 'sensor_zenith':
          orbital_params = np.genfromtxt(orbital_params_path, delimiter=',', dtype='U')
          plot_list = orbital_params[1:, 1].astype(float)
     elif plot == 'sensor_altitude':
          orbital_params = np.genfromtxt(orbital_params_path, delimiter=',', dtype='U')
          plot_list = orbital_params[1:, 2].astype(float)
     elif plot == 't_int' or plot == 'frame_rate':
          plot_list = [0.01, 0.05, 0.10, 0.1667]
     elif plot == 'focal_length':
          plot_list = [25, 50, 75, 100, 125, 150, 175, 200, 225, 250, 275, 300, 325, 350, 375, 400]


     snr_list = np.zeros((len(plot_list), 3))
     diff_band_1 = []
     diff_band_2 = []
     diff_band_3 = []

     for x_num, x_val in enumerate(plot_list):
          if plot == 'season':
               spectral_series, snr, cfg = signal_to_noise(season=x_val)
          elif plot == 'spectral_res':
               spectral_series, snr, cfg = signal_to_noise(spectral_res=x_val)
          elif plot == 'optical_transmittance':
               spectral_series, snr, cfg = signal_to_noise(transmittance=x_val)
          elif plot == 'sensor_zenith':
               spectral_series, snr, cfg = signal_to_noise(zenith=x_val)
          elif plot == 'sensor_altitude':
               spectral_series, snr, cfg = signal_to_noise(altitude=x_val)
          elif plot == 't_int' or plot == 'frame_rate':
               spectral_series, snr, cfg = signal_to_noise(t_int=x_val)
          elif plot == 'focal_length':
               spectral_series, snr, cfg = signal_to_noise(focal_length=x_val)
          print("(%d / %d) Calculating SNR -> Transmittance: %.2f, Spectral Resolution: %.1f, Season: %s, Zenith: %.3f, Altitude: %.3f, Integration Time: %.2f, Focal Length %d" % (
               x_num + 1, len(plot_list), cfg.opt_transmittance, cfg.spectral_res, cfg.season, cfg.zenith, cfg.altitude, cfg.t_int, cfg.focal_length))
          for i in spectral_series:
               diff_band_1.append(abs(i - 1.610e-6))
               diff_band_2.append(abs(i - 1.650e-6))
               diff_band_3.append(abs(i - 1.670e-6))
          snr_list[x_num, 0] = snr[diff_band_1.index(min(diff_band_1))]
          snr_list[x_num, 1] = snr[diff_band_2.index(min(diff_band_2))]
          snr_list[x_num, 2] = snr[diff_band_3.index(min(diff_band_3))]
          save_folder = "%s_scenarios" % plot
          now = str(datetime.now())[:-7]
          now = now.replace(" ", "_")
          now = now.replace(":", "")
          savefile_name = "scenario_%d_(%s).png" % (x_num + 1, now)
          diff_band_1 = []
          diff_band_2 = []
          diff_band_3 = []

     if plot == 'season':
          fig, ax = plt.subplots()
          ax.plot(range(1, len(plot_list)+1), snr_list[:, 0], label="1610nm")
          ax.plot(range(1, len(plot_list)+1), snr_list[:, 1], label="1650nm")
          ax.plot(range(1, len(plot_list)+1), snr_list[:, 2], label="1670nm")
          ax.set_ylabel('Signal to Noise Ratio')
          ax.set_title('Signal to Noise Ratio in each Season')
          ax.set_xlabel('Season')
          ax.set_xticks((range(1, len(plot_list) + 1)))
          ax.set_xticklabels(plot_list)
          ax.legend()
     else:
          plt.figure()
          if plot == 'frame_rate':
               plt.plot(np.divide(1, np.asarray(plot_list)), snr_list[:, 0], label="1610nm")
               plt.plot(np.divide(1, np.asarray(plot_list)), snr_list[:, 1], label="1650nm")
               plt.plot(np.divide(1, np.asarray(plot_list)), snr_list[:, 2], label="1670nm")
          elif plot == 'focal_length':
               plt.semilogy(plot_list, snr_list[:, 0], label="1610nm")
               plt.semilogy(plot_list, snr_list[:, 1], label="1650nm")
               plt.semilogy(plot_list, snr_list[:, 2], label="1670nm")
          else:
               plt.plot(plot_list, snr_list[:, 0], label="1610nm")
               plt.plot(plot_list, snr_list[:, 1], label="1650nm")
               plt.plot(plot_list, snr_list[:, 2], label="1670nm")
          plt.ylabel('Signal to Noise Ratio')
          plt.legend()
          if plot == 'spectral_res':
               plt.xlabel('Spectral Resolution (nm)')
               plt.title('Signal to Noise Ratio versus Spectral Resolution')
          elif plot == 'optical_transmittance':
               plt.xlabel('Optical Transmittance')
               plt.title('Signal to Noise Ratio versus Optical Transmittance')
          elif plot == 'sensor_zenith':
               plt.xlabel('Sensor Zenith (deg)')
               plt.title('Signal to Noise Ratio versus Sensor Zenith')
          elif plot == 'sensor_altitude':
               plt.xlabel('Sensor Altitude (deg)')
               plt.title('Signal to Noise Ratio versus Sensor Altitude')
          elif plot == 't_int':
               plt.xlabel('Integration Time (s)')
               plt.title('Signal to Noise Ratio versus Integration Time')
          elif plot == 'Frame Rate':
               plt.xlabel('Frame Rate')
               plt.title('Signal to Noise Ratio versus Frame Rate')
          elif plot == 'focal_length':
               plt.xlabel('Focal Length (mm)')
               plt.title('Signal to Noise Ratio versus Focal Length (Logarithmic)')

     dirname = os.path.dirname(__file__)
     outputs_path = os.path.join(dirname, cfg.outputs_path)
     if not os.path.exists(outputs_path):
          os.mkdir(outputs_path)
     save_path = os.path.join(outputs_path, save_folder)
     if not os.path.exists(save_path):
          os.mkdir(save_path)
     plt.savefig(os.path.join(save_path, savefile_name))
     plt.show()

     if print_cfg:
          print_config(cfg, plot=plot, path=save_path, time=now)