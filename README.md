# Energy-Efficient-Smart-Home

The project demonstrates a connected smart home which enables remote control of home appliances and deploys energy saving techniques using the sensors installed at strategic locations throughout the home. This project is done as part of Purdue ECE 568 course in Spring 2019. The project is built on raspberry pi and sensors used are: Temp Sensor, PIR Motion Sensor and LDR sensor. We have also build an android app. The communication is done over internet using http post function in python http_server class. We use ngrok for tunneling. The http server is running on raspberry pi which listens to incoming requests on port 8000.
Files:
1. http_server.py: This file has all the code for server, sensors and timers. When run this would start an http server on rpi which listens to port 8000.

2. server.py: This file is a copy of the http python library. We have to add do_Post function in this library file hence a local copy is kept.

NGROK: Ngrok is used for tunneling. It is to be run on rpi after an account has been created. 

Commands:
1. On one terminal start ngrok by this command: ./ngrok http 8000
2. On other terminal start server by this command: python3 http_server.py

The ngrok link has to be updated in the MIT app inventor window to make the app work. Then the app has to be started again. This can be avoided if a paid plan is used.

Video Link: https://www.youtube.com/watch?v=bkjhxuXLGX0&t=20s
