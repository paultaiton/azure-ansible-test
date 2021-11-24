upload this entire directory to an azure cloud shell (or a compatible bash shell location.)
run the following commands as your own unprivileged user (no root required):
  cd ~/resource_tag_convert
	python3 -m venv .venv
	source .venv/bin/activate
	pip install -r requirements.txt

the environment is now set up. Each time you need to re-activate your python virtual environment, you can do so by:
  source .venv/bin/activate

Edit the resource_tag_convert.py file, line 12+ "subscription_names = []"  to be a list of strings of the targeted subscription names.
Then after your python virtual environment is active, run:
  python resources_tag_convert.py
