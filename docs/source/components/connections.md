# Connections

## Model definitions

### Connection

Description of a connection between devices in an instrument

| Field | Type | Description |
|-------|------|-------------|
| `source_device` | `str` |  |
| `source_port` | `Optional[str]` |  |
| `target_device` | `str` |  |
| `target_port` | `Optional[str]` |  |
| `send_and_receive` | `bool` | Whether the connection is bidirectional (send and receive data) |


