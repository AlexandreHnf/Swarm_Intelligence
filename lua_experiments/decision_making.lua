--[[
	TODO 
	- set individual leds on scout and followers
	- change probability of leaving : nb_leds / nb_robots
	- maybe change the way robots enter rooms

]]


-- states 
WALK = "WALK"
AVOID = "AVOID"
ENTER = "ENTER"
STOP = "STOP"
EXPLORE = "EXPLORE"
STAY = "STAY"



-- Global variables
current_state = EXPLORE -- current state of the robot
is_scout = false			-- if the robot is a scout

is_obstacle_sensed = false  -- if an obstacle has been sensed by the robot
is_door_sensed = false  		-- if a door has been sensed by the robot
is_in_room = false 			-- if a robot entered a room

room_quality_memory = 0 -- remembers only the last room's quality he visited
door = -1 			-- door that is sensed if there is any
color_detection = false

-- variables for obstacle avoidance
MAX_TURN_STEPS = 40
current_turn_steps = 0

-- variables for go straight behavior
FWD_STEPS = 200
current_fwd_steps = 0

--sleeping variables
SLEEP_STEPS = 200
current_sleep_steps = 0
BASE_LEAVE_PROB = 0.18 -- the basic probability to stay. It should be small enough to avoid splitting the group, but big enough to achieve stability


-- function used to copy two tables
function table.copy(t)
  local t2 = {}
  for k,v in pairs(t) do
    t2[k] = v
  end
  return t2
end


--[[ This function is executed every time you press the 'execute' button ]]
function init()
	current_state = EXPLORE
	robot.colored_blob_omnidirectional_camera.enable() -- enable LED detection
end



function step()

	-- if not color_detection then 
	-- 	robot.colored_blob_omnidirectional_camera.enable() -- enable LED detection
	-- 	color_detection = true
	-- end

	processObstacles() 		-- checks if there is any obstacle
	processDoors()				-- checks if there is a door nearby
	processRoom()				-- checks if a robot is fully in a room
	nb_leds_scout = get_nb_scout_leds()
	nb_active_neighbors = get_nb_active_robots()

	-- ================================== EXPLORE =====================================
	if current_state == EXPLORE then 
		if is_obstacle_sensed then 			-- OBSTACLE
			current_state = AVOID 
			current_turn_steps = math.random(MAX_TURN_STEPS)
		end
		if is_door_sensed then 				-- DOOR
			current_state = ENTER
			current_fwd_steps = FWD_STEPS
		end
		if not is_obstacle_sensed and not is_door_sensed then 
			robot.wheels.set_velocity(40,40)
		end			

	-- ================================== AVOID =====================================
	elseif current_state == AVOID then 
		robot.wheels.set_velocity(-10,10)	-- ROTATE LEFT
		current_turn_steps = current_turn_steps - 1
		if current_turn_steps <= 0 then
		   current_state = EXPLORE
		end
		
	-- ================================== ENTER =====================================
	elseif current_state == ENTER then 
		current_fwd_steps = current_fwd_steps - 1
		robot.wheels.set_velocity(40,40)
		if current_fwd_steps <= 10 and is_obstacle_sensed then 
			current_state = AVOID -- if encounter a wall, will gets stuck
		end
		if current_fwd_steps <= 0 then -- finished forwarding
		   current_state = STOP
		end

	-- ================================== STOP ======================================
	elseif current_state == STOP then 
		-- the robot just entered a room, so he stop to think and act
		robot.wheels.set_velocity(0, 0) 
		if not is_in_room then  -- if in central room, explore
			current_state = EXPLORE
		elseif is_in_room then  -- if in a special room
			room_quality_memory = get_room_quality() -- room quality
			
			-- room with scout => decide to stay or not
			if nb_leds_scout > 0 and not is_scout then 
				random = robot.random.uniform()
				if random < nb_leds_scout/11 then  
					-- stay with proba proportionnal to the scout's signal strength
					set_scout_colors()
					current_state = STAY
				else 
					current_state = EXPLORE -- leave
				end
			end

			if nb_leds_scout == 0 then  -- room without scout
				set_scout_colors()
				is_scout = true
			end 
		end 

	-- ================================== STAY =====================================
	elseif current_state == STAY then
		-- we stay in the same room as a specific scout robot
		robot.wheels.set_velocity(0,0)
		current_sleep_steps = current_sleep_steps + 1
		if current_sleep_steps == SLEEP_STEPS then -- time to decide
			current_sleep_steps = 0
			-- set the probability to leave based on how many robots we see	
			prob = BASE_LEAVE_PROB * (nb_active_neighbors+1) -- +1 is for this robot
			if robot.random.uniform() < prob then -- stay
				current_state = STAY
			else
				current_state = EXPLORE -- leave and explore
				robot.leds.set_all_colors(0, 0, 0) -- reset leds
			end
		end

	end -- end step big IF
	
	

end -- end function step


function set_scout_colors()
	-- map (0,1) to (1, 11) => floor((Q*10)+1)
	nb_leds_on = math.floor((room_quality_memory*10)+1)
	for i = 1, nb_leds_on do 
		robot.leds.set_single_color(i, 200, 200, 0)
	end
	robot.leds.set_single_color(13, 0, 255, 255) -- unique color cyan to identify the robot
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

function processDoors() -- checks if a door has been sensed (close enough)
	is_door_sensed = false 
	door = -1
	nb_led_sensed = #robot.colored_blob_omnidirectional_camera
	if nb_led_sensed > 0 then
		for i = 1, nb_led_sensed do 
			led_source = robot.colored_blob_omnidirectional_camera[i]
			if is_door(led_source) then 
				-- if door color detected and close enough
				if led_source.distance <= 30 then 
					if led_source.angle < math.pi/2 -- if the angle allows him to enter
						then is_door_sensed = true
						door = i
					end
				end 
			end
		end
	end
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

function get_nb_scout_leds()
	nb_leds_scout = 0
	nb_led_sensed = #robot.colored_blob_omnidirectional_camera
	if nb_led_sensed > 0 then 
		for i = 1, nb_led_sensed do
			-- yellow
			if robot.colored_blob_omnidirectional_camera[i].color.red == 200 and 
				robot.colored_blob_omnidirectional_camera[i].color.green == 200 then
				nb_leds_scout = nb_leds_scout + 1
			end
		end
	end
	return nb_leds_scout
end

function get_nb_active_robots()
	nb_active_robots = 0
	nb_led_sensed = #robot.colored_blob_omnidirectional_camera
	for i = 1, nb_led_sensed do 
		-- cyan
		if robot.colored_blob_omnidirectional_camera[i].color.green == 255 and 
		robot.colored_blob_omnidirectional_camera[i].color.blue == 255 then 
			nb_active_robots = nb_active_robots + 1
		end
	end
	return nb_active_robots
end


function reset()
   	current_state = EXPLORE
	is_obstacle_sensed = false
	is_door_sensed = false
	color_detection = false
	is_scout = false
	is_in_room = false
	current_turn_steps = 0
	number_robot_sensed = 0
	current_fwd_steps = 0
	current_sleep_steps = 0
	robot.colored_blob_omnidirectional_camera.enable() -- enable LED detection
end


function destroy()
end
