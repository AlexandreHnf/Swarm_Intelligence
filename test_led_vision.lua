-- Use Shift + Click to select a robot
-- When a robot is selected, its variables appear in this editor

-- Use Ctrl + Click (Cmd + Click on Mac) to move a selected robot to a different location


ON = "ON"
CHECK = "CHECK"

-- Put your global variables here
current_state = ON


--[[ This function is executed every time you press the 'execute' button ]]
function init()
	current_state = ON
   robot.colored_blob_omnidirectional_camera.enable() -- enable LED detection
end


function nb_yellow_sensed()
	tot_nb_led_sensed = #robot.colored_blob_omnidirectional_camera
	nb_yellow = 0
	for i = 1, tot_nb_led_sensed do 
		led = robot.colored_blob_omnidirectional_camera[i].color
		if led.red == 200 and led.green == 200 and led.blue == 0 then
			nb_yellow = nb_yellow + 1
		end	
	end
	return nb_yellow
end


--[[ This function is executed at each time step
     It must contain the logic of your controller ]]
function step()
	nb_yellow = nb_yellow_sensed()
   if current_state == ON then 
		robot.leds.set_all_colors(200, 200, 0)
	--elseif current_state == CHECK then
		
	end
end





--[[ This function is executed every time you press the 'reset'
     button in the GUI. It is supposed to restore the state
     of the controller to whatever it was right after init() was
     called. The state of sensors and actuators is reset
     automatically by ARGoS. ]]
function reset()
   -- put your code here
end



--[[ This function is executed only once, when the robot is removed
     from the simulation ]]
function destroy()
   -- put your code here
end
