# Recteq Integration - _Developer Notes_

## Architecture

* `hacs.data[DOMAIN]` is a dict created in `async_setup()`.
* We add keys (`ConfigEntry.entry_id`) and values (`RecteqDevice`) in `ascync_setup_entry()`
* We create one climate and 2 sensor entities for each device
* The sensor and climate entities are not polled; instead, they are triggered to update by the device.

## Protocol

* The controller in my 2020 RT-590 uses the 3.3 version of the Tuya protocol.
  Logs from a call to the `pytuya.Device.status()` method are below.

  ```
  2020-10-12 09:24:00 DEBUG (SyncWorker_7) [pytuya] status() entry
  2020-10-12 09:24:00 DEBUG (SyncWorker_7) [pytuya] json_payload=b'{"gwId":"02655252ecfabcxxxxxx","devId":"02655252ecfaxxxxxxxx"}'
  2020-10-12 09:24:00 DEBUG (SyncWorker_7) [pytuya] status received data=b'\x00\x00U\xaa\x00\x00\x00\x00\x00\x00\x00\n\x00\x00\x00\x9c\x00\x00\x00\x00tO\xf8i\x17\xa4\x14M\xb4\x8a\x1f\x95\x18\x83\x1f\xd2\xae\xa2\x05\xf2s\x9eG\xfe\xc89a$\r\xf4\xce\xe3\xb4\xaea\xe75P[\xc9\xbf\x1c\xe5\x1b\xe1\x93\xdb\xde\x95\xa65":\xfc0h\xad\xefA\xf3\x95\xab\xf1cR\xec\x1b\x8b\x85\xb5+C\x1d\xd6.w1\x84\xebgV]%\x0fw\x93\xe9\xfbzd]P\x12\xdcK\xa14XB\x11\xee,g\x19\xeb\'&\xe3\xf9\x07\x9c\x8a]\x95Z;\x1dt\x99\xb8\xbfiU60\xfb-\xe6\x99\xdaC\x1a\x01\x82h:e\xb7\xe7\xa9KrW"1;\xa2(\x00\x00\xaaU'
  2020-10-12 09:24:00 DEBUG (SyncWorker_7) [pytuya] result=b'tO\xf8i\x17\xa4\x14M\xb4\x8a\x1f\x95\x18\x83\x1f\xd2\xae\xa2\x05\xf2s\x9eG\xfe\xc89a$\r\xf4\xce\xe3\xb4\xaea\xe75P[\xc9\xbf\x1c\xe5\x1b\xe1\x93\xdb\xde\x95\xa65":\xfc0h\xad\xefA\xf3\x95\xab\xf1cR\xec\x1b\x8b\x85\xb5+C\x1d\xd6.w1\x84\xebgV]%\x0fw\x93\xe9\xfbzd]P\x12\xdcK\xa14XB\x11\xee,g\x19\xeb\'&\xe3\xf9\x07\x9c\x8a]\x95Z;\x1dt\x99\xb8\xbfiU60\xfb-\xe6\x99\xdaC\x1a\x01\x82h:e\xb7\xe7\xa9KrW"'
  2020-10-12 09:24:00 DEBUG (SyncWorker_7) [pytuya] decrypted result='{"devId":"02655252ecfabcxxxxxx","dps":{"1":false,"102":300,"103":0,"104":30,"105":0,"106":0,"107":0,"109":false,"110":false,"111":false}}'
  ```

* Logs from `pytuya.Device.status()` method when the grill is off are below.
  The response is essentially empty; just the 20-byte header and 8-byte footer
  with nothing in between. The subsequent poll showed 102=300; not the 320 it
  was set to. So, no ACK/NAK in response to set operations.

  ```
  2020-10-12 09:24:01 DEBUG (SyncWorker_12) [pytuya] json_payload=b'{"devId":"02655252ecfabcxxxxxx","uid":"02655252ecfabc6ad10e","t":"1602509041","dps":{"102":320}}'
  2020-10-12 09:24:01 DEBUG (SyncWorker_12) [pytuya] set_status received data=b'\x00\x00U\xaa\x00\x00\x00\x00\x00\x00\x00\x07\x00\x00\x00\x0c\x00\x00\x00\x00x\x93p\x91\x00\x00\xaaU'
  ```

* The `dps` values in the data to/from the grill are integers (or boolean for
  power and errors); floats or strings don't work. It appears they are used to
  produce a JSON object and the given value is encoded as is so it must match
  the value types the grill expected; no value type conversion in pytuya.

* When the grill is off, the actual and probe temperatures report 0 and
  attempts to set the target temperature are silently ignored.

