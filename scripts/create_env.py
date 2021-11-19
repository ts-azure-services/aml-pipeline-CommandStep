from authentication import ws

from azureml.core.environment import Environment
def create_and_build_env(
    name=None,
    ws=None,
    conda_file_path='./conda.yml',
    docker_file_path = './Dockerfile'):

    """Create environment based on specifications"""
    env = Environment.from_conda_specification(name=name, file_path=conda_file_path)
    env.docker.base_image=None
    env.docker.base_dockerfile = docker_file_path
    env.register(workspace=ws)

    ## Trigger a build, will otherwise happen during the experiment run
    build=env.build(workspace=ws)                                                                                      
    build.wait_for_completion(show_output=False)
    return env

# Create and build the environment
env_name = 'new_env'
env = create_and_build_env(name=env_name,ws=ws)
print(f" New environment name is {env_name}")
