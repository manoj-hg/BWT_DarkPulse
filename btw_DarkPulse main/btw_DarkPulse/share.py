#!/usr/bin/env python3
"""
Presidency University Attendance System - Sharing Helper
This script helps you share your system on the local network
"""

import socket
import subprocess
import platform
import webbrowser
import time

def get_local_ip():
    """Get the local IP address"""
    try:
        # Create a socket connection to get local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except:
        return "127.0.0.1"

def get_network_info():
    """Get detailed network information"""
    try:
        if platform.system() == "Windows":
            result = subprocess.run(['ipconfig'], capture_output=True, text=True)
            return result.stdout
        else:
            result = subprocess.run(['ifconfig'], capture_output=True, text=True)
            return result.stdout
    except:
        return "Could not get network info"

def create_sharing_links():
    """Create sharing links for different scenarios"""
    local_ip = get_local_ip()
    
    links = {
        "Local Access": f"http://localhost:5000",
        "Network Access": f"http://{local_ip}:5000",
        "Loopback": f"http://127.0.0.1:5000"
    }
    
    return links

def print_sharing_instructions():
    """Print detailed sharing instructions"""
    print("=" * 60)
    print("🎓 PRESIDENCY UNIVERSITY ATTENDANCE SYSTEM - SHARING GUIDE")
    print("=" * 60)
    
    local_ip = get_local_ip()
    links = create_sharing_links()
    
    print(f"\n🌐 YOUR SHARING LINKS:")
    print("-" * 40)
    for name, link in links.items():
        print(f"📎 {name}: {link}")
    
    print(f"\n🔑 LOGIN CREDENTIALS:")
    print("-" * 40)
    print("👤 Guest Access: guest / guest")
    print("👤 Faculty Access: faculty / faculty123")
    print("👤 Admin Access: admin / admin123")
    
    print(f"\n📋 SHARING STEPS:")
    print("-" * 40)
    print("1️⃣ Make sure your system is on the same WiFi/network")
    print("2️⃣ Share this link: " + links["Network Access"])
    print("3️⃣ Others can access using the credentials above")
    print("4️⃣ For mobile access, use the same link on phone browser")
    
    print(f"\n🔧 TROUBLESHOOTING:")
    print("-" * 40)
    print("❌ If others can't connect:")
    print("   • Check Windows Firewall")
    print("   • Make sure port 5000 is open")
    print("   • Verify same network connection")
    print("   • Try disabling VPN temporarily")
    
    print(f"\n📱 MOBILE ACCESS:")
    print("-" * 40)
    print("📲 Open " + links["Network Access"] + " on mobile browser")
    print("📲 System is responsive and works on phones/tablets")
    
    print(f"\n🌍 FOR DEPLOYMENT OPTIONS:")
    print("-" * 40)
    print("📄 See DEPLOYMENT.md file for detailed deployment guide")
    print("☁️ Options: PythonAnywhere, Heroku, VPS, Docker")
    
    print(f"\n✨ QUICK TEST:")
    print("-" * 40)
    print("🧪 Opening your system in browser...")
    webbrowser.open(links["Local Access"])
    
    print("\n" + "=" * 60)
    print("🎓 READY TO SHARE! Your system is accessible!")
    print("=" * 60)

def generate_qr_code():
    """Generate QR code for easy mobile sharing"""
    try:
        import qrcode
        local_ip = get_local_ip()
        qr_url = f"http://{local_ip}:5000"
        
        # Create QR code
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(qr_url)
        qr.make(fit=True)
        
        # Save QR code
        img = qr.make_image(fill_color="blue", back_color="white")
        img.save("attendance_qr.png")
        
        print(f"\n📱 QR Code saved as 'attendance_qr.png'")
        print(f"📲 Others can scan this QR code to access your system")
        
    except ImportError:
        print(f"\n📱 To generate QR code, install: pip install qrcode[pil]")

if __name__ == "__main__":
    print_sharing_instructions()
    
    # Try to generate QR code
    generate_qr_code()
    
    print(f"\n🔄 Keep this script running for easy reference...")
    print(f"📞 Press Ctrl+C to exit")
    
    try:
        while True:
            time.sleep(60)
            local_ip = get_local_ip()
            print(f"📍 Current IP: {local_ip}:5000 (still accessible)")
    except KeyboardInterrupt:
        print(f"\n👋 Goodbye! Your system is still running if you didn't stop it.")
