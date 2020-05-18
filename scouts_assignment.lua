SCOUT = "SCOUT"
MOVE = "MOVE"

--sleeping variables
SLEEP_STEPS = 50
current_sleep_steps = 0

current_state = SCOUT

is_scout = false

-- function used to copy two tables
function table.copy(t)
	local t2 = {}
	for k,v in pairs(t) do
    	t2[k] = v
  	end
 	return t2
end

function assign_scout_color(color)
	robot.leds.set_single_color(13, color[1], color[2], color[3]) -- purple
	is_scout = true 		
	log("je suis scout !!")
end

function assign_scouts()
	id = robot.id 
	if id == "fb1" then 
		assign_scout_color({100, 0, 200}) -- purple
	elseif id == "fb2" then 
		assign_scout_color({0, 255, 255}) -- cyan
	elseif id == "fb3" then 
		assign_scout_color({200, 200, 0}) -- yellow
	elseif id == "fb4" then 
		assign_scout_color({100, 200, 0}) -- light green
	end
	
end

function init()
	assign_scouts()
	robot.colored_blob_omnidirectional_camera.enable()
	current_state = MOVE
end

-- function map_doors_colors(c)
-- 	if c.red == 255 and c.green == 0 and c.blue == 0 then return {100, 0, 200} -- purple
-- 	elseif c.red == 255 and c.green == 140 and c.blue == 0 then return {200, 200, 0} -- yellow
-- 	elseif c.red == 0 and c.green == 0 and c.blue == 255 then return {0, 255, 255} -- cyan
-- 	elseif c.red == 255 and c.green == 0 and c.blue == 255 then return {100, 200, 0} -- light green
-- 	end
-- end

-- function processDoors() -- checks if a door has been sensed (close enough) 
-- 	nb_led_sensed = #robot.colored_blob_omnidirectional_camera
-- 	if nb_led_sensed > 0 then
-- 		for i = 1, nb_led_sensed do 
-- 			led = robot.colored_blob_omnidirectional_camera[i]
-- 			if is_door(led) then -- if door color has been detected and close enough
-- 				if led.distance <= 100 then return i end -- the door index
-- 			end
-- 		end
-- 	end
-- 	return -1
-- end

-- function can_become_scout(color)
-- 	nb_led_sensed = #robot.colored_blob_omnidirectional_camera
-- 	if nb_led_sensed > 0 then 
-- 		for i = 1, nb_led_sensed do 
-- 			led = robot.colored_blob_omnidirectional_camera[i].color 
-- 			if led.red == color[1] and led.green == color[2] and led.blue == color[3]
-- 				then return false 
-- 			end 
-- 		end
-- 	end
-- 	return true
-- end

-- function is_door(led_source)
-- 	r = led_source.color.red
-- 	g = led_source.color.green
-- 	b = led_source.color.blue
-- 	-- if the color is orange, blue, red or magenta, it is a door
-- 	if (r == 255 and g == 0 and b == 0) or (r == 255 and g == 140 and b == 0)
-- 		or (r == 0 and g == 0 and b == 255) or (r == 255 and g == 0 and b == 255)
-- 		then return true
-- 	end
-- 	return false
-- end

-- function get_nb_unique_scouts() -- get the number of unique color scouts sensed
-- 	tot = 0
-- 	nb_led_sensed = #robot.colored_blob_omnidirectional_camera
-- 	for i = 1, nb_led_sensed do 
-- 		led = robot.colored_blob_omnidirectional_camera[i].color
		-- if led.red == 100 and led.green == 0 and led.blue == 200 then  -- purple
		-- 	tot = tot + 1
		-- elseif led.red == 0 and led.green == 255 and led.blue == 255 then -- cyan 
		-- 	tot = tot + 1
		-- elseif led.red == 100 and led.green == 200 and led.blue == 0 then -- light green
		-- 	tot = tot + 1
		-- elseif led.red == 200 and led.green == 200 and led.blue == 0 then -- yellow
		-- 	tot = tot + 1
		-- end 
-- 		if led.red == 128 and led.green == 0 and led.blue == 0 then  -- brown
-- 			tot = tot + 1
-- 		end
-- 	end
-- 	return tot
-- end 

function get_all_leds_sensed()
	all_leds = table.copy(robot.colored_blob_omnidirectional_camera)
	return all_leds
end

function step()
	-- door = processDoors()
	-- nb_unique_scouts_sensed = get_nb_unique_scouts()

	-- ==================== SCOUT
	-- if current_state == SCOUT then 
	-- 	-- if door detected and no scout with that color 	
	-- 	if door ~= -1 then
	-- 		if nb_unique_scouts_sensed == 4 then 
	-- 			current_state = MOVE 
	-- 		else 
	-- 			color = map_doors_colors(robot.colored_blob_omnidirectional_camera[door].color)
	-- 			if can_become_scout(color) and nb_unique_scouts_sensed < 4 then 
	-- 				robot.leds.set_single_color(13, color[1], color[2], color[3])
	-- 				is_scout = true
	-- 				log("je suis scout !!")
	-- 				current_state = MOVE
	-- 			end
	-- 		end
	-- 	end
	all_leds_sensed = get_all_leds_sensed()

	-- ==================== MOVE
	if current_state == MOVE then 
		robot.wheels.set_velocity(1,1)
	end
end



function reset()
	current_state = SCOUT
	robot.colored_blob_omnidirectional_camera.enable()
	is_scout = false
end



function destroy()
end
