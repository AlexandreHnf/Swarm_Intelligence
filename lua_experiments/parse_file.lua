function readAll(file)
    local f = assert(io.open(file, "rb"))
    local content = f:read("*all")
    f:close()
    return content
end


content = readAll("simulation_parameters.txt")
log("speed " .. content[1])