# img_viewer.py

import PySimpleGUI as sg
import os.path
from vantage6.client import Client
import time

#nicobieber99/v6-mean:1.0
server_url = "http://127.0.0.3"
port = 5000
api_path = "/api"
client = Client(server_url, port, api_path, verbose = True)

final_colab = 0

def create_window(window_title):

    if window_title == "Login":
        window_layout = [ [sg.Text('Username'), sg.InputText(key='Username')],
        [sg.Text('Password'), sg.InputText(key='Password', password_char='*')],
        [sg.Button('Log in')]
    ]

    elif window_title == "Main menu":
        window_layout = [ [sg.Text('What would you like to do:')],
                    [sg.Button('Create task')],
                    [sg.Button('Create user')],
                    [sg.Button('Create node')]
        ]

    elif window_title == "Create task":
        window_layout = [  [sg.Text('Task name'), sg.InputText(key='TaskName')],
                    [sg.Text('Algorithm name'), sg.InputText(key='Algorithm')],
                    [sg.Text('Collaboration name'), sg.Combo([], key='Collaboration', size=(30, 0))],
                    [sg.Text('Input (optional)'), sg.InputText(key='Input')],
                    [sg.Text('Description (optional)'), sg.InputText(key='Description')],
                    [sg.Text('Organizations (optional)'), sg.Listbox([], size =(40,10), select_mode = 'extended', key='Organizations')],
                    [sg.Text('Result:'), sg.Text(size =(40,10), key='Task_result')],
                    [sg.Button('Send task')],
                    [sg.Button('Back')]
        ]

    elif window_title == "Create user":
        window_layout = [  [sg.Text('Username'), sg.InputText(key='Username')],
                    [sg.Text('Password'), sg.InputText(key='Password')],
                    [sg.Text('First name'), sg.InputText(key='First_name')],
                    [sg.Text('Last name'), sg.InputText(key='Last_name')],
                    [sg.Text('Organization'), sg.Listbox([], size =(40,10), select_mode = 'single', key='Organization')],
                    [sg.Text('Role'), sg.Listbox([], size =(40,10), select_mode = 'single', key='Roles')],
                    [sg.Button('Finish')],
                    [sg.Button('Back')]
        ]

    layout = [
        [
            sg.Column(window_layout),
        ]
    ]

    window = sg.Window("Current window", layout, finalize = True)
    return(window)


window = create_window("Login")

while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    # Folder name was filled in, make a list of files in the folder
    elif event == 'Send task':
        colab_value = values['Collaboration'].get('id')
        print(values['Organizations'])
        organization = []
        organization.append(client.collaboration.get(colab_value)["organizations"][0]["id"])
        tinput = {
	       'master': 'true',
           'method': 'master',
           'args': [],
           'kwargs': {
                'column_name': values['Input']
            }
        }
        task = client.task.create(colab_value, organization, values['TaskName'], values['Algorithm'],
        values['Description'], tinput)
        task_id = task['id']
        task_info = client.task.get(task_id)
        attempts = 0
        while not task_info.get("complete") or attempts >10:
            task_info = client.task.get(task_id)
            attempts += 1
            time.sleep(4)
        window['Task_result'].update(client.result.get(task_info['results'][0]['id'])['result'])


    elif event == "Log in":
        client.authenticate(values['Username'], values['Password'])
        client.setup_encryption(None)
        window.close()
        ##Check if admin or regular user
        window = create_window("Main menu")


    elif event == 'Create task':
        window.close()
        window = create_window("Create task")
        collaborations = client.collaboration.list(fields = ('id', 'name'))
        organizationList = client.organization.list(fields = ('id', 'name'))
        window['Collaboration'].update(value='', values = collaborations)
        window['Organizations'].update(values = organizationList)

    elif event == 'Create user':
        window.close()
        window = create_window("Create user")
        organizationList = client.organization.list(fields = ('id', 'name'))
        window['Organization'].update(values = organizationList)
        roleList = client.role.list(fields = ('id', 'name'))
        window['Roles'].update(values = roleList)

    elif event == 'Finish':
        ##ERROR LIST HAS NO ATTRIBUTE GET PROBLEM HERE
        client.user.create(values['Username'], values['First_name'], values['Last_name'], values['Password'], values['Organization'].get('id'), values['Roles'].get('id'), [])

    elif event == 'Back':
        window.close()
        window = create_window("Main menu")
        #client.task.create(collaboration_id, organizations, name, image, description, tinput)

    	#metadata = client.post_task(name, image, 1, tinput, description, organizations)
    	#task_id = metadata.get('id')
    	#print(task_id)
    	## TODO: Find a way to get the result id of the sent task

    	#client.get_results(task_id, None, False, None)

    	#result_id = 10

    # A file was chosen from the listbox
    elif event == "-FILE LIST-":
    	try:
    		filename = os.path.join(
    			values["-FOLDER-"], values["-FILE LIST-"][0]
    		)
    		window["-TOUT-"].update(filename)
    		window["-IMAGE-"].update(filename=filename)
    	except:
    		pass




window.close()
