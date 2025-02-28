import requests
import xml.etree.ElementTree as ET
from urllib.parse import urljoin
import time
from getpass import getpass

class MyCloudClient:
    def __init__(self, host):
        """Initialize MyCloud client with host address"""
        self.host = host if host.startswith('http') else f'http://{host}'
        self.session = requests.Session()
        self.session.headers.update({
            'Accept': 'text/plain, */*; q=0.01',
            'Accept-Language': 'en',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': f'{self.host}/UI/'
        })

    def login(self, username, password):
        """Login to the MyCloud device"""
        login_url = urljoin(self.host, f'/api/2.1/rest/local_login')
        params = {
            'username': username,
            'password': password,
            '_': int(time.time() * 1000)
        }
        
        response = self.session.get(login_url, params=params)
        if response.status_code == 200:
            return True
        return False

    def get_device_info(self):
        """Get device information"""
        device_url = urljoin(self.host, '/api/2.1/rest/device')
        params = {'_': int(time.time() * 1000)}
        
        response = self.session.get(device_url, params=params)
        if response.status_code == 200:
            try:
                root = ET.fromstring(response.text)
                info = {
                    'Device Type': root.find('device_type').text,
                    'Communication': root.find('communication_status').text,
                    'Remote Access': root.find('remote_access').text,
                    'Internal Port': root.find('internal_port').text,
                    'SSL Port': root.find('internal_ssl_port').text
                }
                return info
            except ET.ParseError:
                return None
        return None

    def get_system_info(self):
        """Get system information"""
        info_url = urljoin(self.host, '/api/2.1/rest/system_information')
        params = {'_': int(time.time() * 1000)}
        
        response = self.session.get(info_url, params=params)
        if response.status_code == 200:
            try:
                root = ET.fromstring(response.text)
                info = {
                    'Manufacturer': root.find('manufacturer').text,
                    'Model': root.find('model_description').text,
                    'Host Name': root.find('host_name').text,
                    'Capacity': root.find('capacity').text,
                    'Serial Number': root.find('serial_number').text,
                    'MAC Address': root.find('mac_address').text
                }
                return info
            except ET.ParseError:
                return None
        return None

    def get_system_state(self):
        """Get system state"""
        state_url = urljoin(self.host, '/api/2.1/rest/system_state')
        params = {'_': int(time.time() * 1000)}
        
        response = self.session.get(state_url, params=params)
        if response.status_code == 200:
            try:
                root = ET.fromstring(response.text)
                state = {
                    'Status': root.find('status').text,
                    'Temperature': root.find('temperature').text,
                    'SMART': root.find('smart').text,
                    'Volume': root.find('volume').text,
                    'Free Space': root.find('free_space').text,
                    'Overall': root.find('reported_status').text
                }
                return state
            except ET.ParseError:
                return None
        return None

    def get_media_status(self):
        """Get media crawler status and counts"""
        media_url = urljoin(self.host, '/api/2.1/rest/mediacrawler_status')
        params = {'_': int(time.time() * 1000)}
        
        response = self.session.get(media_url, params=params)
        if response.status_code == 200:
            try:
                root = ET.fromstring(response.text)
                volume = root.find('.//volume')
                media = {}
                
                for category in volume.findall('.//category'):
                    cat_type = category.find('category_type').text
                    media[cat_type] = {
                        'Total': category.find('total').text,
                        'Processed': category.find('extracted_count').text
                    }
                
                return {
                    'Volume State': volume.find('volume_state').text,
                    'Media': media
                }
            except ET.ParseError:
                return None
        return None

    def convert_bytes(self, bytes_value):
        """Convert bytes to human readable format"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes_value < 1024:
                return f"{bytes_value:.2f} {unit}"
            bytes_value /= 1024
        return f"{bytes_value:.2f} TB"

    def get_storage_usage(self):
        """Get storage usage information"""
        usage_url = urljoin(self.host, '/api/2.1/rest/storage_usage')
        params = {'_': int(time.time() * 1000)}
        
        response = self.session.get(usage_url, params=params)
        if response.status_code == 200:
            try:
                root = ET.fromstring(response.text)
                usage = {
                    'Total Size': int(root.find('size').text),
                    'Used Space': int(root.find('usage').text),
                    'Video': int(root.find('video').text),
                    'Photos': int(root.find('photos').text),
                    'Music': int(root.find('music').text),
                    'Other': int(root.find('other').text)
                }
                
                # Convert all values to human readable format
                return {k: self.convert_bytes(v) for k, v in usage.items()}
            except ET.ParseError:
                return None
        return None

    def get_led_status(self):
        """Get LED configuration status"""
        led_url = urljoin(self.host, '/api/2.1/rest/led_configuration')
        params = {'_': int(time.time() * 1000)}
        
        response = self.session.get(led_url, params=params)
        if response.status_code == 200:
            try:
                root = ET.fromstring(response.text)
                return root.find('enable_led').text == 'true'
            except ET.ParseError:
                return None
        return None

    def set_led_status(self, enabled):
        """Set LED configuration status"""
        led_url = urljoin(self.host, '/api/2.1/rest/led_configuration')
        params = {'enable_led': str(enabled).lower()}
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest'
        }
        
        response = self.session.put(led_url, params=params, headers=headers)
        if response.status_code == 200:
            try:
                root = ET.fromstring(response.text)
                return root.find('status').text.lower() == 'success'
            except ET.ParseError:
                return False
        return False

    def get_hdd_standby(self):
        """Get HDD standby configuration"""
        standby_url = urljoin(self.host, '/api/2.1/rest/hdd_standby_time')
        params = {'_': int(time.time() * 1000)}
        
        response = self.session.get(standby_url, params=params)
        if response.status_code == 200:
            try:
                root = ET.fromstring(response.text)
                return {
                    'enabled': root.find('enable_hdd_standby').text == 'true',
                    'minutes': int(root.find('hdd_standby_time_minutes').text)
                }
            except ET.ParseError:
                return None
        return None

    def set_hdd_standby(self, enabled, minutes=10):
        """Set HDD standby configuration"""
        standby_url = urljoin(self.host, '/api/2.1/rest/hdd_standby_time')
        params = {
            'enable_hdd_standby': str(enabled).lower(),
            'hdd_standby_time_minutes': minutes
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest'
        }
        
        response = self.session.put(standby_url, params=params, headers=headers)
        if response.status_code == 200:
            try:
                root = ET.fromstring(response.text)
                return root.find('status').text.lower() == 'success'
            except ET.ParseError:
                return False
        return False

    def reboot_system(self):
        """Reboot the NAS system"""
        reboot_url = urljoin(self.host, '/api/2.1/rest/shutdown')
        params = {'state': 'reboot'}
        headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
        
        response = self.session.put(reboot_url, params=params, headers=headers)
        if response.status_code == 200:
            try:
                root = ET.fromstring(response.text)
                return root.find('status').text == 'success'
            except ET.ParseError:
                return False
        return False

    def shutdown_system(self):
        """Shutdown the NAS system"""
        shutdown_url = urljoin(self.host, '/api/2.1/rest/shutdown')
        params = {'state': 'halt'}
        headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
        
        response = self.session.put(shutdown_url, params=params, headers=headers)
        if response.status_code == 200:
            try:
                root = ET.fromstring(response.text)
                return root.find('status').text == 'success'
            except ET.ParseError:
                return False
        return False

    def get_firmware_info(self):
        """Get firmware information"""
        firmware_url = urljoin(self.host, '/api/2.1/rest/firmware_info')
        params = {'_': int(time.time() * 1000)}
        
        response = self.session.get(firmware_url, params=params)
        if response.status_code == 200:
            try:
                root = ET.fromstring(response.text)
                current_firmware = root.find('.//current_firmware/package')
                update_info = root.find('.//firmware_update_available')
                
                info = {
                    'Firmware Name': current_firmware.find('name').text.strip(),
                    'Firmware Version': current_firmware.find('version').text,
                    'Firmware Description': current_firmware.find('description').text,
                    'Last Upgrade': time.strftime(
                        '%Y-%m-%d %H:%M:%S',
                        time.localtime(int(current_firmware.find('last_upgrade_time').text))
                    ),
                    'Update Available': update_info.find('available').text == 'true'
                }
                return info
            except ET.ParseError:
                return None
        return None

def display_menu():
    """Display the main menu options"""
    print("\nWD MyCloud Meny")
    print("---------------")
    print("1. Visa systeminformation")
    print("2. Visa systemstatus")
    print("3. Visa lagringsinformation")
    print("4. Visa mediastatus")
    print("5. Hantera HDD standby")
    print("6. Hantera LED status")
    print("7. Starta om enheten")
    print("8. Stäng av enheten")
    print("0. Avsluta")
    return input("\nVälj ett alternativ (0-8): ")

def handle_menu(client, choice):
    """Handle menu selection"""
    if choice == "1":
        system_info = client.get_system_info()
        if system_info:
            print("\nSystem Information:")
            for key, value in system_info.items():
                print(f"{key}: {value}")
    
    elif choice == "2":
        system_state = client.get_system_state()
        if system_state:
            print("\nSystem Status:")
            for key, value in system_state.items():
                print(f"{key}: {value}")
    
    elif choice == "3":
        storage = client.get_storage_usage()
        if storage:
            print("\nStorage Usage:")
            for key, value in storage.items():
                print(f"{key}: {value}")
    
    elif choice == "4":
        media_status = client.get_media_status()
        if media_status:
            print("\nMedia Status:")
            print(f"Volume State: {media_status['Volume State']}")
            print("\nMedia Counts:")
            for media_type, counts in media_status['Media'].items():
                print(f"{media_type.title()}: {counts['Processed']}/{counts['Total']}")
    
    elif choice == "5":
        hdd_standby = client.get_hdd_standby()
        if hdd_standby is not None:
            print("\nHDD Standby Settings:")
            print(f"Enabled: {hdd_standby['enabled']}")
            print(f"Standby Time: {hdd_standby['minutes']} minutes")
            
            if input("\nVill du ändra HDD standby inställningar? (j/n): ").lower() == 'j':
                new_enabled = input("Aktivera HDD standby? (j/n): ").lower() == 'j'
                if new_enabled:
                    try:
                        new_minutes = int(input("Ange antal minuter för standby (10-60): "))
                        if 10 <= new_minutes <= 60:
                            if client.set_hdd_standby(new_enabled, new_minutes):
                                print("HDD standby inställningar uppdaterade")
                            else:
                                print("Kunde inte uppdatera HDD standby inställningar")
                        else:
                            print("Ogiltigt antal minuter. Måste vara mellan 10-60.")
                    except ValueError:
                        print("Ogiltigt värde för minuter")
                else:
                    if client.set_hdd_standby(new_enabled):
                        print("HDD standby inaktiverat")
                    else:
                        print("Kunde inte uppdatera HDD standby inställningar")
    
    elif choice == "6":
        led_status = client.get_led_status()
        if led_status is not None:
            print("\nLED Status:")
            print(f"LED Enabled: {led_status}")
            
            if input("\nVill du ändra LED status? (j/n): ").lower() == 'j':
                new_status = not led_status
                if client.set_led_status(new_status):
                    print(f"LED status ändrad till: {new_status}")
                else:
                    print("Kunde inte ändra LED status")
    
    elif choice == "7":
        if input("Är du säker på att du vill starta om? (j/n): ").lower() == 'j':
            if client.reboot_system():
                print("Enheten startar om...")
                return False  # Exit program after reboot
            else:
                print("Kunde inte starta om enheten")
    
    elif choice == "8":
        if input("Är du säker på att du vill stänga av? (j/n): ").lower() == 'j':
            confirm = input("Detta kommer att stänga av enheten helt. Fortsätt? (j/n): ").lower()
            if confirm == 'j':
                if client.shutdown_system():
                    print("Enheten stängs av...")
                    return False
                else:
                    print("Kunde inte stänga av enheten")
    
    return True  # Continue program

def main():
    print("WD MyCloud NAS Client")
    print("--------------------")
    
    ip = input("Ange IP-adress (t.ex. 192.168.1.19): ")
    username = input("Ange användarnamn: ")
    password = getpass("Ange lösenord: ")
    
    client = MyCloudClient(ip)
    if client.login(username, password):
        print("\nLogin successful")
        
        while True:
            choice = display_menu()
            if choice == "0":
                print("\nAvslutar programmet...")
                break
            elif choice in ["1", "2", "3", "4", "5", "6", "7", "8"]:
                if not handle_menu(client, choice):
                    break  # Break if reboot or shutdown was initiated
            else:
                print("\nOgiltigt val, försök igen")
    else:
        print("\nLogin failed")

if __name__ == '__main__':
    main()
