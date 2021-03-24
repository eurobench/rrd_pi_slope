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
run_pi_gait Data/subject_00_cond_5_run_00_gaitEvents.yaml out
# looking at the joint parameter as well
run_pi_joint Data/subject_00_cond_5_run_00_gaitEvents.yaml Data/subject_00_cond_5_run_00_jointAngles.csv out
# combining both
run_pi_walk_slope Data/subject_00_cond_5_run_00_gaitEvents.yaml Data/subject_00_cond_5_run_00_jointAngles.csv out
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
