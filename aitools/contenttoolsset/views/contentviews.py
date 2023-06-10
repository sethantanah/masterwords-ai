import os
import re
import openai
from django.shortcuts import render, reverse, redirect
from ..models import Tools, Tones, PostType, Platforms


def home_page(request):
    tools = Tools.objects.all()
    return render(request, 'home.html', context={'tools': tools})


def generate_post_ideas(request):
    if request.method == 'POST':
        prompt = request.POST.get('prompt')

        try:
            if prompt == request.session['prompt']:
                prompt = request.session['prompt']
                post_ideas = request.session['post_ideas']
                post = request.session['post']
                idea = request.session.setdefault('idea', 'Blog Post')
                return render(request, 'post_ideas.html',
                              {'post_ideas': post_ideas, 'prompt': prompt, 'post': post, 'idea': idea})
        except:
            pass

        message = [
            {"role": "user", "content": prompt}]
        model_engine = "gpt-3.5-turbo-0301"
        openai.api_key = os.environ.get("CHAT_GPT_KEY")  # use the Davinci model for best results

        max_tokens = 1000
        # Generate a response
        response = openai.ChatCompletion.create(
            model=model_engine,
            messages=message,
            max_tokens=max_tokens,
            temperature=0.5,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        post_ideas = response['choices'][0]['message']['content'].strip()
        post_ideas = re.sub(r'"', '', post_ideas).split('\n')

        index = 0
        for idea in post_ideas:
            pattern = r"^[0-9]\."
            post_ideas[index] = re.sub(pattern, "", idea)
            index += 1

        request.session['prompt'] = prompt
        request.session['post_ideas'] = post_ideas

        return render(request, 'post_ideas.html', {'post_ideas': post_ideas, 'prompt': prompt})

    try:
        prompt = request.session.setdefault('prompt', 'Generate five post ideas for a fashion blog')
        post_ideas = request.session.setdefault('post_ideas', '')
        post = request.session.setdefault('post', '')
        idea = request.session.setdefault('idea', 'Blog Post')
        return render(request, 'post_ideas.html',
                      {'post_ideas': post_ideas, 'prompt': prompt, 'post': post, 'idea': idea})
    finally:
        pass

    return render(request, 'post_ideas.html', {'prompt': 'Generate five post ideas for a fashion blog'})


def generate_post(request, idea):
    if request.method == 'GET':
        try:
            if idea == request.session.setdefault('idea', 'idea'):
                prompt = request.session['prompt']
                post_ideas = request.session['post_ideas']
                post = request.session['post']
                return render(request, 'post_ideas.html',
                              {'post': post, 'post_ideas': post_ideas, 'prompt': prompt, 'idea': idea})
        finally:
            pass

        if idea != '':
            message = [
                {"role": "user", "content": "Generate an interesting and uptodate article on: " + idea}]
            model_engine = "gpt-3.5-turbo-0301"
            openai.api_key = os.environ.get("CHAT_GPT_KEY") # use the Davinci model for best results

            max_tokens = 1000
            # Generate a response
            response = openai.ChatCompletion.create(
                model=model_engine,
                messages=message,
                max_tokens=max_tokens,
                temperature=0.5,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
            post = response['choices'][0]['message']['content'].strip()
            post = format_text(post)

            prompt = request.session['prompt']
            post_ideas = request.session['post_ideas']
            request.session['idea'] = idea
            request.session['post'] = post
            return render(request, 'post_ideas.html',
                          {'post': post,
                           'post_ideas': post_ideas, 'prompt': prompt, 'idea': idea})


def word_tuner(request):
    tones = Tones.objects.all()

    platforms = Platforms.objects.all()
    post_type = PostType.objects.all()

    if request.method == 'POST':
        text_content = request.POST.get('text_content')
        tone = request.POST.get('tone')
        platform = request.POST.get('platform')
        post_t = request.POST.get('post_type')

        if text_content == request.session.setdefault('text_content', 'text_content') and tone == request.session.setdefault('tone', 'Neutral'):
            text_content = request.session['text_content']
            tuned_words = request.session['tuned_words']
            tone = request.session['tone']

            return render(request, 'word_tuners.html',
                          {'text_content': text_content, 'tuned_words': tuned_words, 'tones': tones, 'tone':tone, 'platforms': platforms, 'post_type':post_type})

        if tone != '' and post_t != '' and platform != '':
            message = [
                {"role": "user",
                 "content": f"As a professional {platform} writer, rewrite the following {post_t} in a {tone} tone: " + text_content}]
        elif tone != '':
            message = [
                {"role": "user",
                 "content": f"As a professional writer, rewrite the following text in a {tone} tone: " + text_content}]
        else:
            message = [
                {"role": "user", "content": "Rewrite the following text in a professional tone: " + text_content}]

        model_engine = "gpt-3.5-turbo-0301"
        openai.api_key = os.environ.get("CHAT_GPT_KEY")  # use the Davinci model for best results

        max_tokens = 1000
        # Generate a response
        response = openai.ChatCompletion.create(
            model=model_engine,
            messages=message,
            max_tokens=max_tokens,
            temperature=0.5,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        tuned_words = response['choices'][0]['message']['content'].strip()
        tuned_words = format_text(tuned_words)
        request.session['tuned_words'] = tuned_words
        request.session['text_content'] = text_content
        request.session['tone'] = tone
        return render(request, 'word_tuners.html', {'text_content': text_content, 'tuned_words': tuned_words, 'tones': tones, 'tone': tone, 'platforms': platforms, 'post_type':post_type})

    try:
        text_content = request.session.setdefault('text_content', 'Enter or paste your content')
        tuned_words = request.session.setdefault('tuned_words', '')
        tone = request.session.setdefault('tone', 'Professional')
        post_ideas = [
            'Neutral', 'Professional', 'Friendly', 'Empathetic'
        ]
        return render(request, 'word_tuners.html',
                      {'text_content': text_content, 'tuned_words': tuned_words, 'post_ideas': post_ideas, 'tones':tones, 'tone': tone, 'platforms': platforms, 'post_type':post_type})

    finally:
        pass

    return render(request, 'word_tuners.html', {'tones': tones, 'platforms': platforms, 'post_type':post_type})


def format_text(text):
    # Replace single line breaks with double line breaks
    text = text.replace('\n', '\n\n')

    # Split text into paragraphs on double line breaks
    paragraphs = text.split('\n\n')

    # Wrap each paragraph in <p> tags
    paragraphs = [f'<p>{p}</p>' for p in paragraphs]

    # Combine paragraphs into a single string
    formatted_text = '\n'.join(paragraphs)

    return formatted_text
