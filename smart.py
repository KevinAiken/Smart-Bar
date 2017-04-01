#take in data from my accelerometer
#take in data from ardiuno
#send data over bluetooth to cellphone
#send data to aws
while True:
    #read from picell
    #read from ardiunocell
    int repCount = 0
    numberOfRepsNeeded = 5
    while(repCount < numberOfRepsNeeded):
        accel = avgofsensors
        accelleft = avgofSensorsleft
        accelright = avgofSensorsright
        weakright = false
        weakleft = false
        balanced = true
        rep = emptyarraylist
        startTimer2()
        while(accel < .1 && accel > -.1):
            #wait
            accel = avgofsensors

            if(repCount > 0 && timer2 > 7s):
                sendMotivatetophone
        #identify vertical accel
        resettimer2
        if(accel > .1):
            starttimer1
            while(accel > -.1):
                #wait
                accel = avgofsensors
                if(accelLeft > accelRight + 100):
                    weakRight = true
                if(accelRight > accelLeft + 100):
                    weakLeft = true

            while(accel < .1):
                #wait
                accel = avgofsensors
            timeone = timervalue1
            reset timer1

            start timer1
            start timer2
            while(accel < .1 && accel > -.1):
                accel = avgofsensors
                if(repCount > 3 && timer2 > 7s):
                    sendMotivatetophone
            while(accel < -.1):
                accel = avgofsensors
            while(accel > .1):
                accel = avgofsensors
            timetwo = timervalue
            reset timer
        if(weakLeft || weakRight):
            balanced = false
        repCount++
        send repCount to phone
        rep.add(number)
        rep.add(balanced)
        rep.add(peakaccel)
        rep.add(timeup)
        rep.add(timedown)
        liftSet.add(rep)
    sendSetToAWS
    sendSetToPhone
