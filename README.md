### Day2-After-Tomorrow
CodeFest 2020 submission

### Project Day2-After Tomorrow

We will use Python to poll a production vManage server for existing environmental, topological, and logical constructs of the fabric and present them to the user in an easy to consume manner. The goal will be to provide a straight-forward interface that allows the customer to quickly monitor the health of their SD-WAN environment and be alerted to urgent messages.  You will do this by running a python script to retrieve data from vManage, store that data into an influxDB database, and display the data in a grafana dashboard.

-- Future functionality

### Requirements

To use this application you will need:

* Python 3.7.5
* Cisco SD-WAN 18+
* Windows or OSX device

### Install and Setup

Clone the code to your local machine.

```
git clone https://github.com/logarby/Day2-After-Tomorrow
cd Day2-After-Tomorrow
```

Setup Python Virtual Environment (requires Python 3.7+)

```
python3.7 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Setup local environment variables for your Cisco SD-WAN fabric. Provide the info for your Cisco SD-WAN environment.  Execute the following commands in bash in you virtual environment and then execute the env_var_check.py script to verify your environmental variables are set..

Examples:

```
export SDWAN_IP=sandboxsdwan.cisco.com
export SDWAN_USERNAME=devnetuser
export SDWAN_PASSWORD=Cisco123!
```

### Using the application

Once installed and setup, you can now get started.

Investigate the built-in help with the tool.

`./sdwan.py --help`

OUTPUT

```
Usage: sdwan.py [OPTIONS] COMMAND [ARGS]...

  Command line tool for deploying templates to CISCO SDWAN.

Options:
  --help  Show this message and exit.

Commands:
  attach            Attach a template with Cisco SDWAN.
  attached_devices  Retrieve and return devices associated to a...
  detach            Detach a template with Cisco SDWAN.
  device_list       Retrieve and return network devices list.
  template_list     Retrieve and return templates list.
```

Look at the available templates. Each template will provide the number of devices already attached and the template ID.

`./sdwan.py template_list`

OUTPUT

```
Retrieving the templates available.

| Template Name        | Device Type   | Template ID                          |   Attached devices |   Template version |
|----------------------|---------------|--------------------------------------|--------------------|--------------------|
| VEDGE_BASIC_TEMPLATE | vedge-cloud   | 72babaf2-68b6-4176-92d5-fa8de58e19d8 |                  0 |                 15 |
```

Retrieve the list of devices that make up the SD-WAN fabric with ./sdwan.py device_list.

`$ ./sdwan.py device_list`

OUTPUT

```
Retrieving the devices.

| Host-Name   | Device Type   | Device ID                            | System IP   |   Site ID | Version   | Device Model   |
|-------------|---------------|--------------------------------------|-------------|-----------|-----------|----------------|
| vmanage     | vmanage       | 4854266f-a8ad-4068-9651-d4e834384f51 | 4.4.4.90    |       100 | 18.3.1.1  | vmanage        |
| vsmart      | vsmart        | da6c566f-eb5f-4731-a89a-ff745661027c | 4.4.4.70    |       100 | 18.3.0    | vsmart         |
| vbond       | vbond         | 455407de-9327-467e-a0d2-d3444659dbb2 | 4.4.4.80    |       100 | 18.3.1    | vedge-cloud    |
| vedge01     | vedge         | 4af9e049-0052-47e9-83af-81a5825f7ffe | 4.4.4.60    |       200 | 18.3.1    | vedge-cloud    |
| vedge02     | vedge         | f3d4159b-4172-462c-9c8d-8db76c31521d | 4.4.4.61    |       300 | 18.3.1    | vedge-cloud    |
| vedge03     | vedge         | 100faff9-8b36-4312-bf97-743b26bd0211 | 4.4.4.62    |       400 | 18.3.1    | vedge-cloud    |
| vedge04     | vedge         | 46c18a49-f6f3-4588-a49a-0b1cc387f179 | 4.4.4.63    |       500 | 18.3.1    | vedge-cloud    |
```

Attaching a template is as easy as calling the *attach* option of the application and passing in the requested parameters.

`./sdwan.py attach --template TemplateID --target TargetID --hostname devnet01.cisco.com --sysip 1.1.1.1 --loopip 2.2.2.2/24 --geip 3.3.3.3/24 --siteid 999`

To detach a template from a specific device you need to call the detach option of the application and pass in the parameters for the target device ID and the system-ip of that device:

`./sdwan.py detach --target TargetID --sysip 1.1.1.1`
