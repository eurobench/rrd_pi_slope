# Walking on Slope - Performance Indicators

_to be described_

Copyright RRD

## Installation

python3 is used.

Under Linux, a standard installation in a local environment is obtained using:

```term
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r src/pi_walk_slope/requirements.txt
pip install -e src/pi_walk_slope
#once done
deactivate
```

## Usage

Under Linux, assuming the folder `out` is already created:

```term
# focusing on the gait analysis
run_pi_gait test/input/subject_00_cond_5_run_00_gaitEvents.yaml out
# looking at the joint parameter as well
run_pi_joint test/input/subject_00_cond_5_run_00_gaitEvents.yaml test/input/subject_00_cond_5_run_00_jointAngles.csv out
# checking th emg file:
run_pi_emg test/input/subject_00_cond_5_run_00_emg.csv test/input/subject_00_cond_5_run_00_gaitEvents.yaml out
# combining the three
run_pi_walk_slope test/input/subject_00_cond_5_run_00_gaitEvents.yaml test/input/subject_00_cond_5_run_00_jointAngles.csv test/input/subject_00_cond_5_run_00_emg.csv out
```

## Docker image

### Build from source

_(only tested under Linux)_

Run the following command in order to create the docker image for this PI:

```console
docker build . -t pi_walk_slope
```
### Launch the docker image

Assuming `test/input` contains the input data, and that the directory `out/` is **already created**, and will contain the PI output:

```shell
docker run --rm -v $PWD/test/input:/in -v $PWD/out:/out pi_walk_slope run_pi_walk_slope /in/subject_00_cond_5_run_00_gaitEvents.yaml /in/subject_00_cond_5_run_00_jointAngles.csv /in/subject_00_cond_5_run_01_emg.csv /out
```

## Acknowledgements

<a href="http://eurobench2020.eu">
  <img src="http://eurobench2020.eu/wp-content/uploads/2018/06/cropped-logoweb.png"
       alt="rosin_logo" height="60" >
</a>

Supported by Eurobench - the European robotic platform for bipedal locomotion benchmarking.
More information: [Eurobench website][eurobench_website]

<img src="http://eurobench2020.eu/wp-content/uploads/2018/02/euflag.png"
     alt="eu_flag" width="100" align="left" >

This project has received funding from the European Union’s Horizon 2020
research and innovation programme under grant agreement no. 779963.

The opinions and arguments expressed reflect only the author‘s view and
reflect in no way the European Commission‘s opinions.
The European Commission is not responsible for any use that may be made
of the information it contains.

[eurobench_logo]: http://eurobench2020.eu/wp-content/uploads/2018/06/cropped-logoweb.png
[eurobench_website]: http://eurobench2020.eu "Go to website"
