# AirSense

A touchless gesture-control OS-automation system that enables intuitive computer interaction through hand gestures and voice commands. Built with MediaPipe for real-time hand tracking, PyAutoGUI for OS automation, and speech recognition for voice control.

## Overview

AirSense eliminates the need for traditional input devices by leveraging computer vision to recognize hand gestures and voice patterns. This enables seamless, natural interaction with your operating system and applications.

## Features

- **Air Cursor** - Precise finger-based cursor movement and control
- **Click & Drag Operations** - Intuitive file and application manipulation
- **Multi-touch Gestures** - Two-finger scrolling with vertical and horizontal support
- **Pinch Zoom** - Natural zoom in/out functionality
- **Window Management** - Quick switching between open applications
- **Text Selection** - Hand gesture-based text selection and editing
- **Screenshot Capture** - Custom gesture-triggered screenshot functionality
- **Voice Commands** - Hands-free application launching and system controls
- **TCP Networking** - Remote computer control across network connections

## Requirements

- Python 3.7 or higher
- Webcam (integrated or USB)
- Windows 10/11
- Microphone (for voice command features)

## Getting Started

### Installation

1. Clone the repository:

   ```
   git clone https://github.com/vedikaagarwal28/AirSense.git
   cd AirSense
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

### Running the Application

Start the gesture control system:

```
python airsense.py
```

The application will initialize hand tracking and display a real-time window showing gesture recognition feedback.

### Testing Hand Tracking

To verify hand tracking functionality without running the full application:

```
python test_hand_tracking.py
```

This will display a live camera feed with detected hand landmarks.

## Gesture Control Guide

| Gesture                | Action            |
| ---------------------- | ----------------- |
| Index finger movement  | Move cursor       |
| Fingers tap            | Left click        |
| Click and hold         | Drag and drop     |
| Two fingers vertical   | Scroll up/down    |
| Two fingers horizontal | Scroll left/right |
| Pinch thumb and index  | Zoom in/out       |
| Voice input            | Execute commands  |

## Configuration

Customize behavior by editing configuration variables in `airsense.py`:

- `SMOOTHING` (default: 4.0) - Cursor movement smoothing. Higher values reduce jitter.
- `PINCH_THRESHOLD` (default: 0.04) - Sensitivity for pinch gesture detection
- `SCROLL_SENSITIVITY` (default: 50) - Multiplier for scroll speed
- `FPS_TARGET` (default: 30) - Target frames per second for processing
- `SCREENSHOT_COOLDOWN` (default: 1.8) - Minimum seconds between screenshot captures

## Troubleshooting

### Hand tracking is not working

- Ensure adequate lighting in your environment
- Position your hand fully in the camera frame
- Verify webcam is not in use by another application
- Check that requirements are correctly installed

### Cursor movement is jerky

- Increase `SMOOTHING` value to stabilize tracking
- Improve lighting conditions
- Close unnecessary background applications
- Ensure minimum frame rate of 30 FPS

### Gestures not being recognized

- Move hand closer to the camera (1-2 feet optimal distance)
- Ensure full hand visibility in the frame
- Verify gesture parameters in configuration
- Test with `test_hand_tracking.py` to diagnose issues

### Voice commands not responding

- Check microphone is connected and enabled
- Verify audio input device in system settings
- Speak clearly and at normal pace
- Ensure no background noise interference
