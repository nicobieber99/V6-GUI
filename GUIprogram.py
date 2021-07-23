# img_viewer.py

import PySimpleGUI as sg
import os.path
from vantage6.client import Client

#nicobieber99/v6-mean:1.0
server_url = "http://127.0.0.3"
port = 5000
api_path = "/api"
client = Client(server_url, port, api_path, verbose = True)

final_colab = 0

# First the window layout in 2 columns



credentials = [

    [sg.Text('Username'), sg.InputText(key='Username')],
    [sg.Text('Password'), sg.InputText(key='Password', password_char='*')]
    # [sg.Text('Username')],
    # [sg.Text('Enter something on Row 2'), sg.InputText()]
    # [sg.Button('Ok'), sg.Button('Cancel')]
      # ],
    # [
    #     sg.Text("Password"),
    #     sg.In(size=(25, 1), enable_events=True, key="-PASSWORD-"),
    # ],
    # [
    #     sg.Listbox(
    #         values=[], enable_events=True, size=(40, 20), key="-FILE LIST-"
    #     )
    # ],
]
task_info = [  [sg.Text('Task name'), sg.InputText(key='TaskName')],
            [sg.Text('Algorithm name'), sg.InputText(key='Algorithm')],
            [sg.Text('Collaboration name'), sg.InputText(key='Collaboration')],
            [sg.Text('Input (optional)'), sg.InputText(key='Input')],
            [sg.Text('Description (optional)'), sg.InputText(key='Description')],
            [sg.Text('Organizations (optional)'), sg.InputText(key='Organizations')],
            [sg.Button('Send task')] ]

# ----- Full layout -----
layout = [
    [
        sg.Column(credentials),
        sg.Column(task_info)
    ]
]

window = sg.Window("Image Viewer", layout)

while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    # Folder name was filled in, make a list of files in the folder
    elif event == 'Send task':
        client.authenticate(values['Username'], values['Password'])
        client.setup_encryption(None)
        collaboration1 = client.collaboration.list(fields = ('id', 'name'))

        for collaborations in collaboration1:
    	    if collaborations.get('name') == values['Collaboration']:
                final_colab = collaborations.get('id')

        organizations = [1,2]
        if values['Organizations'] != '':
            organizations.append(int(values['Organizations']))

        ## TODO: implement parsing and fetching of org id for organizattion selection
    	##if organizations_run != ''
    	##	organizations = client.organization.list(fields = ('id', 'name'))
    	##	for organization in Organizations
        print(values['TaskName'], values['Algorithm'])

        client.task.create(final_colab, organizations, values['TaskName'], values['Algorithm'],
        values['Description'], values['Input'])

        #client.task.create(collaboration_id, organizations, name, image, description, tinput)

    	#metadata = client.post_task(name, image, 1, tinput, description, organizations)
    	#task_id = metadata.get('id')
    	#print(task_id)
    	## TODO: Find a way to get the result id of the sent task

    	#client.get_results(task_id, None, False, None)

    	#result_id = 10
        client.get_results()

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
