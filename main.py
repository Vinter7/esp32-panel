from fastapi import FastAPI
import psutil, wmi, socket, time
import GPUtil

app = FastAPI()
# fastapi dev main.py

cpuinfo = wmi.WMI().Win32_Processor()[0]


# print(cpuinfo)

info = {
    "recognize": True,
    "systemName": cpuinfo.SystemName,
    "cpuName": cpuinfo.Name.strip(),
    "cpuCores": str(cpuinfo.NumberOfLogicalProcessors),
    "cpuFreq": str(round(cpuinfo.MaxClockSpeed / 1000,1)) + "G",
}


def get_net_speed():
    s1 = psutil.net_io_counters().bytes_sent
    r1 = psutil.net_io_counters().bytes_recv
    time.sleep(1)
    s2 = psutil.net_io_counters().bytes_sent
    r2 = psutil.net_io_counters().bytes_recv
    sb = (s2 - s1) / 1024
    rb = (r2 - r1) / 1024

    if sb > 1024:
        sb = str(sb / 1024)[:4] + "M"
    else:
        sb = str(sb)[:4] + "K"
    if rb > 1024:
        rb = str(rb / 1024)[:4] + "M"
    else:
        rb = str(rb)[:4] + "K"

    return sb, rb


@app.get("/")
def getroot():
    mem = psutil.virtual_memory()
    gpuinfo = GPUtil.getGPUs()[0]
    info["cpuPercent"] = str(psutil.cpu_percent()) + "%"

    info["gpuName"] = gpuinfo.name
    info["gpuTemp"] = str(round(gpuinfo.temperature)) + "C"
    # info["gpuMemTotal"] = str(round(gpuinfo.memoryTotal / 1000, 2)) + "GB"
    # info["gpuMemUsed"] = str(round(gpuinfo.memoryUsed / 1000, 2)) + "GB"
    # info["gpuMemPercent"] = str(round(gpuinfo.memoryUtil * 100, 1)) + "%"
    info["gpuPercent"] = str(round(gpuinfo.load * 100,1)) + "%"

    info["memPercent"] = str(mem.percent) + "%"
    info["memUsed"] = str(round(mem.used / 1024 / 1024 / 1024, 2)) + "G"
    info["memTotal"] = str(round(mem.total / 1024 / 1024 / 1024, 2)) + "G"

    # info['ip'] = socket.gethostbyname(socket.gethostname())
    info["ip"] = socket.gethostbyname(info["systemName"])
    # print(socket.gethostname())
    info["send"], info["recv"] = get_net_speed()

    # try:
    #     info["temprature"] = psutil.sensors_temperatures()
    # except:
    #     info["temprature"] = psutil.sensors_battery()

    return info
