from django.contrib.auth.decorators import login_required
import markdown
import bleach
from django.shortcuts import render, redirect
from .models import Conversation, Message
from .forms import MessageForm
import openai
from django.conf import settings

openai.api_key = settings.OPENAI_API_KEY

@login_required
def chat_view(request):
    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES)
        if form.is_valid():
            message = form.save(commit=False)
            conversation_id = request.session.get('conversation_id')

            if not conversation_id:
                conversation = Conversation(user=request.user)
                conversation.save()
                request.session['conversation_id'] = conversation.id
            else:
                conversation = Conversation.objects.get(id=conversation_id)
            
            message.conversation = conversation
            message.save()

            # Get the conversation history
            messages = Message.objects.filter(conversation=conversation)

            # Send message to OpenAI API with context and get the AI response
            ai_message_text = send_message_to_openai(messages, message.text)
            ai_message = Message(conversation=conversation, text=ai_message_text, is_ai=True)
            ai_message.save()

            return redirect('chat:chat_view')
    else:
        form = MessageForm()

    conversation_id = request.session.get('conversation_id')
    if conversation_id:
        messages = Message.objects.filter(conversation__id=conversation_id)
    else:
        messages = []

    # Convert Markdown to HTML and sanitize
    for msg in messages:
        html = markdown.markdown(msg.text)
        msg.text = bleach.clean(html, tags=['p', 'strong', 'em', 'ul', 'ol', 'li', 'br'], strip=True)

    return render(request, 'chat/chat.html', {'form': form, 'messages': messages})

def send_message_to_openai(messages, user_message):
    message_list = []
    for msg in messages:
        role = "user" if not msg.is_ai else "assistant"
        message_list.append({"role": role, "content": msg.text})
    
    message_list.append({"role": "user", "content": user_message})

    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=message_list,
    )

    ai_message_text = response.choices[0].message.content
    return ai_message_text
