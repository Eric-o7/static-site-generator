This is a recommended project from boot.dev

The project utilizes a series of nodes in a class structure to accurately parse Markdown into HTML.
There are four major classes used:
Blocknodes take in the initial Markdown and separates into blocks for further processing.
The content in Blocknodes is then converted to HTML.ParentNodes.
These ParentNodes are recursively iterated through to find the end points and turn them into TextNodes. Those TextNoes
are then parsed into LeafNodes as a list that belongs to a ParentNode.
Each node has a way to track the content type, or HTML tag, so that it can be properly written in HTML.

This project is the first major project I've completed and the learnings from it are endless.
Among them, I became much more familiar with OOP: class structure, class manipulation, recursion through polymorphism, and enumeration with match/case functionality.
I practice more recursion in image and link conversions and page generation.

AI helped work through some tough problems, but all code is written and debugged by me. 
