# Reflected CSRF Attacks and Mitigation: CVE-2021-32677 Demo

Anders Lie

## Corresponding Research Paper

Available in this repository, [here](CPRE_530_Research_Paper.pdf).

## Installing the vulnerable version of FastAPI and its dependencies:
```
pip install -r requirements.txt
```
You may wish to do this step in a virtual enviornment.

## Running the Target Site
```
cd target-site
python server.py
```

## Running the Attacker Site
```
cd attacker-site
```
Run the HTTP server of your choice in this directory.
Make sure to run on a different port than the target site.
For example, using Python's built-in simple HTTP server on port 5000:
```
python -m http.server 5000
```