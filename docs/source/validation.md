# Validation

To ensure that your metadata is valid you need to construct the full [Metadata](metadata.md#metadata) object. *Validition* does not guarantee in any way that your metadata is *complete*. Many fields are marked as `Optional[]` because not all situations require them, but they may be expected for your use case. If you have a piece of metadata accessible, it should be reported!

## Instrument and Acquisition

If you are validating your `Instrument` and `Acquisition` on your rig, you may not have access to the other metadata files like the procedures. To allow for partial validation of these files we include an `InstrumentAcquisitionCompatibility` class. Construct it as follows:

```{python}
from aind_data_schema.utils.compatibility_check import InstrumentAcquisitionCompatibility

# Construct your Instrument and Acquisition objects

compatibility_check = InstrumentAcquisitionCompatibility(instrument, acquisition)
compatibility_check.run_compatibility_check(raise_for_missing_devices=True)
```

The `raise_for_missing_devices` will raise a `ValidationError` if `Acquisition.active_devices` can't be found in the instrument. Note that if your situation includes implanted devices in the procedures, then errors will be raised because the procedures are not available. In that case, you should construct the a full `Metadata` object for validation.
