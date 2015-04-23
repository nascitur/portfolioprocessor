Setup instructions for portfolioprocessor.py

1) You must have Python installed. If you have a mac you're good to go, otherwise you'll need to download it.  This has only been tested on a mac.
2) Copy portfolioprocessor.py to your home folder or whatever folder you can easily navigate to.
3) Go Jira Portfolio Plan: choose "Plan...Export" from the "Plan" button  on the right.  Uncheck both boxes and save to your Desktop as export.xml.
4) Create a folder on the desktop called "output" You should create a folder on the desktop named "output" and give it permissions "chmod -R 755 output"
4) Open Terminal (on Mac: Applications...Utilities...terminal)
5) Type "python portfolioprocessor.py" and follow the instructions... hit enter to use the default name and location.
6) It should output a CSV file to your Desktop/Output folder with the date and time.


Advanced:
- If you want to save to a folder or use a different name (for example Downloads/IronFistPlan.xml) then just put that full path into the prompt when it asks for the file name.
- Note if you want to make this executable with just the file name:
1) make the file executable:
2) chmod +x portfolioprocessor.py
3) and put it in a directory on your PATH (can be a symlink):
4) export PATH=/my/directory/with/pythonscript:$PATH
5) For permanence add that at the bottom of your .bashrc or .bash_profile
