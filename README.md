# Job Interview Assistant
If this helped you to ace your job interview and you would like to thank me you can do it here!
[<img src="paypal-donate-button.png">](https://www.paypal.com/donate/?hosted_button_id=MBW7WAP8SSVAN)

## Introduction
You have the feeling that you suck at online job interviews? Then this is for you. Knowhow, confidence in your skills, good preparation - who needs all of that, when you have your good friend ChatGPT? Just record what the interviewer askes and let ChatGPT generate the answers for you. Stand out with minimal effort. You will be amazed how well it works <sub><sup>(*results may vary)</sup></sub>.
## Prerequisites
Since this is a python project, you need to have python installed. I used python 3.10, but it should work with other python3 versions as well.

 After cloning the project and placing it somewhere on your computer you also need to install the requirements. Open a command promt in the main folder and execute 
 ```pip install -r requirements.txt```.


Last but not least you will need an [OpenAI](https://openai.com/) account to generate an api key. After setting up your account follow [these](https://help.openai.com/en/articles/5112595-best-practices-for-api-key-safety) instructions to set up your OPENAI_API_KEY as an environment variable. For credits you can either use the free budget of $5 which you get for creating a new account - the $5 will expire after 3 months - or you can buy credits with a credit card ([see here](https://platform.openai.com/account/billing/payment-methods)).
## Limits and Pricing
With a new account you start with a budget of $5 which expires in 3 months. It has some limitations though. you can only have 3 requests/minute (RPM) and 200 requests/day (RPD). This might be a tiny bit too low for our usecase.

I would recommend to deposit atleast $5 to get to Tier 1. You can read about the Tiers [here](https://platform.openai.com/docs/guides/rate-limits?context=tier-one). By doing that you can do 3,500 RPM and 10,000 RPD, which is more than enough already.

The price/minute in case of the speech-to-text transcription and the price/1000 tokens in case of the text generation is very fair. We are using the `whisper-1` model for the speech-to-text transcription and either `gpt-3.5-turbo` or `gpt-4-1106-preview` model for the text generation.

`whisper-1` speech-to-text transcription: $0.0006/minute

`gpt-3.5-turbo`
text generation input tokens: $0.0010 / 1K tokens

`gpt-3.5-turbo`
text generation output tokens: $0.0020 / 1K tokens

`gpt-4-1106-preview`
text generation input tokens: $0.01 / 1K tokens

`gpt-4-1106-preview`
text generation output tokens: $0.03 / 1K tokens

For comparison: The whole shakespeare corpus has ~900,000 words. That would be roughly 1,200,000 tokens. So the price for generating the whole shakespeare corpus with `gpt-3.5-turbo` would be roughly $2.40 and with `gpt-4-1106-preview` $36. 
Note however, that for our chatbot to have a memory we need to feed it the previous conversation. So the price per request will increase per request, because one request is previous conversation + new input. When you start a new session it will not know the conversation from the previous session. 

## Usage
Open a command promt in the JobInterviewAssistant folder and execute ```python JobInterviewAssistant.py```. A window with a big red button on the left side will open. If you **hover** over that button it starts recording. Clicking it does nothing extra. If you stop hovering over the button it stops recording, the transcription process starts and an answer  is generated. The transcript and the generated answer will be displayed right next to the red button. Notice that your microphone is never recorded, just the sound output channel of your computer.

To test if it works you can play a random youtube video, where someone speaks. Play the video, record it by hovering over the button and stop recording by moving your mouse away from the button. The transcript should be displayed within a few seconds and an answer should be generated. If that works, you are ready to go.