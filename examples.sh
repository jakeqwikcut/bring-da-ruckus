#!/bin/bash
# 36 Chambers of Chaos - Example Configurations
# Bring Da Ruckus on Ubuntu Server
# Wu-Tang Sword Style
#
# Created by Jake Mammen - 2025
# 🥷 Wu-Tang is for the children. Test responsibly. 🥷
#
# This file shows how to configure bring-da-ruckus for different setups# =============================================================================
# BASIC USAGE - THE CHAMBERS
# =============================================================================

# Chamber 0: Peace (Normal Network - No disruption)
sudo python3 bring-da-ruckus.py --level peace

# Chamber 1: The Swarm (Light Disruption)
sudo python3 bring-da-ruckus.py --interface eth0 --level first

# Chamber 9: The Mystery (Moderate Chaos)
sudo python3 bring-da-ruckus.py --interface eth0 --level ninth

# Chamber 18: The Deadly Venoms (Heavy Ruckus)
sudo python3 bring-da-ruckus.py --interface eth0 --level eighteenth

# Chamber 36: Liquid Swords (Extreme Chaos)
sudo python3 bring-da-ruckus.py --interface eth0 --level thirtysixth

# Shaolin Shadow: Total Darkness (Complete Outage)
sudo python3 bring-da-ruckus.py --interface eth0 --level shaolin

# =============================================================================
# ADVANCED CONFIGURATIONS - ENTER THE CHAMBERS
# =============================================================================

# Example 1: Chamber 36 with Heavy Disruption and Extended Timeout
sudo python3 bring-da-ruckus.py \
  --interface eth0 \
  --level thirtysixth \
  --timeout 15

# Example 2: Long-Term Chamber 9 Testing with Extended Timeout
sudo python3 bring-da-ruckus.py \
  --interface eth0 \
  --level ninth \
  --timeout 60

# Example 3: Shaolin Shadow with Short Timeout (Total Darkness)
sudo python3 bring-da-ruckus.py \
  --interface eth0 \
  --level shaolin \
  --timeout 5

# =============================================================================
# FINDING YOUR NETWORK INTERFACE
# =============================================================================

# List all interfaces:
ip link show

# Or with more detail:
ip addr show

# Or show just interface names:
ls /sys/class/net/

# Find the default route interface:
ip route show default

# Check which interface is UP:
ip link show | grep "state UP"

# =============================================================================
# TESTING SPECIFIC SCENARIOS - PROGRESS THROUGH THE CHAMBERS
# =============================================================================

# Scenario: Simulating Poor Rural Internet (Chamber 36)
sudo python3 bring-da-ruckus.py --level thirtysixth --timeout 30

# Scenario: Testing Upload Queue with Bandwidth Limit (Chamber 9)
sudo python3 bring-da-ruckus.py --level ninth --timeout 45

# Scenario: Complete Outage Test (Shaolin Shadow - 15 min timeout for safety)
sudo python3 bring-da-ruckus.py --level shaolin --timeout 15

# Scenario: Light Network Congestion (Chamber 1 - 1 hour test)
sudo python3 bring-da-ruckus.py --level first --timeout 60

# =============================================================================
# QWIKCUT-SPECIFIC EXAMPLES - BRINGING DA RUCKUS TO YOUR CAMERA
# =============================================================================

# Test Case 1: Chamber 9 - The Mystery (typical test)
sudo python3 bring-da-ruckus.py \
  --interface eth0 \
  --level ninth \
  --timeout 30

# Test Case 2: Testing S3 upload resilience (Chamber 18 - Heavy disruption)
sudo python3 bring-da-ruckus.py \
  --interface eth0 \
  --level eighteenth \
  --timeout 20

# Test Case 3: WebSocket command latency test (Chamber 1 - Light disruption)
sudo python3 bring-da-ruckus.py \
  --interface eth0 \
  --level first \
  --timeout 15

# Test Case 4: Complete network failure and recovery (Shaolin Shadow)
sudo python3 bring-da-ruckus.py \
  --interface eth0 \
  --level shaolin \
  --timeout 10

# =============================================================================
# SAFETY CONFIGURATIONS - PROTECT YA NECK
# =============================================================================

# Very Short Timeout (5 min) for Initial Testing - Chamber 1
sudo python3 bring-da-ruckus.py --level first --timeout 5

# Standard Timeout (30 min) for Regular Testing - Chamber 9
sudo python3 bring-da-ruckus.py --level ninth --timeout 30

# Extended Timeout (90 min) for Long-Duration Tests - Chamber 1
sudo python3 bring-da-ruckus.py --level first --timeout 90
# =============================================================================
# COMMON INTERFACE NAMES ON UBUNTU/LINUX
# =============================================================================

# Traditional naming:
#   eth0, eth1, eth2...     - Ethernet interfaces
#   wlan0, wlan1...         - Wireless interfaces

# Predictable naming (Ubuntu 16.04+):
#   eno1, eno2...           - Onboard Ethernet
#   enp0s3, enp0s8...       - PCI Ethernet (common in VMs)
#   ens33, ens34...         - Another predictable naming scheme
#   enx[MAC]...             - USB Ethernet adapters

# Special interfaces:
#   lo                      - Loopback (don't use this!)
#   br0, br1...             - Bridge interfaces
#   docker0                 - Docker bridge
#   tun0, tap0              - VPN/Tunnel interfaces
#   "vEthernet (Default Switch)" - Hyper-V virtual switch

# =============================================================================
# VALIDATION COMMANDS
# =============================================================================

# Test if disruption is working (run in separate SSH session):

# Continuous ping test to see latency/loss:
ping -c 100 192.168.1.100

# Or continuous:
ping 192.168.1.100

# Show active traffic control rules:
sudo tc qdisc show dev eth0

# Show detailed tc statistics:
sudo tc -s qdisc show dev eth0

# Bandwidth test (requires iperf3 on both machines):
iperf3 -c 192.168.1.100

# Test HTTP download speed:
wget -O /dev/null http://192.168.1.100/test-file

# Monitor network with ping while applying disruptions:
watch -n 1 ping -c 3 192.168.1.100
