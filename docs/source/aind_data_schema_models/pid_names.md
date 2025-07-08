# Pid_names

## Model definitions

### PIDName

Model for associate a name with a persistent identifier (PID),
the registry for that PID, and abbreviation for that registry

| Field | Type | Description |
|-------|------|-------------|
| `name` | `str` | Name |
| `abbreviation` | `Optional[str]` | Abbreviation |
| `registry` | `Optional[aind_data_schema_models.pid_names.BaseName]` | Registry |
| `registry_identifier` | `Optional[str]` | Registry identifier |


