import psutil, os, string,gpiozero

def cpu_percent(once=False):
    """
    cpu_percant get loads of all cpu cores
    :param once: if true -> return full cpu load
    :return: percent
    """ 
    if once:
        return psutil.cpu_percent()
    return psutil.cpu_percent(percpu=True)

def cpu_count(logical=False):
    """
    cpu_count get cpu cores count
    :param logical: if true -> return logical cores
    :return: number of cores
    """ 
    if logical:
        return psutil.cpu_count()
    return psutil.cpu_count(logical=False)

def cpu_freq():
    """
    cpu_freq get frequency of cpu
    :return: CPU frequency in MHz
    """ 
    return round(psutil.cpu_freq().current)

def disk_data(disk="C",used=False):
    """
    disk_data get disk data
    :param disk: choose disk to get data
    :param used: return only used disk space
    :return: GB of disk space
    """ 
    if used:
        return round(psutil.disk_usage(f"{disk}://").used/1024/1024/1024,2)
    return round(psutil.disk_usage(f"{disk}://").total/1024/1024/1024,2)

def disk_using_percentage(disk="C"):
    """
    disk_using get disk data of using
    :param disk: choose disk to get data
    :return: percent of disk using
    """ 
    return round(psutil.disk_usage(f"{disk}://").percent,2)

def ram_data(used=False):
    """
    ram_data get ram data
    :param used: return only used ram
    :return: GB of ram
    """ 
    if used:
        return round(psutil.virtual_memory().used/1024/1024/1024,2)
    return round(psutil.virtual_memory().total/1024/1024/1024,2)

def ram_using_percentage():
    """
    ram_using get percentage use of ram
    :return: percent of ram use
    """ 
    return round(psutil.virtual_memory().percent,2)


def get_avaible_drives():
    """
    get_avaible_drives return in-use drive letters of windows 
    :return: List of strings
    """ 
    return ['%s' % d for d in string.ascii_uppercase if os.path.exists('%s:' % d)]

def disk_get_all_using_percentage():
    """
    disk_get_all_using_percentage gets data of percent load from all disks
    :return: percent of load
    """ 
    all_disk_volume = 0
    all_disk_used = 0
    for i in get_avaible_drives():
        all_disk_volume+=disk_data(disk=i,used = False)
        all_disk_used+=disk_data(disk=i,used = True)
    return round((all_disk_used/all_disk_volume)*100)

def disk_get_all_disk_data(used= False):
    """
    disk_get_all_disk_data gets all datas
    :param used: if true return only used gbs
    :return: return gbs
    """ 
    data = 0
    if used:
        for i in get_avaible_drives():
            data = data+ disk_data(i,True)
    else:
        for i in get_avaible_drives():
            data = data+ disk_data(i,False)
    return round(data,2)

def battery_percent():
    """
    battery_percent gets battery charge percent
    :return: if battery in component, return percent, if no - return False
    """ 
    data = psutil.sensors_battery()
    if data != None:
        return data.percent()
    else:
        return False