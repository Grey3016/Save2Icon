A Custom node to 'Save to an icon' for ComfyUI

Oversight

    It saves your picture as an Icon.
    Its a small quality of life node to not have to individually adjust corners on pics, their corner transparencies and saving as an icon .

What it does

    It takes your output from the Vae-Decode node and rounds the corners (making them transparent) and save the output as an .ico (icon) file

What can I adjust ?

    1.You can change the size of the icon - 128 , 256 up to a max of 512 (default setting). I defaulted it to 512 because thats how I make them .

    2.The node also allows you attach to a Preview node (optional) 

    3. You can also see the Output Location by attaching to a text node (that has an input), this is also optional

    4.Finally, you can adjust the corner rounding profile - remember that if you change icon size the ratio of picture to profile radius changes 

    Personally , I join the Icon Save node with the Preview node via the 'Convert to Group Node' function

What does it need?

    A square ratio input (eg 1024x1024 etc) , it'll squash the pic otherwise


Installation

    git clone https://github.com/Grey3016/Save2Icon

Requirements

    Pillow >= 9.0.0

Below : "Save To Icon" node attached to Preview and a Text node

![Screenshot 2025-01-05 171001](https://github.com/user-attachments/assets/c9d8a05c-cffc-4039-a681-30dc6b811cdf)


Below : "Save To Icon" node attched to the Preview node via 'Convert To Group Node' function

![image](https://github.com/user-attachments/assets/692e1fc1-726e-4591-bd89-01f11ea37cbe)

Usage

    Git Clone above and select Save to Icon node from menu. I've also attached a Comfy workflow that I use as an Icon maker flow. 

    NB I wouldn't use the word "icon" in your prompt as Flux will double round the corners, I use the word 'logo' instead. 