import time
import navio.mpu9250, navio.ms5611, navio.ublox, navio.util
import spidev, argparse, sys

navio.util.check_apm()

# GPS Initialization
ubl = navio.ublox.UBlox("spi:0.0", baudrate=5000000, timeout=2)

ubl.configure_poll_port()
ubl.configure_poll(navio.ublox.CLASS_CFG, navio.ublox.MSG_CFG_USB)
#ubl.configure_poll(navio.ublox.CLASS_MON, navio.ublox.MSG_MON_HW)

ubl.configure_port(port=navio.ublox.PORT_SERIAL1, inMask=1, outMask=0)
ubl.configure_port(port=navio.ublox.PORT_USB, inMask=1, outMask=1)
ubl.configure_port(port=navio.ublox.PORT_SERIAL2, inMask=1, outMask=0)
ubl.configure_poll_port()
ubl.configure_poll_port(navio.ublox.PORT_SERIAL1)
ubl.configure_poll_port(navio.ublox.PORT_SERIAL2)
ubl.configure_poll_port(navio.ublox.PORT_USB)
ubl.configure_solution_rate(rate_ms=1000)

ubl.set_preferred_dynamic_model(None)
ubl.set_preferred_usePPP(None)

ubl.configure_message_rate(navio.ublox.CLASS_NAV, navio.ublox.MSG_NAV_POSLLH, 1)
ubl.configure_message_rate(navio.ublox.CLASS_NAV, navio.ublox.MSG_NAV_PVT, 1)
ubl.configure_message_rate(navio.ublox.CLASS_NAV, navio.ublox.MSG_NAV_STATUS, 1)
ubl.configure_message_rate(navio.ublox.CLASS_NAV, navio.ublox.MSG_NAV_SOL, 1)
ubl.configure_message_rate(navio.ublox.CLASS_NAV, navio.ublox.MSG_NAV_VELNED, 1)
ubl.configure_message_rate(navio.ublox.CLASS_NAV, navio.ublox.MSG_NAV_SVINFO, 1)
ubl.configure_message_rate(navio.ublox.CLASS_NAV, navio.ublox.MSG_NAV_VELECEF, 1)
ubl.configure_message_rate(navio.ublox.CLASS_NAV, navio.ublox.MSG_NAV_POSECEF, 1)
ubl.configure_message_rate(navio.ublox.CLASS_RXM, navio.ublox.MSG_RXM_RAW, 1)
ubl.configure_message_rate(navio.ublox.CLASS_RXM, navio.ublox.MSG_RXM_SFRB, 1)
ubl.configure_message_rate(navio.ublox.CLASS_RXM, navio.ublox.MSG_RXM_SVSI, 1)
ubl.configure_message_rate(navio.ublox.CLASS_RXM, navio.ublox.MSG_RXM_ALM, 1)
ubl.configure_message_rate(navio.ublox.CLASS_RXM, navio.ublox.MSG_RXM_EPH, 1)
ubl.configure_message_rate(navio.ublox.CLASS_NAV, navio.ublox.MSG_NAV_TIMEGPS, 5)
ubl.configure_message_rate(navio.ublox.CLASS_NAV, navio.ublox.MSG_NAV_CLOCK, 5)
#ubl.configure_message_rate(navio.ublox.CLASS_NAV, navio.ublox.MSG_NAV_DGPS, 5)

# Pressure Initialization
baro = navio.ms5611.MS5611()
baro.initialize()

# IMU Initialization
imu = navio.mpu9250.MPU9250()

while(True):
	# GPS Loop
	msg = ubl.receive_message()
	if msg.name() == "NAV_POSLLH": # Should Provide Lat and Long data
	    outstr = str(msg).split(",")[1:]
	    outstr = "".join(outstr)
	    print(outstr)
	if msg.name() == "NAV_STATUS": # Should Provide fpsFixOK flag to validate speed
	    outstr = str(msg).split(",")[1:2]
	    outstr = "".join(outstr)
	    print(outstr)
	#print(str(msg))
	
	# Barometer Loop
	baro.refreshPressure()
	time.sleep(0.01) # Waiting for pressure data ready 10ms
	baro.readPressure()
	
	baro.refreshTemperature()
	time.sleep(0.01) # Waiting for temperature data ready 10ms
	baro.readTemperature()
	
	baro.calculatePressureAndTemperature()
	
	print "Temperature(C): %.6f" % (baro.TEMP), "Pressure(millibar): %.6f" % (baro.PRES)
	
	# IMU Loop
	m9a, m9g, m9m = imu.getMotion9()
	print " Mag:", "{:+7.3f}".format(m9m[0]), "{:+7.3f}".format(m9m[1]), "{:+7.3f}".format(m9m[2])