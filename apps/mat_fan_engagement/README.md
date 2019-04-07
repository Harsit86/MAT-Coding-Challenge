# MAT Coding Challenge Solution

## Prerequisites:

* [pyton3.7](https://www.python.org/downloads/release/python-370/)
* [mkvirtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/)


## Environment and dependency setup 

The code has been developed using `python3` and uses `virtualenvwrapper`. To get started,
please create a virtual environment and run:

```bash
mkvirtualenv mat_fan_challenge -p python3 -r requirements.txt
workon mat_fan_chellenge
``` 

If you do not want to create a virtual environment, you can install the dependencies:

```bash
pip install -r requirements.txt
```
           
           
## MAT Fan Engagement

The main entrypoint to run the application is [main.py](./main.py), which can be run as follows:

```bash
python main.py
```

The script instantiates an instance of [MATFanEngagementManager](./src/mat_fan_engagement_manager.py)
which is the manges the app, mainly:

* Sets up a client to connect to the `MQTT Broker` and subscribes to the `carStatus` queue
* Validates and parses telemetry data against expected schema as defined in [CarCoordinatesSchema](./src/schemas/car_coordinates.py).
* For a valid message, it transforms and enriches the data by updating the state of the car
* Publishes two messages to `carStatus` queue:
    * `POSITION` message indicating the track position of the car
    * `SPEED` message providing information of the speed of the car in miles per hour
* Publishes `events` queues **if the car has overtaken car(s)**, otherwise does not publish an event message.


### Race Manager 

Upon receiving a message, the `MATFanEngagementManager` object creates an instance of [Race](./src/models/race.py)
object which manges the state of the race:

* Creates an instance of [Car](./src/models/car.py) object if car does not exist for a given `carIndex`
and updates the status of the car, mainly it's `speed` and `position` on the track
* Maintains state of current and new positions of the cars on each new message received and sets the `event` type by
comparing the current position of the car to its new position and setting `_event` attribute iff the car has 
overtaken any car(s).

#### Caveats

Some limitation of `Race` model:

* Position of the cars is only calculated once we have received telemetry for all the cars. This is done to avoid
displaying incorrect information in the webapp in absence of full information.
* An `_event` attribute is only set when a car has overtaken another car.


### Car Manger

The `Race` class keeps track of all the cars in the race in an attribute `_cars` where each item if of type [Car](./src/models/car.py).
The car object stores the state of the car as it progresses through the race, mainly its speed, position and other
metadata needed to stream the data back to the MQTT broker.


## Further Work

If I had more time, I would do a lot of things differently, naming a few below:

* More and rigorous testing
* Add docstrings to the functions
* Dockerise the application and add it to the [docker-compose.yaml](../../docker-compose.yaml)
* Read enviornment variables from [mqtt.env](../../mqtt.env) and [car.env](../../cars.env), but for now have hard-coded
them in the code.
* Car position and event generation has been done vary naively using just the distance travelled by each car which
stricly isn't right but would've taken a lot longer to implement the logic.
* Use a proper pipeline framework e.g. [luigi](https://github.com/spotify/luigi) or [Airflow](https://airflow.apache.org/) although
for this task both seemed to be an overkill.
* Better error handling e.g. on client unable to connect or disconnect
* Better event messages
