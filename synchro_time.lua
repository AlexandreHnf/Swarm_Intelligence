-- Use Shift + Click to select a robot
-- When a robot is selected, its variables appear in this editor

-- Use Ctrl + Click (Cmd + Click on Mac) to move a selected robot to a different location



-- Put your global variables here
EXPLORE = "EXPLORE"
AVOID = "AVOID"
ALIGN = "ALIGN"
ENTER = "ENTER"
SYNCHRO = "SYNCHRO"

current_state = SYNCHRO 

is_obstacle_sensed = false  -- if an obstacle has been sensed by the robot

-- is_door_sensed = false 
door = -1
new_nest = -1

-- variables for obstacle avoidance
MAX_TURN_STEPS = 40
current_turn_steps = 0

-- variables for go straight behavior
FWD_STEPS = 50
current_fwd_steps = 0

-- variables for alignment
MAX_ALIGN_STEPS = 50
current_align_steps = 0

current_wiggle_time = 0


-- function used to copy two tables
function table.copy(t)
	local t2 = {}
	for k,v in pairs(t) do
		t2[k] = v
	end
	return t2
end


function init()
	current_state = SYNCHRO
	robot.colored_blob_omnidirectional_camera.enable()
	robot.leds.set_single_color(13, 0, 255, 255)
end


function step()
	processObstacles()
	processRoom()
	door = processDoors()
	nb_unique_scouts = get_nb_unique_scouts()

	-- ================================== SYNCHRO =====================================
	if current_state == SYNCHRO then 
		if nb_unique_scouts == 1 then 
			new_nest = map_scout_color()
			robot.leds.set_all_colors(new_nest[1], new_nest[2], new_nest[3])
			current_state == EXPLORE -- will gather in to the ultimate room
		else
			current_wiggle_time = current_wiggle_time - 1
			if current_wiggle_time <= 0 then -- finished wiggling
				robot.leds.set_single_color(13, 0, 0, 0)
			end
		end

	-- ================================== EXPLORE =====================================
	elseif current_state == EXPLORE then 
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

	-- ================================== AVOID =====================================
	elseif current_state == AVOID then 
		robot.wheels.set_velocity(-10,10)	-- ROTATE LEFT
		current_turn_steps = current_turn_steps - 1
		if current_turn_steps <= 0 then
		   current_state = EXPLORE
		end

	-- ================================== ALIGN =====================================
	elseif current_state == ALIGN then 
		if door ~= -1 then -- to check if still sensed, could have moved
			current_align_steps = current_align_steps - 1
			door_angle = robot.colored_blob_omnidirectional_camera[door].angle 
			if door_angle >= -0.25 and door_angle <= 0.25 then -- aligned
				current_state = ENTER
				current_fwd_steps = FWD_STEPS
			else 
				robot.wheels.set_velocity(1, -1)
			end
			if current_align_steps <= 0 then current_state = EXPLORE end
		else current_state = EXPLORE -- if no door sensed anymore
		end

	-- ================================== ENTER =====================================
	elseif current_state == ENTER then 
		-- robot.wheels.set_velocity(0,0)
		current_fwd_steps = current_fwd_steps - 1
		robot.wheels.set_velocity(50,50)
		if current_fwd_steps <= 0 then -- finished forwarding
		   current_state = STOP
		end

	elseif current_state == STOP then 
		robot.wheels.set_velocity(0,0)

	end

end


function map_scout_color() -- scout color to door color in rgb
	nb_led_sensed = #robot.colored_blob_omnidirectional_camera
	for i = 1, nb_led_sensed do 
		led = robot.colored_blob_omnidirectional_camera[i]
		if scout_color(led) then 
			if led.red == 100 and led.green == 0 and led.blue == 200 then return {255, 0, 0}
			elseif led.red == 0 and led.green == 255 and led.blue == 255 then return {0, 0, 255}
			elseif led.red == 200 and led.green == 200 and led.blue == 0 then return {255, 140, 0}
			elseif led.red == 100 and led.green == 200 and led.blue == 0 then return {255, 0, 255}
			end
		end
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

function found_new_nest(led)
	if new_nest ~= -1 then
		if led.red == new_nest[1] and led.green == new_nest[2] and 
			led.blue == new_nest[3] then
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


function get_nb_unique_scouts() -- get the number of unique color scouts sensed
	nb_purple = 0
	nb_cyan = 0
	nb_light_green = 0
	nb_yellow = 0 
	nb_led_sensed = #robot.colored_blob_omnidirectional_camera
	for i = 1, nb_led_sensed do 
		led = robot.colored_blob_omnidirectional_camera[i].color
		if led.red == 100 and led.green == 0 and led.blue == 200 then  -- purple
			if (nb_purple == 0) then nb_purple = nb_purple + 1 end
		elseif led.red == 0 and led.green == 255 and led.blue == 255 then -- cyan 
			if (nb_cyan == 0) then nb_cyan = nb_cyan + 1 end
		elseif led.red == 100 and led.green == 200 and led.blue == 0 then -- light green
			if (nb_light_green == 0) then nb_light_green = nb_light_green + 1 end
		elseif led.red == 200 and led.green == 200 and led.blue == 0 then -- yellow
			if (nb_yellow == 0) then nb_yellow = nb_yellow + 1 end
		end 
	end
	tot = nb_purple + nb_cyan + nb_light_green + nb_yellow
	-- log("nb scout : " .. tot)
	return tot
end 

function reset()
	current_state = EXPLORE
	robot.colored_blob_omnidirectional_camera.enable()
	-- new_nest = "blue"
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
