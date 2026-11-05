# Project Plan

This plan sets out what the project aims to do, what will be built, and when. It is a working plan and may change as the project progresses. Any changes are recorded at the bottom of this page.

## Aim

To investigate whether a Kinect camera, a slow-motion phone camera and an AI coach can give golfers accurate feedback on their swing, and to build a working prototype that shows this.

## What Will Be Built

- The Kinect tracks the golfer's body from the front.
- A phone records the swing from behind in slow motion to track the club.
- Recording starts and stops automatically, so the golfer does not press any buttons.
- The two recordings are lined up so they match in time.
- The swing is split into four stages: address, top of backswing, impact and finish.
- Swing measurements are calculated, such as hip turn, shoulder turn, spine angle, head movement and tempo.
- The biggest fault in the swing is found.
- An AI coach explains the fault and suggests a drill from a drill library.
- Results are shown on a laptop web app.
- Sessions are saved so progress can be tracked.

## Not Included

- Measuring ball flight
- Measuring the club face angle
- A mobile app for viewing results

## Milestones

- **M0 - Planning and setup**  GitHub repo, documentation, CI pipeline
- **M1 - Kinect capture** -  Kinect body tracking working
- **M2 - Phone capture, backend and syncing** phone records automatically, backend receives both recordings and they are lined up
- **M3 – Club detection model** club head images labelled and YOLO model trained
- **M4 – Swing analysis** swing stages, measurements and fault detection
- **M5 – Web app and database** results screens and saved sessions
- **M6 – AI coaching** drill library and AI feedback
- **M7 – Testing and evaluation** accuracy testing and user feedback
- **M8 – Dissertation and submission** write-up, demo video and final submission

## Risks

- **Kinect not available or not working** – confirm access early; use phone-only body tracking as a backup.
- **Kinect too slow for a fast swing (30fps)** – use the Kinect for body movement and the phone (240fps) for the club.
- **Lining up the two recordings** – match them at the moment of impact.
- **Blurry club head in video** – record in slow motion with good lighting.
- **AI gives wrong advice** – the AI only suggests drills from the drill library, and is given the real swing measurements.
- **Running out of time** – track progress weekly against the milestones and focus on the core features.

## How Progress Is Tracked

- Each task is a GitHub issue, linked to a milestone.
- Tasks move across a GitHub Project board: Backlog, In progress, Done.
- Supervisor meetings are recorded in `docs/meetings`.
- Research is kept in a handwritten notebook and summarised in `docs/research`.

## Changes to the Plan

- **3 Nov 2026** – Plan created from the approved project proposal.

- **4 Nov 2026** - CD pipeline moved to later in the project, as there is nothing to deploy until the backend and web app exist.

- **4 Nov 2026** - Dates removed from the milestones in this plan, as they change week to week. Due dates are kept on the GitHub milestones instead.
