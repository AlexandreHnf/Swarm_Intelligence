function readLines(file_path)
	local f = io.open(file_path, "rb")
	local all_lines = {}
	
	for line in io.lines(file_path) do
		table.insert(all_lines, line)
	end
	return all_lines
end

all_lines = readLines("simulation_parameters5.txt")


-- states 
EXPLORE = "EXPLORE"
AVOID = "AVOID"
ENTER = "ENTER"
ROOM = "ROOM"
CENTRAL_ROOM = "CENTRAL_ROOM"
STOP = "STOP"
ALIGN = "ALIGN"
STAY = "STAY"
SLEEP = "SLEEP"
SYNCHRO = "SYNCHRO"
DECIDE = "DECIDE"

-- Global variables
current_state = EXPLORE 
is_scout = false 

is_obstacle_sensed = false
is_in_room = false 

Q = -1 -- remembers only the last room's quality he visited
new_nest = -1
finished = false -- when the robot joined the best room

ENTER_DEEP_VELOCITY = tonumber(all_lines[1])
ROTATE_VELOCITY = tonumber(all_lines[2])
ALIGN_ANGLE = tonumber(all_lines[3])
AVOID_DISTANCE = tonumber(all_lines[4])
FWD_VELOCITY = tonumber(all_lines[5])
FWD_STEPS = tonumber(all_lines[6])
ENTER_VELOCITY = tonumber(all_lines[7])

current_fwd_steps = 0
MAX_ALIGN_STEPS = 50
current_align_steps = 0
MAX_TURN_STEPS = 20 -- 40



-- function used to copy two tables
function table.copy(t)
	local t2 = {}
	for k,v in pairs(t) do
    	t2[k] = v
  	end
 	return t2
end

function assign_scout_color(color) -- assign one of the 4 color room to the scout
	robot.leds.set_single_color(13, color[1], color[2], color[3]) -- purple
	is_scout = true
end

function assign_scouts() -- the first 4 robots become scouts
	id = robot.id 
	if id == "fb1" then 
		assign_scout_color({100, 0, 200}) -- purple
		new_nest = "purple"
	elseif id == "fb2" then 
		assign_scout_color({0, 255, 255}) -- cyan
		new_nest = "cyan"
	elseif id == "fb3" then 
		assign_scout_color({200, 200, 0}) -- yellow
		new_nest = "yellow"
	elseif id == "fb4" then 
		assign_scout_color({100, 200, 0}) -- light green
		new_nest = "light_green"
	end
	
end

function init()
	assign_scouts()
	robot.colored_blob_omnidirectional_camera.enable() -- enable color detection
	current_state = EXPLORE
end

function get_all_leds_sensed(nb_led_sensed)
	all_leds = table.copy(robot.colored_blob_omnidirectional_camera)
	-- sort by increasing order and based on distance towards the led source
	table.sort(all_leds, function(a,b) return a.distance<b.distance end)
	return all_leds
end

function get_leds_counters(all_leds)
	leds_counters = {}
	for i = 1, 3 do table.insert(leds_counters, 0) end 

	if nb_led_sensed > 0 then
		for i = 1, nb_led_sensed do 
			c = all_leds[i].color 
			if c.red == 255 and c.green == 255 and c.blue == 255 then 
				leds_counters[1] = leds_counters[1] + 1 -- white = follower
			elseif c.red == 128 and c.green == 0 and c.blue == 0 then 
				leds_counters[2] = leds_counters[2] + 1 -- brown = scout
			elseif c.red == 0 and c.green == 255 and c.blue == 0 then 
				if (all_leds[i].distance <= 350) then  -- close enough
					leds_counters[3] = leds_counters[3] + 1	 -- green = object
				end
			end
		end
	end
	return leds_counters
end

function synchronize()
	if is_scout then 
		robot.leds.set_single_color(13, 128, 0, 0) -- brown
	elseif not is_scout then 
		robot.leds.set_single_color(13, 255, 255, 255) -- white
	end

	current_state = SYNCHRO
end


function step()
	nb_led_sensed = #robot.colored_blob_omnidirectional_camera
	all_leds_sensed = get_all_leds_sensed(nb_led_sensed)
	leds_counters = get_leds_counters(all_leds_sensed)

	processRoom()				-- checks if the robot is fully in a room
	processObstacles() 			-- checks if there is any obstacle
	door = processDoors(nb_led_sensed, all_leds_sensed) --checks if there is a door nearby
	can_synchro = can_synchronize(leds_counters)

	-- ================================== EXPLORE =====================================
	if current_state == EXPLORE then 
		if is_obstacle_sensed then 			-- OBSTACLE
			current_state = AVOID 
			current_turn_steps = MAX_TURN_STEPS
		end
		if door ~= -1 then 				-- if a door has been sensed
			current_state = ALIGN
			current_align_steps = MAX_ALIGN_STEPS
		end
		-- if no obstacle and no door sensed nearby
		if not is_obstacle_sensed and door == -1 then -- go straight forward
			robot.wheels.set_velocity(FWD_VELOCITY,FWD_VELOCITY)
		end

		if not is_in_room and can_synchro then synchronize() end

	-- ================================== AVOID =====================================
	elseif current_state == AVOID then 
		-- if not can_synchro then 
		robot.wheels.set_velocity(-ROTATE_VELOCITY,ROTATE_VELOCITY)	-- ROTATE LEFT
		current_turn_steps = current_turn_steps - 1
		if not is_in_room and can_synchro then 
			synchronize()
		else 
			if current_turn_steps <= 0 then current_state = EXPLORE end
		end
	
	-- ================================== ALIGN =====================================
	elseif current_state == ALIGN then 
		if door ~= -1 then -- to check if still sensed, could have moved
			current_align_steps = current_align_steps - 1
			door_angle = all_leds_sensed[door].angle
			-- if aligned with door angle with a margin of -x° and x°
			if door_angle >= -ALIGN_ANGLE and door_angle <= ALIGN_ANGLE then -- aligned
				current_state = ENTER
				current_fwd_steps = FWD_STEPS
				if finished then 
					-- current_fwd_steps = FWD_STEPS + 50 
					current_fwd_steps = FWD_STEPS
					ENTER_VELOCITY = ENTER_DEEP_VELOCITY
				end --enter deep
			else 
				robot.wheels.set_velocity(ROTATE_VELOCITY, -ROTATE_VELOCITY)
			end
			if current_align_steps <= 0 then -- VRAIMENT UTILE ?
				robot.wheels.set_velocity(1,1)
				current_state = EXPLORE 
			end
		else 
			current_state = EXPLORE -- if no door sensed anymore
		end

	-- ================================== ENTER =====================================
	elseif current_state == ENTER then 
		current_fwd_steps = current_fwd_steps - 1
		robot.wheels.set_velocity(ENTER_VELOCITY,ENTER_VELOCITY)

		if current_fwd_steps <= 0 then -- finished forwarding during a nb of steps
			
			if is_in_room then current_state = ROOM 
			else current_state = CENTRAL_ROOM end 

		end

	-- ================================== ROOM =====================================
	elseif current_state == ROOM then 
		-- the robot just entered a room, so he stops to think and act
		robot.wheels.set_velocity(0, 0)

		if is_in_room then  -- ROOM

			if finished and nest ~= -1 then -- entered the final room
				current_state = STOP
			else 

				if is_scout and Q == -1 then Q = get_room_quality(leds_counters) end 
				current_state = EXPLORE 
			end

		else 
			current_state = EXPLORE -- DANGEREUX
		end
	
	-- ================================== CENTRAL ROOM ===============================
	elseif current_state == CENTRAL_ROOM then 
		robot.wheels.set_velocity(0, 0)

		if can_synchro and not is_in_room then 
	
			synchronize() 

		else 
			current_state = EXPLORE -- DANGEREUX
		end

	-- ================================== SYNCHRO ===============================
	elseif current_state == SYNCHRO then 
		robot.wheels.set_velocity(0,0)

		if is_in_room then -- if stopped in some way in a room, continue exploring
			current_state = EXPLORE
		else

			-- the scout senses 3 other scouts and min 13 followers (min 17 in total)
			if is_scout and leds_counters[2] == 3 and leds_counters[1] > 12 then 
				current_wiggle_time = Q*100 -- timer proportional to the quality
				current_state = DECIDE 

			-- the follower senses 4 scouts and min 12 other followers (min 17 in total)
			elseif not is_scout and leds_counters[2] == 4 and leds_counters[1] > 11 then  
				current_state = DECIDE
			end
		end

	-- ================================== DECIDE ===============================
	elseif current_state == DECIDE then 
		if is_scout then  			-- SCOUT 
			if leds_counters[2] == 0 then -- it means he is the only remaining
				-- reput his nest color (purple, cyan ..)
				new_color = from_color_to_rgb(new_nest)
				robot.leds.set_single_color(13, new_color[1], new_color[2], new_color[3])
				finished = true
				current_state = EXPLORE
			else
				current_wiggle_time = current_wiggle_time - 1
				if current_wiggle_time <= 0 then -- finished wiggling
					robot.leds.set_single_color(13, 0, 0, 0) -- leds OFF
					is_scout = false -- becomes a follower
				end
			end


		elseif not is_scout then		  -- FOLLOWER
			if leds_counters[2] == 0 then -- only one scout wiggling remaining
				ult = get_ultimate_room(nb_led_sensed, all_leds_sensed)
				new_nest = ult[2]
				if new_nest ~= -1 then -- if the scout hasn't set his color yet
					robot.leds.set_all_colors(ult[1].red, ult[1].green, ult[1].blue)
					current_state = EXPLORE -- will gather in to the ultimate room
					finished = true
					is_scout = true -- becomes a scout
				end
			end
		end

	
	-- ================================== STOP ===============================
	elseif current_state == STOP then 
		robot.wheels.set_velocity(0,0) -- do nothing, stops moving

	end -- End BIG IF

end

-- ===============================================================================
-- ===============================================================================
-- ===============================================================================
function processObstacles() 
	-- checks if there is a obstacle nearby and close enough
	is_obstacle_sensed = false 
	sort_prox = table.copy(robot.proximity)
	table.sort(sort_prox, function(a,b) return a.value>b.value end)
	if sort_prox[1].value > AVOID_DISTANCE and math.abs(sort_prox[1].angle) < math.pi/2
		then is_obstacle_sensed = true
	end
end

function processDoors(nb_led_sensed, all_leds_sensed)
	if nb_led_sensed > 0 then 
		for i = 1, nb_led_sensed do 
			if is_door(all_leds_sensed[i]) then 
				-- SCOUT
				if is_scout and is_in_room then return i end
				if is_scout and not is_in_room and found_nest_room(all_leds_sensed[i].color) then return i end  
				-- FOLLOWER
				if not is_scout and is_in_room then return i end 
				if not is_scout and not is_in_room then 
					if finished and found_nest_room(all_leds_sensed[i].color) then return i 
					else return -1 end
				end
			end
		end
	end
	return -1
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

function is_room_color(color) -- yellow, cyan, purple or light green 
	if (color.red == 200 and color.green == 200 and color.blue == 0) or 
		(color.red == 0 and color.green == 255 and color.blue == 255) or 
		(color.red == 100 and color.green == 0 and color.blue == 200) or 
		(color.red == 100 and color.green == 200 and color.blue == 0) then 
		return true 
	end
	return false
end 

function found_nest_room(led) -- checks whether led is the nest color
	if new_nest ~= -1 then
		nest_door_color = map_doors_colors(new_nest) -- purple => red
		if led.red == nest_door_color[1] and led.green == nest_door_color[2] and 
			led.blue == nest_door_color[3] then
			return true
		end
	end
	return false
end


function processRoom() --checks if a robot is fully in a room
	-- ASSUME THAT THE CENTER ROOM ALWAYS HAS A DIFFERENT COLOR THAN ROOMS= BLACK
	is_in_room = false
	nb_black = 0
	for i, ground_sensor in pairs(robot.motor_ground) do 
		if ground_sensor.value == 0 then
			nb_black = nb_black + 1 
		end
	end
	if nb_black == 0 then is_in_room = true end
end



function get_room_quality(leds_counters) 
	-- returns quality of a room based on ground color and objects
	sort_ground = table.copy(robot.motor_ground)
	table.sort(sort_ground, function(a,b) return a.value < b.value end)
	v_f = sort_ground[1].value -- color within (0,1) = floor quality

	nb_objects = leds_counters[3] -- nb of green leds close enough
	v_o = (nb_objects - 2) / 10 -- object quality within [0,1]

	if is_scout then 
		-- log(robot.id .. " Q : " .. (v_f + v_o) / 2)
		-- log(robot.id .. " ground: " .. v_f) 
		-- log(robot.id .. " nb obj: " .. nb_objects) 
		-- log(robot.id .. " obj quality: " .. v_o)
	end
	
	return (v_f + v_o) / 2 -- room quality
end

function can_synchronize(leds_counters)
	-- checks if the robot can synchronize
	if is_scout and not is_in_room and Q ~= -1 and not finished then return true end
	if not is_scout and not is_in_room and leds_counters[2] == 4 and new_nest == -1 
		and not finished then return true end
	return false
end

function from_rgb_to_color(led)
	-- from rgb color (door or room color) to their respective color names
	r = led.red
	g = led.green
	b = led.blue
	if 	   r == 255 and g == 0 and b == 0 then return "red"
	elseif r == 255 and g == 140 and b == 0 then return "orange"
	elseif r == 0 and g == 255 and b == 0 then return "green"
	elseif r == 0 and g == 0 and b == 255 then return "blue"
	elseif r == 255 and g == 0 and b == 255 then return "magenta"
	elseif r == 200 and g == 200 and b == 0 then return "yellow"
	elseif r == 0 and g == 255 and b == 255 then return "cyan"
	elseif r == 100 and g == 0 and b == 200 then return "purple"
	elseif r == 100 and g == 200 and b == 0 then return "light_green"
	end 
end

function from_color_to_rgb(color)
	-- from door or room color to their respective rgb color
	if color == "red" then return {255, 0, 0} -- red
	elseif color == "orange" then return {255, 140, 0} -- orange
	elseif color == "blue" then return {0, 0, 255} -- blue
	elseif color == "magenta" then return {255, 0, 255} -- magenta
	elseif color == "yellow" then return {200, 200, 0} -- yellow
	elseif color == "cyan" then return {0, 255, 255} -- cyan 
	elseif color == "purple" then return {100, 0, 200} -- purple
	elseif color == "light_green" then return {100, 200, 0} -- light green
	end
end


function map_doors_colors(color)
	-- from room color to rgb door color
	if color == "purple" then return {255, 0, 0} -- red
	elseif color == "yellow" then return {255, 140, 0} -- orange
	elseif color == "cyan" then return {0, 0, 255} -- blue
	elseif color == "light_green" then return {255, 0, 255} -- magenta
	end
end

function get_ultimate_room(nb_led_sensed, all_leds_sensed) -- get the final room color 
	for i = 1, nb_led_sensed do 
		if is_room_color(all_leds_sensed[i].color) then  -- yellow, cyan, purple or light green
			return {all_leds_sensed[i].color, from_rgb_to_color(all_leds_sensed[i].color)}
		end
	end
	return -1
end


function reset()
	current_state = EXPLORE
	   
	is_obstacle_sensed = false
	is_scout = false
	is_in_room = false
	finished = false
	can_synchro = false

	Q = -1 -- quality memory

	current_turn_steps = 0
	current_fwd_steps = 0

	new_nest = -1

	assign_scouts()
	robot.colored_blob_omnidirectional_camera.enable() -- enable LED detection
	nb_led_sensed = #robot.colored_blob_omnidirectional_camera
end

function destroy()
end
