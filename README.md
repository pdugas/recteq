# Home Assistant Recteq Integration

Custom integration for [recteq][recteq] grills and smokers providing a climate
entity to control the unit and sensor entities for the probes.

[![hacs-badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)
[![issue-badge](https://img.shields.io/github/issues/pdugas/recteq)](https://github.com/pdugas/recteq/issues)
[![pr-badge](https://img.shields.io/github/issues-pr/pdugas/recteq)](https://github.com/pdugas/recteq/issues)
[![release-badge](https://img.shields.io/github/v/release/pdugas/recteq?sort=semver)](https://github.com/pdugas/recteq/releases/latest)
[![commit-badge](https://img.shields.io/github/last-commit/pdugas/recteq)](https://github.com/pdugas/recteq/commit/main)
[![license-badge](https://img.shields.io/github/license/pdugas/recteq)](https://github.com/pdugas/recteq/blob/main/LICENSE)
[![commits-badge](https://img.shields.io/github/commits-since/pdugas/recteq/latest/main?sort=semver)](https://github.com/pdugas/recteq/commits/main)

> **NOTE** - This isn't supported or approved by [recteq][recteq] at all!

![climate](img/climate.png)

![entities](img/entities.png)

## Installation

We recommend you install [HACS](https://hacs.xyz/) first, then add
<https://github.com/pdugas/recteq> as a custom integration repository and
finally, add the integration from there.

Instead, if you prefer the manual route, you could download a copy of the
[latest release][latest] and unpack the contents into into
`config/custom_components/recteq/` on your HA machine. Feeling adventurous?
Using `git clone` in `config/custom_components/` to pull the project from
Github works too.

In either case, you need to restart HS once it's installed. Then you need to
[configure](#configuration) it.

## Configuration

This integration is configured using the UI only; no changes in
`configuration.yaml` are needed. Navigate to Configuration > Integrations and
tap the red "+" button in the bottom right. Search for and select the "Rectec"
entry. You'll get the dialog shown below. Enter the details for your grill and
tap "Submit".

![config](img/config.png)

Repeat the process if you have multiple grills to control. _(ps: I'm jealous!)_

## IP Address, Device ID & Local Key

The IP address of your grill can usually be found if you dig into the logs
for your DHCP server. Poke around on your router for that. Mine registered
using `ESP_######` as the name where the part after the "_" is part of the MAC
address. Alternatively, you could run `tcpdump -n port 6666 or port 6667` to
listen for the broadcasts. The grill broadcasts on port 6666 (older 3.1
protocol) or 6667 (newer 3.3 protocol) periodically.

[tuyapower project](https://github.com/jasonacox/tuyapower) can be used to scan
more intelligently for Tuya devices (the embedded controller in the recteq) on
your network. The IP address it shows (10.0.0.100 below) is the one you want.
The ID value in the output is the 20-digit device ID needed. The product value
in the output **_is not the local key_**!

```shell
# python -m tuyapower
TuyaPower (Tuya compatible smart plug scanner) [0.0.25] tinytuya [1.0.3]

Scanning on UDP ports 6666 and 6667 for devices (15 retries)...

FOUND Device [Valid payload]: 10.0.0.100
    ID = 00000000000000000000, product = XXXXXXXXXXXXXXXX, Version = 3.3
    Device Key required to poll for stats

Scan Complete!  Found 1 devices.
```

[tuyapower](https://github.com/jasonacox/tuya) has some notes on how to get
the local key but I found it on my Android phone much easier. I connect it via
USB to my laptop, allow MTP access, then I can browse the filesystem on the
phone. I found `Phone/Android/data/com.ym.rectecgrill/cache/1.abj` has logs
from the app and includes JSON-formatted messages that include a `localKey`
property. That's the 16-digit local key value needed here.

> **NOTE** - Hey recteq, if you're listenting, please just expose this value in
> the app!

## Change Log

* 0.0.2 
  * HACS support
  * README additions
* 0.0.1 
  * Initial release candidate
  * Works for me. Looking for others to test.

## License

Copyright (c) 2020 Paul Dugas

See [LICENSE](LICENSE) for details.

## Support

Submit [issues](https://github.com/pdugas/recteq/issues) for defects, feature
requests or questions. I'll try to help as I can.

## Credits

I'm Paul Dugas, <paul@dugas.cc>. This is my first HA integration so be gentle!

I learned this was possible from [`SDNick484/rectec_status`][rectec_status] and
based the intial versions of the project on his examples. Much thanks to
[SDNick](https://github.com/SDNick484/) along with those he credits;
[codetheweb](https://github.com/codetheweb/),
[clach04](https://github.com/clach04),
[blackrozes](https://github.com/blackrozes),
[jepsonrob](https://github.com/jepsonrob), and all the other contributors on
tuyapi and python-tuya who have made communicating to Tuya devices possible
with open source code.

[recteq]: https://www.recteq.com/
[latest]: https://github.com/pdugas/recteq/releases/latest
[rectec_status]: https://github.com/SDNick484/rectec_status
