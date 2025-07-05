#!/usr/bin/env python3
"""
LED Status Indicator Controller for PiWardrive
Provides visual status indicators for field deployment
"""

import logging
import sys
import time
from enum import Enum
from threading import Thread
from typing import Optional

# Try to import GPIO libraries
try:
    import RPi.GPIO as GPIO
    GPIO_AVAILABLE = True
except ImportError:
    GPIO_AVAILABLE = False
    print("Warning: RPi.GPIO not available. LED control disabled.")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LEDColor(Enum):
    """LED Color definitions"""
    RED = "red"
    GREEN = "green"
    BLUE = "blue"
    YELLOW = "yellow"

class LEDPattern(Enum):
    """LED Pattern definitions"""
    SOLID = "solid"
    BLINK_SLOW = "blink_slow"
    BLINK_FAST = "blink_fast"
    PULSE = "pulse"
    OFF = "off"

class SystemStatus(Enum):
    """System status definitions"""
    STARTING = "starting"
    RUNNING = "running"
    ERROR = "error"
    WARNING = "warning"
    NETWORK_ISSUE = "network_issue"
    GPS_ISSUE = "gps_issue"
    STORAGE_LOW = "storage_low"
    OVERHEATING = "overheating"
    DIAGNOSTIC_MODE = "diagnostic_mode"

class LEDStatusController:
    """Controls LED status indicators"""
    
    # GPIO pin assignments (adjust based on hardware)
    LED_PINS = {
        LEDColor.RED: 18,
        LEDColor.GREEN: 19,
        LEDColor.BLUE: 20,
        LEDColor.YELLOW: 21
    }
    
    def __init__(self):
        self.running = False
        self.current_status = SystemStatus.STARTING
        self.led_threads = {}
        
        if GPIO_AVAILABLE:
            self._setup_gpio()
        else:
            logger.warning("GPIO not available - using console output for LED simulation")
    
    def _setup_gpio(self):
        """Setup GPIO pins for LED control"""
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        
        for color, pin in self.LED_PINS.items():
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.LOW)
    
    def start(self):
        """Start the LED controller"""
        self.running = True
        self.set_status(SystemStatus.STARTING)
        logger.info("LED Status Controller started")
    
    def stop(self):
        """Stop the LED controller"""
        self.running = False
        
        # Stop all LED threads
        for thread in self.led_threads.values():
            if thread.is_alive():
                thread.join(timeout=1)
        
        # Turn off all LEDs
        if GPIO_AVAILABLE:
            for pin in self.LED_PINS.values():
                GPIO.output(pin, GPIO.LOW)
            GPIO.cleanup()
        
        logger.info("LED Status Controller stopped")
    
    def set_status(self, status: SystemStatus):
        """Set system status and update LEDs accordingly"""
        if status == self.current_status:
            return
        
        logger.info(f"Status changed: {self.current_status.value} -> {status.value}")
        self.current_status = status
        
        # Stop all current LED patterns
        self._stop_all_leds()
        
        # Set new LED pattern based on status
        if status == SystemStatus.STARTING:
            self._set_led_pattern(LEDColor.GREEN, LEDPattern.BLINK_SLOW)
            
        elif status == SystemStatus.RUNNING:
            self._set_led_pattern(LEDColor.GREEN, LEDPattern.SOLID)
            
        elif status == SystemStatus.ERROR:
            self._set_led_pattern(LEDColor.RED, LEDPattern.SOLID)
            
        elif status == SystemStatus.WARNING:
            self._set_led_pattern(LEDColor.RED, LEDPattern.BLINK_SLOW)
            
        elif status == SystemStatus.NETWORK_ISSUE:
            self._set_led_pattern(LEDColor.BLUE, LEDPattern.BLINK_FAST)
            
        elif status == SystemStatus.GPS_ISSUE:
            self._set_led_pattern(LEDColor.YELLOW, LEDPattern.SOLID)
            
        elif status == SystemStatus.STORAGE_LOW:
            self._set_led_pattern(LEDColor.YELLOW, LEDPattern.BLINK_SLOW)
            
        elif status == SystemStatus.OVERHEATING:
            self._set_led_pattern(LEDColor.RED, LEDPattern.BLINK_FAST)
            
        elif status == SystemStatus.DIAGNOSTIC_MODE:
            self._set_led_pattern(LEDColor.BLUE, LEDPattern.SOLID)
    
    def _stop_all_leds(self):
        """Stop all LED patterns"""
        for color in LEDColor:
            if color in self.led_threads:
                self.led_threads[color] = None
            
            if GPIO_AVAILABLE:
                GPIO.output(self.LED_PINS[color], GPIO.LOW)
    
    def _set_led_pattern(self, color: LEDColor, pattern: LEDPattern):
        """Set LED pattern for specific color"""
        if pattern == LEDPattern.OFF:
            if GPIO_AVAILABLE:
                GPIO.output(self.LED_PINS[color], GPIO.LOW)
            else:
                print(f"LED {color.value}: OFF")
            return
        
        # Start new thread for this LED pattern
        thread = Thread(target=self._led_pattern_worker, args=(color, pattern))
        thread.daemon = True
        self.led_threads[color] = thread
        thread.start()
    
    def _led_pattern_worker(self, color: LEDColor, pattern: LEDPattern):
        """Worker thread for LED patterns"""
        pin = self.LED_PINS[color]
        
        if pattern == LEDPattern.SOLID:
            if GPIO_AVAILABLE:
                GPIO.output(pin, GPIO.HIGH)
            else:
                print(f"LED {color.value}: SOLID ON")
            
            while self.running and self.led_threads.get(color) == Thread.current_thread():
                time.sleep(0.1)
        
        elif pattern == LEDPattern.BLINK_SLOW:
            while self.running and self.led_threads.get(color) == Thread.current_thread():
                if GPIO_AVAILABLE:
                    GPIO.output(pin, GPIO.HIGH)
                else:
                    print(f"LED {color.value}: ON")
                
                time.sleep(1.0)
                
                if not (self.running and self.led_threads.get(color) == Thread.current_thread()):
                    break
                
                if GPIO_AVAILABLE:
                    GPIO.output(pin, GPIO.LOW)
                else:
                    print(f"LED {color.value}: OFF")
                
                time.sleep(1.0)
        
        elif pattern == LEDPattern.BLINK_FAST:
            while self.running and self.led_threads.get(color) == Thread.current_thread():
                if GPIO_AVAILABLE:
                    GPIO.output(pin, GPIO.HIGH)
                else:
                    print(f"LED {color.value}: ON")
                
                time.sleep(0.2)
                
                if not (self.running and self.led_threads.get(color) == Thread.current_thread()):
                    break
                
                if GPIO_AVAILABLE:
                    GPIO.output(pin, GPIO.LOW)
                else:
                    print(f"LED {color.value}: OFF")
                
                time.sleep(0.2)
        
        elif pattern == LEDPattern.PULSE:
            # TODO: Implement PWM pulse pattern
            pass
        
        # Turn off LED when pattern ends
        if GPIO_AVAILABLE:
            GPIO.output(pin, GPIO.LOW)

class AudioAlertController:
    """Controls audio alerts via system beep"""
    
    def __init__(self):
        self.enabled = True
    
    def beep(self, count: int = 1, duration: float = 0.1, interval: float = 0.1):
        """Generate audio beep"""
        if not self.enabled:
            return
        
        try:
            import os
            for i in range(count):
                # Use system beep command
                os.system(f"beep -l {int(duration * 1000)}")
                if i < count - 1:
                    time.sleep(interval)
        except Exception as e:
            logger.debug(f"Could not generate beep: {e}")
            # Fallback to print
            print(f"BEEP x{count}")
    
    def startup_beep(self):
        """Single beep for startup complete"""
        self.beep(1, 0.2)
    
    def warning_beep(self):
        """Double beep for warning"""
        self.beep(2, 0.1, 0.1)
    
    def error_beep(self):
        """Triple beep for error"""
        self.beep(3, 0.1, 0.1)
    
    def critical_beep(self):
        """Continuous beeping for critical issues"""
        for _ in range(10):
            self.beep(1, 0.1)
            time.sleep(0.1)

class FieldStatusManager:
    """Manages field status indicators and alerts"""
    
    def __init__(self):
        self.led_controller = LEDStatusController()
        self.audio_controller = AudioAlertController()
        self.last_status = None
    
    def start(self):
        """Start the field status manager"""
        self.led_controller.start()
        logger.info("Field Status Manager started")
    
    def stop(self):
        """Stop the field status manager"""
        self.led_controller.stop()
        logger.info("Field Status Manager stopped")
    
    def update_status(self, status: SystemStatus, play_audio: bool = True):
        """Update system status with LEDs and audio"""
        self.led_controller.set_status(status)
        
        if play_audio and status != self.last_status:
            if status == SystemStatus.RUNNING and self.last_status == SystemStatus.STARTING:
                self.audio_controller.startup_beep()
            elif status == SystemStatus.WARNING:
                self.audio_controller.warning_beep()
            elif status == SystemStatus.ERROR:
                self.audio_controller.error_beep()
            elif status in [SystemStatus.OVERHEATING]:
                self.audio_controller.critical_beep()
        
        self.last_status = status
    
    def test_indicators(self):
        """Test all LED and audio indicators"""
        logger.info("Testing status indicators...")
        
        statuses = [
            SystemStatus.STARTING,
            SystemStatus.RUNNING,
            SystemStatus.WARNING,
            SystemStatus.ERROR,
            SystemStatus.NETWORK_ISSUE,
            SystemStatus.GPS_ISSUE,
            SystemStatus.STORAGE_LOW,
            SystemStatus.OVERHEATING,
            SystemStatus.DIAGNOSTIC_MODE
        ]
        
        for status in statuses:
            logger.info(f"Testing status: {status.value}")
            self.update_status(status, play_audio=False)
            time.sleep(2)
        
        # Return to normal status
        self.update_status(SystemStatus.RUNNING)
        logger.info("Indicator test completed")

def main():
    """Main function for testing"""
    import argparse
    
    parser = argparse.ArgumentParser(description='PiWardrive LED Status Controller')
    parser.add_argument('--test', action='store_true', help='Test all indicators')
    parser.add_argument('--status', choices=[s.value for s in SystemStatus], 
                       help='Set specific status')
    parser.add_argument('--daemon', action='store_true', help='Run as daemon')
    
    args = parser.parse_args()
    
    manager = FieldStatusManager()
    
    try:
        manager.start()
        
        if args.test:
            manager.test_indicators()
        elif args.status:
            status = SystemStatus(args.status)
            manager.update_status(status)
            if not args.daemon:
                time.sleep(5)  # Show status for 5 seconds
        elif args.daemon:
            # TODO: Implement daemon mode with system monitoring
            logger.info("Daemon mode not yet implemented")
            while True:
                time.sleep(1)
        else:
            # Default: show running status
            manager.update_status(SystemStatus.RUNNING)
            time.sleep(2)
    
    except KeyboardInterrupt:
        logger.info("Shutting down...")
    finally:
        manager.stop()

if __name__ == '__main__':
    main()
