from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from .const import DOMAIN

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the WD MyCloud switches."""
    client = hass.data[DOMAIN][config_entry.entry_id]
    
    entities = [
        WDMyCloudLEDSwitch(client, config_entry.entry_id),
        WDMyCloudHDDStandbySwitch(client, config_entry.entry_id)
    ]
    
    async_add_entities(entities)

class WDMyCloudLEDSwitch(SwitchEntity):
    """Representation of WD MyCloud LED switch."""

    def __init__(self, client, entry_id):
        """Initialize the LED switch."""
        self._client = client
        self._entry_id = entry_id
        self._attr_name = "WD MyCloud LED"
        self._attr_unique_id = f"{entry_id}_led"
        self._state = None

    @property
    def device_info(self):
        """Return device information."""
        return {
            "identifiers": {(DOMAIN, self._entry_id)},
            "name": "WD MyCloud",
            "manufacturer": "Western Digital",
        }

    async def async_update(self) -> None:
        """Fetch new state data for the switch."""
        self._state = await self.hass.async_add_executor_job(
            self._client.get_led_status
        )

    @property
    def is_on(self) -> bool:
        """Return true if switch is on."""
        return self._state

    async def async_turn_on(self, **kwargs) -> None:
        """Turn the switch on."""
        await self.hass.async_add_executor_job(
            self._client.set_led_status, True
        )

    async def async_turn_off(self, **kwargs) -> None:
        """Turn the switch off."""
        await self.hass.async_add_executor_job(
            self._client.set_led_status, False
        )

class WDMyCloudHDDStandbySwitch(SwitchEntity):
    """Representation of WD MyCloud HDD Standby switch."""

    def __init__(self, client, entry_id):
        """Initialize the HDD standby switch."""
        self._client = client
        self._entry_id = entry_id
        self._attr_name = "WD MyCloud HDD Standby"
        self._attr_unique_id = f"{entry_id}_hdd_standby"
        self._state = None

    @property
    def device_info(self):
        """Return device information."""
        return {
            "identifiers": {(DOMAIN, self._entry_id)},
            "name": "WD MyCloud",
            "manufacturer": "Western Digital",
        }

    async def async_update(self) -> None:
        """Fetch new state data for the switch."""
        standby_info = await self.hass.async_add_executor_job(
            self._client.get_hdd_standby
        )
        if standby_info:
            self._state = standby_info['enabled']

    @property
    def is_on(self) -> bool:
        """Return true if switch is on."""
        return self._state

    async def async_turn_on(self, **kwargs) -> None:
        """Turn the switch on."""
        await self.hass.async_add_executor_job(
            self._client.set_hdd_standby, True
        )

    async def async_turn_off(self, **kwargs) -> None:
        """Turn the switch off."""
        await self.hass.async_add_executor_job(
            self._client.set_hdd_standby, False
        )
