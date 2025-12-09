#!/bin/bash
#
# EMERGENCY RECOVERY SCRIPT
# Run this to clear all network chaos rules if the server is accessible
#
# Usage: sudo ./emergency-recovery.sh
#

set -e

echo "======================================================================"
echo "⚠️  EMERGENCY RECOVERY - Bring Da Ruckus"
echo "======================================================================"
echo ""
echo "This script will:"
echo "  1. Clear all tc (traffic control) rules"
echo "  2. Remove all iptables DROP rules"
echo "  3. Remove SSH protection iptables rules"
echo "  4. Restore network to normal state"
echo ""
echo "Press ENTER to continue or Ctrl+C to abort..."
read

echo ""
echo "🔍 Detecting primary network interface..."
INTERFACE=$(ip route | grep default | awk '{print $5}' | head -n 1)

if [ -z "$INTERFACE" ]; then
    echo "❌ Could not detect network interface"
    echo "Please run manually:"
    echo "   sudo tc qdisc del dev <interface> root"
    exit 1
fi

echo "   Found: $INTERFACE"
echo ""

echo "🧹 Clearing tc rules on $INTERFACE..."
tc qdisc del dev "$INTERFACE" root 2>/dev/null || echo "   (No tc root rules found)"
tc filter del dev "$INTERFACE" 2>/dev/null || echo "   (No tc filters found)"
echo "   ✅ tc rules cleared"
echo ""

echo "🧹 Clearing iptables rules..."
# Flush all chains
iptables -F 2>/dev/null || echo "   (Could not flush chains)"

# Remove SSH protection rules specifically
iptables -D INPUT -p tcp --dport 22 -j ACCEPT 2>/dev/null || echo "   (No SSH INPUT rule)"
iptables -D OUTPUT -p tcp --sport 22 -j ACCEPT 2>/dev/null || echo "   (No SSH OUTPUT rule)"

# List all rules with line numbers and delete DROP rules
echo "   Checking for remaining DROP rules..."
iptables -L INPUT -n --line-numbers | grep DROP | awk '{print $1}' | tac | while read line_num; do
    iptables -D INPUT "$line_num" 2>/dev/null && echo "   Removed INPUT DROP rule #$line_num"
done

iptables -L OUTPUT -n --line-numbers | grep DROP | awk '{print $1}' | tac | while read line_num; do
    iptables -D OUTPUT "$line_num" 2>/dev/null && echo "   Removed OUTPUT DROP rule #$line_num"
done

echo "   ✅ iptables rules cleared"
echo ""

echo "🔍 Current network status:"
echo "   Interface: $INTERFACE"
ip addr show "$INTERFACE" | grep "inet " | awk '{print "   IP: " $2}'
echo ""

echo "🧪 Testing connectivity..."
if ping -c 1 -W 2 8.8.8.8 >/dev/null 2>&1; then
    echo "   ✅ Internet connectivity: WORKING"
else
    echo "   ⚠️  Internet connectivity: FAILED"
    echo "   (May be normal if offline or no internet)"
fi
echo ""

echo "======================================================================"
echo "✅ RECOVERY COMPLETE"
echo "======================================================================"
echo ""
echo "Network should be restored to normal operation."
echo ""
echo "To prevent future lockouts:"
echo "  1. Always run bring-da-ruckus in screen/tmux"
echo "  2. Test SSH protection before using Shaolin Shadow"
echo "  3. Consider using the systemd service for background operation"
echo ""
echo "☯️  Peace has been restored to the chambers"
