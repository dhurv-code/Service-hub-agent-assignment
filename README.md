# AutoStream Social-to-Lead Agentic Workflow

## Overview

This project is a conversational AI agent built for the ServiceHive Machine Learning Intern assignment.

The agent is designed for a fictional SaaS company called **AutoStream**, which provides AI-powered automated video editing tools for content creators.

The system converts user conversations into qualified leads by detecting intent, answering product questions, and collecting lead details.

---

## Features

### 1. Intent Detection

The agent classifies user intent into:

- Casual Greeting
- Product / Pricing Inquiry
- High-Intent Lead

### 2. Knowledge Retrieval (Local RAG)

The agent uses a local JSON knowledge base containing:

- Basic Plan ($29/month)
- Pro Plan ($79/month)
- Features
- Refund Policy
- Support Policy

### 3. Lead Capture Workflow

When a user shows buying intent, the agent collects:

- Name
- Email
- Creator Platform

After collecting all values, it triggers:

```python
mock_lead_capture(name, email, platform)