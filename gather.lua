-- Use Shift + Click to select a robot
-- When a robot is selected, its variables appear in this editor

-- Use Ctrl + Click (Cmd + Click on Mac) to move a selected robot to a different location



-- Put your global variables here
EXPLORE = "EXPLORE"
AVOID = "AVOID"
ALIGN = "ALIGN"
ENTER = "ENTER"

current_state = EXPLORE 

is_obstacle_sensed = false  -- if an obstacle has been sensed by the robot

-- is_door_sensed = false 
door = -1
new_nest = -1

-- variables for obstacle avoidance
MAX_TURN_STEPS = 40
current_turn_steps = 0

-- variables for go straight behavior
FWD_STEPS = 10
ENTER_VELOCITY = 1000 
current_fwd_steps = 0

-- variables for alignment
MAX_ALIGN_STEPS = 50
current_align_steps = 0


-- function used to copy two tables
function table.copy(t)
	local t2 = {}
	for k,v in pairs(t) do
		t2[k] = v
	end
	return t2
end


function init()
	current_state = EXPLORE
	robot.colored_blob_omnidirectional_camera.enable()
	new_nest = "blue"
end


function step()
	processObstacles()
	door = processDoors()
	processRoom()
	
	if current_state == EXPLORE then 
		if is_obstacle_sensed then 			-- OBSTACLE
			current_state = AVOID 
			current_turn_steps = math.random(MAX_TURN_STEPS)
		end
		if door ~= -1 then 				-- DOOR sensed
			current_state = ALIGN
			current_align_steps = MAX_ALIGN_STEPS
		end
		if not is_obstacle_sensed and door == -1 then 
			robot.wheels.set_velocity(15,15)
		end	

	elseif current_state == AVOID then 
		robot.wheels.set_velocity(-10,10)	-- ROTATE LEFT
		current_turn_steps = current_turn_steps - 1
		if current_turn_steps <= 0 then
		   current_state = EXPLORE
		end

	elseif current_state == ALIGN then 
		if door ~= -1 then -- to check if still sensed, could have moved
			current_align_steps = current_align_steps - 1
			door_angle = robot.colored_blob_omnidirectional_camera[door].angle 
			if door_angle >= -0.30 and door_angle <= 0.30 then -- aligned
				current_state = ENTER
				current_fwd_steps = FWD_STEPS
			else 
				robot.wheels.set_velocity(1, -1)
			end
			if current_align_steps <= 0 then current_state = EXPLORE end
		else current_state = EXPLORE -- if no door sensed anymore
		end

	elseif current_state == ENTER then 
		-- robot.wheels.set_velocity(0,0)
		current_fwd_steps = current_fwd_steps - 1
		robot.wheels.set_velocity(ENTER_VELOCITY,ENTER_VELOCITY)
		if current_fwd_steps <= 0 then -- finished forwarding
		   current_state = STOP
		end

	elseif current_state == STOP then 
		robot.wheels.set_velocity(0,0)
		if not is_in_room then current_state = EXPLORE end

	end

end

function processObstacles() -- checks if there is a obstacle nearby
	is_obstacle_sensed = false 
	sort_prox = table.copy(robot.proximity)
	table.sort(sort_prox, function(a,b) return a.value>b.value end)
	if sort_prox[1].value > 0.03 and math.abs(sort_prox[1].angle) < math.pi/2
		then is_obstacle_sensed = true
	end
end

-- ATTENTION, USILISER DES COPIES DES TABLES
function processDoors() -- checks if a door has been sensed (close enough) 
	nb_led_sensed = #robot.colored_blob_omnidirectional_camera
	if nb_led_sensed > 0 then
		for i = 1, nb_led_sensed do 
			led = robot.colored_blob_omnidirectional_camera[i]
			if is_door(led) then -- if door color has been detected and close enough
				if new_nest ~= -1 then 
					if found_new_nest(led.color) then return i end-- the door index
				else
					if led.distance <= 100 then return i end -- the door index
				end
			end
		end
	end
	return -1
end

function from_color_to_rgb(color)
	if color == "red" then return {255, 0, 0}
	elseif color == "orange" then return {255, 140, 0}
	elseif color == "blue" then return {0, 0, 255}
	elseif color == "magenta" then return {255, 0, 255}
	end
end

function found_new_nest(led)
	if new_nest ~= -1 then
		nest_door_color = from_color_to_rgb(new_nest)
		if led.red == nest_door_color[1] and led.green == nest_door_color[2] and 
			led.blue == nest_door_color[3] then
			return true
		end
	end
	return false
end

function is_door(led_source)
	r = led_source.color.red
	g = led_source.color.green
	b = led_source.color.blue
	-- if the color is orange, blue, red or magenta, it is a door
	if (r == 255 and g == 0 and b == 0) or (r == 255 and g == 140 and b == 0)
		or (r == 0 and g == 0 and b == 255) or (r == 255 and g == 0 and b == 255)
		then return true
	end
	return false
end

function processRoom() --checks if a robot is fully in a room
	is_in_room = false
	nb_black = 0
	for i, ground_sensor in pairs(robot.motor_ground) do 
		if ground_sensor.value == 0 then
			nb_black = nb_black + 1 
		end
	end
	if nb_black == 0 then is_in_room = true end
end

function reset()
	current_state = EXPLORE
	robot.colored_blob_omnidirectional_camera.enable()
	new_nest = "blue"
	-- is_door_sensed = false
	is_in_room = false
	is_obstacle_sensed = false
	current_fwd_steps = 0
	current_turn_steps = 0
	current_align_steps = 0
	-- new_nest = -1
	door = -1
end


function destroy()
end
