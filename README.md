# GymScribe2 (working title)
This is a mobile app that will be used to create and manage a catalog of exercises which can be tracked according to user-created metrics. The goal of this app is to make the process of tracking your workouts seamless, to that end, a variety of metrics and exercices presets will be built into the application. The UI should be simple and accessible. I intend to first develop this with Python and JS (FastAPI and React) so I can get a working application. I'll then re-create the frontend UI with react native and hope to deploy on mobile.


## Startup
Get it running:
- Clone the directory,
- Navigate to that directory,
    - `docker volume create gymscribe2-postgres-data`
    - `docker compose build`
    - `docker compose up`

For now, you can interact with the api through the docs at localhost:8000/docs .

### Current Broad-Scope Work

As of today (2023-09-13),

If you look at db.png, and then at the migrations, you'll see that as of now only the tables associated with exercises are created in the initial migrations. I'm planning to build out the endpoints associated with the current tables before creating the tables and endpoints for the rest of this api. I'm doing this primarily so I and hopefully others can get the frontend started so work can be divided to any extent.

I'm working on building the endpoints for the tables which currently exist, i'm not putting much thought into it for now, just making the five usual endpoints for each table, each time writing the tests before the routers/queries (TDD). I intend to expand upon these endpoints as necessary once I get to the next big chunk of the backend.


#### How you can help,
There should be a number of issues, if you're interested in the application and want to help out or want to get more information, please reach out at rmvh01@proton.me or if anywhere else if you have my information already.
