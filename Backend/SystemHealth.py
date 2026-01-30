import subprocess
import os
import logging

def get_system_stats():
    """Returns a dictionary with CPU, RAM, and Battery stats on Windows using PowerShell."""
    try:
        # Requesting specific properties in a cleaner list format
        ps_cmd = (
            "Get-CimInstance Win32_Processor | Select-Object -ExpandProperty LoadPercentage; "
            "Get-CimInstance Win32_OperatingSystem | Select-Object FreePhysicalMemory, TotalVisibleMemorySize | Format-List; "
            "Get-CimInstance Win32_Battery | Select-Object EstimatedChargeRemaining | Format-List"
        )
        
        system_root = os.environ.get('SystemRoot', 'C:\\Windows')
        powershell_path = os.path.join(system_root, 'System32\\WindowsPowerShell\\v1.0\\powershell.exe')
        
        process = subprocess.Popen(
            [powershell_path, "-NoProfile", "-Command", ps_cmd],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding='utf-8', # Use UTF-8 for better encoding support
            shell=False 
        )
        stdout, stderr = process.communicate(timeout=5)
        
        if not stdout:
            return {"CPU": "0%", "RAM": "0%", "Battery": "N/A"}

        lines = [line.strip() for line in stdout.split('\n') if line.strip()]
        
        cpu_usage = "0"
        free_mem = 0
        total_mem = 0
        battery = "N/A"

        for line in lines:
            if line.isdigit() and int(line) <= 100:
                cpu_usage = line
            elif "FreePhysicalMemory" in line:
                free_mem = int(line.split(":")[1].strip())
            elif "TotalVisibleMemorySize" in line:
                total_mem = int(line.split(":")[1].strip())
            elif "EstimatedChargeRemaining" in line:
                battery = line.split(":")[1].strip() + "%"

        ram_perc = "0%"
        if total_mem > 0:
            ram_perc = f"{round(((total_mem - free_mem) / total_mem) * 100, 1)}%"

        return {
            "CPU": f"{cpu_usage}%",
            "RAM": ram_perc,
            "Battery": battery
        }
    except Exception as e:
        logging.error(f"Error getting system stats: {e}")
        return {"CPU": "N/A", "RAM": "N/A", "Battery": "N/A"}

if __name__ == "__main__":
    print(get_system_stats())
