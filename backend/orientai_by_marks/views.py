from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import MarkForm
from .models import Mark
from backend import settings
import openai

openai.api_key = settings.OPENAI_API_KEY

@login_required
def index(request):
    ai_suggestions = "AI-generated suggestions will appear here."
    form = MarkForm()

    if request.method == 'POST':
        subjects = request.POST.getlist('subjects')
        scores = request.POST.getlist('scores')
        level = request.POST.get('level')

        for subject, score in zip(subjects, scores):
            Mark.objects.create(user=request.user, subject=subject, score=score, level=level)

        marks = Mark.objects.filter(user=request.user)
        # Call OpenAI API
        if marks.exists():
            prompt = f"Based on the following marks for user {request.user.username}, suggest a career path:\n"
            for mark in marks:
                prompt += f"{mark.subject}: {mark.score}\n"
            response = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": "Suggest a career path for me."}
                ],
                max_tokens=300
            )
            ai_suggestions = response.choices[0].message.content

    return render(request, 'orientai_by_marks/index.html', {'form': form, 'ai_suggestions': ai_suggestions})
