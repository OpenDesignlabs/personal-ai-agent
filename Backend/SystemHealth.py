import subprocess
import os
import logging

def get_system_stats():
    """Returns a dictionary with CPU, RAM, and Battery stats on Windows using PowerShell."""
    try:
        # Construct a more robust PowerShell command
        ps_cmd = (
            "Get-CimInstance Win32_Processor | Select-Object -ExpandProperty LoadPercentage; "
            "Get-CimInstance Win32_OperatingSystem | Select-Object FreePhysicalMemory, TotalVisibleMemorySize; "
            "Get-CimInstance Win32_Battery | Select-Object EstimatedChargeRemaining"
        )
        
        # Use full path to powershell to avoid 9009 errors
        system_root = os.environ.get('SystemRoot', 'C:\\Windows')
        powershell_path = os.path.join(system_root, 'System32\\WindowsPowerShell\\v1.0\\powershell.exe')
        
        process = subprocess.Popen(
            [powershell_path, "-Command", ps_cmd],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            shell=False 
        )
        stdout, stderr = process.communicate(timeout=5)
        
        if process.returncode != 0:
            logging.error(f"PowerShell Error: {stderr}")
            return {"CPU": "N/A", "RAM": "N/A", "Battery": "N/A"}

        output = stdout.strip().split('\n')
        
        # Parse CPU
        cpu_usage = output[0].strip() if len(output) > 0 else "0"
        
        # Parse RAM
        ram_info = output[1].strip() if len(output) > 1 else ""
        free_kb = 0
        total_kb = 1
        if "FreePhysicalMemory" in ram_info:
            parts = ram_info.replace("@{", "").replace("}", "").split(";")
            for p in parts:
                if "FreePhysicalMemory=" in p:
                    free_kb = int(p.split("=")[1])
                if "TotalVisibleMemorySize=" in p:
                    total_kb = int(p.split("=")[1])
        
        ram_usage = round(((total_kb - free_kb) / total_kb) * 100, 1) if total_kb > 0 else 0
        
        # Parse Battery
        battery_usage = "N/A"
        if len(output) > 2 and "EstimatedChargeRemaining" in output[2]:
            battery_usage = output[2].split("=")[1].replace("}", "").strip() + "%"

        return {
            "CPU": f"{cpu_usage}%",
            "RAM": f"{ram_usage}%",
            "Battery": battery_usage
        }
    except Exception as e:
        logging.error(f"Error getting system stats: {e}")
        return {"CPU": "N/A", "RAM": "N/A", "Battery": "N/A"}

if __name__ == "__main__":
    print(get_system_stats())
