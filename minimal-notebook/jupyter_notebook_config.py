import os
c.Spawner.environment = {}
port = int(os.environ.get('JUPYTER_NOTEBOOK_PORT', '8080'))

c.NotebookApp.ip = '0.0.0.0'
c.NotebookApp.port = port
c.NotebookApp.open_browser = False
c.NotebookApp.quit_button = False

if os.environ.get('JUPYTERHUB_SERVICE_PREFIX'):
    c.NotebookApp.base_url = os.environ.get('JUPYTERHUB_SERVICE_PREFIX')

password = os.environ.get('JUPYTER_NOTEBOOK_PASSWORD')
if password:
    import notebook.auth
    c.NotebookApp.password = notebook.auth.passwd(password)
    del password
    del os.environ['JUPYTER_NOTEBOOK_PASSWORD']

image_config_file = '/opt/app-root/src/.jupyter/jupyter_notebook_config.py'

if os.path.exists(image_config_file):
    with open(image_config_file) as fp:
        exec(compile(fp.read(), image_config_file, 'exec'), globals())

# Set Nvidia GPU configuration.

c.Spawner.environment.update(dict(
       NVIDIA_VISIBLE_DEVICES='all',
       NVIDIA_DRIVER_CAPABILITIES='compute,utility',
       NVIDIA_REQUIRE_CUDA='cuda>=8.0'))

c.KubeSpawner.extra_resource_limits = {'nvidia.com/gpu': '1'}