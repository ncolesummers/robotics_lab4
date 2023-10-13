# Lab 4

Nathan Summers and Robert Carne

CS 453

## Introduction

This lab serves as an introduction to inter-robot communication. The robots will need to pass a die back and forth between each other. We will not be using vision to detect the location of the die, but instead will be commuicating the location of the die between the robots.

## Approach

Each robot will have its own controller. Operation of the different robots is implemented using the provided robot controller library. Communication between the controllers is done by binding to sockets with python. Serialization and deserialization will be performed using the `pickle` library.
