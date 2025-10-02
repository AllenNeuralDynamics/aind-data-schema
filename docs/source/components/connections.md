# Connections

## Model definitions

### Connection

Description of a connection between devices in an instrument

| Field | Type | Title (Description) |
|-------|------|-------------|
| `source_device` | `str` | Source device name  |
| `source_port` | `Optional[str]` | Source device port index/name  |
| `target_device` | `str` | Target device name  |
| `target_port` | `Optional[str]` | Target device port index/name  |
| `send_and_receive` | `bool` | Send and receive (Whether the connection is bidirectional (send and receive data)) |


