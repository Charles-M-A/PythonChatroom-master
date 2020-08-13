Description:
------------------------------------------------------------------------------------------------------------------------
A very basic chat room with the following functions:
    --> user authentication
        > first time input of name and password is stored (users.csv).
        > password is encrypted using Fernet method
        > second time input of a name iis cross checked with the stored credentials
    --> create rooms
        > possible to create multiple rooms
        > each room is capable of having many users
    --> list
        > list all available rooms
    --> join
        > join any of the available rooms
        > can be used to switch to a new room
    --> leave
        > can leave the current roomm
    --> quit
        > close the program (logout)
    --> private chat
        > can chat privately with any user
        > assumed that the user already knows the name of the person who he wants to chat with
    --> admin capabilities
        > functions that only the admin is capable of
            >> allUsers
                -- can view all the users connnected to the server
            >> kick
                -- can kick a particular user from any room
            >> admin also is like a normal user and still join room to send messages
    --> any message sent is stored with a timestamp in two csv files
        > an encrypted message file (enc_convo.csv)
        > an unencrypted message file (convo.csv)
------------------------------------------------------------------------------------------------------------------------

Flaws
------------------------------------------------------------------------------------------------------------------------
--> Have not used threads
    > reason is that using threads led to a deadlock
        >> the recv() & send() fuctions cannot be used simultaneously  as they both are blocking
        >> the print() and input() function cannot be used simultaneously in a terminal
        >> a solution to use both print() and input() together is to use the curses package
        >> curses allows us to control the terminal completely but it cannot be used for windows
        >> i do not have a good understanding of how to use curses considering the short time
        >> solution is to use classes, objects and functions
    > tried to solve it using multiprocessing and asyncio packages but did not work
        >> still a deadlock
--> will have to press enter every time to get new messages printed onto screen
    > it can be solved by using a GUI
    > did not find time to develop te GUI
    > i have tried it with a tkinter GUI that i found to test
        >> the GUI client is not attached as it not my work
--> do not have many ways to handle exceptions
    > only some have been implemented
------------------------------------------------------------------------------------------------------------------------

Commmon errors
------------------------------------------------------------------------------------------------------------------------
--> having extra newline in the csv files can throw errors
--> index out of bounds
    > correct - private username msg
    > incorrect - private (or) private username
        > such erroors have not beem handled yet
------------------------------------------------------------------------------------------------------------------------