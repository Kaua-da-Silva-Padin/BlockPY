import os
import shutil
import requests
from rich import print
from rich.prompt import Prompt
from rich.panel import Panel
from textwrap import dedent

samples_API = 'https://blockpyapi.vercel.app'

def write_file(file: str, txt: str) -> None:
    with open(file, 'w') as f:
        f.write(dedent(txt))

def fetch_sample(endpoint: str, params):
    res = requests.get(
        samples_API + endpoint,
        params=params
    ).json()
    return res

def main() -> None:
    light_themes = ['cosmo', 'flatly', 'journal', 'litera', 'lumen', 'minty', 'pulse', 'sandstone', 'united', 'yeti', 'morph', 'simplex', 'cerculean']
    
    dark_themes = ['solar', 'superhero', 'darkly', 'cyborg', 'vapor']
    
    sample_components = ['label', 'input', 'textarea', 'button']
    
    try:
        print(Panel('[bold green]Ttkbootstrap Project Creator[/bold green]', expand=False))
        project_name = Prompt.ask(
            'Project Name',
            default='Sample Project'
        )
        
        file_path = f'{project_name}/main.py'
        
        if not os.path.exists(file_path):
            theme = Prompt.ask(
                'Project Theme',
                choices=['DARK', 'LIGHT'],
                default='DARK',
                case_sensitive=False
            ).lower()
            
            if theme == 'dark':
                theme = Prompt.ask(
                    'Choose a dark theme',
                    choices=dark_themes,
                    default='DARK'
                )
            else:
                theme = Prompt.ask(
                    'Choose a light theme',
                    choices=light_themes,
                    default='cosmo'
                )
            
            os.makedirs(f'{project_name}/components')
            
            for component in sample_components:
                component_path = f'{project_name}/components/{component}'
                os.makedirs(component_path)
                write_file(
                    f'{component_path}/ui.py',
                    fetch_sample(
                        '/components',
                        {'name': component}
                    )['sample']
                )
                
            write_file(
                file_path,
                fetch_sample(
                    '/main',
                    {
                        'title': project_name,
                        'theme': theme
                    }
                )['sample']
            )
            
            run = Prompt.ask(
                'Run your project now?',
                default='N',
                choices=['N', 'NO', 'YES', 'Y'],
                case_sensitive=False
            ).lower()
            
            if run == 'y' or run == 'yes':
                print(Panel('[bold italic blue]Starting Project...[/bold italic blue]', expand=False))
                os.system(f'python {file_path}')
                
        else:
            overwrite = Prompt.ask(
                '[bold red]A project is already created in the current folder, overwrite it?[/bold red]',
                default='NO',
                case_sensitive=False,
                choices=['Y', 'N', 'YES', 'NO']
            ).lower()
            
            if overwrite == 'y' or overwrite == 'yes':
                shutil.rmtree(project_name)
                
                print(Panel(f'[bold italic green]Your "{project_name}" project[/bold italic green] was [bold red]overwritten![/bold red]\n[bold italic green]Creating new one...[/bold italic green]', expand=False))
                
                main()
                
    except Exception as e:
        print(Panel(f'[bold red]Something went wrong!\n{e}[/bold red]', expand=False))
        os.system('pause')
main()