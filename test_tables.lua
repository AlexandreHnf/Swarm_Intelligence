-- states 
EXPLORE = "EXPLORE"
AVOID = "AVOID"
ENTER = "ENTER"
ROOM = "ROOM"
STOP = "STOP"
ALIGN = "ALIGN"
STAY = "STAY"
SLEEP = "SLEEP"


-- Global variables
current_state = EXPLORE 	-- current state of the robot
is_scout = false			-- if the robot is a scout
same_room_scout_sensed = false

is_obstacle_sensed = false  -- if an obstacle has been sensed by the robot
-- is_door_sensed = false  		-- if a door has been sensed by the robot
is_in_room = false 			-- if a robot entered a room

last_room_visited = -1 	-- color of the last visited room
room_quality_memory = 0 	-- remembers only the last room's quality he visited
-- door = -1 					-- door that is sensed if there any

-- variables for obstacle avoidance
MAX_TURN_STEPS = 40
current_turn_steps = 0

-- variables for go straight behavior
FWD_STEPS = 30
current_fwd_steps = 0

-- variables for alignment
MAX_ALIGN_STEPS = 50
current_align_steps = 0
new_nest = -1 

--sleeping variables
SLEEP_STEPS = 400
current_sleep_steps = 0


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
	robot.colored_blob_omnidirectional_camera.enable() -- enable LED detection
end



function step()

	processObstacles() 			-- checks if there is any obstacle
	processRoom()				-- checks if a robot is fully in a room
	door = processDoors()		-- checks if there is a door nearby
	
	nb_unique_scouts = get_nb_unique_scouts()
	-- nb_unique_scouts = get_nb_unique_scouts()

   -- ================================== EXPLORE =====================================
	if current_state == EXPLORE then
		if is_obstacle_sensed then 			-- OBSTACLE
			current_state = AVOID 
			current_turn_steps = math.random(MAX_TURN_STEPS)
		end
		if door ~= -1 then 				-- if a door has been sensed
			current_state = ALIGN
			current_align_steps = MAX_ALIGN_STEPS
		end
		-- if no obstacle and no door sensed nearby
		if not is_obstacle_sensed and door == -1 then -- go straight forward
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
			-- if aligned with door angle with a margin of -15° and 15°
			if door_angle >= -0.25 and door_angle <= 0.25 then -- aligned
				current_state = ENTER
				current_fwd_steps = FWD_STEPS
				last_room_visited = from_rgb_to_color(robot.colored_blob_omnidirectional_camera[door].color)
			else 
				robot.wheels.set_velocity(1, -1)
			end
			if current_align_steps <= 0 then current_state = EXPLORE end
		else 
			current_state = EXPLORE -- if no door sensed anymore
		end

	-- ================================== ENTER =====================================
	elseif current_state == ENTER then 
		current_fwd_steps = current_fwd_steps - 1
		robot.wheels.set_velocity(50,50)

		if current_fwd_steps <= 0 then -- finished forwarding during a nb of steps
			if is_scout and not is_in_room then 
				current_state = STOP -- scout went back to the central room
			else  
				if not is_in_room then  
					-- IF NOT SCOUT AND SENSE 4 SCOUTS : DECIDE 
					if nb_unique_scouts == 4 and new_nest == -1 then 
						current_state = SLEEP -- (for now, go to SLEEP before gathering)
					else	-- if he got blocked and didn't go in a room
						current_state = EXPLORE
					end
				else 
					if new_nest ~= -1 then 
						current_state = STOP -- if entered the final room
					else current_state = ROOM end
				end
			end
		end

	-- ================================== ROOM =====================================
	elseif current_state == ROOM then 
		-- the robot just entered a room, so he stops to think and act
		robot.wheels.set_velocity(0, 0)
		if is_in_room then 
			room_quality_memory = get_room_quality() -- replace room quality in memory

			if can_be_scout() then  	-- room without scout
				set_scout_color()
				is_scout = true 		-- he becomes the scout of this room
			end 
			current_state = EXPLORE 	-- continues to explore
		end

	-- ================================== SLEEP =====================================
	elseif current_state == SLEEP then 
		robot.wheels.set_velocity(0,0)
		current_sleep_steps = current_sleep_steps + 1
		if current_sleep_steps == SLEEP_STEPS then -- time to decide

			new_nest = "blue" -- TEMPORARY
			current_state = EXPLORE -- he will explore until finding the nest room
		end
		
	-- ================================== STOP =====================================
	elseif current_state == STOP then
		robot.wheels.set_velocity(0,0) -- do nothing, stops moving
		
	end -- End  BIG IF des options

end


function processObstacles() -- checks if there is a obstacle nearby
	is_obstacle_sensed = false 
	sort_prox = table.copy(robot.proximity)
	table.sort(sort_prox, function(a,b) return a.value>b.value end)
	if sort_prox[1].value > 0.03 and math.abs(sort_prox[1].angle) < math.pi/2
		then is_obstacle_sensed = true
	end
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

-- ATTENTION, USILISER DES COPIES DES TABLES
function processDoors() -- checks if a door has been sensed (close enough) 
	nb_led_sensed = #robot.colored_blob_omnidirectional_camera
	if nb_led_sensed > 0 then
		for i = 1, nb_led_sensed do 
			led = robot.colored_blob_omnidirectional_camera[i]
			if is_door(led) then -- if door color has been detected and close enough
				if found_new_nest(led.color) then 
					return i -- the door index
				else 
					if is_in_room then -- if in room, the distance doesn't matter
						return i
					else -- if in central room, choose the closest door
						if led.distance <= 100 then return i end
					end
				end
			end
		end
	end
	return -1
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


function get_room_quality() -- returns quality of a room based on ground color and objects
	sort_ground = table.copy(robot.motor_ground)
	-- BESOIN DE SORT ICI ?
	table.sort(sort_ground, function(a,b) return a.value < b.value end)
	v_f = sort_ground[1].value -- color within (0,1) = floor quality

	nb_led_sensed = #robot.colored_blob_omnidirectional_camera
	nb_objects = 0
	for i = 1, nb_led_sensed do 
		if robot.colored_blob_omnidirectional_camera[i].color.green == 255 then -- green
			nb_objects = nb_objects + 1
		end
	end 
	v_o = (nb_objects - 2) / 10 -- object quality within [0,1]
	
	return (v_f + v_o) / 2 -- room quality
end

function set_quality_colors()
	-- map (0,1) to (1, 11) => floor((Q*10)+1)
	nb_leds_on = math.floor((room_quality_memory*10)+1)
	for i = 1, nb_leds_on do 
		robot.leds.set_single_color(i, last_room_visited) -- last room visited color
	end
end


function set_scout_color()
	color = map_doors_colors(last_room_visited)
	robot.leds.set_single_color(13, color[1], color[2], color[3])
		
end

function from_rgb_to_color(led)
	r = led.red
	g = led.green
	b = led.blue
	if 	   r == 255 and g == 0 and b == 0 then return "red"
	elseif r == 255 and g == 140 and b == 0 then return "orange"
	elseif r == 0 and g == 255 and b == 0 then return "green"
	elseif r == 0 and g == 0 and b == 255 then return "blue"
	elseif r == 255 and g == 0 and b == 255 then return "magenta"
	end 
end

function from_color_to_rgb(color)
	if color == "red" then return {255, 0, 0} -- red
	elseif color == "orange" then return {255, 140, 0} -- orange
	elseif color == "blue" then return {0, 0, 255} -- blue
	elseif color == "magenta" then return {255, 0, 255} -- magenta
	end
end

function map_doors_colors(color)
	if color == "red" then return {100, 0, 200}
	elseif color == "orange" then return {200, 200, 0} -- yellow
	elseif color == "blue" then return {0, 255, 255} -- cyan
	elseif color == "magenta" then return {100, 200, 0} -- light green
	end
end

function get_nb_scouts_sensed()
	nb_scouts_sensed = 0
	nb_led_sensed = #robot.colored_blob_omnidirectional_camera
	for i = 1, nb_led_sensed do 
		-- cyan
		if robot.colored_blob_omnidirectional_camera[i].color.green == 255 and 
		   robot.colored_blob_omnidirectional_camera[i].color.blue == 255 then 
			nb_scouts_sensed = nb_scouts_sensed + 1
		end
	end
	return nb_scouts_sensed
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

function can_be_scout()
	color = map_doors_colors(last_room_visited) -- to match scout colors

	nb_led_sensed = #robot.colored_blob_omnidirectional_camera
	for i = 1, nb_led_sensed do 
		led = robot.colored_blob_omnidirectional_camera[i].color
		if color.red == led.red and color.green == led.green and color.blue == led.blue then
			return false -- there is a scout already assigned to this room
		end
	end
	return true -- no scout assigned for this room => we can be scout
end


function reset()
	current_state = EXPLORE
	   
	is_obstacle_sensed = false
	-- is_door_sensed = false
	is_scout = false
	same_room_scout_sensed = false
	is_in_room = false

	current_turn_steps = 0
	number_robot_sensed = 0
	current_fwd_steps = 0
	current_sleep_steps = 0

	new_nest = -1
	last_room_visited = -1

	robot.colored_blob_omnidirectional_camera.enable() -- enable LED detection
end


function destroy()
end
