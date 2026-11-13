# Development Log

A record of the work done on the project each session, the reasons behind decisions, and what is planned next.

## Background – How the Project Got to This Point

Before any setup work started, the project idea went through a few stages:

- **Original idea** – an AI golf coach that could tell golfers what was wrong with their swing and point them to the right drill, instead of guessing from videos online. This came from my own experience as a golfer.
- **First supervisor meeting (15 Oct 2026)** – Damien Costello liked the idea and showed examples of similar projects. He suggested looking into **YOLO** for detection and the **Kinect v2** because it has built-in skeleton tracking. A two-camera setup was also discussed.
- **Research** – papers and existing apps were reviewed in the research notebook. The most useful was *Twelfth Tee* (Zhai & Park, 2025), which used GPT-4 to give swing feedback. It worked well, but golfers found it hard to know which fault to fix first, it had no club tracking, and the AI picked drills from general knowledge. This shaped three key decisions:
  - show **one main fault at a time**
  - track the **club** as well as the body
  - give the AI a **drill library** to choose from (RAG) so it does not make up advice
- **Two-camera decision** – research showed the Kinect only records at 30 frames per second, which is too slow to track a fast-moving club. The design became: **Kinect from the front** for the body, and a **phone from behind at 240fps** for the club.
- **Web app instead of a phone app** – with the laptop and Kinect in front of the golfer and the phone behind them, the golfer would not be able to see a phone screen. So the results are shown on the laptop, and the phone is only used as a camera.
- **Proposal feedback (27–28 Oct 2026)** – Damien asked for all writing to be in the third person, for the context to focus on golf improvement and getting the right drills, and for the proposal to describe what the project *proposes* rather than what it *will* do. The proposal was updated and submitted.

## 3 November 2026 - Setting Up the Repository and CI

### What Was Done

- Created the GitHub repository and wrote the README.
- Cloned it onto the laptop and set up VS Code as the main tool.
- Created a folder for each part of the system, based on the design from the research:
  - `backend/` – analysis and AI coaching (Python, FastAPI)
  - `web/` – the web app on the laptop (React)
  - `capture/kinect/` – the Kinect app (C#)
  - `capture/phone/` – the phone camera app (React Native)
  - `ml/` – training the YOLO club detection model
  - `drills/` – the drill library for the AI coach
  - `deploy/` – Docker setup
  - `docs/` – plan, meetings, research and design decisions
- Added a `.gitignore` so things like API keys, videos and large model files are not uploaded.
- Wrote the project plan with the milestones from the proposal.
- Set up a CI pipeline using GitHub Actions. Claude (an AI assistant) was used to help write the pipeline file and explain how each part works.

### How the CI Pipeline Works

- It runs every time code is pushed to GitHub.
- It checks that all the documentation is formatted properly.
- It has a separate check for each part of the project (backend, web app, phone app, Kinect app). These only switch on once that folder has code in it, so the pipeline passes now and grows as the project is built.
- A final **CI status** check only passes if everything else passed.

### Problems and How They Were Fixed

- **Push was rejected** – the README had been edited on the GitHub website, so GitHub had a change the laptop did not. Fixed by running `git pull` first. Lesson: make all changes in VS Code.
- **First pipeline run failed** – the docs check found that `project-plan.md` was missing a blank line at the end. Fixed it and turned on the VS Code setting that adds one automatically. Good to see the pipeline catching mistakes straight away.

### Next Steps

- Turn on branch protection so all changes go through pull requests.
- Write the requirements document.
- Write the architecture document.
- Add notes from the supervisor meetings and a summary of the research.
- Set up the CD pipeline for releases.
- Create labels, milestones, issues and a Project board on GitHub.

## 4 - 5 November 2026 - Planning, Docs and Weekly Epics

### What Was Done

- Met Damien and showed the repository, CI pipeline, epics and project board.
- Turned on branch protection
- Added the meeting notes, research summary, requirements and architecture documents.
- Closed Epic 1.
- Changed M1 to Kinect capture
- Removed dates from the milestones in project
plan as they change often.
- Moved the CD pipeline to later in the project as it is not needed yet.
- Started Epic 2: Camera Capture (Kinect)

### Problems and How They Were Fixed

- **Missing comma** in the markdownlint settings file broke the docs check. Fixed by correcting the file.
- **Bold line used as a heading** in the research summary failed the docs check. Fixed by changing it to plain text.
- **GitHub Actions outage** on 4 Nov delayed the checks. The pull requests were left open until the checks passed, instead of bypassing them.

### Next Steps

- Epic 2: Phone capture this week.

## 5 November 2026

### What I did

- Tried to connect the Kinect. It was plugged into the HDMI port, but it needs the Kinect Adapter for Windows to work on a PC. I didn't have one, so I started the phone epic (Epic 3) first. Damien said either camera was fine for this week.
- 3.1 - Recorded test swings on my phone in normal and slow motion. The club is blurry in both, but less blurry in slow motion. I added screenshots to the research doc.
- 3.2 - Set up the backend with FastAPI. Added a health check and a test. The backend job in CI ran for the first time.

### Problems

- The push failed because GitHub was down. I waited and pushed again later.

## 7 November 2026

### What I did

- Added the Python build and test files to .gitignore so they don't get committed.
- 3.3 - Made an upload page for the phone. The phone opens the page in its browser and sends the video to the laptop, which saves it in an uploads folder. Only .mp4 and .mov files are allowed.
- Wrote tests for the upload. They use a temporary folder so they don't touch the real uploads folder.
- Uploaded a real slow-motion swing from my phone and it worked.

### Problems

- VS Code tried to open the video as text. Videos have to be opened in a media player.

## 9 November 2026

### What I did

- 3.4 - Added a page on the laptop that lists the uploaded videos and plays the one I click.
- Numbered all the GitHub issues (1.1, 2.1, 3.1 and so on).

### Problems

- The video list was empty when I tested it. The server was saving videos to a different folder depending on where I started it from. I fixed it so it always uses backend/uploads. The tests didn't catch this because they use a temporary folder, so testing it by hand was important.
- Ruff failed because my imports weren't in order. ruff check --fix sorted them.

## 10 November 2026

### What I did

- 3.5 - Recorded 5 slow-motion swings from behind at home, uploaded them from my phone and played them back on the laptop.
- 3.6 - Changed the page to look like the results screen I planned. It has the swing list on the left and two panels. One is for the Kinect skeleton later and the other plays the phone video.
- Thought about how recording could start on its own later. I'll get it working with saved videos first.

### Next

- Meeting with Damien on 11 November to show the phone capture and the results page.
- Then Epic 2 (Kinect).

## 11 November 2026

### What I did

- Met Damien and showed the phone capture and the results page with my uploaded swings.
- Still waiting on the Kinect adapter, so we agreed I'd work on club tracking with OpenCV this week.
- Damien told me about a Udemy course on OpenCV to look into.

## 12 November 2026

### What I did

- Made Epic 5 (Club Tracking with OpenCV).
- Bought a Udemy OpenCV course to use as my main reference. I'm only doing the lessons I need and keeping my code as close to the course as I can.
- Added notes to the research doc comparing what I'm doing with the course.
- 5.1 - Read a swing video frame by frame with OpenCV. OpenCV says the video is 39.8 fps with 550 frames, even though the phone records slow motion at 240fps. I think it's giving an average because the video has normal-speed and slow-motion parts.
- 5.2 - Tested all six OpenCV trackers on the club head. I drew a box around the club head on the first frame and the tracker follows it. Every tracker lost the club during the takeaway or backswing. CSRT jumped to my hi-vis vest and stayed there. I got the same result on a second swing.
- 5.7 - Recorded 4 new swings with the phone lower, closer and no hi-vis. The trackers still lost the club once it turned or reached my body. A better camera setup can't fix that, because the trackers need the club head to look the same in every frame.
- Changed Epic 5 to use YOLO instead of the OpenCV trackers.
- Ran the standard YOLO model on a swing. It found me as a person, but guessed the club was a sports ball, a kite or a baseball bat, because it doesn't know what a golf club is.
- Looked at a ready-made club head model on Roboflow, but it runs in the cloud, so my frames would leave the laptop. Decided to train my own model instead.
- Trained YOLO11n on Google Colab using a club head dataset from Roboflow Universe (about 3,200 images). It scored 0.98 mAP50 on the dataset's own validation images.
- Ran my model on my swings. Much better than the trackers. It loses the club in the fastest parts of the swing but finds it again. Lowering the confidence to 0.1 helped.

### Problems

- The course uses an older version of OpenCV. I had to install opencv-contrib-python, and some trackers have moved to cv2.legacy.
- The video was too big for my screen, so I shrank each frame with cv2.resize.
- Closing the video window with the X didn't stop the script. Now I press q or ESC to quit.
- Pressing space for every frame was too slow, so I changed waitKey(0) to waitKey(30) so it plays by itself.
- Ruff wanted a blank line between import sys and import cv2.
- Markdownlint failed on bare links and two blank lines in a row in the research doc.
- The camera was too high in my first videos. Most of the frame is sky and the club head is tiny.
- Installing Ultralytics also installed opencv-python, which clashes with opencv-contrib-python. I uninstalled it and reinstalled contrib.
- Roboflow gave me an API key in its example code. I kept it out of my code and GitHub, because anyone with it could use my account.

## 13 November 2026

### What I did

- 5.3 - Saved the club head position for every frame of a swing to a CSV file. YOLO found it in 436 of 536 frames (81%), but only about two thirds during the actual swing.
- Found the biggest gaps: the fast part of the backswing (18 frames), the follow-through and coming into the finish.
- Looked into whether greyscale or edge detection would help. Decided they wouldn't, because the model was trained on colour images and the blur removes the edges anyway.

### Next

- 5.4 - Fill the short gaps with interpolation and draw the club path. Long gaps are too big to fill with a straight line.
- Label frames from my own swings, especially the blurry ones, and train a better model.
