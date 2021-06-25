## Signal to Noise Ratio Analysis
This code produces signal to noise ratio estimates for a fixed set of values, or to generate trends based on independent parameters.
For an in-depth description of formulas and methods used, visit the [Confluence Page](http://spacesys.utat.ca/confluence/display/FIN/Signal+to+Noise+Ratio+Analysis).

### 1. Assumptions
- **Quantum Efficiency** was assumed to linearly decay over the spectral range.
- **Optical Transmittance** was assumed to be constant over the spectral range.
- **Integration Time** was assumed to be equal to the Frame Period.

### 2. File Structure
- `snr_main.py` runs the main Signal to Noise Ratio code for a single set of parameters that can be configured through `config.py`.
- `snr_plots.py` can generate trends based on a defined array of independent variables that are set inside `snr_plots.py`, including:
    1. Spectral Resolution
    2. Optical Transmittance
    3. Sensor Zenith
    4. Season
    5. Integration Time / Frame Rate
- Only one independent variable can be run at a time, all the other variables are held constant. These constants can be changed in `plots_config.py`.
- The `modtran_inputs.csv` file path must be edited in the `snr_plots.py` code to fit your computer paths.

### 3. Utility Configuration Options
- `--print_config`: when set to True, print a timestamped text file with all of the configuration parameters in the same path as the plot outputs.
- `--background`: when set to True, use the background reflectances in the SNR calculation. If you wish to use these reflectances, the `/reflectance_landsat` folder
                  must be downloaded.
- `--headless`: when set to False, will show the MODTRAN window and how chromedriver is actually controlling the inputs. Helpful for debugging.
- `--chromedriver`: links to the filepath of the Chromedriver.exe, change it to fit your computer.
- `--orbit_params_path`: links to the `modtran_inputs.csv` file. Must be manually set if using `snr_plots.py`. 
- `--outputs_path`: root folder to save all SNR plots and config files. Program will automatically create subfolders and timestamp files.

### 4. Dependencies
- Must have [ChromeDriver](https://chromedriver.chromium.org/downloads) with a version that matches your version of Chrome.
- Download newest stable versions of `selenium`, `numpy`, `matplotlib`, `scipy`, and `pillow`.
                  
