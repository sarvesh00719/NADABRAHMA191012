import re

# Update Yoga
with open(r'd:\NADABRAHMA\mobile\app\sahasrara\yoga.tsx', 'r', encoding='utf-8') as f:
    yoga = f.read()

yoga_old = '"Welcome to Sahasrara. I am here to guide your focus. What are you studying today, and how is your energy level?"'
yoga_new = '"Welcome to Yoga Sadhana. I am your Yoga Helper. Let\'s begin with some Pranayama practices. How is your breathing today?"'
yoga = yoga.replace(yoga_old, yoga_new)

with open(r'd:\NADABRAHMA\mobile\app\sahasrara\yoga.tsx', 'w', encoding='utf-8') as f:
    f.write(yoga)


# Update Espresso
with open(r'd:\NADABRAHMA\mobile\app\sahasrara\espresso.tsx', 'r', encoding='utf-8') as f:
    espresso = f.read()

espresso_old = '"Welcome to Sahasrara. I am here to guide your focus. What are you studying today, and how is your energy level?"'
espresso_new = '"Welcome to Digital Espresso. I am here to help you manage your workload and work pressure. What kind of heavy tasks are you facing today?"'
espresso = espresso.replace(espresso_old, espresso_new)

with open(r'd:\NADABRAHMA\mobile\app\sahasrara\espresso.tsx', 'w', encoding='utf-8') as f:
    f.write(espresso)
