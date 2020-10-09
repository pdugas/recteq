# Recteq Integration - _Developer Notes_

* Architecture
  * `hacs.data[DOMAIN]` is a dict created in `async_setup()`.
  * We add keys (`ConfigEntry.entry_id`) and values (`RecteqDevice`) in `ascync_setup_entry()`
  * We create one climate and 2 sensor entities for each device
  * The sensor and climate entities are not polled; instead, they are triggered to update by the device.
* The `dps` values in the data to/from the grill are integers (or boolean for
  power); floats or strings don't work.
* ToDo
  * Discovery - should be able to detect device IDs and IP addresses then prompt for local keys
  * "Full" and "Max Smoke" modes.
  * The climate UI widget doesn't appear to be updating the circular slider when the target temp changes.
  * Is there any reason to add entities for the Error, temperature adjustment, or min-feedrate values?
