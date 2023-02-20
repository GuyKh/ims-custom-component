# ims-custom-component

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration) [![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=techblog_ims-custom-component&metric=security_rating)](https://sonarcloud.io/summary/new_code?id=techblog_ims-custom-component)



IMS custom component for HomeAssistant allows you to integrate the Israel Meteorological Service easily and with minimal configuration.
With IMS, you can get the following information for the current status (Updates every hour):
* Temperature
* Real feel
* Humidity
* Wind speed
* Rain status

[![IMS custom component](https://github.com/t0mer/ims-custom-component/blob/main/screenshots/ims.png?raw=true "IMS custom component")](https://github.com/t0mer/ims-custom-component/blob/main/screenshots/ims.png?raw=true "IMS custom component")



And also, the forecast data for today and the next four days in six hours intervals includes the following information:
* Maximum temperature.
* Minimum temperature.
* Max UVI.
* Weather.
* Daily forecast.

* And in six hours interval:
* Weather forecast.
* Temperature.


[![IMS custom component](https://github.com/t0mer/ims-custom-component/blob/main/screenshots/ims_attributes.png?raw=true "IMS custom component")](https://github.com/t0mer/ims-custom-component/blob/main/screenshots/ims_attributes.png?raw=true "IMS custom component")


### Installation
The IMS custom component can be installed manualy by downloading the files and place it under custom_components folder.

The second way is by adding the repo address to HACS custom repositories.

First, in HACS you need to add the repository to the lis of custom repositories by clicking the 3 dots on the upper right corner and click the "Custom repositories" button:

[![IMS custom component](https://github.com/t0mer/ims-custom-component/blob/main/screenshots/add_custom_repositories.png?raw=true "IMS custom component")](https://github.com/t0mer/ims-custom-component/blob/main/screenshots/add_custom_repositories.png.png?raw=true "IMS custom component")


Now, add the custom repository address: https://github.com/t0mer/ims-custom-component and under category select "Integration".

Click on the "Add button" to add the repository.

[![IMS custom component](https://github.com/t0mer/ims-custom-component/blob/main/screenshots/add_custom_repositories.pmg_2.png?raw=true "IMS custom component")](https://github.com/t0mer/ims-custom-component/blob/main/screenshots/add_custom_repositories.pmg_2.png?raw=true "IMS custom component")

You can now see that the repository has been added to the custom repositories list:

[![IMS custom component](https://github.com/t0mer/ims-custom-component/blob/main/screenshots/repo_added.png?raw=true "IMS custom component")](https://github.com/t0mer/ims-custom-component/blob/main/screenshots/repo_added.png?raw=true "IMS custom component")

Now, click the big blue button on the lower lef corner "Explor & Download repositories" and in the list enter ims. you will see a repo called "Israel Meteorological Service / Sensor", click it.

[![IMS custom component](https://github.com/t0mer/ims-custom-component/blob/main/screenshots/add_the_repo.png?raw=true "IMS custom component")](https://github.com/t0mer/ims-custom-component/blob/main/screenshots/add_the_repo.png?raw=true "IMS custom component")

Now click the download button on the lower left corner:

[![IMS custom component](https://github.com/t0mer/ims-custom-component/blob/main/screenshots/add_the_integration.png?raw=true "IMS custom component")](https://github.com/t0mer/ims-custom-component/blob/main/screenshots/add_the_integration.png?raw=true "IMS custom component")

**Restart** the Home Assistant instance to load ims integration before moving on

Finally, use the UI to add the integration:

Under settings, go to "Devices & Services"

[![IMS custom component](https://github.com/t0mer/ims-custom-component/blob/main/screenshots/settings-devices.png?raw=true "IMS custom component")](https://github.com/t0mer/ims-custom-component/blob/main/screenshots/settings-devices.png?raw=true "IMS custom component")

In the lower left cornet click on "Add Integration" button
[![IMS custom component](https://github.com/t0mer/ims-custom-component/blob/main/screenshots/add-integration.png?raw=true "IMS custom component")](https://github.com/t0mer/ims-custom-component/blob/main/screenshots/add-integration.png?raw=true "IMS custom component")

In the list of integrations, search for IMS:

[![IMS custom component](https://github.com/t0mer/ims-custom-component/blob/main/screenshots/select-brand.png?raw=true "IMS custom component")](https://github.com/t0mer/ims-custom-component/blob/main/screenshots/select-brand.png?raw=true "IMS custom component")

Enter the relevant parameters (Location and Language) and click sthe submit button in the bottom:

[![IMS custom component](https://github.com/t0mer/ims-custom-component/blob/main/screenshots/submit-settings.png?raw=true "IMS custom component")](https://github.com/t0mer/ims-custom-component/blob/main/screenshots/submit-settings.png?raw=true "IMS custom component")


The Languages can be one of two:
* he - For hebrew
* en - For english.

The city code must be one of the codes in the following table:

| Id | Location |
| ------------ | ----------- |
| 1| Jerusalem| 
| 2| Tel Aviv - Yafo| 
| 3| Haifa| 
| 4| Rishon le Zion| 
| 5| Petah Tiqva| 
| 6| Ashdod| 
| 7| Netania| 
| 8| Beer Sheva| 
| 9| Bnei Brak| 
| 10| Holon| 
| 11| Ramat Gan| 
| 12| Asheqelon| 
| 13| Rehovot| 
| 14| Bat Yam| 
| 15| Bet Shemesh| 
| 16| Kfar Sava| 
| 17| Herzliya| 
| 18| Hadera| 
| 19| Modiin| 
| 20| Ramla| 
| 21| Raanana| 
| 22| Modiin Illit| 
| 23| Rahat| 
| 24| Hod Hasharon| 
| 25| Givatayim| 
| 26| Kiryat Ata| 
| 27| Nahariya| 
| 28| Beitar Illit| 
| 29| Um al-Fahm| 
| 30| Kiryat Gat| 
| 31| Eilat| 
| 32| Rosh Haayin| 
| 33| Afula| 
| 34| Nes-Ziona| 
| 35| Akko| 
| 36| Elad| 
| 37| Ramat Hasharon| 
| 38| Karmiel| 
| 39| Yavneh| 
| 40| Tiberias| 
| 41| Tayibe| 
| 42| Kiryat Motzkin| 
| 43| Shfaram| 
| 44| Nof Hagalil| 
| 45| Kiryat Yam| 
| 46| Kiryat Bialik| 
| 47| Kiryat Ono| 
| 48| Maale Adumim| 
| 49| Or Yehuda| 
| 50| Zefat| 
| 51| Netivot| 
| 52| Dimona| 
| 53| Tamra| ,
| 54| Sakhnin| 
| 55| Yehud| 
| 56| Baka al-Gharbiya| 
| 57| Ofakim| 
| 58| Givat Shmuel| 
| 59| Tira| 
| 60| Arad| 
| 61| Migdal Haemek| 
| 62| Sderot| 
| 63| Araba| 
| 64| Nesher| 
| 65| Kiryat Shmona| 
| 66| Yokneam Illit| 
| 67| Kafr Qassem| 
| 68| Kfar Yona| 
| 69| Qalansawa| 
| 70| Kiryat Malachi| 
| 71| Maalot-Tarshiha| 
| 72| Tirat Carmel| 
| 73| Ariel| 
| 74| Or Akiva| 
| 75| Bet Shean| 
| 76| Mizpe Ramon| 
| 77| Lod| 
| 78| Nazareth| 
| 79| Qazrin| 
| 80| En Gedi| 



