
# ims-custom-component

[![hacs_badge](https://img.shields.io/badge/HACS-Default-41BDF5.svg)](https://github.com/hacs/integration) [![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=techblog_ims-custom-component&metric=security_rating)](https://sonarcloud.io/summary/new_code?id=techblog_ims-custom-component)



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
The IMS custom component can be installed from HACS default repository.

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
| 53| Tamra |
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
| 200| Nimrod Fortress|
| 201| Banias|
| 202| Tel Dan|
| 203| Snir Stream|
| 204| Horshat Tal |
| 205| Ayun Stream|
| 206| Hula|
| 207| Tel Hazor|
| 208| Akhziv|
| 209| Yehiam Fortress|
| 210| Baram|
| 211| Amud Stream|
| 212| Korazim|
| 213| Kfar Nahum|
| 214| Majrase |
| 215| Meshushim Stream|
| 216| Yehudiya |
| 217| Gamla|
| 218| Kursi |
| 219| Hamat Tiberias|
| 220| Arbel|
| 221| En Afek|
| 222| Tzipori|
| 223| Hai-Bar Carmel|
| 224| Mount Carmel|
| 225| Bet Shearim|
| 226| Mishmar HaCarmel |
| 227| Nahal Me‘arot|
| 228| Dor-HaBonim|
| 229| Tel Megiddo|
| 230| Kokhav HaYarden|
| 231| Maayan Harod|
| 232| Bet Alpha|
| 233| Gan HaShlosha|
| 235| Taninim Stream|
| 236| Caesarea|
| 237| Tel Dor|
| 238| Mikhmoret Sea Turtle|
| 239| Beit Yanai|
| 240| Apollonia|
| 241| Mekorot HaYarkon|
| 242| Palmahim|
| 243| Castel|
| 244| En Hemed|
| 245| City of David|
| 246| Me‘arat Soreq|
| 248| Bet Guvrin|
| 249| Sha’ar HaGai|
| 250| Migdal Tsedek|
| 251| Haniya Spring|
| 252| Sebastia|
| 253| Mount Gerizim|
| 254| Nebi Samuel|
| 255| En Prat|
| 256| En Mabo‘a|
| 257| Qasr al-Yahud|
| 258| Good Samaritan|
| 259| Euthymius Monastery|
| 261| Qumran|
| 262| Enot Tsukim|
| 263| Herodium|
| 264| Tel Hebron|
| 267| Masada |
| 268| Tel Arad|
| 269| Tel Beer Sheva|
| 270| Eshkol|
| 271| Mamshit|
| 272| Shivta|
| 273| Ben-Gurion’s Tomb|
| 274| En Avdat|
| 275| Avdat|
| 277| Hay-Bar Yotvata|
| 278| Coral Beach|


