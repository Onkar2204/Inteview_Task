import socket
import platform
import speedtest
import psutil
import winreg as reg
import uuid
import wmi

def get_installed_software():
    try:
        uninstall_key = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"
        software_list = []

        with reg.OpenKey(reg.HKEY_LOCAL_MACHINE, uninstall_key) as key:
            for i in range(reg.QueryInfoKey(key)[0]):
                try:
                    subkey_name = reg.EnumKey(key, i)
                    with reg.OpenKey(key, subkey_name) as subkey:
                        software_name = reg.QueryValueEx(subkey, "DisplayName")[0]
                        software_list.append(software_name)
                except (FileNotFoundError, PermissionError):
                    pass

        return software_list
    except Exception as e:
        print(f"Error getting installed software: {e}")
        return []


def get_internet_speed():
    try:
        st = speedtest.Speedtest()
        download_speed = st.download() / 1_000_000
        upload_speed = st.upload() / 1_000_000
        return f"Download Speed: {download_speed:.2f} Mbps, Upload Speed: {upload_speed:.2f} Mbps"
    except Exception as e:
        print(f"Error getting internet speed: {e}")
        return None


def get_screen_resolution():
    try:
        w = wmi.WMI()
        desktop_res = w.Win32_DesktopMonitor()
        return [int(desktop_res[0].ScreenWidth), int(desktop_res[0].ScreenHeight)] if desktop_res else None
    except Exception as e:
        print(f"Error getting screen resolution: {e}")
        return None


def get_cpu_info():
    try:
        return {
            "model": platform.processor(),
            "cores": psutil.cpu_count(logical=False),
            "threads": psutil.cpu_count(logical=True),
        }
    except Exception as e:
        print(f"Error getting CPU info: {e}")
        return None


def get_gpu_info():
    try:
        w = wmi.WMI()
        gpu_info = [gpu.Name for gpu in w.Win32_VideoController()]
        return gpu_info[0] if gpu_info else None
    except Exception as e:
        print(f"Error getting GPU info: {e}")
        return None


def get_ram_size():
    try:
        ram = psutil.virtual_memory()
        ram_size_gb = ram.total / (1024 ** 3)
        return f"{ram_size_gb:.2f} GB"
    except Exception as e:
        print(f"Error getting RAM size: {e}")
        return None


def get_screen_size():
    resolution = get_screen_resolution()
    if resolution:
        diagonal_size = round((resolution[0] ** 2 + resolution[1] ** 2) ** 0.5 / 25.4, 2)
        return f"{diagonal_size} inch"
    else:
        return "Screen size information not available"


def get_mac_address():
    try:
        mac = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) for elements in range(5, -1, -1)])
        return mac
    except Exception as e:
        print(f"Error getting MAC address: {e}")
        return None


def get_public_ip():
    try:
        public_ip = socket.gethostbyname(socket.gethostname())
        return public_ip
    except Exception as e:
        print(f"Error getting public IP address: {e}")
        return None


def get_windows_version():
    return platform.version()


def display_info(title, info):
    print(f"\n{title}:\n{info}" if info is not None else f"\n{title}: Error fetching information")


print("Installed Software:")
display_info("Installed Software", ", ".join(get_installed_software()))

print("Internet Speed:")
display_info("Internet Speed", get_internet_speed())

print("Screen Resolution:")
display_info("Screen Resolution", f"{get_screen_resolution()} pixels")

print("CPU Information:")
cpu_info = get_cpu_info()
display_info("CPU Information", f"Model: {cpu_info['model']}\nCores: {cpu_info['cores']}\nThreads: {cpu_info['threads']}")

print("GPU Information:")
display_info("GPU Information", get_gpu_info())

print("RAM Size:")
display_info("RAM Size", get_ram_size())

print("Screen Size:")
display_info("Screen Size", get_screen_size())

print("MAC Address (Ethernet):")
display_info("MAC Address (Ethernet)", get_mac_address())

print("Public IP Address:")
display_info("Public IP Address", get_public_ip())

print("Windows Version:")
display_info("Windows Version", get_windows_version())
