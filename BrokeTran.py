#Dependencies: selenium, matplotlib

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time
import matplotlib.pyplot as plt
import csv
from datetime import date
from selenium.webdriver.support.select import Select
from PIL import Image

today = date.today()

today_date = today.strftime("%b-%d-%Y")

chrome_options = Options()
chrome_options.add_argument("--headless")

PATH = "C:\chromedriver.exe"
#download location for exe extracted from chromedriver_win32.zip (from https://chromedriver.storage.googleapis.com/index.html?path=90.0.4430.24/)
#example: "C:\chromedriver.exe"

CSV_FILE_PATH = r"C:\Users\dhruv\Downloads\modtran_orbit_params.csv"
#example: r"C:\Users\user1\Documents\modtran_orbit_params.csv"
MODTRAN_FOLDER_PATH = r"C:\Users\dhruv\Documents\Modtran_Graphs"
#example: r"C:\Users\user1\Documents\Modtran_Graphs"

js_code_snippet = "arguments[0].setAttribute('value', "
js_code_snippet2 = "arguments[0].setAttribute('style', "

if False:
    #CSV_FILE_PATH == "uninitialized" or MODTRAN_FOLDER_PATH == "uninitialized" or PATH == "uninitialized": 
    print("ERROR: path(s) not initialized")
    
else:
    driver = webdriver.Chrome(PATH,options=chrome_options)

    with open(CSV_FILE_PATH) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
                line_count += 1
                if line_count > 1:    

                    Mode = row[0]
                    Atm_Model = row[1]
                    Water_Column = row[2]
                    Ozone_Column = row[3]
                    CO2 = row[4]
                    CO = row[5]
                    CH4 = row[6]
                    GT = row[7]
                    GA = row[8]
                    AM = row[9]
                    V = row[10]
                    sensor_altitude = row[11]
                    sun_zenith = row[12]
                    SR1 = row[13]
                    SR2 = row[14]
                    Res = row[15]
                    number = row[16]

                    if (Mode == 'Both'):
                        for i in range(0,2):
                            driver.get('http://modtran.spectral.com/modtran_home')

                            time.sleep(2)
                            if (i==0):
                                btn_mode = driver.find_element_by_xpath('//*[@id="inputs_table"]/tbody/tr[1]/td[2]/input[1]')
                                btn_mode.click()
                            if (i==1):
                                btn_mode = driver.find_element_by_xpath('//*[@id="inputs_table"]/tbody/tr[1]/td[2]/input[2]')
                                btn_mode.click()
                            
                            #CHANGING ATM Model
                            ATM_drop_down = driver.find_element_by_xpath('//*[@id="inputs_table"]/tbody/tr[3]/td[2]/select')
                            select = Select(ATM_drop_down)
                            if(Atm_Model == 'Tropical'):
                                select.select_by_index(0)
                            if(Atm_Model == 'Mid-Latitude Summer'):
                                select.select_by_index(1)
                            if(Atm_Model == 'Mid-Latitude Winter'):
                                select.select_by_index(2)
                            if(Atm_Model == 'Sub-Arctic Summer'):
                                select.select_by_index(3)
                            if(Atm_Model == 'Sub-Arctic Winter'):
                                select.select_by_index(4)
                            if(Atm_Model == 'US Standard 1976'):
                                select.select_by_index(5)
                            
                                
                            #CHANGING WC
                            WC_text = driver.find_element_by_xpath('//*[@id="inputs_table"]/tbody/tr[4]/td[2]/input')
                            WC_text.send_keys(Keys.CONTROL,"a", Keys.DELETE)
                            WC_text.send_keys(Water_Column)
                            
                            #CHANGING OC
                            OC_text = driver.find_element_by_xpath('//*[@id="inputs_table"]/tbody/tr[5]/td[2]/input')
                            OC_text.send_keys(Keys.CONTROL,"a", Keys.DELETE)
                            OC_text.send_keys(Ozone_Column)

                            #CHANGING CO2
                            CO2_text = driver.find_element_by_xpath('//*[@id="inputs_table"]/tbody/tr[6]/td[2]/input')
                            CO2_text.send_keys(Keys.CONTROL,"a", Keys.DELETE)
                            CO2_text.send_keys(CO2)

                            #CHANGING CO
                            CO_text = driver.find_element_by_xpath('//*[@id="inputs_table"]/tbody/tr[7]/td[2]/input')
                            CO_text.send_keys(Keys.CONTROL,"a", Keys.DELETE)
                            CO_text.send_keys(CO)

                            #CHANGING CH4
                            CH4_text = driver.find_element_by_xpath('//*[@id="inputs_table"]/tbody/tr[8]/td[2]/input')
                            CH4_text.send_keys(Keys.CONTROL,"a", Keys.DELETE)
                            CH4_text.send_keys(CH4)

                            #CHANGING GT
                            GT_text = driver.find_element_by_xpath('//*[@id="inputs_table"]/tbody/tr[17]/td[2]/input')
                            GT_text.send_keys(Keys.CONTROL,"a", Keys.DELETE)
                            GT_text.send_keys(GT)

                            #CHANGING GA
                            GA_slider = driver.find_element_by_xpath('//*[@id="albedo_slider"]/span')
                            move = ActionChains(driver)
                            move.click_and_hold(GA_slider).move_by_offset(5, 0).release().perform()

                            #CHANGING AM
                            AM_drop_down = driver.find_element_by_xpath('//*[@id="inputs_table"]/tbody/tr[21]/td[2]/select')
                            select = Select(AM_drop_down)
                            if(AM == 'Rural'):
                                print('rural')
                                select.select_by_index(0)
                            if(AM == 'Urban'):
                                select.select_by_index(1)
                            if(AM == 'Navy Aerosol Model'):
                                select.select_by_index(2)
                            if(AM == 'Desert'):
                                select.select_by_index(3)
                                
                            #CHANGING V
                            V_text = driver.find_element_by_xpath('//*[@id="inputs_table"]/tbody/tr[22]/td[2]/input')
                            V_text.send_keys(Keys.CONTROL,"a", Keys.DELETE)
                            V_text.send_keys(V)


                            #CHANGING SZ
                            sz_drop_down = driver.find_element_by_xpath('//*[@id="inputs_table"]/tbody/tr[25]/td[2]/select')
                            all_children_by_xpath = sz_drop_down.find_elements_by_xpath(".//*")
                            js_code_full_sz = js_code_snippet + sun_zenith + ")"
                            driver.execute_script(js_code_full_sz, all_children_by_xpath[0]);
                            select = Select(sz_drop_down)
                            select.select_by_index(0)
                            
                            #CHANGING SA
                            sa_drop_down = driver.find_element_by_xpath('//*[@id="inputs_table"]/tbody/tr[24]/td[2]/select')
                            all_children_by_xpath = sa_drop_down.find_elements_by_xpath(".//*")
                            js_code_full_sa = js_code_snippet + sensor_altitude + ")"
                            driver.execute_script(js_code_full_sa, all_children_by_xpath[0]);
                            select = Select(sa_drop_down)
                            select.select_by_index(0)

                            #Changing SR2
                            SR2_slider = driver.find_element_by_xpath('//*[@id="spectral_range"]/span[2]')
                            move = ActionChains(driver)
                            move.click_and_hold(SR2_slider).move_by_offset(12, 0).release().perform()

                            time.sleep(1)
                            
                            #Changing SR1
                            SR1_slider = driver.find_element_by_xpath('//*[@id="spectral_range"]/span[1]')
                            move = ActionChains(driver)
                            move.click_and_hold(SR1_slider).move_by_offset(21, 0).release().perform()

                            #Changing Res
                            res_slider = driver.find_element_by_xpath('//*[@id="resolution_slider"]/span')
                            move = ActionChains(driver)
                            move.click_and_hold(res_slider).move_by_offset(250, 0).release().perform()

                            #pressing submit button
                            btn_submit = driver.find_element_by_xpath('/html/body/div[3]/div[2]/div[1]/button')
                            btn_submit.click()

                            time.sleep(5)
                            if i == 0:
                                #extracting json data
                                div_plot = driver.find_element_by_id('plot')
                                jsondata = div_plot.get_attribute('innerHTML')

                                while(jsondata == '<div class="initial_plot_msg"><img src="/static/modtran6/img/spinner.gif"><br>Running MODTRAN...</div>'):
                                    print("graph not loaded yet")
                                    time.sleep(2)
                                    jsondata = div_plot.get_attribute('innerHTML')

                                #parsing json data
                                jsondata = jsondata.split("var docs_json = ")[1].lstrip().split("var render_items")[0].rstrip()

                                series = jsondata.split('"data":{"x":')[1].split('},"selected":')[0]

                                xseries = series.split(',"y":')[0]
                                yseries = series.split(',"y":')[1]

                                x_list, y_list = xseries.split(','), yseries.split(',')

                                x_list[0],x_list[-1] = x_list[0][1:], x_list[-1][:-1]
                                y_list[0],y_list[-1] = y_list[0][1:], y_list[-1][:-1]

                                #converting strings in list to floats
                                x_float_list, y_float_list  = list(map(float,x_list)),list(map(float,y_list))

                                #plotting
                                plt.plot(x_float_list,y_float_list)
                                plt.xlabel('Wavelength (Microns)')
                                if i==0:
                                    ylabel = 'Transmittance'
                                if i==1:
                                    ylabel = 'Radiance'
                                plt.ylabel(ylabel)
                                plt.title("Scenario: " + number)

                                #saving and closing plot
                                title = "\MODTRAN_" + ylabel+ "_Scenario_" + number + "_" + today_date + ".png"
                                plt.savefig(MODTRAN_FOLDER_PATH + title)
                                plt.clf()
                            if i ==1:
                                #driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
                                WC_text = driver.find_element_by_xpath('//*[@id="inputs_table"]/tbody/tr[4]/td[2]/input')
                                WC_text.send_keys(Keys.PAGE_DOWN)
                                """
                                im = Image.open(MODTRAN_FOLDER_PATH + title)
                                width, height = im.size
                                left = 0
                                right = width*.45
                                top = height*0.62
                                bottom = height
                                cropped = im.crop((left, top, right, bottom))
                                cropped.save(MODTRAN_FOLDER_PATH + title)
                                """
                                
                                WC_text.send_keys(Keys.PAGE_DOWN)
                                title = "\MODTRAN_TOTAL_FLUX_Scenario1_" + number + "_" + today_date + ".png"
                                driver.save_screenshot(MODTRAN_FOLDER_PATH + title)
                                WC_text.send_keys(Keys.PAGE_DOWN)
                                title = "\MODTRAN_TOTAL_FLUX_Scenario2_" + number + "_" + today_date + ".png"
                                driver.save_screenshot(MODTRAN_FOLDER_PATH + title)
                                WC_text.send_keys(Keys.PAGE_DOWN)
                                title = "\MODTRAN_TOTAL_FLUX_Scenario3_" + number + "_" + today_date + ".png"
                                driver.save_screenshot(MODTRAN_FOLDER_PATH + title)
                                WC_text.send_keys(Keys.PAGE_DOWN)
                                title = "\MODTRAN_TOTAL_FLUX_Scenario4_" + number + "_" + today_date + ".png"
                                driver.save_screenshot(MODTRAN_FOLDER_PATH + title)
                                WC_text.send_keys(Keys.PAGE_UP)
                                title = "\MODTRAN_TOTAL_FLUX_Scenario5_" + number + "_" + today_date + ".png"
                                driver.save_screenshot(MODTRAN_FOLDER_PATH + title)
                                WC_text.send_keys(Keys.PAGE_UP)
                                title = "\MODTRAN_TOTAL_FLUX_Scenario6_" + number + "_" + today_date + ".png"
                                driver.save_screenshot(MODTRAN_FOLDER_PATH + title)
                                





