from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import FieldForm
from backend import settings
import openai

openai.api_key = settings.OPENAI_API_KEY

@login_required
def index(request):
    suggestions = "AI-generated suggestions will appear here."
    if request.method == 'POST':
        form = FieldForm(request.POST)
        if form.is_valid():
            field = form.cleaned_data['field']
            # Call OpenAI API
            prompt = f"Based on the field '{field}', suggest schools or universities."
            response = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": "Suggest schools or universities for this field."}
                ],
            )
            suggestions = response.choices[0].message.content
    else:
        form = FieldForm()

    return render(request, 'orientai_by_field/index.html', {'form': form, 'suggestions': suggestions})
