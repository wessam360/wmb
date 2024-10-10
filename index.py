#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
import argparse
import logging
import socket
from random import choice
from Crypto.Cipher import AES
from ipaddress import ip_address, AddressValueError

# Set up logging for better traceability
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def pad(data_to_pad, block_size):
    """Apply zero-padding to the data to match block size."""
    padding_len = block_size - len(data_to_pad) % block_size
    return data_to_pad + b'\x00' * padding_len

def unpad(padded_data, block_size):
    """Remove padding from the data (works for null-terminated strings)."""
    return padded_data[:-block_size] + padded_data[-block_size:].rstrip(b'\x00')

class WebFac:
    def __init__(self, ip, port, user, pw, aes_key_pool):
        self.ip = ip
        self.port = port
        self.user = user
        self.pw = pw
        self.aes_key_pool = aes_key_pool
        self.aes_key = self.select_aes_key()

    def select_aes_key(self):
        """Select a random AES key from the pool."""
        logging.debug("Selecting a random AES key from the pool")
        return bytes([choice(self.aes_key_pool) for _ in range(16)])

    def encrypt(self, data):
        """Encrypt the provided data using AES encryption."""
        logging.info("Encrypting data")
        cipher = AES.new(self.aes_key, AES.MODE_ECB)
        return cipher.encrypt(pad(data, AES.block_size))

    def decrypt(self, encrypted_data):
        """Decrypt the provided data using AES encryption."""
        logging.info("Decrypting data")
        cipher = AES.new(self.aes_key, AES.MODE_ECB)
        return unpad(cipher.decrypt(encrypted_data), AES.block_size)

def validate_ip(ip):
    """Validate the IP address format."""
    try:
        ip_address(ip)
        logging.debug(f"Valid IP address: {ip}")
        return True
    except AddressValueError:
        logging.error(f"Invalid IP address: {ip}")
        return False

def validate_port(port):
    """Validate the port number."""
    if 1 <= port <= 65535:
        logging.debug(f"Valid port: {port}")
        return True
    else:
        logging.error(f"Invalid port: {port}. Must be between 1 and 65535.")
        return False

def dealTelnet(ip, port, user, pw, action):
    """Handle the telnet operation."""
    if validate_ip(ip) and validate_port(port):
        try:
            logging.info(f"Attempting to {action} telnet on {ip}:{port} with user {user}")
            # Your telnet logic here
            # For example, establishing a telnet connection and executing commands
        except socket.error as e:
            logging.error(f"Telnet connection error: {e}")
        except Exception as e:
            logging.error(f"An error occurred: {e}")

def dealSerial(ip, port, user, pw, action):
    """Handle the serial operation."""
    if validate_ip(ip) and validate_port(port):
        try:
            logging.info(f"Attempting to {action} serial on {ip}:{port} with user {user}")
            # Your serial logic here
        except socket.error as e:
            logging.error(f"Serial connection error: {e}")
        except Exception as e:
            logging.error(f"An error occurred: {e}")

def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description='Router Factory Mode Control', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    
    parser.add_argument('--user', '-u', nargs='+', help='factory mode auth username', default=[
        'factorymode', "CMCCAdmin", "CUAdmin", "telecomadmin", "cqadmin", "user", "admin", "cuadmin", "lnadmin", "useradmin"])
    parser.add_argument('--pass', '-p', metavar='PASS', dest='pw', nargs='+', help='factory mode auth password', default=[
        'nE%jA@5b', "aDm8H%MdA", "CUAdmin", "nE7jA%5m", "cqunicom", "1620@CTCC", "1620@CUcc", "admintelecom", "cuadmin", "lnadmin"])
    parser.add_argument('--ip', help='Router IP address', default="192.168.1.1")
    parser.add_argument('--port', help='Router HTTP port', type=int, default=80)
    
    subparsers = parser.add_subparsers(dest='cmd', title='subcommands', description='valid subcommands', help='supported commands')
    
    telnet_parser = subparsers.add_parser("telnet", help='Control telnet services on/off', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    telnet_parser.add_argument('action', nargs="?", choices=['open', 'close'], help='action', default='open')
    
    serial_parser = subparsers.add_parser("serial", help='Control /proc/serial on/off', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    serial_parser.add_argument('action', nargs="?", choices=['open', 'close'], help='action', default='open')
    
    return parser.parse_args()

def main():
    """Main execution entry point."""
    args = parse_args()
    
    aes_key_pool = [0x7B, 0x56, 0xB0, 0xF7, 0xDA, 0x0E, 0x68, 0x52, 0xC8, 0x19,
                    0xF3, 0x2B, 0x84, 0x90, 0x79, 0xE5, 0x62, 0xF8, 0xEA, 0xD2]  # Example AES Key pool

    web_fac = WebFac(args.ip, args.port, args.user, args.pw, aes_key_pool)
    
    if args.cmd == 'serial':
        dealSerial(args.ip, args.port, args.user, args.pw, args.action)
    elif args.cmd == 'telnet':
        dealTelnet(args.ip, args.port, args.user, args.pw, args.action)

if __name__ == '__main__':
    main()
