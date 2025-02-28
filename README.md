# Home Assistant Integration for WD MyCloud NAS

A custom Home Assistant integration for Western Digital MyCloud NAS devices that provides detailed monitoring and control capabilities.

## Features

- **System Information**: Monitor device details including model, hostname, capacity, and serial number
- **Status Monitoring**: Track system status, temperature, SMART status, and overall health
- **Storage Details**: View storage usage statistics for total space, used space, and media categories
- **Media Status**: Monitor media indexing progress for videos, photos, and music
- **Power Management**: 
  - Control HDD standby mode
  - Remote reboot and shutdown capabilities
- **Hardware Control**:
  - Toggle LED status
  - Monitor and adjust HDD standby settings
- **Firmware Information**: View current firmware details and update status

## Installation

1. Copy the `custom_components/wd_mycloud` folder to your Home Assistant `custom_components` directory
2. Restart Home Assistant
3. Go to Configuration -> Integrations
4. Click the "+ ADD INTEGRATION" button
5. Search for "WD MyCloud"
6. Enter your device's IP address/hostname, username, and password

## Configuration Options

- **Update Interval**: Customize how often the integration polls your device (10-300 seconds)
- **LED Control**: Toggle device LED through Home Assistant
- **HDD Standby**: Configure hard drive power saving settings

## Supported Entities

### Sensors
- System information (model, hostname, capacity, etc.)
- System state (temperature, SMART status, etc.)
- Storage usage statistics
- Firmware information

### Switches
- LED control
- HDD standby mode

### Buttons
- System reboot
- System shutdown

## Requirements

- Home Assistant 2023.8.0 or newer
- WD MyCloud NAS device with firmware 4.0 or newer
- Network access to your WD MyCloud device

## Translation Support

Currently available in:
- English
- Swedish

## Note

This is an unofficial integration and is not affiliated with Western Digital. Use at your own risk.
