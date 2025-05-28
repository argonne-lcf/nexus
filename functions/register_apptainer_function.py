import globus_compute_sdk

# Test function when workers are deployed outside of the container.
# This is an alternative to executing functions directly within
# running containers. If the science teams come with already-built 
# container images, this approach allows them to preverse their images.
# Otherwise, they would need to re-build them include Globus Compute.
#
# Below was an example to run the LSST/DESC environment.
def test(sif_sing_path=None):
    """
    Test function that will load the LSST/Desc environment and print
    the location of the python executable from within the container.
    
    Argument
    --------
        sif_sing_path (str): Full path to the Apptainer .sif or .sing file
    """

    # Import the necessary python packages
    import subprocess

    # Make sure the sif_sing_path is a string
    if not isinstance(sif_sing_path, str):
        return "Error: 'sif_sing_path' parameter should be provided as a string."

    # Define all commands that need to be executed in the container
    # This needs to be hardcoded or vetted (no arbitrary code execution)
    commands = """
    source /opt/lsst/software/stack/loadLSST.bash
    setup lsst_distrib
    eups list lsst_distrib
    command -v python
    """

    # Define subprocess arguments
    kwargs = {
        "shell": True, 
        "check": True,
        "text": True,
        "stdout": subprocess.PIPE,
        "stderr": subprocess.PIPE,
        "executable": "/bin/bash"
    }

    # Define the Apptainer command to be executed on the compute node
    one_line_command = " && ".join(line.strip() for line in commands.strip().splitlines() if line.strip())
    apptainer_command = f"apptainer exec --fakeroot {sif_sing_path} bash -c '{one_line_command}'"

    # Execute the command lines
    try:
        result = subprocess.run(apptainer_command, **kwargs)
    except subprocess.CalledProcessError as e:
        return f"Error: {e}"
        
    # Return command line output
    return result.stdout


# Creating Globus Compute client
gcc = globus_compute_sdk.Client()

# # Register the function
COMPUTE_FUNCTION_ID = gcc.register_function(test)

# # Write function UUID in a file
uuid_file_name = "uuid_test_function.txt"
with open(uuid_file_name, "w") as file:
    file.write(COMPUTE_FUNCTION_ID)
    file.write("\n")
file.close()

# # End of script
print(f"\Function registered with UUID - {COMPUTE_FUNCTION_ID}")
print(f"The UUID is stored in {uuid_file_name}.\n")
