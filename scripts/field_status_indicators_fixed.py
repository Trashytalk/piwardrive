#!/usr/bin/env python3
"""
Field Status Indicators - Visual and Audio Status Feedback
Provides LED indicators, audio alerts, and display feedback for field operations
"""

import logging
import subprocess
import time
from enum import Enum
from threading import Thread
from typing import Dict

# Try to import GPIO - fallback to simulation if not available
try:
    import RPi.GPIO as GPIO
    GPIO_AVAILABLE = True
except ImportError:
    GPIO_AVAILABLE = False

logger = logging.getLogger(__name__)


class LEDColor(Enum):
    """LED Color definitions"""
    GREEN = "green"
    YELLOW = "yellow"
    RED = "red"
    BLUE = "blue"


class LEDPattern(Enum):
    """LED Pattern definitions"""
    SOLID = "solid"
    BLINK_SLOW = "blink_slow"
    BLINK_FAST = "blink_fast"
    PULSE = "pulse"


class SystemStatus(Enum):
    """System status definitions"""
    STARTING = "starting"
    RUNNING = "running"
    WARNING = "warning"
    ERROR = "error"
    NETWORK_ISSUE = "network_issue"
    GPS_ISSUE = "gps_issue"
    STORAGE_LOW = "storage_low"
    OVERHEATING = "overheating"
    DIAGNOSTIC_MODE = "diagnostic_mode"
    SHUTDOWN = "shutdown"


class LEDStatusController:
    """Controls LED status indicators"""
    
    # GPIO pin assignments for LEDs
    LED_PINS = {
        LEDColor.GREEN: 18,
        LEDColor.YELLOW: 19,
        LEDColor.RED: 20,
        LEDColor.BLUE: 21
    }
    
    def __init__(self):
        self.running = False
        self.current_status = None
        self.led_threads: Dict[LEDColor, Thread] = {}
        
        if GPIO_AVAILABLE:
            self._setup_gpio()
        else:
            logger.warning("GPIO not available - using console output for LED simulation")
    
    def _setup_gpio(self):
        """Setup GPIO pins for LED control"""
        GPIO.setmode(GPIO.BCM)
        
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
        
        # Stop all LED patterns
        self._stop_all_leds()
        
        # Wait for threads to complete
        for thread in self.led_threads.values():
            if thread.is_alive():
                thread.join(timeout=1)
        
        if GPIO_AVAILABLE:
            GPIO.cleanup()
        
        logger.info("LED Status Controller stopped")
    
    def set_status(self, status: SystemStatus):
        """Set system status and update LEDs accordingly"""
        if status == self.current_status:
            return
        
        self.current_status = status
        self._stop_all_leds()
        
        # Status to LED pattern mapping
        status_patterns = {
            SystemStatus.STARTING: [(LEDColor.BLUE, LEDPattern.PULSE)],
            SystemStatus.RUNNING: [(LEDColor.GREEN, LEDPattern.SOLID)],
            SystemStatus.WARNING: [(LEDColor.YELLOW, LEDPattern.BLINK_SLOW)],
            SystemStatus.ERROR: [(LEDColor.RED, LEDPattern.BLINK_FAST)],
            SystemStatus.NETWORK_ISSUE: [(LEDColor.YELLOW, LEDPattern.BLINK_FAST), (LEDColor.RED, LEDPattern.BLINK_SLOW)],
            SystemStatus.GPS_ISSUE: [(LEDColor.BLUE, LEDPattern.BLINK_FAST)],
            SystemStatus.STORAGE_LOW: [(LEDColor.YELLOW, LEDPattern.PULSE)],
            SystemStatus.OVERHEATING: [(LEDColor.RED, LEDPattern.SOLID)],
            SystemStatus.DIAGNOSTIC_MODE: [(LEDColor.BLUE, LEDPattern.BLINK_SLOW)],
            SystemStatus.SHUTDOWN: [(LEDColor.RED, LEDPattern.PULSE)]
        }
        
        patterns = status_patterns.get(status, [])
        for color, pattern in patterns:
            self._set_led_pattern(color, pattern)
    
    def _stop_all_leds(self):
        """Stop all LED patterns"""
        for color in LEDColor:
            if color in self.led_threads:
                # Signal thread to stop (will be handled by thread check)
                pass
            
            if GPIO_AVAILABLE:
                GPIO.output(self.LED_PINS[color], GPIO.LOW)
    
    def _set_led_pattern(self, color: LEDColor, pattern: LEDPattern):
        """Set LED pattern for specific color"""
        if pattern == LEDPattern.SOLID and color in self.led_threads:
            # Stop existing thread first
            if GPIO_AVAILABLE:
                GPIO.output(self.LED_PINS[color], GPIO.LOW)
            else:
                print(f"LED {color.value}: OFF")
            return
        
        # Start new pattern thread
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
            
            while (self.running and 
                   self.led_threads.get(color) == Thread.current_thread()):
                time.sleep(0.1)
        
        elif pattern == LEDPattern.BLINK_SLOW:
            while (self.running and 
                   self.led_threads.get(color) == Thread.current_thread()):
                if GPIO_AVAILABLE:
                    GPIO.output(pin, GPIO.HIGH)
                else:
                    print(f"LED {color.value}: ON")
                
                time.sleep(1.0)
                
                if not (self.running and 
                        self.led_threads.get(color) == Thread.current_thread()):
                    break
                
                if GPIO_AVAILABLE:
                    GPIO.output(pin, GPIO.LOW)
                else:
                    print(f"LED {color.value}: OFF")
                
                time.sleep(1.0)
        
        elif pattern == LEDPattern.BLINK_FAST:
            while (self.running and 
                   self.led_threads.get(color) == Thread.current_thread()):
                if GPIO_AVAILABLE:
                    GPIO.output(pin, GPIO.HIGH)
                else:
                    print(f"LED {color.value}: ON")
                
                time.sleep(0.2)
                
                if not (self.running and 
                        self.led_threads.get(color) == Thread.current_thread()):
                    break
                
                if GPIO_AVAILABLE:
                    GPIO.output(pin, GPIO.LOW)
                else:
                    print(f"LED {color.value}: OFF")
                
                time.sleep(0.2)
        
        elif pattern == LEDPattern.PULSE:
            # Implement PWM pulse pattern
            if GPIO_AVAILABLE:
                try:
                    # Set up PWM with frequency of 1000Hz
                    pwm = GPIO.PWM(pin, 1000)
                    pwm.start(0)  # Start with 0% duty cycle
                    
                    while (self.running and 
                           self.led_threads.get(color) == Thread.current_thread()):
                        # Fade in
                        for duty_cycle in range(0, 101, 5):  # 0 to 100% in steps of 5
                            if not (self.running and 
                                   self.led_threads.get(color) == Thread.current_thread()):
                                break
                            pwm.ChangeDutyCycle(duty_cycle)
                            time.sleep(0.02)  # 20ms per step
                        
                        # Fade out
                        for duty_cycle in range(100, -1, -5):  # 100 to 0% in steps of 5
                            if not (self.running and 
                                   self.led_threads.get(color) == Thread.current_thread()):
                                break
                            pwm.ChangeDutyCycle(duty_cycle)
                            time.sleep(0.02)  # 20ms per step
                        
                        # Brief pause before next pulse
                        time.sleep(0.1)
                    
                    pwm.stop()
                    
                except Exception as e:
                    logger.error(f"PWM pulse error: {e}")
                    # Fallback to simple on/off pattern
                    while (self.running and 
                           self.led_threads.get(color) == Thread.current_thread()):
                        GPIO.output(pin, GPIO.HIGH)
                        time.sleep(0.5)
                        if not (self.running and 
                               self.led_threads.get(color) == Thread.current_thread()):
                            break
                        GPIO.output(pin, GPIO.LOW)
                        time.sleep(0.5)
            else:
                # Software simulation of PWM pulse
                while (self.running and 
                       self.led_threads.get(color) == Thread.current_thread()):
                    # Simulate fade in
                    for intensity in range(0, 21):  # 0 to 20 intensity levels
                        if not (self.running and 
                               self.led_threads.get(color) == Thread.current_thread()):
                            break
                        brightness = "█" * intensity + "░" * (20 - intensity)
                        print(f"LED {color.value}: PULSE [{brightness}] {intensity*5}%")
                        time.sleep(0.02)
                    
                    # Simulate fade out
                    for intensity in range(20, -1, -1):  # 20 to 0 intensity levels
                        if not (self.running and 
                               self.led_threads.get(color) == Thread.current_thread()):
                            break
                        brightness = "█" * intensity + "░" * (20 - intensity)
                        print(f"LED {color.value}: PULSE [{brightness}] {intensity*5}%")
                        time.sleep(0.02)
                    
                    # Brief pause
                    time.sleep(0.1)
        
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
        
        for i in range(count):
            try:
                # Try using system beep
                subprocess.run(['beep', '-f', '1000', '-l', str(int(duration * 1000))], 
                              check=False, capture_output=True)
            except FileNotFoundError:
                # Fallback to console bell
                print('\a', end='', flush=True)
            
            if i < count - 1:
                time.sleep(interval)
    
    def alert_pattern(self, pattern: str):
        """Play specific alert pattern"""
        patterns = {
            'startup': lambda: self.beep(1, 0.2),
            'warning': lambda: self.beep(2, 0.1, 0.1),
            'error': lambda: self.beep(3, 0.2, 0.1),
            'shutdown': lambda: self.beep(1, 0.5)
        }
        
        if pattern in patterns:
            patterns[pattern]()


class StatusDisplayController:
    """Controls status display (LCD/OLED if available)"""
    
    def __init__(self):
        self.display_available = False
        self.current_message = ""
        
        # Try to detect display hardware
        self._detect_display()
    
    def _detect_display(self):
        """Detect available display hardware"""
        # Check for I2C displays
        try:
            result = subprocess.run(['i2cdetect', '-y', '1'], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0 and ('3c' in result.stdout or '27' in result.stdout):
                self.display_available = True
                logger.info("Display hardware detected")
        except:
            pass
    
    def show_message(self, message: str, duration: float = 0):
        """Show message on display"""
        self.current_message = message
        
        if self.display_available:
            # TODO: Implement actual display code
            logger.info(f"Display: {message}")
        else:
            print(f"STATUS: {message}")
        
        if duration > 0:
            time.sleep(duration)
            self.clear()
    
    def clear(self):
        """Clear the display"""
        self.current_message = ""
        if self.display_available:
            # TODO: Implement actual display clear
            logger.info("Display: CLEARED")
        else:
            print("STATUS: CLEARED")


class FieldStatusIndicator:
    """Main field status indicator controller"""
    
    def __init__(self):
        self.led_controller = LEDStatusController()
        self.audio_controller = AudioAlertController()
        self.display_controller = StatusDisplayController()
        
        self.running = False
    
    def start(self):
        """Start all status indicators"""
        self.running = True
        self.led_controller.start()
        self.audio_controller.alert_pattern('startup')
        self.display_controller.show_message("PiWardrive Starting...", 2)
        logger.info("Field Status Indicator started")
    
    def stop(self):
        """Stop all status indicators"""
        self.running = False
        self.led_controller.stop()
        self.audio_controller.alert_pattern('shutdown')
        self.display_controller.show_message("PiWardrive Shutdown", 2)
        logger.info("Field Status Indicator stopped")
    
    def set_status(self, status: SystemStatus, message: str = None):
        """Set system status across all indicators"""
        self.led_controller.set_status(status)
        
        # Audio alerts for important status changes
        if status == SystemStatus.ERROR:
            self.audio_controller.alert_pattern('error')
        elif status == SystemStatus.WARNING:
            self.audio_controller.alert_pattern('warning')
        
        # Display message
        if message:
            self.display_controller.show_message(message)
        else:
            status_messages = {
                SystemStatus.STARTING: "Starting up...",
                SystemStatus.RUNNING: "System running",
                SystemStatus.WARNING: "Warning condition",
                SystemStatus.ERROR: "Error detected",
                SystemStatus.NETWORK_ISSUE: "Network problem",
                SystemStatus.GPS_ISSUE: "GPS problem",
                SystemStatus.STORAGE_LOW: "Storage low",
                SystemStatus.OVERHEATING: "Overheating",
                SystemStatus.DIAGNOSTIC_MODE: "Diagnostic mode",
                SystemStatus.SHUTDOWN: "Shutting down"
            }
            self.display_controller.show_message(
                status_messages.get(status, f"Status: {status.value}")
            )


def test_status_indicators():
    """Test all status indicators"""
    indicator = FieldStatusIndicator()
    
    try:
        indicator.start()
        
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
            indicator.set_status(status)
            time.sleep(3)
        
        indicator.set_status(SystemStatus.RUNNING)
        time.sleep(2)
        
    finally:
        indicator.stop()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    test_status_indicators()
