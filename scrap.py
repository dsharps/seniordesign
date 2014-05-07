channel_data = random.sample(range(0, 5), 4)
            print "CD: %s" % channel_data
            print "AT: %s" % active_thumbsticks

            for d in xrange(0, len(channel_data)-1, 2):
                if len(active_thumbsticks) >= 6: #at max notes, skip the rest
                    break
                print "d:%s, t:%s" % (d, channel_to_thumbstick[d])
                #pitch = thumbstick_to_midi_pitch[channel_to_thumbstick[d]]
                pitch = 0
                print "checking active"
                if note_active(channel_data[d], channel_data[d+1]):
                    #add at index of first zero, update
                    print "checking d"
                    if d not in active_thumbsticks:
                        print "d not found"
                        try:
                            #get the index of the first zero, set the new pitch there
                            active_thumbsticks[active_thumbsticks.index(0)] = pitch
                        except:
                            #do nothing, try again next time
                            print "Error: %s" % repr(sys.exc_info())
                            pass
                    #update
                    #client.send(OSC.OSCMessage("/n%s"%d, [pitch, ((channel_data[d]/255.0)*10), ((channel_data[d+1]/255.0)*100),
                    #                       (distance_with_deadzone(channel_data[d], channel_data[d+1])/255.0)*100]))
                #note not active, but still in active_thumbsticks
                elif channel_to_thumbstick[d] in active_thumbsticks:
                    #delete this thumbstick
                    print "removing d"
                    active_thumbsticks.remove(pitch)
                    #shut off OSC
            print "CD: %s" % channel_data
            print "AT: %s" % active_thumbsticks
            print "-------"

            time.sleep(2)
