# Encrypted Traffic Classification
Classify user activity from encrypted Wi-Fi traffic. The system uses a wireless interface in monitor mode to sniff messages from the radio channel to and from a known MAC address and a ML classifier to recognize the device activity.
The system recognizes three types of activities:
- **idle**: the device is asleep or awake but it doesn't perform any request
- **web browsing**: the device is performing web requests
- **video streaming**: the device is streaming a video
It's advised to limit the Access Point channels to a single fixed channel and configure the interface to listen on that in order to capture every packet
## Usage
The `classifier.py` script can be used to tune the model hyperparameters and evaluate the model performance while the `gather_data.py` script can be used to collect and label data from the specified device and build a dataset usable by the predictor: it must be run with root privileges.
To get an online classification:
- enable the monitor mode on a wireless interface
- change the parameters in the `config.yml` file
  - `target`: MAC address of target device
  - `interface`: linux interface name of the monitor mode enabled wireless interfac
  - `dataset_path`: path to the dataset csv file to use
  - `window`: duration of the window, must be consistent with the window used to  build the training dataset
  - `estimators`: number of estimators used in the random forest algorithm
- run the `predict.py` script with root privileges (required by the connection socket)
The prediction occurs every `window` seconds.
