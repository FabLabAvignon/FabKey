# FabKey
A simple project made a FabLab in Avignon, for the door opening, featuring an **Arduino Uno** with a **GSM Shield** and what ever board (or maybe a computer) who runs the **Python Backend**.

This is the workflow :  
You send a SMS **->** The Arduino stores it in RAM **->** The Backend asks for latest received SMS and check in the database **->** The backend tells the Arduino to trigger a relay who enables the outdoor button(or not :D) **->** You push the button and the door opens !

# Dependencies
<u>Building and uploading to Arduino :</u>
  * Arduino **from the Arduino website, not from `apt` !**
  * `apt install arduino-mk`
  * `apt install python python-serial`

<u>Using the python backend :</u>
  * `apt install python python-serial python-mysqldb python-configparser`
