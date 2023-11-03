# Spot DB 
This is a mobile app that will be used to create and manage a catalog of exercises which can be tracked according to user-created metrics. The goal of this app is to make the process of tracking your workouts seamless, to that end, a variety of metrics and exercices presets will be built into the application. The UI should be simple and accessible. I intend to develop this with Python and JS (FastAPI and React Native) with postgres for the database.

## Startup

#### Backend Startup
To develop the API, you need to get the environment running. For that you'll need docker. 
- Clone the directory for this repository,
- Navigate to where the directory was cloned,
    - `docker volume create spotdb-postgres-data`
    - `docker compose build`
    - `docker compose up`
 With that you can make and observe your changes in real time.

#### Frontend Startup
This is my first project developing for mobile first using React Native, so bear with me for a time as I get a simple UI up and running. For now, I have an environment running with XCode, and am deciding how I want to configure the developer environment. If you have ideas or advice, please reach out. 

For now, you can interact with the api through the docs at localhost:8000/docs .

I intend to deploy to ios first. 

If you would like to contribute, email me at rmvh01@proton.me . 

