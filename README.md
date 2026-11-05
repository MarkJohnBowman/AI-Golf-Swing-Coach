# AI Golf Swing Coach

Final Year Project – B.Sc. (Hons) in Software Development, ATU Galway

- **Student:** Mark Bowman (G00389705)
- **Supervisor:** Damien Costello
- **Year:** 2026 – 2027

## About the Project

Improving a golf swing often comes down to small details, and it can be hard for golfers to know exactly what they are doing wrong. There are plenty of practice drills online, but a drill only helps if it fixes the right problem.

This project aims to build an AI golf swing coach. A Kinect camera tracks the golfer's body, and a phone camera filmed from behind tracks the club. The system measures the swing, finds the biggest fault, and uses AI to explain what went wrong and suggest a drill to fix it. Each session is saved so golfers can see their progress over time.

## How It Works

1. The Kinect tracks the golfer's body movement from the front.
2. A phone records the swing from behind in slow motion to track the club.
3. The two recordings are lined up and the swing is measured.
4. The biggest fault in the swing is found.
5. An AI coach explains the fault and suggests a drill from a drill library.
6. The results are shown on a laptop screen in front of the golfer.

## Technologies

- **Kinect v2** – tracks the golfer's body in 3D
- **Phone camera (240fps)** – records the club in slow motion
- **YOLO** – detects the club head in each video frame
- **Python and FastAPI** – the backend that runs the analysis
- **LLM with RAG** – AI coaching feedback using a library of drills
- **MySQL and ChromaDB** – stores sessions and the drill library
- **React** – the web app shown on the laptop
- **Docker and GitHub Actions** – packaging, testing and deployment

## Project Structure

- `backend/` – analysis and AI coaching
- `web/` – the web app
- `capture/kinect/` – Kinect capture app
- `capture/phone/` – phone capture app
- `ml/` – training the club detection model
- `drills/` – the drill library
- `deploy/` – Docker setup
- `docs/` – project plan, research and meeting notes

## Project Status

The project is run as one small epic per week, with a weekly supervisor meeting. Current work is on the GitHub project board.

- **November 2026** – Setup, Kinect capture and backend
- **December 2026** – Phone capture and syncing the two cameras
- **January 2027** – Training the club detection model
- **February 2027** – Swing analysis
- **March 2027** – Web app and AI coaching
- **April 2027** – Testing and user feedback
- **May 2027** – Final submission
