# VoiceBoard
A Canvas application that can recognise speech

This is an application that has all the features that a whiteborad needs.
Features :
1. Save the canvas as pdf files or postscrip files
2. Speech Recognition and inserting the text into the canvas.

How to use the Speech Recognition

The speech recognition systen needs an active internet connection to run
First click on the 'listen' button , then click anywhere on the canvas
Now the button shows 'listening' . Until and unless the button appears so , it means that it is listening
You can speack into the mic whenever you want , the recorder detectcs silence automatically
When the recorder detetcs silence , it send the text for recognition , and prints the text where clicked
This printed text is editable by clicking on it (It cannot yet be edited by voice,but by keyboard)
If the sent voice is unrecognised , it prints an 'E' onto the canvas(This E can also be deleted with a simple backspace)
One Important Note :
If you see that even after finishing speech , the button stays on 'Listening' , tap the microphone with your hand(Such that it makes some noice) or clap,
The mic detects this and the button renders to normal(After a few seconds)
Note that the recognition process might as well take a few seconds , so please be patient.


Please feel free to reprot bugs , compability issues etc.
More updates are expected


Tested on :
Ubuntu 20.04
Python 3.8.5


