# pulser_suite
The suite of application that composes the pulser app: dpu, the data processing unit; pulser, the central web app and brain, where the learning model resides

*requires python3 and pip*   
- run ``` pip install requirements.txt```   
- for brain:
  - run ```cd brain```
  - download dataset (TODO add link) and place it the app folder
  - point in constants.py the test_ds 
  - run ```python3 trainer.py```
  - run ```python3 routes.py```
- for dpu:
  - run ```cd dpu```
  - ```python3 routes.py```
- for main app:
  - run ```cd router/pulser```
  - ```python3 manage.py --host 0.0.0.0```
- for mobile app - set up on mobile phone with Android Studio
