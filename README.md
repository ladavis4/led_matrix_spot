# RaspberryPi LED Matrix 
## Installation/Preqs
**Install python dependencies:**
- Use the requirements.txt file

**Set up google authentication**  
To use this application, you must have OAuth client ID credentials provided by the Google cloud platform. 
- Open the Google Cloud Console
- From the top left go to APIs & Services > Credentials
- If an application is already created, then download the credentials and save them as "credentials.json" in the main directory 
- If an application is not created, create an application with the proper permissions
For more guidance follow this [link](https://developers.google.com/workspace/guides/create-credentials)

**Install Raspberry Pi Matrix Software**
- Use the script provided in [this guide](https://learn.adafruit.com/adafruit-rgb-matrix-bonnet-for-raspberry-pi/driving-matrices) to install the setup software for running the led matrix bonnet
- You should now be able to run any of the example scripts provided in the bin folder of the repository. Just remember to specify the matrix size and GPIO slowdown. 

**Test That It Works** 
You should now be able to run the "main.py" file in the home of the directory and see the matrix working! The program requires sudo to control the pins for the matrix bonnet. 

## Making the Program Run on Launch
To have the program run on launch, you will need to set up a systemd service. An example service file is provided in the "/services" directory. The steps for setting up launch on boot are: 
- Take "/services/led-matrix.service and led-app.service" and move them to "lib/systemd/system" 
- Reload systemctl and add the service to start on boot
```bash
sudo systemctl daemon-reload
sudo systemctl enable led-matrix.service
sudo systemctl enable led-app.service
```
If you want to test that it works without rebooting the pi, run: 
```bash
sudo systemctl start led-matrix.service
```
If something goes wrong and you need to check the logs of the program, run: 
```bash
journalctl -u led-matrix.service -b
```


