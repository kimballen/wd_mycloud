from homeassistant.const import CONF_HOST, CONF_USERNAME, CONF_PASSWORD, Platform
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from .const import DOMAIN
from .wdmycloud import MyCloudClient

PLATFORMS = [Platform.SENSOR, Platform.SWITCH, Platform.BUTTON]

async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up the WD MyCloud component."""
    hass.data.setdefault(DOMAIN, {})
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up WD MyCloud from a config entry."""
    client = MyCloudClient(entry.data[CONF_HOST])
    
    # Login to the device
    if not await hass.async_add_executor_job(
        client.login, 
        entry.data[CONF_USERNAME], 
        entry.data[CONF_PASSWORD]
    ):
        return False

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = client

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok
