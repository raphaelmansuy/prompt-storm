

PROMPT_FORMAT_EXAMPLE = """
name: illustration_pattern
version: "1.0"
description: >
    This prompt is designed to help creative artists to illustrate the concept of a subject through a unique and engaging pattern.
author: quantalogic
input_variables:
  subject:
    type: string
    description: The subject to illustrate
    place_holder: "Marketing"
    examples: 
      - "Marketing"
      - "Design"
      - "Art"
  emotion:
    type: string
    description: Emotion to convey
    place_holder: "Excitement"
    examples: 
      - "Excitement"
      - "Confidence"
      - "Hope"
  inspiration: 
    type: string
    description: Sources of inspiration
    place_holder: "Architecture"
    examples: 
      - "Architecture"
      - "Art"
      - "Design"
  palette:
    type: string
    description: The color palette to use
    place_holder: "Pastel"
    examples: 
      - "Pastel"
      - "Vibrant"
      - "Monochrome"
tags: 
  - creative
  - illustration
categories:
  - art

content: >

  As a creative artist, I am tasked with illustrating the concept of a subject through a unique and engaging pattern.

  - First I will choose a primary color palette that reflects the essence of the subject. 
"""