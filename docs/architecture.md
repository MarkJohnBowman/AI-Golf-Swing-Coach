# Architecture

This document shows how the parts of the AI Golf Swing Coach fit together. It is based on the System Design and Main Components pages in my research notebook.

## Physical Setup

- The laptop and Kinect sit in front of the golfer (face-on), so the golfer can see the results on the laptop screen.
- The phone sits on a tripod behind the golfer (down-the-line) and records the swing in slow motion.
- The laptop and phone are on the same Wi-Fi network.

The interface is on the laptop rather than the phone because the phone is behind the golfer, so the golfer would not be able to see it.

## System Overview

1. Kinect v2 (face-on) - tracks the body and sends it to the capture service.
2. Phone (down-the-line) - records the swing and uploads the video.
3. Backend (FastAPI) - receives the Kinect data and the phone video.
4. Sync on impact - lines the two recordings up.
5. Clean data - fills in missing points and smooths the data.
6. Swing phases - finds address, top, impact and finish.
7. Metrics - calculates the swing measurements.
8. Rank faults - puts the biggest fault first.
9. AI coach (LLM) - uses the drill library (ChromaDB) to explain the fault and give a drill.
10. Web app - shows the results on the laptop.
11. MySQL - saves sessions, swings and results.

## Main Components

### 1. Capture Service (C#, Kinect SDK 2.0)

- Reads the golfer's skeleton from the Kinect (25 joints in 3D).
- Adds a timestamp to every frame.
- Sends the frames to the backend as JSON.
- Detects when the golfer sets up and finishes the swing, so recording starts and stops on its own.

### 2. Phone Capture

- Records the swing from behind in slow motion.
- Starts and stops recording when the backend tells it to.
- Uploads the video to the laptop automatically.

### 3. Club Tracking (Python, YOLO)

- YOLO finds the club head in each frame of the phone video.
- Joining the detections gives the club path, used for swing plane, over-the-top and a speed estimate.

### 4. Analysis Engine (Python)

- Syncs the two recordings at impact. On the Kinect this is when the hands are at their lowest point, and on the phone it is the sound of the club hitting the ball.
- Cleans the data by filling in missing points (interpolation) and smoothing out shaky data.
- Detects the four swing phases (address, top, impact and finish) using wrist height.
- Calculates the swing metrics and ranks the faults, with the biggest fault first.

### 5. AI Coach (LLM and RAG)

- A drill library of around 50 drills, each tagged by fault and stored as embeddings in ChromaDB so similar drills can be looked up.
- The top fault is used to find the matching drills.
- The LLM (Claude API) gets the metrics and the matching drills, and returns what went wrong, why it matters and one drill.

### 6. Web App (React)

- Live screen showing the live skeleton, whether the Kinect and phone are connected, and the swings so far.
- Results screen with the skeleton replay and the phone video with the club path, a timeline, the top fault, the swing metrics and the drill.
- Session history and progress charts.

### 7. Database (MySQL)

- Stores users, sessions, swings, metrics and feedback, so progress can be shown over time.

## How a Swing Moves Through the System

1. The golfer sets up over the ball. The Kinect detects this and the backend tells the phone to start recording.
2. The golfer swings. The Kinect streams the skeleton to the backend and the phone records.
3. The Kinect detects the finish and the backend tells the phone to stop and upload the video.
4. The backend syncs the two recordings, finds the club head, cleans the data, detects the phases, calculates the metrics and ranks the faults.
5. The AI coach finds the drills for the top fault and the LLM writes the feedback.
6. The results are saved to the database and shown on the web app.

## Design Decisions

- **Two cameras** - the Kinect gives a real 3D skeleton but only records at 30fps, which is too slow for the club. The phone records in slow motion to track the club without blur.
- **Kinect face-on** - research (Twelfth Tee) showed face-on video is the least accurate view because the legs overlap. The Kinect's depth sensor helps with this.
- **Skeleton data, not raw video** - research (AI Golf) showed skeleton-based models beat video-based models.
- **Web app on the laptop** - the golfer faces the laptop, so results are shown there.
- **One top fault and one drill** - from DeepSwing and Twelfth Tee, to avoid overloading the golfer.
- **RAG drill library** - the LLM only suggests drills from the library, so it does not make up advice.
- **FastAPI (Python)** - the same language as the computer vision and AI code.
- **Video stays on the laptop** - only the metrics and drill text are sent to the LLM.
