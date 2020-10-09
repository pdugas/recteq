# Recteq Integration - _Developer Notes_

* Architecture
  * `hacs.data[DOMAIN]` is a dict create in `async_setup()`.
  * We add keys (`ConfigEntry.entry_id`) and values (`RecteqDevice`) in `ascunc_setup_entry()`
  * We create one climate and 2 sensor entities for each device
  * The sensor and climate entities are not polled; instead, they are triggered to update by the device.
* ToDo
  * Discovery - should be able to detect device IDs and IP addresses then prompt for local keys
  * "Full" and "Max Smoke" modes.
  * The climate UI widget doesn't appear to be updating the circular slider when the target temp changes.
