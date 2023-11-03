# Spot DB 
This is a mobile app that will be used to create and manage a catalog of exercises which can be tracked according to user-created metrics. The goal of this app is to make the process of tracking your workouts seamless, to that end, a variety of metrics and exercices presets will be built into the application. The UI should be simple and accessible. I intend to first develop this with Python and JS (FastAPI and React) so I can get a working application. I'll then re-create the frontend UI with react native and hope to deploy on mobile.


## Startup
Get it running:
- Clone the directory,
- Navigate to that directory,
    - `docker volume create gymscribe2-postgres-data`
    - `docker compose build`
    - `docker compose up`

For now, you can interact with the api through the docs at localhost:8000/docs .

I intend to deploy to ios first, however the frontend is going to be built with REACT native. 

If you would like to contribute, email me at rmvh01@proton.me . 
