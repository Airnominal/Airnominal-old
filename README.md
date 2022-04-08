# Airnominal

An open platform for collection and collaborative sharing of air quality data.

## About

The problem of air pollution is one of the most acutely dangerous ecological problems we face today. According to studies made by World Health Organization, almost all of the global population breathe air that exceeds WHO guideline limits containing high levels of pollutants. Even though sensors and other measurement equipment is already available, data that researchers use usually comes from two to three stations in an area, and large datasets of high spatial resolution are not available. To test if any solution addressing air quality is effective, researchers need to be able to obtain many higher quality data in a standardized format.

To address this problem, we built an open platform of air quality measuring stations that enables people to connect and exchange air quality measurements and design an open measuring station that anyone can build and connect to the platform, thus providing valuable information for the research and limiting of the main causes of high PM particles concentration.

The platform is publicly deployed at [`zrak.gimvic.org`](https://zrak.gimvic.org).

## Features

- [x] Easy station registration and setup
- [x] Viewing all stations on a list and a map
- [x] Viewing station's measurements and locations
- [x] Comparing measurements from multiple stations
- [x] Support for arbitrary measurement types (partial)
- [ ] Better stations management (editing, removing, etc.)
- [ ] Better stations list (filtering, searching, sorting, etc.)

## Usage

### Registering Stations

You can access the [station registration](https://zrak.gimvic.org/stations/register) page with a button in the top-right corner of the website. You need to enter details about the station (name and description), as well as specify which sensors the station provides. After registering the station, you will receive a station config with the API key which you need to use to configure the station. Please see the [boards documentation](boards/README.md) for more details about configuring the station.

**Important:** Once you create a station, you currently cannot modify or remove it. This includes not being able to rename the station or add new sensors. Please be sure the provided information is correct before submitting a form. We are working hard to improve the stability of the service and implement missing station management features.

### Viewing Measurements

You can view a list of registered stations, as well as the map of their latest locations. Clicking on the station will open the measurements page, where you can view current measurements, charts with all historical data and a map with station's current and past location. If you do not want specific display type, you can disable it through the settings page.

By default, charts display data from the last hour, but you can also choose other intervals, as well as select arbitrary datetime range. Your range will be stored in the URL, so you can share it with others. This can be disabled in settings. You can move in a chart using `Alt+Drag`, and select a range using `Ctrl+Drag`.  Charts support zooming with a scroll-wheel, and gestures on touch devices.

You can also compare data from multiple stations, although this currently requires manually editing the page URL, for example, [`/stations/view/3,4`](https://zrak.gimvic.org/stations/view/3,4) for comparing stations `3` and `4`.

## Development

Check READMEs in subdirectories for details:

- [Arduino library](boards/README.md)
- [Backend](API/README.md)
- [Frontend](website/README.md)
