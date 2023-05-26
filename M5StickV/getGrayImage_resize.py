
import sensor, image, time, lcd

lcd.init(freq=15000000)

lcd.direction(lcd.YX_LRDU)
sensor.reset()                      # Reset and initialize the sensor. It will
                                    # run automatically, call sensor.run(0) to stop
sensor.set_pixformat(sensor.GRAYSCALE) # Set pixel format to RGB565 (or GRAYSCALE)
sensor.set_framesize(sensor.QQVGA)   # Set frame size to QVGA (320x240) QQVGA (160x120)
sensor.skip_frames(time = 2000)     # Wait for settings take effect.
sensor.set_contrast(+2)             # Contrast +2 to -2
#sensor.set_brightness(-2)           # Brightness +2 to -2
#sensor.set_saturation(-2)           # Saturation +2 to -2
sensor.set_auto_gain(0,20)           # enable,gain_db enable=1:auto,0:off
#sensor.set_vflip(1)                 # 1:enable 0:disable
sensor.set_hmirror(1)                 # 1:enable 0:disable

clock = time.clock()                # Create a clock object to track the FPS.

while(True):
    clock.tick()                    # Update the FPS clock.
    img = sensor.snapshot()         # Take a picture and return the image.
    img = img.copy((20,0,140,120))
    img = img.resize(16,16)
    lcd.display(img)                # Display on LCD
#    print(clock.fps())              # Note: MaixPy's Cam runs about half as fast when connected
                                    # to the IDE. The FPS should increase once disconnected.
#    print(sensor.get_gain_db())
