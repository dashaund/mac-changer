#!/usr/bin/env python


import subprocess
import optparse
import re


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change its MAC address")
    parser.add_option("-m", "--mac", dest="new_mac", help="New MAC address")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("Please specify an interface to change with -i, use -h for help")
    if not options.new_mac:
        parser.error("Please specify a new MAC address with -m, use -h for help")
    return options


def change_mac(interface, new_mac):
    subprocess.call(["ifconfig", interface, "down"])
    print("[+] Taking down the interface")
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    print("[+] Changing MAC address to > " + new_mac)
    subprocess.call(["ifconfig", interface, "up"])
    print("[+] Restoring the interface")


def read_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    mac_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)
    if mac_result:
        return mac_result.group(0)
    else:
        print("[-] Could not read MAC address")


def check_mac(mac_result):
    if not mac_result == options.new_mac:
        print("[-] Failed changing MAC address")
    else:
        print("[+] MAC address changed successfully")


options = get_arguments()
old_mac = read_mac(options.interface)
print("[+] The current MAC address is > "+str(old_mac))
change_mac(options.interface, options.new_mac)
mac_result = read_mac(options.interface)
check_mac(mac_result)
print("[+] The new MAC address is > "+str(mac_result))
