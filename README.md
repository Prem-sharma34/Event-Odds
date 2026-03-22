# EventOdds

**EventOdds** is a real-time audience prediction platform designed for live events where participants compete and spectators can predict the most likely winner.

The platform allows users to cast predictions during an event, while the system dynamically updates probability-style odds based on audience sentiment. Results are broadcast in real time so viewers can see how predictions evolve as more people participate.

## Concept

Many events involve multiple participants competing for a final outcome — for example:

* University hackathons
* Local football tournaments
* Singing competitions
* Startup pitch events
* Debate contests

EventOdds provides a lightweight system where audiences can interact with the event by predicting which participant they believe will win. These predictions are aggregated to produce **live odds**, giving a real-time view of audience sentiment.

## Core Idea

The platform models each event with:

* **Events** – competitions such as hackathons or tournaments
* **Participants** – teams or individuals competing in the event
* **Predictions** – audience votes indicating the most likely winner
* **Live Odds** – dynamically calculated probabilities based on predictions

When a user submits a prediction, the backend updates the aggregated vote counts and broadcasts updated odds to connected clients.


## Current Status

This project is currently **under active development**.

The goal is to build a high-concurrency backend system capable of:

* handling simultaneous predictions
* maintaining transactional integrity for voting
* broadcasting live updates to connected clients

Initial development is focused on implementing the core backend architecture.

## Planned Architecture

* **Backend Framework:** FastAPI
* **Database:** PostgreSQL
* **Real-Time Updates:** WebSockets
* **Containerization:** Docker
* **Package manager:** uv

The system will be designed with an **async backend architecture** to support concurrent users and real-time event updates.

Further updates will be added as development progresses.
