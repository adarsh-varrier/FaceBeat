from transformers import pipeline

# Initialize the emotion detection model
emotion_classifier = pipeline('text-classification', model='j-hartmann/emotion-english-distilroberta-base', return_all_scores=True)

def detect_emotion(text):
    """
    Detects the most relevant emotion from the input text using the transformer model.
    Args:
        text (str): Input text from the user.
    Returns:
        str: Detected emotion label.
    """
    # Get predictions from the emotion classifier
    predictions = emotion_classifier(text)
    
    # Extract the highest-scored emotion
    highest_emotion = max(predictions[0], key=lambda x: x['score'])['label']
    
    # Map detected emotion to moods in the model
    emotion_to_mood = {
        'admiration': 'overjoyed',
        'adoration': 'happy',
        'amusement': 'happy',
        'anger': 'anger',
        'anxiety': 'sad',
        'awe': 'relax',
        'awkwardness': 'relax',
        'boredom': 'relax',
        'calmness': 'relax',
        'confusion': 'interest',
        'craving': 'satisfaction',
        'disgust': 'sad',
        'empathic pain': 'sad',
        'entrancement': 'excitement',
        'excitement': 'excitement',
        'fear': 'fear',
        'happiness': 'happy',
        'interest': 'happy',
        'joy': 'happy',
        'nostalgia': 'relax',
        'relief': 'relax',
        'romance': 'happy',
        'sadness': 'sad',
        'satisfaction': 'happy',
        'surprise': 'happy',
    }
    
    # Return the corresponding mood or a default
    return emotion_to_mood.get(highest_emotion, 'relax')
