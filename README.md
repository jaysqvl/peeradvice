# 🏫 peerAdvice
**Contributors:** Shariq Imran Hassan, Sujal Bolia, Nima Motieifard, Jay Esquivel Jr

Couldn't find what you were looking for on the UBC webpage or with UBC advisors? Looking for consultation, advice, or just a different perspective on your academic situation?

The peerAdvice concept provides exactly that in a peer-to-peer connection with someone who truly understands you.

## Demonstration
[![WATCH THE FULL THING HERE]](https://youtu.be/_7WZNNuexCQ)
![peerAdvice](https://github.com/jaysqvl/peeradvice/blob/main/demo_media/peeradvice.gif?raw=true)

**Implemented Features:**
* Google Authentication Deployed Using FireBase
* PostgreSQL User Database
* Fully Functioning Flask Back-end
* Calendly API for client-to-advisor booking
* React Front-end (Coming Soon)

## How it works
1. Sign-up using google-authentication
2. Check out the list of all available advisors and their area of expertise
3. Schedule an appointment with Calendly
4. Meet-up and discuss!

## Installation Instructions

- Use Python 3.10 or newer (CI tests 3.10 and 3.12) and PostgreSQL. Installing the existing `psycopg2` driver from source also needs a C compiler and libpq development headers.
- Run `python -m pip install --require-hashes --only-binary=:all: --no-binary=psycopg2 -r requirements.lock` inside a virtual environment.
- Create a PostgreSQL database
  - Add the two tables in [`setup.sql`](setup.sql)
  - Edit the database connection URI in [`.env.example`](.env.example) and rename the file to `.env`
- Run `python server.py` to run the app!

### Dependency verification

CI uses a disposable PostgreSQL database and runs `python -m unittest discover -s tests -v` against the real Flask routes, Jinja templates, SQL statements, and psycopg2 driver. Tests refuse a missing, non-loopback, or non-test `TEST_DATABASE_URL`; never point them at application data. The test database must be named `peeradvice_dependency_tests`.

For local testing, create that empty database and set a loopback `TEST_DATABASE_URL` before running the test command. Tests recreate the two tables from `setup.sql` and truncate them between cases. They verify profile creation/read/update, redirects, advisor listing, HTML escaping, and CORS behavior, not live Firebase login or Calendly bookings.

`requirements.txt` pins direct dependencies; `requirements.lock` pins and hashes their full tree. With libpq build headers available, regenerate the lock with `uv pip compile requirements.txt --python-version 3.10 --generate-hashes --output-file requirements.lock`, then verify both CI runtimes.

## Challenges
**Feature management:**
* For 3 out of 4 of us, this hackathon was a first. Not knowing what to expect as well as due to our sheer excitement and eagerness to dive in, we bit off more than we could initially chew off. Wanting to implement a variety of novel APIs and use technologies and languages we have never touched before such as react and typescript, we ended up spending the first ~7ish hours of the hackathon with just setup.

**Language Gap:**
* With our expertise being in different coding languages, we had to settle for our commonalities to finally all get on the same page.
* We stumbled a bit with compatibility as not all of our machines produced the expected behaviour of our program. A possible solution to this could have been implementing a containerized application environment technology such as docker.

## Accomplishments
* We were able to solve all of our problems together efficiently despite being newly formed and met
* Were able to experiment and explore features and although not fully implement, understand to some degree their requirements for the future
