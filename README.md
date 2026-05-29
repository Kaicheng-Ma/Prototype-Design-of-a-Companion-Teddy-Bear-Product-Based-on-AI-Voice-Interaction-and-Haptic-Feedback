# AI Voice Interactive Companion Toy Bear with Haptic Feedback

## Project Overview

This project is a human-centered product prototype that explores how AI voice interaction, haptic feedback, and physical companion design can be combined to support college students who experience loneliness, stress, and sleep difficulties.

The final concept is an interactive companion toy bear that provides emotional companionship through AI voice dialogue, expressive screen-based eye animations, breathing-guidance vibration, soft toy-like appearance, and physical interaction. The project aims to create a comforting object that is not only functional, but also emotionally approachable and suitable for everyday use by students.

The prototype integrates product design, user research, AI interaction, microcontroller programming, physical computing, 3D modeling, 3D printing, and hardware assembly into one complete MVP.

## Background and Motivation

Loneliness among college students is a common and meaningful problem. During the early research stage, the project identified that students may experience loneliness due to academic pressure, lack of communication, difficulty adapting to new environments, and limited emotional support.

The project was motivated by the question:

> Can a physical AI companion provide students with a sense of comfort, emotional support, and stress relief in daily life?

To explore this question, the product was designed as a companion toy bear that combines three main forms of support:

1. **AI voice dialogue** for emotional communication
2. **Breathing-guidance vibration** for stress relief and sleep support
3. **Soft and intimate physical appearance** for companionship and comfort

## Target Users

The target users include:

- College students
- International students
- Students who feel lonely or stressed
- Students who have difficulty sleeping
- Students who want a low-pressure emotional companion
- Users who prefer physical and tactile interaction rather than purely screen-based interaction

## Design Goal

The main goal of this project is to design and prototype a physical AI companion that can reduce loneliness and provide a calming interaction experience.

The design focuses on:

- Creating a warm and approachable companion object
- Supporting voice-based emotional interaction
- Providing haptic breathing guidance for relaxation
- Making the product physically squeezable, friendly, and comforting
- Building a working MVP with real hardware, software, and physical assembly

## Core Features

### 1. AI Voice Dialogue

The toy bear is designed to allow users to talk with an AI companion through voice interaction.

The software workflow includes:

- **Sound recognition**
- **Speech-to-text processing**
- **AI response generation**
- **Text-to-speech output**

In the prototype design, the voice interaction pipeline uses:

- **Vosk** for speech-to-text
- **ChatGPT 3.5** for dialogue generation
- **pyttsx** for text-to-speech output

This allows the toy bear to act as a conversational companion that users can talk to and share feelings with.

### 2. Haptic Breathing Guidance

The product includes a vibration-based breathing guidance system inspired by slow-paced breathing exercises and breathing-assist products such as Somnox.

The vibration motor gradually strengthens and weakens to guide the user through inhale and exhale cycles. This haptic rhythm is designed to help users relax, reduce stress, and support sleep.

The vibration curve was iteratively adjusted through multiple tests to find a more comfortable breathing rhythm.

### 3. Expressive Eye Animation

The toy bear uses a screen to display eye expressions. The eye design went through multiple iterations:

- Static eye design
- Pixel-based custom character design
- Improved eye layout after screen display limitations were discovered
- Animated eye expression to make the bear feel more lively and less mechanical

The pixel art eyes were manually designed and programmed using hexadecimal values, allowing the screen to display customized emotional expressions.

### 4. Physical Companion Form

The product uses a bear-like form to create a familiar and emotionally safe appearance. The design draws inspiration from teddy bears, stress balls, and plush companions.

The physical form is intended to be:

- Cute
- Comfortable
- Emotionally warm
- Easy to hold
- Suitable for stress relief
- Friendly rather than technological or intimidating

### 5. Light and Interaction Feedback

The MVP includes light feedback together with breathing guidance, allowing users to understand the inhale and exhale rhythm more clearly.

The combination of light, vibration, and eye states helps the product communicate its state without relying only on speech.

## Technical Implementation

### Hardware Platform

The project originally considered Arduino UNO, but the final implementation switched to **ESP32-S3** because the system required I2S signal input and better integration with AI-related audio processing.

The microcontroller-related work included:

- ESP32-S3 board selection
- Arduino IDE environment setup
- Circuit wiring
- Button-based trigger design
- Vibration motor control
- Screen connection
- Hardware testing and debugging

### Microcontroller Programming

The prototype was programmed using Arduino IDE.

One major technical challenge was that multiple functions needed to run without blocking each other. When the screen animation and vibration guidance were merged into one program, using `delay()` caused mutual waiting between different functions.

To solve this, the timing logic was changed from `delay()` to `millis()`, allowing state persistence and non-blocking control for multiple functions.

### Sensor and Trigger Design

The original plan was to use a pressure sensor to trigger the breathing guidance. However, because of unclear voltage specifications and the risk of damaging the sensor, the design was changed to a button-triggered interaction.

This decision made the prototype more stable and easier to implement within the project timeline.

### AI Voice Interaction Pipeline

The software interaction workflow was designed as:

```text
User Voice Input
        ↓
Sound Recognition / Audio Processing
        ↓
Speech-to-Text Model
        ↓
ChatGPT 3.5 Response Generation
        ↓
Text-to-Speech Output
        ↓
Toy Bear Voice Response
