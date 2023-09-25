# RaspberryPi LED Matrix 
## Installation/Preqs
**Install python dependencies:**
- Use the requirements.txt file

**Set up google authentication**  
To use this application, you must have OAuth client ID credentials provided by the Google cloud platform. 
- Open the Google Cloud Console
- From the top left go to APIs & Services > Credentials
- If an application is already created, then download the credentials and save them as "credentials.json". Create a "credentials/" folder in the root directory. Place the "credentials.json" in that folder. 
- If an application is not created, create an application with the proper permissions
For more guidance follow this [link](https://developers.google.com/workspace/guides/create-credentials)

**Set up spotify auth**
- Go to [this link](https://developer.spotify.com/dashboard) to get the client ID and secret key
- Create a file named "spotify_credentials.json" in the credentials folder
- Add the information into the "cid" and "secret" fields of a json and save
- You'll probably be launched into the spotify browser in order to complete login
  
**Install Raspberry Pi Matrix Software**
- Use the script provided in [this guide](https://learn.adafruit.com/adafruit-rgb-matrix-bonnet-for-raspberry-pi/driving-matrices) to install the setup software for running the led matrix bonnet
- You should now be able to run any of the example scripts provided in the bin folder of the repository. Just remember to specify the matrix size and GPIO slowdown. 

**Test That It Works** 
You should now be able to run the "main.py" file in the home of the directory and see the matrix working! The program requires sudo to control the pins for the matrix bonnet. 

## Making the Program Run on Launch
To have the program run on launch, you will need to set up a systemd service. An example service file is provided in the "/services" directory. The steps for setting up launch on boot are: 
- Take "/services/led-matrix.service" and move it to "lib/systemd/system" 
- Reload systemctl and add the service to start on boot
```bash
sudo systemctl daemon-reload
sudo systemctl enable led-matrix.service
```
If you want to test that it works without rebooting the pi, run: 
```bash
sudo systemctl start led-matrix.service
```
If something goes wrong and you need to check the logs of the program, run: 
```bash
journalctl -u led-matrix.service -b
```

# Functionality
**Change images from google drive** 
- In the "utils/constants" file, change the id of DRIVE_IMAGE_FOLDER_ID. Any files that are placed in this google drive folder will be downloaded locally to the pi and displayed on the screen. 

**Change settings from your phone** 
- Before or after launching the "main.py" script, launch the "app.py" script
- You can now go to 192.168.0.11:500 on your phone to change the settings of the screen (as long as your are on the same wifi)
