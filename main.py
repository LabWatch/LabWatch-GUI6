#importing all functions
from email_attachment import sendfile, sendwarning
import settings
import Sensor_Read
import thingspeak
import Local_logging
import GUI_inter
import matplotlib.animation as animation 
#importing threading
import _thread

#for Finding the date 
from datetime import date
from dateutil.relativedelta import relativedelta

#System Restart 
import subprocess


# finds last months file to send
date_file = date.today() + relativedelta(months=0)




settings.init()
GUI_inter.setup()
#ani = animation.FuncAnimation(GUI_inter.fig, GUI_inter.animate, interval=2000, fargs=(GUI_inter.xs,GUI_inter.ys,GUI_inter.xs2,GUI_inter.ys2) )


try: 
    #settings.init()
    _thread.start_new_thread( Sensor_Read.sensor0, (0,2 ) )#starts recording sensor on D4
    _thread.start_new_thread( Sensor_Read.sensor1, (1,2 ) )#starts recording sensor on D18
    _thread.start_new_thread( Sensor_Read.avg,     (2, ) )
    _thread.start_new_thread( thingspeak.cloud,    (300, ) )
    _thread.start_new_thread( Local_logging.local,       (300, ) )
    
    #ani = animation.FuncAnimation(GUI_inter.fig, GUI_inter.animate, interval=2000, fargs=(GUI_inter.xs,GUI_inter.ys,GUI_inter.xs2,GUI_inter.ys2) )

except:
    print ("Error: unable to start thread")

#-----------------------------End of Starting Threads----------------------------------------------------
#_________________________________________________________________________________________________________

#______________________________________________________________________________________________
#-------------------main loop for the programe------------------------------------------------- 

#Tkinter window backgorund color
# while True: 
try:
    GUI_inter.win.mainloop()
except:
    # subprocess.run('~/LabWatchGUI6/runme.sh', shell=True)
    quit()
finally:
    pass


