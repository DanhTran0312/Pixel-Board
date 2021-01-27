import BlynkLib, time

# Initialize Blynk
blynk = BlynkLib.Blynk('gWccqWX-FZoCWHrJ5IOr-q97prFF8L6W',
                       server='blynk.iot-cm.com', port=8080)


# ON/OFF
@blynk.VIRTUAL_WRITE(1)
def on_off_handler(value):
    print(1)

# SKIP ANIMATION
@blynk.VIRTUAL_WRITE(2)
def skip_handler(value):
    time.sleep(0.5)
    print(2)

# LOOP
@blynk.VIRTUAL_WRITE(3)
def loop_handler(value):
   print(3)



while(True):
    blynk.run()
