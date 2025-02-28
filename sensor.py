from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, CoordinatorEntity
import logging
from datetime import timedelta
from .const import DOMAIN, SCAN_INTERVAL

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(seconds=60)  # Ändra till timedelta-objekt

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the WD MyCloud sensors."""
    client = hass.data[DOMAIN][config_entry.entry_id]

    # Get scan interval from options and convert to timedelta
    scan_interval_seconds = config_entry.options.get("scan_interval", SCAN_INTERVAL.total_seconds())
    update_interval = timedelta(seconds=scan_interval_seconds)

    async def async_update_data():
        """Fetch data from API."""
        data = {}
        data["system_info"] = await hass.async_add_executor_job(client.get_system_info)
        data["system_state"] = await hass.async_add_executor_job(client.get_system_state)
        data["storage_usage"] = await hass.async_add_executor_job(client.get_storage_usage)
        data["media_status"] = await hass.async_add_executor_job(client.get_media_status)
        data["firmware_info"] = await hass.async_add_executor_job(client.get_firmware_info)
        return data

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name="wd_mycloud",
        update_method=async_update_data,
        update_interval=update_interval,
    )

    # Fetch initial data
    await coordinator.async_config_entry_first_refresh()

    entities = []
    
    # System info sensors
    for key in ["Model", "Host Name", "Capacity", "Serial Number"]:
        entities.append(WDMyCloudSensor(
            coordinator, 
            config_entry.entry_id, 
            "system_info",
            key,
            "system_info"
        ))

    # Firmware info sensors
    for key in ["Firmware Name", "Firmware Version", "Firmware Description", "Last Upgrade", "Update Available"]:
        entities.append(WDMyCloudSensor(
            coordinator,
            config_entry.entry_id,
            "firmware_info",
            key,
            "firmware"
        ))

    # System state sensors
    for key in ["Status", "Temperature", "SMART", "Overall"]:
        entities.append(WDMyCloudSensor(
            coordinator, 
            config_entry.entry_id,
            "system_state",
            key,
            "system_state"
        ))

    # Storage usage sensors
    for key in ["Total Size", "Used Space", "Video", "Photos", "Music"]:
        entities.append(WDMyCloudSensor(
            coordinator,
            config_entry.entry_id,
            "storage_usage",
            key,
            "storage"
        ))

    async_add_entities(entities)


class WDMyCloudSensor(CoordinatorEntity, SensorEntity):
    """Representation of a WD MyCloud sensor."""

    def __init__(self, coordinator, entry_id, data_type, key, device_class):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._entry_id = entry_id
        self._data_type = data_type
        self._key = key
        self._attr_name = f"WD MyCloud {key}"
        self._attr_unique_id = f"{entry_id}_{data_type}_{key}".lower()
        self._attr_device_class = device_class

    @property
    def native_value(self):
        """Return the state of the sensor."""
        if self.coordinator.data and self._data_type in self.coordinator.data:
            return self.coordinator.data[self._data_type].get(self._key)
        return None

    @property
    def device_info(self):
        """Return device information."""
        return {
            "identifiers": {(DOMAIN, self._entry_id)},
            "name": "WD MyCloud",
            "manufacturer": "Western Digital",
        }
