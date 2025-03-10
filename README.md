# Module wifi 

This module is meant to help with monitoring your wifi network and measure things
such as ping and run speed tests

## Model brad-grigsby:wifi:pingmonitor

Model that pings your router and the internet (8.8.8.8) every time get_readings is called

### Configuration
The following attribute template can be used to configure this model:

```json
{
"router_address": <string>
}
```

#### Attributes

The following attributes are available for this model:

| Name          | Type   | Inclusion | Description                |
|---------------|--------|-----------|----------------------------|
| `router_address` | string  | Required  | Address of your router |

#### Example Configuration

```json
{
  "router_address": "192.168.0.1"
}
```

## Model brad-grigsby:wifi:speedtest

Model that runs speedtests every x seconds (60 seconds by default)

### Configuration
The following attribute template can be used to configure this model:

```json
{
"speedtest_interval": <int>
}
```

#### Attributes

The following attributes are available for this model:

| Name          | Type   | Inclusion | Description                |
|---------------|--------|-----------|----------------------------|
| `speedtest_interval` | int  | Optional  | Interval in seconds to run the speedtest (60 seconds by default) |

#### Example Configuration

```json
{
  "speedtest_interval": 90
}
```
