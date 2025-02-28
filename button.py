from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from .const import DOMAIN

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the WD MyCloud buttons."""
    client = hass.data[DOMAIN][config_entry.entry_id]
    
    entities = [
        WDMyCloudRebootButton(client, config_entry.entry_id),
        WDMyCloudShutdownButton(client, config_entry.entry_id)
    ]
    
    async_add_entities(entities)

class WDMyCloudRebootButton(ButtonEntity):
    """Representation of WD MyCloud reboot button."""

    def __init__(self, client, entry_id):
        """Initialize the reboot button."""
        self._client = client
        self._entry_id = entry_id
        self._attr_name = "WD MyCloud Reboot"
        self._attr_unique_id = f"{entry_id}_reboot"

    @property
    def device_info(self):
        """Return device information."""
        return {
            "identifiers": {(DOMAIN, self._entry_id)},
            "name": "WD MyCloud",
            "manufacturer": "Western Digital",
        }

    async def async_press(self) -> None:
        """Handle the button press."""
        await self.hass.async_add_executor_job(self._client.reboot_system)

class WDMyCloudShutdownButton(ButtonEntity):
    """Representation of WD MyCloud shutdown button."""

    def __init__(self, client, entry_id):
        """Initialize the shutdown button."""
        self._client = client
        self._entry_id = entry_id
        self._attr_name = "WD MyCloud Shutdown"
        self._attr_unique_id = f"{entry_id}_shutdown"

    @property
    def device_info(self):
        """Return device information."""
        return {
            "identifiers": {(DOMAIN, self._entry_id)},
            "name": "WD MyCloud",
            "manufacturer": "Western Digital",
        }

    async def async_press(self) -> None:
        """Handle the button press."""
        await self.hass.async_add_executor_job(self._client.shutdown_system)
