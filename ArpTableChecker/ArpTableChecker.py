import os
import tkinter as tk
from tkinter import scrolledtext
from datetime import datetime

config_filename = 'config.txt'
log_filename = 'changes.log'

def scan_arp_table():
    arp_table = os.popen('arp -a').read()
    return arp_table

def parse_arp_table(arp_table):
    lines = arp_table.split('\n')[3:]
    arp_dict = {}
    for line in lines:
        if line:
            parts = line.split()
            ip = parts[0].strip()
            mac = parts[1].replace('-', ':').strip()
            arp_dict[ip] = mac
    return arp_dict



def display_arp_table():
    arp_table = scan_arp_table()
    display_window("ARP таблиця", arp_table)

def load_config():
    try:
        with open(config_filename, 'r') as file:
            config = file.read().split('\n')
            config_dict = {}
            for line in config:
                if line:
                    ip, mac = line.split(': ')
                    config_dict[ip] = mac
            return config_dict
    except FileNotFoundError:
        return {}

def compare_with_config(arp_dict):
    config_dict = load_config()
    new_or_changed = {}
    for ip, mac in arp_dict.items():
        if ip not in config_dict or config_dict[ip] != mac:
            new_or_changed[ip] = mac
    return new_or_changed

def log_changes(changes):
    with open(log_filename, 'a') as file:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        for ip, mac in changes.items():
            file.write(f'[{timestamp}] {ip}: {mac}\n')

def display_changes():
    arp_table = scan_arp_table()
    arp_dict = parse_arp_table(arp_table)
    changes = compare_with_config(arp_dict)
    if changes:
        log_changes(changes)
        changes_text = '\n'.join([f'{ip}: {mac}' for ip, mac in changes.items()])
        display_window("Зміни MAC адресу", changes_text)
    else:
        display_window("Змін немає", "Змін немає")

def clear_changes():
    global changes_mac_address
    changes_mac_address = ""

def display_window(title, message):
    window = tk.Toplevel(root)
    window.title(title)

    text_area = scrolledtext.ScrolledText(window, wrap=tk.WORD)
    text_area.insert(tk.END, message)
    text_area.pack(expand=True, fill='both')


def main():
    global root
    global changes_mac_address
    changes_mac_address = ""

    root = tk.Tk()
    root.title("ARP Таблиця та Зміни")

    btn_get_arp = tk.Button(root, text="Вивести ARP таблицю", command=display_arp_table)
    btn_get_arp.pack(pady=5)

    btn_show_changes = tk.Button(root, text="Вивести зміни MAC адресу", command=display_changes)
    btn_show_changes.pack(pady=5)

    btn_clear_changes = tk.Button(root, text="Очистити зміни", command=clear_changes)
    btn_clear_changes.pack(pady=5)


    root.mainloop()


main()