import docker

#TODO: Transfor into singleton to avoid opening a client multiple times
#TODO: Make sure this runs async
def run_job(image: str, command: dict = '') :
    try:
        # We're assuming this api will be running in the server in which docker is running
        client = docker.DockerClient(base_url='unix://var/run/docker.sock')
    except Exception as err:
        print(f"[ERROR] Something went wrong while trying to stablish connection to docker socket...\n{err}")
    
    try:
        output = client.containers.run(image, command, detach=True)
        return output
    except Exception as err:
        print(f"[ERROR] Failed to run job {image}\n{err}")