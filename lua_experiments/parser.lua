-- Use Shift + Click to select a robot
-- When a robot is selected, its variables appear in this editor

-- Use Ctrl + Click (Cmd + Click on Mac) to move a selected robot to a different location



-- Put your global variables here

function readLines(file_path)
	local f = io.open(file_path, "rb")
	local all_lines = {}
	
	for line in io.lines(file_path) do
		table.insert(all_lines, line)
	end
	return all_lines
end

all_lines = readLines("simulation_parameters.txt")
MAX_TURN_STEPS = all_lines[1]
FWD_STEPS = all_lines[2]
MAX_ALIGN_STEPS = all_lines[3]
FWD_VELOCITY = all_lines[4]
ENTER_VELOCITY = all_lines[5]
ROTATE_VELOCITY = all_lines[6]
AVOID_DISTANCE = all_lines[7]

--local content = readAll("simulation_parameters.txt")
lines = readLines("simulation_parameters.txt")

--[[ This function is executed every time you press the 'execute' button ]]
function init()
   -- put your code here
	log(robot.id .. MAX_TURN_STEPS)
end



--[[ This function is executed at each time step
     It must contain the logic of your controller ]]
function step()
   -- put your code here
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
