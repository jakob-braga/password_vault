import tkinter as tk
import hashlib
from functools import partial
from password_data import PasswordData

class Application:

    def __init__(self):
        # init nessiasry data
        self.window = tk.Tk()
        self.window.title('Password Vault')
        self.password_data = PasswordData()

        # initial login
        self.login_frame = tk.Frame(self.window)
        self.login_box = tk.Entry(self.login_frame)
        self.login_response_box = tk.Label(self.login_frame)

        # main display
        self.main_frame = tk.Frame(self.window)
        self.sites_frame = tk.Frame(self.main_frame)
        self.control_frame = tk.Frame(self.main_frame)
        self.password_list = []

        # editing
        self.details_frame = tk.Frame(self.window)
        self.info_side = tk.Frame(self.details_frame)
        self.action_side = tk.Frame(self.details_frame)
        self.action_confirmation = tk.Label(self.action_side)
        self.site_name = tk.Entry(self.info_side)
        self.site_username = tk.Entry(self.info_side)
        self.site_password = tk.Entry(self.info_side)

    #########
    # login #
    #########
    def login(self):
        # check if first time
        hash_file = open('./password_hash.dat', 'r')
        _hash = hash_file.read()
        hash_file.close()

        if _hash == '':
            greeting = tk.Label(
                self.login_frame,
                text="Enter Password You Wish to Use"
            )
        else:
            greeting = tk.Label(
                self.login_frame,
                text="Enter Password"
            )
        greeting.pack()
        self.login_box['width'] = 50
        self.login_box.pack()
        continue_button = tk.Button(master=self.login_frame, text='submit', command=self.verify_login)
        continue_button.pack()
        self.login_response_box.pack()
        self.login_frame.pack()
    
    def verify_login(self):
        hash_file = open('./password_hash.dat', 'r')
        _hash = hash_file.read()
        hash_file.close()
        
        if _hash != '':
            if self.password_data.verify_login(self.login_box.get()):
                self.login_frame.destroy()
                self.display_passwords()
            else:
                self.login_response_box['text'] = 'incorrect password'
        else:
            # save hash for future
            hash_file = open('./password_hash.dat', 'w')
            new_hash = hashlib.sha224(self.login_box.get().encode()).hexdigest()
            hash_file.write(new_hash)
            hash_file.close()
            # register hash with verify login
            self.password_data.verify_login(new_hash)
            self.login_response_box['text'] = 'password set, restart to use'

    ################
    # main display #
    ################
    def init_main_display(self):
        self.password_data.get_passwords()
        self.main_frame = tk.Frame(self.window)
        self.sites_frame = tk.Frame(self.main_frame)
        self.control_frame = tk.Frame(self.main_frame)
        self.password_list = []

    def display_passwords(self):
        # make site/application column on left and minsize it
        self.sites_frame['relief'] = tk.SUNKEN
        self.main_frame.columnconfigure(0, minsize=300, weight=1)
        self.main_frame.rowconfigure(0, minsize=20, weight=1)

        # add title to left and right
        site_title = tk.Label(self.main_frame, text='Sites/Applications')
        site_title.grid(column=0, row=0)
        options_title = tk.Label(self.main_frame, text='Options')
        options_title.grid(column=1, row=0)

        # loop through site/applications and display them
        for site in self.password_data.passwords:
            self.password_list.append(
                tk.Button(self.sites_frame, width=50, text=site, command=partial(self.set_up_details, site))
            )
        for i in range(len(self.password_list)):
            #self.password_list[i].grid(row=i, column=0, sticky='w')
            self.password_list[i].pack()
        self.sites_frame.grid(row=1, column=0, sticky='w', padx=5, pady=5)

        # handle buttons on the right
        self.control_frame['relief']=tk.RAISED
        add_button = tk.Button(
            self.control_frame,
            text='add',
            width=10,
            height=3,
            command=partial(self.set_up_details, '')
        )
        exit_button = tk.Button(
            self.control_frame,
            text='exit',
            width=10,
            height=3,
            command=self.exit_out
        )
        add_button.pack()
        exit_button.pack()
        self.control_frame.grid(row=1, column=1, padx=5, pady=5)

        self.main_frame.pack()

    ####################
    # details deisplay #
    ####################
    def init_details(self):
        self.details_frame = tk.Frame(self.window)
        self.info_side = tk.Frame(self.details_frame)
        self.action_side = tk.Frame(self.details_frame)
        self.action_confirmation = tk.Label(self.action_side)
        self.site_name = tk.Entry(self.info_side)
        self.site_username = tk.Entry(self.info_side)
        self.site_password = tk.Entry(self.info_side)
    
    def set_up_details(self, site):
        self.main_frame.destroy()
        self.init_details()
        # set up left side
        info_side_width = 30
        # site if its not '' then put in the site were viewing
        if site != '':
            self.site_name.insert(tk.END, site)
            self.site_username.insert(tk.END, self.password_data.passwords[site]['username'])
            self.site_password.insert(tk.END, self.password_data.passwords[site]['password'])
        site_label = tk.Label(
            self.info_side,
            text='Site/Application Name',
            width=info_side_width
        )
        site_label.pack()
        self.site_name['width'] = info_side_width
        self.site_name.pack()
        # username
        user_label = tk.Label(
            self.info_side,
            text='Username',
            width=info_side_width
        )
        user_label.pack()
        self.site_username['width'] = info_side_width
        self.site_username.pack()
        # password
        pass_label = tk.Label(
            self.info_side,
            text='Password',
            width=info_side_width
        )
        pass_label.pack()
        self.site_password['width'] = info_side_width
        self.site_password.pack()

        # set up right side
        back_button = tk.Button(
            self.action_side,
            text='back',
            width=10,
            height=3,
            command=self.back_to_list
        )
        save_button = tk.Button(
            self.action_side,
            text='save',
            width=10,
            height=3,
            command=partial(self.save, site)
        )
        delete_button = tk.Button(
            self.action_side,
            text='delete',
            width=10,
            height=3,
            fg='red',
            command=partial(self.delete, site)
        )
        back_button.pack()
        save_button.pack()
        delete_button.pack()
        self.action_confirmation.pack()

        self.info_side.grid(row=0, column=0, padx=5, pady=5)
        self.action_side.grid(row=0, column=1, padx=5, pady=5)

        self.details_frame.pack()

    #################
    # functionality #
    #################

    def save(self, site):
        # check for adding
        if site == '':
            self.password_data.passwords[self.site_name.get()] = {
                'username': self.site_username.get(),
                'password': self.site_password.get()
            }
            self.password_data.save_passwords()
        # check for if the site name has been replaced
        elif site != self.site_name.get():
            self.password_data.passwords.pop(site)
            self.password_data.passwords[self.site_name.get()] = {
                'username': self.site_username.get(),
                'password': self.site_password.get()
            }
            self.password_data.save_passwords()
        else:
            self.password_data.passwords[site] = {
                'username': self.site_username.get(),
                'password': self.site_password.get()
            }
            self.password_data.save_passwords()
        
        self.action_confirmation['text'] = 'Saved'
    
    def delete(self, site):
        if site != '' and site in self.password_data.passwords.keys():
            self.password_data.passwords.pop(site)
            self.action_confirmation['text'] = 'Delete Successful'
        else:
            self.action_confirmation['text'] = 'Nothing to Delete'
        self.password_data.save_passwords()

    def back_to_list(self):
        self.details_frame.destroy()
        self.init_main_display()
        self.display_passwords()

    def exit_out(self):
        self.window.destroy()
        print('goodbye')

    def loop(self):
        self.window.mainloop()
