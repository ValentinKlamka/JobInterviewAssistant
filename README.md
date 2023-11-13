# Job Interview Assistant
If this helped you ace your job interview and you would like to thank me you can do it here!
[<img src="paypal-donate-button.png">](https://www.paypal.com/donate/?hosted_button_id=MBW7WAP8SSVAN)

## Introduction
You have the feeling that you suck at online job interviews? Then this is for you. All-embracing knowhow, serious skills, impressive expertise, good preparation - who needs all of that, when you have your good friend ChatGPT? Just record what the interviewer askes and let ChatGPT generate the answers for you. Stand out with minimal effort. You will be amazed how well it works <sub><sup>(*results may vary)</sup></sub>.
## Prerequisites
Since this is a python project, you need to have python installed. I used python 3.10, but it should work with other python3 versions as well.

 After cloning the project and placing it somewhere on your computer you also need to install the requirements. Open a command promt in the main folder and execute 
 ```pip install -r requirements.txt```.


Last but not least you need an open ai api key and credits for your openai account, which you have to buy with a credit card(not prepaid). Please note, that this is an external service and I do not get any money from that. You can set it up [here](https://platform.openai.com/account/billing/payment-methods). Then you need to generate an OpenAI API key [here](https://beta.openai.com/account/api-keys) and set it as an environment variable with the name OPENAI_API_KEY. Follow these [instructions](https://help.openai.com/en/articles/5112595-best-practices-for-api-key-safety) if you don't know how to do that.

## Usage
Open a command promt in the JobInterviewAssistant folder and execute ```python JobInterviewAssistant.py```. A window with a big red button on the left side will open. If you **hover** over that button it starts recording. Clicking it does nothing extra. If you stop hovering over the button it stops recording, the transcription process starts and an answer  is generated. The transcript and the generated answer will be displayed right next to the red button. You can scroll through that generated conversation. Notice that your microphone is never recorded, just sound which comes from your computer. (And don't worry, also not your fan noises). 

To get a feeling how long the processing takes or to test if it even works you can play a random youtube video, where someone speaks. Play the video, record it by hovering over the button and stop recording by moving your mouse away from the button. The transcript should be displayed within a few seconds and an answer should be generated. If that works, you are ready to go.