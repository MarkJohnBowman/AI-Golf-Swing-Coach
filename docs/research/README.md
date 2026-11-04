# Research Summary

A summary of the research behind the project's design. Full notes are kept in the handwritten research notebook.

## First Conception - 17 October 2026

As a lifelong golfer, the idea came from wanting to improve the swing and figure out the fine margins between a good and a bad shot. Golf is a solo sport, so it is hard to see changes in your swing on the range. Many people spend a lot of money on golf lessons, only to forget the tips and tricks learned. With the advancement of AI and computer vision, the idea was to tackle this problem with an AI swing coach that gives real-time feedback.

### First Idea

1. User films the swing on a tripod.
2. Video is uploaded and body points are tracked.
3. Swing is split into positions: address, top of backswing, impact and finish.
4. App calculates metrics such as hip and shoulder rotation, spine angle, head movement and tempo.
5. An LLM gets the metrics plus a drill library (RAG) and returns feedback.

After the first supervisor meeting, Damien gave pointers on research to help shape the final project design and scope.

## AI Golf: Golf Swing Analysis Tool for Self-Training

Liao, Hwang and Koike (2022), IEEE Access.

### How It Works

1. **Motion synchroniser** - a neural network (TCC) maps each frame into a latent space, so the same moment in two swings lands close together. Dynamic time warping then lines them up.
2. **Discrepancy detector** - after alignment, it measures the distance between the user's frame and the pro's frame. Large distances mark the key moments where the swing differs most.
3. **Motion manipulator** - a decoder generates in-between poses that blend the beginner's and the pro's swing, so the learner can work towards the pro's form.

### Data and Models

- Trained on GolfDB.
- 2D pose from HRNet, lifted to 3D.
- Compared three inputs: raw video, skeleton only, and skeleton with self-attention.

### Results

- Skeleton-based models beat video-based models. Swing classification was over 90%.
- Removing the background helped the video model, because shadows and scenery confused it.

### Learnings

- Use skeleton data, not raw video.
- 3D beats 2D. They had to estimate 3D from 2D, but the Kinect gives 3D depth directly.
- Control the background.
- The output is only visual. It shows where you differ from the pro but not how to fix it.

## DeepSwing

Commercial phone app.

### How It Works

1. Automatic phase detection: setup, backswing, top, downswing, impact and finish.
2. Body and club head tracking in every frame, with a skeleton overlay and club head path.
3. Club and ball speed estimated from video.
4. Coaching features: a swing score, a drill for the biggest fault, a searchable drill library and a ghost pro swing overlay.

### Learnings

- One top fix and one drill is good UX. Don't overload the user.
- Confirms club tracking is possible on the phone.
- The Kinect can be combined with the phone for body and club tracking.

## YOLO

Damien mentioned YOLO in the meeting on 15 October 2026.

### How It Works

YOLO looks at the whole image once, in a single pass through a neural network (a CNN).

- The image is divided into a grid.
- Each grid cell predicts bounding boxes, how confident it is that an object is there, and which class it is.
- Overlapping boxes for the same object are merged, leaving one box per object.
- A single pass makes it fast enough for real-time video.

### Use in This Project

- **Phone camera:** YOLO detects the club head in each frame. Joining the detections gives the club path.
- **Kinect:** handles the body skeleton in 3D using its own depth sensor.

## Twelfth Tee: An Intelligent Mobile System for Personalized Golf Swing Analysis Using Computer Vision and Artificial Intelligence

Zhai and Park (2025). Notes from 20 October 2026.

A mobile app that gives GPT-4 coaching feedback.

### How It Works

- Pose estimation detects four phases: rest, backswing, downswing and follow-through.
- Calculates angles, tempo and balance, and sends them to GPT-4 in a structured prompt.
- GPT-4 returns an assessment, strengths, faults and practice drills.

### Stack

- Flutter app, Flask backend on AWS, Firebase login and Firestore database.

### Learnings

- LLM coaching from pose metrics works and scores close to human coaches.
- Send the LLM numbers, not video. They measured first, then gave GPT-4 structured metrics in the prompt.
- Prioritisation is the LLM's main weakness, so the design ranks faults and leads with one top fault and one drill.

## Web App Over Mobile App - 21 October 2026

Since the phone will be behind the golfer, it makes more sense for the interface to be on the laptop, so the golfer can see results and carry on practising. The laptop and Kinect sit in front of the golfer, and the phone sits on a tripod behind.

The first screen sketches were a live screen (live skeleton, live cues, focus and session list) and a results screen (skeleton replay, down-the-line video with club path, timeline, top fault, swing metrics and drill).

## Final Design - 20 October 2026

**AI Swing Coach: Multi-Sensor Golf Swing Analysis with LLM Coaching Feedback**

The project combines:

- Kinect v2 for true 3D body tracking
- Phone camera and YOLO for club tracking
- LLM with RAG over a drill library

### Objectives

1. Capture the swing with both sensors and sync them.
2. Track the body with the Kinect skeleton, cleaned with interpolation and smoothing.
3. Detect the club head with a YOLO model.
4. Detect four swing phases: address, top, impact and finish.
5. Calculate swing metrics: spine angle, hip turn, shoulder turn, sway, head movement, tempo ratio and swing plane.
6. Rank faults by how far each metric is from its target range, and show the top fault first.
7. Generate LLM feedback grounded in the RAG drill library: explanation, cause and one drill.
8. Store sessions and show progress over time.
9. Evaluate accuracy, feedback quality and usability.

### System Design

- **Kinect v2, face-on** - 3D skeleton.
- **Phone, down-the-line** - club head path for swing plane, over-the-top and speed estimate.

Pipeline: sync on impact, clean data, swing phases, metrics, rank faults, LLM coach (with the drill library), app.

### Main Components

1. **Capture service (C#, Kinect SDK 2.0)** - records skeleton frames with timestamps and sends them to the backend as JSON.
2. **Club tracking (Python, YOLO)** - club path tracked through the video.
3. **Analysis engine (Python)** - syncs the two streams on impact (Kinect: hands at their lowest point; phone: audio spike on impact), cleans the data (interpolation and smoothing), detects phases (wrist height), calculates metrics and ranks faults.
4. **AI coach (LLM and RAG)** - a drill library of around 50 drills, tagged by fault and stored as embeddings so similar drills can be looked up. The top faults are used to retrieve matching drills, and the LLM gets the metrics plus the retrieved drills and returns what's wrong, why it matters and one drill.
5. **App** - results with skeleton and club path overlay, top fault and drill, session history and progress charts.

### Technologies

- **Body capture:** Kinect v2 - real 3D skeleton
- **Club capture:** Phone - can capture the club without blur
- **Club detection:** YOLO and Roboflow - proven club detection
- **Analysis:** Python, NumPy, OpenCV, SciPy - standard computer vision and maths libraries
- **Backend API:** FastAPI (Python) - same language as the computer vision and AI code
- **LLM:** Claude API - natural language coaching
- **RAG:** Embeddings and ChromaDB - retrieves verified drills
- **Database:** MySQL - users, sessions, metrics
- **Front end:** React web app - shown on the laptop in front of the golfer
- **Testing:** pytest, API tests, accuracy benchmarks - QA focus, testing on real swings
- **DevOps:** GitHub, Docker, GitHub Actions - version control, CI, deployable demo
