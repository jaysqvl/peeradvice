# 🏫 peerAdvice
**Contributors:** Shariq Imran Hassan, Sujal Bolia, Nima Motieifard, Jay Esquivel Jr

Couldn't find what you were looking for on the UBC webpage or with UBC advisors? Looking for consultation, advice, or just a different perspective on your academic situation?

The peerAdvice concept provides exactly that in a peer-to-peer connection with someone who truly understands you.

**Implemented Features:**
* Google Authentication Deployed Using FireBase
* PostgreSQL User Database
* Fully Functioning Flask Back-end
* React Front-end (Coming Soon)

## How it works
1. Sign-up using google-authentication
2. Check out the list of all available advisors and their area of expertise
3. Schedule an appointment with Calendly
4. Meet-up and discuss!

## Demonstration
[![WATCH HERE]](https://youtu.be/_7WZNNuexCQ)


## Installation Instructions

- Run `python -m pip install -Ur requirements.txt` (preferably inside a virtual env)
- Create a PostgreSQL database
  - Add the two tables in [`setup.sql`](setup.sql)
  - Edit the database connection URI in [`.env.example`](.env.example) and rename the file to `.env`
- Run `python server.py` to run the app!

## Challenges
**Feature management:**
* For 3 out of 4 of us, this hackathon was a first. Not knowing what to expect as well as due to our sheer excitement and eagerness to dive in, we bit off more than we could initially chew off. Wanting to implement a variety of novel APIs and use technologies and languages we have never touched before such as react and typescript, we ended up spending the first ~7ish hours of the hackathon with just setup.

**Language Gap:**
* With our expertise being in different coding languages, we had to settle for our commonalities to finally all get on the same page.
* We stumbled a bit with compatibility as not all of our machines produced the expected behaviour of our program. A possible solution to this could have been implementing a containerized application environment technology such as docker.

## Accomplishments
* We were able to solve all of our problems together efficiently despite being newly formed and met
* Were able to experiment and explore features and although not fully implement, understand to some degree their requirements for the future
