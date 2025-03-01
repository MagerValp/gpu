#!/usr/local/munkireport/munkireport-python2

"""
GPU  info for munkireport.
Will return all details about connected GPUs and video cards
"""

import subprocess
import os
import plistlib
import sys


def get_gpu_info():
    '''Uses system profiler to get GPU info for this machine.'''
    cmd = ['/usr/sbin/system_profiler', 'SPDisplaysDataType', '-xml']
    proc = subprocess.Popen(cmd, shell=False, bufsize=-1,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (output, unused_error) = proc.communicate()
    try:
        plist = plistlib.readPlistFromString(output)
        # system_profiler xml is an array
        sp_dict = plist[0]
        items = sp_dict['_items']
        return items
    except Exception:
        return {}

def flatten_gpu_info(array):
    '''Un-nest GPUs, return array with objects with relevant keys'''
    out = []
    for obj in array:
        device = {'model': '','metal': 0}
        for item in obj:
            if item == '_items':
                out = out + flatten_gpu_info(obj['_items'])
            elif item == 'spdisplays_device-id':
                device['device_id'] = obj[item]
            elif item == 'spdisplays_gmux-version':
                device['gmux_version'] = obj[item]
            elif item == 'spdisplays_efi-version':
                device['efi_version'] = obj[item]
            elif item == 'spdisplays_pcie_width':
                device['pcie_width'] = obj[item]
            elif item == 'spdisplays_revision-id':
                device['revision_id'] = obj[item]
            elif item == 'spdisplays_rom-revision':
                device['rom_revision'] = obj[item]
            elif item == 'spdisplays_vendor':
                device['vendor'] = obj[item]
            elif item == 'spdisplays_vram_shared':
                device['vram_shared'] = obj[item]
            elif item == 'spdisplays_vram':
                device['vram'] = obj[item]
            elif item == 'sppci_model':
                device['model'] = obj[item]
            elif item == 'sppci_cores':
                device['num_cores'] = obj[item]
            elif item == 'sppci_slot_name':
                device['slot_name'] = obj[item]
            elif item == 'spdisplays_ndrvs':
                device['ndrvs'] = obj[item]
            elif item == 'spdisplays_metalfamily' and obj[item] == 'spdisplays_mtlgpufamilymac1':
                device['metal'] = 8
            elif item == 'spdisplays_metalfamily' and obj[item] == 'spdisplays_mtlgpufamilyapple7':
                device['metal'] = 7
            elif item == 'spdisplays_metalfamily' and obj[item] == 'spdisplays_mtlgpufamilymac2':
                device['metal'] = 6
            elif item == 'spdisplays_metal' and obj[item] == 'spdisplays_metalfeaturesetfamily21':
                device['metal'] = 5
            elif item == 'spdisplays_metal' and obj[item] == 'spdisplays_metalfeaturesetfamily14':
                device['metal'] = 4
            elif item == 'spdisplays_metal' and obj[item] == 'spdisplays_metalfeaturesetfamily13':
                device['metal'] = 3 
            elif item == 'spdisplays_metal' and obj[item] == 'spdisplays_metalfeaturesetfamily12':
                device['metal'] = 2
            elif item == 'spdisplays_metal' and (obj[item] == 'spdisplays_supported' or obj[item] == 'spdisplays_metalfeaturesetfamily11'):
                device['metal'] = 1
        out.append(device)
    return out
    

def main():
    """Main"""
    # Create cache dir if it does not exist
    cachedir = '%s/cache' % os.path.dirname(os.path.realpath(__file__))
    if not os.path.exists(cachedir):
        os.makedirs(cachedir)

    # Skip manual check
    if len(sys.argv) > 1:
        if sys.argv[1] == 'manualcheck':
            print 'Manual check: skipping'
            exit(0)

    # Get results
    result = dict()
    info = get_gpu_info()
    result = flatten_gpu_info(info)
    
    # Write GPU results to cache
    output_plist = os.path.join(cachedir, 'gpuinfo.plist')
    plistlib.writePlist(result, output_plist)
    #print plistlib.writePlistToString(result)


if __name__ == "__main__":
    main()
