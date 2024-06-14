from django.shortcuts import render
from django.contrib.auth.models import User
from dotenv import load_dotenv
import google.generativeai as genai
import os
import re
import requests
import json
from groq import Groq



load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

client = Groq(
    # This is the default and can be omitted
    api_key= os.environ.get("GROQ_API_KEY"),
)


# API endpoint URL
api_url = 'http://sheldonchettiar3.pythonanywhere.com/predict-mental-health/'

# Create your views here.

def Home(request):
    return render(request, 'baseApp/index.html')


videos = {
    1: {
        "https://youtu.be/9mPwQTiMSj8?si=tkaZ40cu20cLtjNu": "https://img.youtube.com/vi/9mPwQTiMSj8/0.jpg",
        "https://youtu.be/JOKS9Bx8-Sw?si=s_paZtpEv8ERHnlO": "https://img.youtube.com/vi/JOKS9Bx8/0.jpg",
        "https://youtu.be/BVJkf8IuRjE?si=moZNs1ow-k7tLsNz": "https://img.youtube.com/vi/BVJkf8IuRjE/0.jpg",
        "https://youtu.be/zTuX_ShUrw0?si=7pJx_dcU3IEoKnMm": "https://img.youtube.com/vi/zTuX_ShUrw0/0.jpg",
        "https://youtu.be/vtUdHOx494E?si=cMhLCCbPolitlF1u": "https://img.youtube.com/vi/vtUdHOx494E/0.jpg",
    },
    2: {
        "https://youtu.be/z-IR48Mb3W0?si=5V8YxrbxuXTcN3Se": "https://img.youtube.com/vi/z-IR48Mb3W0/0.jpg",
        "https://youtu.be/Fm73eVoi4dw?si=yiRGIfOsi4VIrYpp": "https://img.youtube.com/vi/Fm73eVoi4dw/0.jpg",
        "https://youtu.be/BZOLxSQwER8?si=vUNztWxoFUPzw6ey": "https://img.youtube.com/vi/BZOLxSQwER8/0.jpg",
        "https://youtu.be/OzO8EAOEGJ8?si=Oi_oMnBGtPlhIJFR": "https://img.youtube.com/vi/OzO8EAOEGJ8/0.jpg",
        "https://youtu.be/MZ5r99SBLrs?si=dT5TX5Yme2Mlt3de": "https://img.youtube.com/vi/MZ5r99SBLrs/0.jpg",
    },
    3: {
        "https://youtu.be/1BBiaxOxXas?si=lVXUCIqY7N5NjpFN": "https://img.youtube.com/vi/1BBiaxOxXas/0.jpg",
        "https://youtu.be/1BBiaxOxXas?si=j9gatadXIKovNBSH": "https://img.youtube.com/vi/1BBiaxOxXas/0.jpg",
        "https://youtu.be/QFt_5kSUQyM?si=1twlenCwPjN-2ocC": "https://img.youtube.com/vi/QFt_5kSUQyM/0.jpg",
        "https://youtu.be/2KXtlIX_yUs?si=SE4RS5y7xjoYgp85": "https://img.youtube.com/vi/2KXtlIX_yUs/0.jpg",
        "https://youtu.be/aAvZPaDlwR0?si=WTc4o6bcdIl9mTrv": "https://img.youtube.com/vi/aAvZPaDlwR0/0.jpg",
    },
    4: {
        "https://youtu.be/n3Xv_g3g-mA?si=cfU5SLQnIEPtIo-E": "https://img.youtube.com/vi/n3Xv_g3g-mA/0.jpg",
        "https://youtu.be/JxbYPk1MIyw?si=tujk_3eTEHw1a9Mh": "https://img.youtube.com/vi/JxbYPk1MIyw/0.jpg",
        "https://youtu.be/TWNL7EClClo?si=Hao7pDbhBrrWqg2e": "https://img.youtube.com/vi/TWNL7EClClo/0.jpg",
        "https://youtu.be/dWS3A2EAwTk?si=Kc2XICKov-MdgR-m": "https://img.youtube.com/vi/dWS3A2EAwTk/0.jpg",
        "https://youtu.be/GdcDKpLUajs?si=GNXZWE7bZqNJVMi9": "https://img.youtube.com/vi/GdcDKpLUajs/0.jpg",
    },
}


def Test(request):
    context = {}
    # ... (existing code to collect form data)
    if request.method == 'POST':
        # Extract the form data from the POST request
        feeling_nervous = request.POST.get('feeling_nervous')
        panic = request.POST.get('panic')
        breathing_rapidly = request.POST.get('breathing_rapidly')
        sweating = request.POST.get('sweating')
        trouble_in_concentration = request.POST.get('trouble_in_concentration')
        having_trouble_in_sleeping = request.POST.get('having_trouble_in_sleeping')
        having_trouble_with_work = request.POST.get('having_trouble_with_work')
        hopelessness = request.POST.get('hopelessness')
        anger = request.POST.get('anger')
        over_react = request.POST.get('over_react')
        change_in_eating = request.POST.get('change_in_eating')
        suicidal_thought = request.POST.get('suicidal_thought')
        feeling_tired = request.POST.get('feeling_tired')
        close_friend = request.POST.get('close_friend')
        social_media_addiction = request.POST.get('social_media_addiction')
        weight_gain = request.POST.get('weight_gain')
        material_possessions = request.POST.get('material_possessions')
        introvert = request.POST.get('introvert')
        popping_up_stressful_memory = request.POST.get('popping_up_stressful_memory')
        having_nightmares = request.POST.get('having_nightmares')
        avoids_people_or_activities = request.POST.get('avoids_people_or_activities')
        feeling_negative = request.POST.get('feeling_negative')
        trouble_concentrating = request.POST.get('trouble_concentrating')
        blamming_yourself = request.POST.get('blamming_yourself')

        # Prediction Logic (replace with your actual model)

        input_list = [feeling_nervous, panic, breathing_rapidly, sweating, trouble_in_concentration,
                      having_trouble_in_sleeping, having_trouble_with_work, hopelessness, anger, over_react, change_in_eating, suicidal_thought, feeling_tired, close_friend, social_media_addiction, weight_gain, material_possessions, introvert, popping_up_stressful_memory, having_nightmares, avoids_people_or_activities, feeling_negative, trouble_concentrating, blamming_yourself]
        


        # Prepare request data
        data = {
            'input_features': input_list
        }


        # Send POST request to API endpoint
        response = requests.post(api_url, json=data)

        prediction = None

        if response.status_code == 200:
            # Extract prediction from response
            try:
                prediction = response.json()['prediction']
                print("Prediction:", prediction)
            except KeyError:
                raise Exception("Response does not contain 'prediction' key.")
        else:
            raise Exception("Error occurred: {}".format(response.text))

        # Mental health conditions and descriptions dictionary
        conditions = {
            0: {"issue": "no issues", "description": "The user is fine."},
            1: {"issue": "Anxiety", "description": "Feeling nervous, restless, or having trouble concentrating. You might also have physical symptoms like rapid heartbeat, sweating, or trouble sleeping."},
            2: {"issue": "Depression", "description": "Feeling hopeless, sad, or losing interest in activities you used to enjoy. You might also have changes in sleep or appetite."},
            3: {"issue": "Stress", "description": "Feeling overwhelmed, anxious, or irritable. Stress can also cause physical symptoms like headaches, muscle tension, or fatigue."},
            4: {"issue": "Loneliness", "description": "Feeling isolated or alone, even when you're around other people."},
        }

        # Access data based on prediction
        current_issue = conditions.get(prediction)

        if prediction == 0:
            prompt = f"The User is completely normal. Just provide some more self-care tips."
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "you are a helpful mental health assistant focused on improving the mental health of the user by giving some insights and tips."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                model="llama3-8b-8192",
            )
            response = chat_completion.choices[0].message.content
            context = {
                "issue": "No issue",
                "description": "The user is completely normal.",
                "generated_content": response,
                "videos": None,
            }
        else: 
            prompt = f"Write a supportive and informative message about {current_issue['issue']}. Include information on what it is, symptoms, and how to cope."
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "you are a helpful mental health assistant focused on improving the mental health of the user by giving some insights and tips."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                model="llama3-8b-8192",
            )
            response = chat_completion.choices[0].message.content
            context = {
                "issue": current_issue["issue"],
                "description": current_issue["description"],
                "generated_content": response,
                "videos": videos.get(prediction),
            }

        return render(request, 'baseApp/result.html', context)

    else:
        # If the request method is GET, just render the form
        return render(request, 'baseApp/test.html')
