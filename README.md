# wave-apps
Step 1: 
    To run the app first Install the h2o-wave package from PyPI:        

        pip install h2o-wave

But,
    We recommended method is to install h2o_wave into a virtual environment for best practice 
    so you can work with multiple projects which require different versions of packages

        python3 -m venv venv
        source venv/bin/activate
        pip install h2o-wave

Step 2:
    download and unzip wave package from https://wave.h2o.ai/docs/installation    (Ex:- wave-0.25.2-linux-amd64)
    or You can simply do it with the command  
        
        wave fetch

Step 3:
    Then install needed dependencies:

        cd wave-0.25.2-linux-amd64     (may differ according to your OS)
        pip install -r examples/requirements.txt

        wave run --no-reload examples.tour (you can try this to check all installed properly and have a practice of h2o_wave)

Step 4:
    Run the app:

        wave run app 

    Now You can view your app by navigating to localhost:10101  in your web browser
