# pulser_suite
The suite of application that composes the pulser app: dpu, the data processing unit; pulser, the central web app and brain, where the learning model resides

*requires python3 and pip*   
- run ``` pip install requirements.txt```   
- for brain:
  - run ```cd brain```
  - download trained model from [here](https://drive.google.com/open?id=0B9cBcdhbAeQbSG14WmR6d29pQ1U) and place it in the trained_models folder
  - run ```python3 routes.py```
- for main app:
  - run ```cd router/pulser```
  - run ```sudo pip install -r requirements.txt```
  - run ```python3 manage.py --host 0.0.0.0```
- for mobile app - set up on mobile phone with Android Studio
