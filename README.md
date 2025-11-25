
# Network setup

0. _Note that all programs work exclusively on Windows._
1. Connect the Musical isntruments, BCI, and MR headset to the computer.
2. Connect all coomputers to the a local network.
3. Make sure all the computers have their firewalls turned off. When you run each program for the first time, you will be prompted to allow the program access. Allow the programs to communicate on all networks.

    ![Alt text](https://github.com/ns2max/musmet_recording/blob/main/img/firewall1.png)

4. One computer will act as the MASTER - to start and stop the recordings. Assign one of the computers to this role. 



# Connecting Unicorn BCI interface

First we have to ensure that the BCI is connected and the signals are good. These instructions are for the Unicorn BCI from gTec.

1. Connect the BCI to the computer using bluetooth.

    ![Alt text](https://github.com/ns2max/musmet_recording/blob/main/img/unicorn1.png)

2. Run _**Unicorn Suite Hybrid Black**_ from the _**Start Menu**_

    ![Alt text](https://github.com/ns2max/musmet_recording/blob/main/img/unicorn2.png)

3. Select _**Apps**_ -> _**Unicorn Reader**_ -> _**Open**_

    ![Alt text](https://github.com/ns2max/musmet_recording/blob/main/img/unicorn3.png)

4. When you Press _**Play/Stop**_ you will see the signals. The panel on the right will specify if the BCI nodes are connected properly, and transmitting a good signal. 

    ![Alt text](https://github.com/ns2max/musmet_recording/blob/main/img/unicorn4.png)

5. Once you have confirmed that the BCI is connected and all connections are good, close _**Unicorn Suite Hybrid Black**_




# Recording Multiple streams of Data

We use LSL streams to record the data with time stamps. **LabRecorder is used for the actual recording**. There are 3 other applications that act as bridges, plus a controller which should **only** run on the master. 

    1. Unicorn LSL will convert the BCI signals into LSL streams
    2. audio2lsl will convert the audio into LSL streams
    3. osc2lsl will convert OSC signals into LSL streams

You need to clone this repo, which includes all the software for recording.


## Controller

**This application is required to start and stop the recordings on all devices simultaneously. THIS SHOULD ONLY RUN ON THE MASTER COMPUTER**


1. Select **0-START CONTROLLER.bat** 

    ![Alt text](https://github.com/ns2max/musmet_recording/blob/main/img/apps.png)
    
2. Type the IP addresses of each computer on the interface. The first one should be left as *localhost* to start/stop recording on the MASTER. You can find the IP address of the computer using the OSC bridge that will be introduced next.


3. Once you are ready, and the Audio, OSC, and UNICORN bridges are set up, you may press **Start All** to start the recording.

4. Once recording is complete, press **Stop All** to end.

    ![Alt text](https://github.com/ns2max/musmet_recording/blob/main/img/controller.png)




### What to do in Case the Controller does not start recording on all computers.

This situation can happen due to issues in the network, or if the firewalls block network ports. In case this happens, follow the alternate steps below to start/stop recording.

    1. Start the recording on each computer
    2. Ask the musicians to play a single note together, such that the streams may be synchronized later.



## Audio Bridge

The audio bridge will convert the audio into LSL streams to be saved and synchronized.

1. Select **2-START_audio-bridge.bat** 

    ![Alt text](https://github.com/ns2max/musmet_recording/blob/main/img/apps.png)

2. Select the corresponding input from the Audio Interface.

3. Enter a filename for the audio to be saved. The files are saved in the _/audio_ folder on the working directory.

4. **Start Stream** button starts streaming the audio as a LSL stream and recording.
5. **Stop Stream** button will end the LSL stream, and save the audio as a _.wav_ file.

    ![alt text](https://github.com/ns2max/musmet_recording/blob/main/img/audio.png)




## OSC Bridge

The OSC bridge will convert the OSC into LSL streams to be saved and synchronized.
~~**There is a bug in the system. Once you Stop the server, you need to close and re-open the OSC Bridge**~~ 
*-------- bug is fixed* 

1. Select **3-START_osc-bridge.bat** 

    ![Alt text](https://github.com/ns2max/musmet_recording/blob/main/img/apps.png)

2. The window will show the IP address of the device, along with the port to create the OSC server.

3. The terminal window that will open will show each OSC message as it arrives.

4. **Start Stream** button starts the OSC server and LSL stream.
5. **Stop Stream** button will end the server.

    ![alt text](https://github.com/ns2max/musmet_recording/blob/main/img/osc.png)



## Unicorn Bridge

1. Select **4-START_unicorn-bridge.bat** 

    ![Alt text](https://github.com/ns2max/musmet_recording/blob/main/img/apps.png)

2. Select the connected Unicorn device.

3. Select the optiion _Send each signal in one stream_.

4. Enter a name for the LSL stream. You may leave this field blank, and the program will automatically insert the ID of the connected device here.

5. Press **_Open_** to open the BCI.

6. **Start Stream** button starts the LSL stream.
7. **Stop Stream** button will end the stream.

    ![alt text](https://github.com/ns2max/musmet_recording/blob/main/img/unicorn5.png)




## LabRecorder

1. Select **1-START_LabRecorder.bat** 

    ![Alt text](https://github.com/ns2max/musmet_recording/blob/main/img/apps.png)

2. The interface will show all the available LSL streams. Select all the streams. You can use the Select All button. If all steps are above were done correctly, you should see

    - **ONE** Audio Stream
    - **ONE** OSC stream
    - **SIX** BCI streams
        - BAT stream
        - ACC stream
        - VALID stream
        - GYR stream
        - EEG stream 
        - CNT stream

5. The field _**Study Root**_ is the location where the xdf file will be saved. 

6. The filenames are generated using the BIDS framework. 
You can choose to use this framework, or uncheck the BIDS checkbox. _This setting only affects the filename and you are free to use either option_. 

7. Press Start/Stop to start or stop the recording ONLY in the local COMPUTER. You can use the Controller to start and stop all recordings simultaneously.


    ![alt text](https://github.com/ns2max/musmet_recording/blob/main/img/labrecorder.png)




## All apps view

If all steps were followed corectly, you will see the windows as shown below:

    1. RC Controller
    2. LSL Audio Streamber
    3. OSC to LS Bridge
    4. Unicorn LSL
    5. Lab Recorder
    

![alt text](https://github.com/ns2max/musmet_recording/blob/main/img/all.png)
