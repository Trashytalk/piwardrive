Hardware Setup
==============
.. note::
   Please read the legal notice in the project `README.md` before using PiWardrive.

MPU-6050 Wiring
---------------
The MPU-6050 orientation sensor connects via I\ :sup:`2`\ C. Wire the module to the Raspberry Pi pins as shown below.

.. mermaid::

   graph TD
       VCC[MPU-6050 VCC] --> Pi3V3[Pi 3V3]
       GND[MPU-6050 GND] --> PiGND[Pi GND]
       SDA[MPU-6050 SDA] --> PiSDA[Pi SDA (GPIO2)]
       SCL[MPU-6050 SCL] --> PiSCL[Pi SCL (GPIO3)]

GPS Module Wiring
-----------------
A typical serial GPS module uses the Pi's UART interface.

.. mermaid::

   graph TD
       GPSVCC[GPS VCC] --> Pi3V3
       GPSGND[GPS GND] --> PiGND
       GPSTX[GPS TX] --> PiRX[Pi RXD (GPIO15)]
       GPSRX[GPS RX] --> PiTX[Pi TXD (GPIO14)]
