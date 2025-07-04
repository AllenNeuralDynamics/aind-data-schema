# Connections

## Model definitions

### Connection

Description of a connection between devices in an instrument

| Field | Type | Description |
|-------|------|-------------|
| `device_names` | `List[str]` |  |
| `connection_data` | Dict[str, [ConnectionData](#connectiondata)] |  |


### ConnectionData

Configuration data for a device connection including direction and port information

| Field | Type | Description |
|-------|------|-------------|
| `direction` | Optional[[ConnectionDirection](#connectiondirection)] |  |
| `port` | `Optional[str]` |  |


### ConnectionDirection

Direction of a connection

| Name | Value |
|------|-------|
| `SEND` | `Send` |
| `RECEIVE` | `Receive` |
| `SEND_AND_RECEIVE` | `Send and receive` |


