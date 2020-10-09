# Home Assistant Recteq Integration

Custom integration for [recteq][recteq] grills and smokers providing a climate
entity to control the unit and sensor entities for the probes.

> **NOTE** - This isn't supported or approved by [recteq][recteq] at all!

## Installation

Download a copy of the [latest release][latest] and unpack the contents into 
into `config/custom_components/recteq/` on your HA machine then restart it.

You can also add <https://github.com/pdugas/recteq> as a custom repostory in 
[HACS](https://hacs.xyz/) instead if you like.

## Configuration

This integration is configured using the UI only. Navigate to Configuration >
Integrations and tap the red "+" button in the bottom right. Search for and
select the "Rectec" entry. You'll get the dialog shown below. Enter the
details for your grill and tap "Submit".

## License

Copyright (c) 2020 Paul Dugas

See [LICENSE](LICENSE) for details.

## Support

Submit [issues](https://github.com/pdugas/recteq/issues) for defects, feature
requests or questions. I'll try to help as I can.

[recteq]: https://www.recteq.com/
[latest]: https://github.com/pdugas/recteq/releases/latest
[rectec_status]: https://github.com/SDNick484/rectec_status
