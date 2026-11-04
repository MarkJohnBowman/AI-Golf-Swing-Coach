# Requirements

This is the list of what the system needs to do, based on the objectives from the proposal and final design in my notebook. Each requirement has an ID so it can be linked to issues and tests later on. Must means it has to be in the final project, Should means it would be good to have.

## Who Uses It

- The golfer - hits balls at the range or indoors and gets feedback without touching anything.
- The person setting it up - sets up the laptop, Kinect and phone before the session. Usually this is the golfer too.

## Functional Requirements

### Capturing the Swing

- FR1 (Must) - The Kinect tracks the golfer's body in 3D from the front. Checked by making sure all 25 joints are recorded with a timestamp for every frame.
- FR2 (Must) - The phone records the swing from behind in slow motion. Checked by making sure the video is 240fps, or the highest the phone can do.
- FR3 (Must) - Recording starts and stops on its own. When the golfer sets up over the ball it starts, and when they finish the swing it stops. The golfer shouldn't have to press anything.
- FR4 (Should) - The phone connects to the laptop by scanning a QR code instead of typing anything in.
- FR5 (Must) - The phone video gets sent to the laptop automatically. It should arrive within about 10 seconds of the swing.

### Processing

- FR6 (Must) - The Kinect and phone recordings are lined up at impact. They should be within one Kinect frame (around 33ms) of each other.
- FR7 (Must) - The data gets cleaned up. Missing points are filled in (interpolation) and shaky data is smoothed out.
- FR8 (Must) - YOLO finds the club head in each frame of the phone video. The aim is at least 0.85 mAP@50 on the test images.
- FR9 (Must) - The swing is split into address, top, impact and finish. At least 90% should be within 3 frames of where I mark them by hand.

### Analysing the Swing

- FR10 (Must) - Swing metrics are worked out: spine angle, hip turn, shoulder turn, sway, head movement, tempo and swing plane. Each one is tested with data where the answer is already known.
- FR11 (Must) - Each metric is compared to a target range, with a source for where each range came from.
- FR12 (Must) - Faults are ranked by how far off the target they are, so the biggest fault is shown first.

### AI Coach

- FR13 (Must) - A drill library of around 50 drills, each one tagged with the fault it helps fix.
- FR14 (Must) - The system finds the right drills for the top fault using RAG. A correct drill should be in the top three results at least 90% of the time.
- FR15 (Must) - The LLM explains what went wrong, why it matters and gives one drill. It should only ever suggest drills from the library.

### Web App

- FR16 (Must) - The app shows if the Kinect and phone are connected.
- FR17 (Must) - Results come up on their own after each swing, no clicking needed.
- FR18 (Must) - The results screen plays the skeleton replay and the phone video with the club path side by side, in sync, with the four swing phases marked.
- FR19 (Must) - The metrics, top fault and drill are all visible on the laptop screen without scrolling.
- FR20 (Must) - Sessions are saved and there's a chart to show progress over time.

## Non-Functional Requirements

- NFR1 (Speed) - Feedback should be on screen within 20 seconds of the swing.
- NFR2 (Ease of use) - The golfer doesn't touch any device during a session.
- NFR3 (Ease of use) - The system should score at least 68 on the SUS questionnaire when tested with users.
- NFR4 (Reliability) - If the Kinect or phone drops out, the app shows an error and picks back up when it reconnects.
- NFR5 (Privacy) - Videos stay on the laptop. Only the metrics and drill text get sent to the LLM.
- NFR6 (Code quality) - All the CI checks have to pass before anything is merged.
- NFR7 (Testing) - Recorded swings can be played back through the system, so it can be tested without the Kinect or phone plugged in.
- NFR8 (Cost) - It only needs a Kinect v2, a phone and a laptop.

## How These Link to the Objectives

- Objective 1, capture and sync both sensors - FR1 to FR6
- Objective 2, track the body and clean the data - FR1, FR7
- Objective 3, detect the club head with YOLO - FR8
- Objective 4, detect the four swing phases - FR9
- Objective 5, calculate swing metrics - FR10, FR11
- Objective 6, rank faults and show the top one first - FR12, FR19
- Objective 7, LLM feedback using the drill library - FR13 to FR15
- Objective 8, store sessions and show progress - FR20
- Objective 9, evaluate accuracy, feedback and usability - FR8, FR9, FR14, NFR3
