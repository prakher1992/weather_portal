# Current Weather Portal
### Steps to Build  and Run Project
1. Clone GitHub repository  for weather portal.( https://github.com/prakher1992/weather_portal)

2. Go to the root directory by executing "cd weather_portal"

3. Install the required Python dependencies mentioned in the ‘requirements.txt’ file
```
pip install -r requirements.txt
```
4. You need to replace the current weather report API access key with your own key in the file (weather_app/routes.py)
![api_key](https://github.com/prakher1992/weather_portal/assets/23658440/d6b4167d-fe15-41b7-9fea-08b83ccdf586)

 Note: You can get this API key by signup at https://openweathermap.org/api
 
5. You also need to replace the current location API access key with your own key in the file (weather_app/static/script.js)
![location_api](https://github.com/prakher1992/weather_portal/assets/23658440/8c25158b-ad70-497a-88b3-72474d0ac9e7)

Note: You can get this API key by signup on  https://www.locationiq.com/

6. Now execute the command ‘python run.py’ to run the application

7. Open the browser and go to http://127.0.0.1:5000

### Database design

![dbdiagram](https://github.com/prakher1992/weather_portal/assets/23658440/06cc538e-4567-4e64-8a19-f6f524d71ef8)


