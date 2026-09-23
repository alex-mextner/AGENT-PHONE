# AGENT hardware × Agent OS

Updated: 2026-09-23

Agent OS:
- Site: https://agentos-bible.vercel.app/
- Source: https://github.com/alex-mextner/AgentOS

AGENT is the hardware expression of Agent OS rather than a second, unrelated platform.

## What maps directly

Agent OS describes itself as:
- app-last;
- local-first;
- agent-native;
- built around durable entities rather than application silos;
- capable of composing task-specific micro-apps;
- explicit about agent capabilities and authority;
- designed for Agent Mesh peer-to-peer connectivity.

Those properties are particularly useful on a small wrist display because the user should not navigate a phone-style grid of full-screen applications.

## AGENT UI model

The primary object on the screen is a **task or entity**, not an app.

Examples:
- a person → messages, call, shared files, next meeting;
- a calendar event → participants, directions, notes, join action;
- a product → compare, buy, track delivery;
- a room → lights, TV, climate, audio;
- a research task → current status, sources, result, follow-up;
- a photo → share, move to TV, ask about it.

Providers can still exist, but they should not dictate the whole UI.

## Micro-apps fit the wide display

The landscape panel is well suited to small temporary compositions:
- chat on the left + photos on the right;
- calendar event + map;
- delivery status + building entry control;
- AI research progress + relevant document;
- TV playback + light/AC controls.

These are not permanent app installations. They are task-specific views assembled from typed capabilities and data sources.

## Always-on agent layer

The low-power controller should not run the whole Agent OS.

It runs a narrow **Agent Edge** service:
- accessory authentication;
- sensor events;
- notification triage;
- haptics;
- screen-off text state;
- tiny local classifier;
- wake requests.

It sends typed events to the suspended application environment.

Example:

```
RingGesture {
  actor: local_user
  gesture: squeeze
  target_hint: living_room_tv
  confidence: 0.96
}
```

The higher-trust Agent OS layer resolves permissions and effects.

## Telekinesis as an Agent OS input provider

Telekinesis should publish:
- text hypotheses;
- confidence spans;
- gesture events;
- gaze targets;
- correction intents;
- provenance: which sensors contributed.

It must not inject arbitrary key events behind the OS's back.

That lets the same silent phrase be interpreted differently depending on context:
- in a chat entity → draft a reply;
- over a product → ask a question;
- over a room → issue a device command;
- while nothing is selected → open the universal command surface.

## Spatial entities

Physical devices should be first-class Agent OS entities:
- TV;
- speaker;
- lamp;
- room;
- another person's AGENT;
- camera tile;
- glasses.

The ring/glasses stack estimates **which entity the user is pointing at**. Agent OS then handles identity, capability, ownership, transport and action.

This separation is important: geometry says "that object"; the entity system says "Living Room TV owned by this household, with these allowed actions."

## Air transfer

"Throwing" a photo or card to another screen is modeled as an explicit entity transfer:

1. select/grab an entity;
2. spatial input proposes a target entity;
3. UI/haptic preview confirms target;
4. capability layer checks whether the action is allowed;
5. Agent Mesh/local transport sends the object or grants access;
6. both devices receive an effect receipt.

The gesture is only the front-end. The transfer remains inspectable and revocable.

## Local-first policy

Raw high-rate sensor streams should remain local whenever possible:
- sEMG;
- PPG;
- gaze;
- camera hand tracking;
- ring IMU;
- throat/neck sensor data.

Derived events such as `pinch`, `target=TV`, or a text hypothesis are what normally enter the entity/action layer.

Cloud AI can be used for explicitly chosen workloads, but local state should not depend on a vendor cloud to remain usable.

## App-last marketplace

The commercial layer does not need an app store full of monoliths.

A seller/integrator can expose:
- typed data source;
- action;
- widget/component;
- model/tool;
- device driver;
- transport provider.

Agent OS composes those pieces into the current task.

This directly supports the project's "hyper-targeting without ads" idea: a user-controlled local agent may decide that a need exists, ask permission, then query competing providers. It should not sell a behavioral profile or allow hidden sponsored ranking.

## Hardware implications

Agent OS should eventually expose hardware capabilities such as:

```
display.sparse_indicator
display.wrist_surface
haptic.pulse
telekinesis.text
telekinesis.gesture
spatial.point
camera.context
camera.capture
audio.private_tts
cellular.low_power
uwb.range
health.read
```

Each should have explicit permissions and power-cost metadata.

## Boot and persistence

Agent OS should optimize for:
- suspend/resume, not repeated boot;
- crash-safe durable entities;
- small always-on service boundary;
- incremental UI composition;
- local encrypted history;
- ability to continue core actions offline.

The hardware project should not create a separate mobile-app abstraction that Agent OS later has to undo.
