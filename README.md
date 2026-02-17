Hollow Purple Engine 💜

This is a real-time hand gesture project built using OpenCV and MediaPipe.

When you raise both index fingers, blue and red energy orbs appear.
When they touch, they fuse into a purple energy core and trigger a blast effect.

It’s basically a computer vision + VFX experiment inspired by anime-style energy attacks.

What It Does

Tracks hands in real time using MediaPipe

Generates blue and red energy orbs

Detects when both index fingers touch

Triggers fusion animation

Creates a purple blast with particles, shockwave, and camera shake

Tech Used

Python

OpenCV

MediaPipe

NumPy

How To Run

Clone the repo:

git clone https://github.com/rishi01811/hollow-purple.git
cd hollow-purple


Install dependencies:

pip install -r requirements.txt


Run:

python main.py


Press ESC to exit.

Why I Built This

I wanted to experiment with real-time gesture tracking and create something visually fun instead of just another ML demo.
This project helped me understand:

Hand landmark detection

State machine logic

Particle systems

Real-time rendering performance
