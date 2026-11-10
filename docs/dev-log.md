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

## 3 November 2026 – Setting Up the Repository and CI

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

## 4- 5 November 2026 - Planning, Docs and Weekly Epics

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
