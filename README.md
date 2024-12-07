# HandSign-AI
HandSign AI is a gesture recognition project designed to detect custom hand signs using Mediapipe, enabling hands-free control for various tasks. It identifies gestures like a fist, palm, and V-sign to automate actions such as starting/stopping video recording and capturing screenshots.

## Features  
- Detects **fist**, **palm**, and **V-sign** gestures.  
- Automates:  
  - **Start Recording** with a V-sign after 3 seconds.  
  - **Stop Recording** with a palm gesture.  
  - **Capture Screenshot** with a fist after 3 seconds.  
- Hands-free interaction for improved accessibility.  

## Installation  

1. Clone the repository:  
   ```bash  
   git clone https://github.com/yourusername/HandSignAI.git  
   cd HandSignAI 
   ```
2. Install dependencies:
    ```bash
    pip install opencv-python mediapipe numpy  
    ```
3. Run the project:
    ```bash
    python main.py  
    ```

## Usage
1. Ensure your webcam is connected.
2. Show the following gestures:
- V-sign: Start recording after a 3-second countdown.
- Palm: Stop recording.
- Fist: Capture a screenshot after a 3-second countdown.
3. Press 'q' to quit the application.

## Dependencies
- Python 3.x
- OpenCV
- Mediapipe
- NumPy

## Future Enhancement
- Train custom hand gestures using machine learning models.
- Add gesture-based system control (e.g., volume, brightness adjustment).
- Integrate audio feedback for gesture detection.


## Licence
This project is licensed under the MIT License.